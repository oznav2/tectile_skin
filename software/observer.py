"""Bounded, actuation-free skin observations. All freshness uses monotonic time."""
from dataclasses import dataclass
import re

from .skin_protocol import Gate, Frame, MASK, CELLS

PROFILES = {'2x2': 0xF, '3x2': 0x3F, '7x4': MASK}
SCHEMA = 'tectile_skin.observation.v1'


@dataclass(frozen=True)
class Patch:
    patch_id: str
    interface: str
    node_id: int
    uid: str
    config_crc: int
    body_frame: str
    profile: str
    expected_mask: int
    sheet_serial: str
    calibration_sha256: str


def parse_config(config, *, demo=False):
    if config.get('schema') != 1:
        raise ValueError('requires electronic-skin configuration schema 1')
    if not demo and config.get('commissioned') is not True:
        raise ValueError('commissioned identities and configuration are required')
    patches, addresses, identifiers, uids = [], set(), set(), set()
    nodes = config.get('nodes', [])
    if not 1 <= len(nodes) <= 256:
        raise ValueError('requires 1..256 patches, at most 8 per region')
    for n in nodes:
        p = Patch(str(n['patch_id']), str(n['interface']), n['node_id'],
                  str(n['uid']).lower(), int(n['config_crc'], 16),
                  str(n['body_frame']), str(n['profile']), int(n['expected_mask'], 16),
                  str(n.get('sheet_serial', '')), str(n.get('calibration_sha256', '')))
        if not re.fullmatch(r'can_skin_[a-z0-9_]{1,6}', p.interface):
            raise ValueError('use a dedicated can_skin_* interface; motor interfaces are prohibited')
        if p.profile not in PROFILES or p.expected_mask != PROFILES[p.profile]:
            raise ValueError('profile / expected_mask mismatch')
        if not re.fullmatch(r'[0-9a-f]{24}', p.uid) or int(p.uid, 16) == 0:
            raise ValueError('UID must contain a nonzero 96-bit physical identity')
        if type(p.node_id) is not int or not 1 <= p.node_id <= 8 or not 0 <= p.config_crc <= 0xffffffff:
            raise ValueError('invalid regional node ID or configuration CRC')
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_/-]{0,95}', p.patch_id) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_/-]{0,95}', p.body_frame):
            raise ValueError('patch ID and an explicit local frame name are required')
        if not demo and (not re.fullmatch(r'[0-9a-fA-F]{64}', str(n.get('calibration_sha256', '')))
                         or not n.get('sheet_serial') or 'REPLACE' in n['sheet_serial']):
            raise ValueError('production requires measured calibration hash and sheet serial')
        if (p.interface, p.node_id) in addresses or p.patch_id in identifiers or p.uid in uids:
            raise ValueError('duplicate physical address, patch ID, or UID')
        addresses.add((p.interface, p.node_id)); identifiers.add(p.patch_id); uids.add(p.uid)
        patches.append(p)
    return tuple(patches)


class Observer:
    """One latest observation per patch. No motor SDK, command output, or backlog."""
    def __init__(self, config, *, demo=False):
        self.patches = parse_config(config, demo=demo)
        self.interface_devices = config.get('interface_device_realpaths', {})
        if not demo:
            for interface in {p.interface for p in self.patches}:
                path = self.interface_devices.get(interface, '')
                if not path.startswith('/sys/devices/') or 'REPLACE' in path:
                    raise ValueError('record each skin interface physical device realpath before commissioning')
        self.gates = {(p.interface, p.node_id): Gate(p.uid, p.node_id, p.config_crc)
                      for p in self.patches}
        self.by_address = {(p.interface, p.node_id): p for p in self.patches}
        self.samples = {}
        self.rejected = 0
        self.demo = demo

    def fail_region(self, interface, reason):
        for key, gate in self.gates.items():
            if key[0] == interface:
                gate.invalidate(reason)
                gate.sync = None
                gate.pending = None
                self.samples.pop(key, None)

    def ingest(self, interface, can_id, payload, now):
        if 0x201 <= can_id <= 0x208:
            node, kind = can_id - 0x200, 'data'
        elif 0x301 <= can_id <= 0x308:
            node, kind = can_id - 0x300, 'announce'
        elif 0x381 <= can_id <= 0x388:
            node, kind = can_id - 0x380, 'sync'
        else:
            return 'unrelated'
        key = (interface, node)
        if key not in self.gates:
            self.fail_region(interface, 'uncommissioned_node')
            self.rejected += 1
            return 'rejected'
        gate, patch = self.gates[key], self.by_address[key]
        try:
            if kind == 'announce':
                old_boot = gate.boot
                gate.announce(payload)
                if old_boot != gate.boot:
                    self.samples.pop(key, None)
            elif kind == 'sync':
                gate.accept_sync(payload, now)
            else:
                f = Frame.decode(payload)
                if (f.valid_mask | f.open_mask | f.overload_mask) & ~patch.expected_mask:
                    raise ValueError('status_bit_outside_installed_profile')
                sample = gate.accept(payload, now)
                sample['temperature_valid_until'] = now + max(
                    0.0, .250 - (f.temperature_age_ms + max(0, sample['oldest_capture_age_ms'])) / 1000)
                self.samples[key] = sample
            return kind
        except (ValueError, TypeError) as exc:
            gate.invalidate(str(exc))
            if kind == 'announce':
                # Revocation must prohibit sync until a matching UID announces.
                gate.boot = gate.pending = gate.sync = gate.sequence = gate.capture = None
            elif kind == 'sync':
                gate.sync = gate.pending = None
            self.samples.pop(key, None)
            self.rejected += 1
            return 'rejected'

    def snapshot(self, now):
        rows, features, valid_count, expected_count = [], [], 0, 0
        for p in self.patches:
            key = (p.interface, p.node_id)
            gate, sample = self.gates[key], self.samples.get(key)
            sync_fresh = gate.sync is not None and 0 <= now - gate.sync[3] <= 2.5
            fresh = (sample is not None and gate.last_good is not None and sync_fresh
                     and gate.last_good <= now <= gate.expiry)
            valid = (sample['valid_mask'] & p.expected_mask) if fresh else 0
            overload = (sample['contact_or_fault_mask'] & p.expected_mask) if fresh else 0
            intensity = [sample['intensity'][i] if valid & (1 << i) else None for i in range(CELLS)]
            temperature = (list(sample['temperature_C']) if fresh and now <= sample['temperature_valid_until']
                           else [None, None])
            valid_count += valid.bit_count()
            expected_count += p.expected_mask.bit_count()
            if not fresh:
                reason = gate.reason if sample is None else ('capture_expired' if sync_fresh else 'time_sync_expired')
            elif overload:
                reason = 'contact_or_fault'
            elif valid != p.expected_mask:
                reason = 'touch_channels_unavailable'
            elif any(t is None for t in temperature):
                reason = 'temperature_unavailable'
            else:
                reason = 'ok'
            row = {'patch_id': p.patch_id, 'interface': p.interface, 'node_id': p.node_id,
                   'uid': p.uid, 'config_crc': f'{p.config_crc:08x}',
                   'sheet_serial': p.sheet_serial, 'calibration_sha256': p.calibration_sha256,
                   'body_frame': p.body_frame, 'profile': p.profile,
                   'expected_mask': p.expected_mask, 'valid_mask': valid,
                   'unavailable_mask': p.expected_mask & ~valid,
                   'disabled_mask': MASK & ~p.expected_mask,
                   'contact_or_fault_mask': overload, 'fresh': fresh,
                   'reason': reason, 'health_ok': reason == 'ok',
                   'intensity_ordinal': intensity, 'temperature_C': temperature,
                   'boot': gate.boot, 'sequence': sample['sequence'] if fresh else None,
                   'valid_until_monotonic_s': min(sample['valid_until_monotonic_s'], gate.sync[3] + 2.5) if fresh else None,
                   'geometry_status': 'not_control_commissioned'}
            rows.append(row)
            # Versioned 89 values per patch. Masks always accompany zero fill.
            features.extend([(v / 254) if v is not None else 0.0 for v in intensity])
            features.extend([float(bool(valid & (1 << i))) for i in range(CELLS)])
            features.extend([float(bool(overload & (1 << i))) for i in range(CELLS)])
            features.extend([(t / 100) if t is not None else 0.0 for t in temperature])
            features.extend([float(t is not None) for t in temperature])
            features.append(float(fresh))
        return {'schema': SCHEMA, 'simulated': self.demo,
                'host_monotonic_s': now, 'patches': rows, 'expected_taxels': expected_count,
                'valid_taxels': valid_count, 'coverage_fraction': valid_count / expected_count,
                'full_coverage': valid_count == expected_count, 'rejected_frames': self.rejected,
                'feature_schema': 'tectile_skin.features.v1.89_per_patch', 'features': features,
                'control_ready': False, 'actuation_enabled': False}
