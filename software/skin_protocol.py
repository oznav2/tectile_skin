"""Electronic skin protocol v2. Dependency-free reference codec and freshness gate.

This is tested host logic, not a certified control system or a flashed MCU image.
Times passed to this module MUST use time.monotonic(), never wall-clock time.
"""
from dataclasses import dataclass
import struct

VERSION = 2
CELLS = 28
MASK = (1 << CELLS) - 1
DATA = struct.Struct('<BBHIII28BhhIIIHH')
ANNOUNCE = struct.Struct('<BBH12sIIIHH')
SYNC_REQUEST = struct.Struct('<BBHQI')
SYNC_REPLY = struct.Struct('<BBHQIIIII')
assert DATA.size == 64 and ANNOUNCE.size == 32 and SYNC_REPLY.size == 32


def delta32(a, b):
    """Signed modulo difference; correct within +/- 2**31 milliseconds."""
    return ((a - b + 0x80000000) & 0xffffffff) - 0x80000000


@dataclass(frozen=True)
class Frame:
    flags: int
    sequence: int
    boot: int
    capture_ms: int
    config_crc: int
    intensity: tuple
    temperatures: tuple
    open_mask: int
    overload_mask: int
    valid_mask: int
    temperature_age_ms: int
    diagnostics: int

    def encode(self):
        if len(self.intensity) != CELLS or len(self.temperatures) != 2:
            raise ValueError('wrong channel count')
        return DATA.pack(VERSION, self.flags, self.sequence, self.boot,
                         self.capture_ms, self.config_crc, *self.intensity,
                         *self.temperatures, self.open_mask, self.overload_mask,
                         self.valid_mask, self.temperature_age_ms, self.diagnostics)

    @classmethod
    def decode(cls, payload):
        if len(payload) != DATA.size:
            raise ValueError('data length must be 64')
        v = DATA.unpack(payload)
        if v[0] != VERSION or v[1] & 0xf0:
            raise ValueError('version or reserved flag mismatch')
        if any(m & ~MASK for m in v[36:39]) or v[40] & ~0x00ff:
            raise ValueError('reserved mask/diagnostic bits set')
        result = cls(v[1], v[2], v[3], v[4], v[5], tuple(v[6:34]),
                     tuple(v[34:36]), v[36], v[37], v[38], v[39], v[40])
        if result.open_mask & result.valid_mask:
            raise ValueError('open channel cannot also be valid')
        for i, value in enumerate(result.intensity):
            valid = bool(result.valid_mask & (1 << i))
            if (value == 255) == valid:
                raise ValueError('invalid sentinel inconsistent with validity mask')
        return result


class Gate:
    """One commissioned physical node. Announce + nonce sync precede valid data.

    A bad frame never refreshes freshness. All unknown/fault states invalidate
    coverage. Overload remains an explicit CONTACT_OR_FAULT, never zero force.
    Boot/config updates require a new announcement and synchronization.
    """
    def __init__(self, uid_hex, node_id, config_crc):
        self.uid = bytes.fromhex(uid_hex)
        if len(self.uid) != 12 or not 1 <= node_id <= 8:
            raise ValueError('UID must be 96 bits; regional node ID is 1..8')
        self.node_id, self.config_crc = node_id, config_crc
        self.boot = None
        self.pending = None
        self.sync = None
        self.sequence = None
        self.capture = None
        self.last_good = None
        self.valid_mask = 0
        self.reason = 'not_announced'

    def invalidate(self, reason):
        self.last_good = None
        self.valid_mask = 0
        self.reason = reason

    def reject_identity(self, reason):
        # SYNC/DATA do not carry the UID. A rejected announcement must revoke
        # the previously accepted identity before any new sync is permitted.
        self.boot = self.pending = self.sync = self.sequence = self.capture = None
        self.invalidate(reason)

    def announce(self, payload):
        if len(payload) != ANNOUNCE.size:
            self.reject_identity('bad_announcement_length')
            raise ValueError('bad announcement length')
        version, kind, node, uid, boot, cfg, caps, period, reserved = ANNOUNCE.unpack(payload)
        if (version, kind, node, uid, cfg, period, reserved) != (
                VERSION, 0xa1, self.node_id, self.uid, self.config_crc, 10, 0):
            self.reject_identity('identity_or_config_mismatch')
            raise ValueError(self.reason)
        if boot == 0:
            self.reject_identity('invalid_boot_epoch')
            raise ValueError(self.reason)
        if caps != 0x00000007:  # 28 touch, 2 temperature, freshness protocol
            self.reject_identity('capability_mismatch')
            raise ValueError('capability mismatch')
        if boot != self.boot:
            self.boot = boot
            self.sync = self.pending = self.sequence = self.capture = None
            self.invalidate('new_boot_requires_sync')

    def request_sync(self, nonce, now):
        if self.boot is None:
            raise ValueError('node must announce first')
        self.pending = (nonce, now, self.boot)
        return SYNC_REQUEST.pack(VERSION, 0x51, self.node_id, nonce, self.boot)

    def accept_sync(self, payload, now):
        if self.pending is None or len(payload) != SYNC_REPLY.size:
            raise ValueError('unsolicited/malformed sync')
        v, kind, node, nonce, boot, rx_ms, tx_ms, cfg, reserved = SYNC_REPLY.unpack(payload)
        expected_nonce, t0, expected_boot = self.pending
        self.pending = None
        if (v, kind, node, nonce, boot, cfg, reserved) != (
                VERSION, 0x52, self.node_id, expected_nonce, expected_boot,
                self.config_crc, 0):
            raise ValueError('sync identity mismatch')
        rtt = now - t0
        service = delta32(tx_ms, rx_ms) / 1000
        # Millisecond timestamps quantize both bounds. Include 1 ms each side.
        if not 0 <= rtt <= 0.012 or not 0 <= service <= rtt + 0.002:
            raise ValueError('sync round-trip/service time out of bounds')
        earliest_tx = t0 + max(0.0, service - 0.001)
        latest_tx = now + 0.001
        self.sync = (tx_ms, earliest_tx, latest_tx, now)

    def accept(self, payload, now):
        try:
            f = Frame.decode(payload)
            if f.boot != self.boot or f.config_crc != self.config_crc:
                raise ValueError('boot_or_config_mismatch')
            if self.sync is None or not 0 <= now - self.sync[3] <= 2.5:
                raise ValueError('time_sync_expired')
            anchor_ms, earliest, latest, synced_at = self.sync
            relative = delta32(f.capture_ms, anchor_ms) / 1000
            if abs(relative) > 3:
                raise ValueError('capture_outside_sync_window')
            drift = abs(relative) * 0.0001 + 0.001  # 100 ppm + quantization
            oldest_age = now - (earliest + relative - drift)
            youngest_age = now - (latest + relative + drift)
            if oldest_age > 0.040 or youngest_age < -0.003:
                raise ValueError('stale_or_future_capture')
            if self.sequence is not None:
                advance = (f.sequence - self.sequence) & 0xffff
                if not 0 < advance < 0x8000:
                    raise ValueError('duplicate_or_reordered_sequence')
                if delta32(f.capture_ms, self.capture) <= 0:
                    raise ValueError('nonadvancing_capture')
            if f.flags != 0x0f:
                raise ValueError('global_acquisition_calibration_witness_or_power_fault')
            for bank in range(4):
                if f.diagnostics & (1 << bank) and f.valid_mask & (0x7f << (bank * 7)):
                    raise ValueError('bad_bank_marked_valid')
            if f.diagnostics & 0x80:
                raise ValueError('persistent_storage_fault')
            temps = []
            for i, t in enumerate(f.temperatures):
                ok = (f.temperature_age_ms + max(0.0, oldest_age * 1000) <= 250
                      and not (f.diagnostics & (1 << (4 + i))))
                temps.append(t / 100 if ok and -2000 <= t <= 8500 else None)
            self.sequence, self.capture = f.sequence, f.capture_ms
            self.last_good, self.reason = now, 'ok'
            self.valid_mask = f.valid_mask
            # Coverage expiration uses capture-time bound, not receive-time alone.
            self.expiry = min(now + max(0.0, 0.040 - oldest_age), synced_at + 2.5)
            return {'valid_mask': f.valid_mask, 'open_mask': f.open_mask,
                    'contact_or_fault_mask': f.overload_mask,
                    'intensity': f.intensity, 'temperature_C': temps,
                    'oldest_capture_age_ms': oldest_age * 1000,
                    'valid_until_monotonic_s': self.expiry,
                    'sequence': f.sequence, 'boot': f.boot}
        except (ValueError, struct.error) as exc:
            self.invalidate(str(exc))
            raise

    def coverage_available(self, now):
        return bool(self.valid_mask) and self.last_good is not None and 0 <= now - self.last_good and now <= self.expiry
