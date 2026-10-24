import copy
import json
from pathlib import Path
import socket
import struct
import unittest
from unittest.mock import Mock, patch

from software.observer import Observer, parse_config
from software.demo import announce_and_sync, feed_demo
from software.transport import Transport, check_interface
from software.skin_protocol import Frame, ANNOUNCE, SYNC_REPLY, VERSION
from software.can_wire import WIRE, CAN_ERR_FLAG, SO_RXQ_OVFL


def config():
    path = Path(__file__).parents[1] / 'software/config/limb_skin.example.json'
    return json.loads(path.read_text())


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.config = config()
        self.observer = Observer(self.config, demo=True)
        announce_and_sync(self.observer)

    def test_eight_patches_88_real_taxels_and_712_features(self):
        feed_demo(self.observer)
        snapshot = self.observer.snapshot(100.012)
        self.assertEqual((snapshot['expected_taxels'], snapshot['valid_taxels']), (88, 88))
        self.assertEqual(len(snapshot['features']), 712)
        self.assertTrue(snapshot['full_coverage'])
        self.assertFalse(snapshot['control_ready'])
        self.assertFalse(snapshot['actuation_enabled'])
        for row in snapshot['patches']:
            self.assertEqual(row['disabled_mask'] & row['unavailable_mask'], 0)

    def test_silence_expires_without_new_packets(self):
        feed_demo(self.observer)
        snapshot = self.observer.snapshot(100.080)
        self.assertEqual(snapshot['valid_taxels'], 0)
        self.assertFalse(snapshot['full_coverage'])
        self.assertEqual(snapshot['features'], [0.0] * 712)

    def test_config_does_not_accept_motor_bus_or_uncommissioned(self):
        with self.assertRaises(ValueError):
            Observer(self.config)
        for interface in ('can0', 'can3', 'motor_bus', 'other_bus'):
            self.config['nodes'][0]['interface'] = interface
            with self.assertRaises(ValueError):
                Observer(self.config, demo=True)

    def test_commissioned_toggle_does_not_accept_example_calibration(self):
        self.config['commissioned'] = True
        with self.assertRaises(ValueError):
            Observer(self.config)

    def test_duplicate_identity_and_profile_mismatch(self):
        for change in ({'uid': self.config['nodes'][1]['uid']}, {'expected_mask': '0fffffff'}):
            cfg = copy.deepcopy(self.config)
            cfg['nodes'][0].update(change)
            with self.assertRaises(ValueError):
                parse_config(cfg, demo=True)

    def test_frame_names_are_user_defined_without_robot_model(self):
        cfg = copy.deepcopy(self.config)
        cfg['nodes'][0]['body_frame'] = 'test_fixture/contact_panel_a'
        observer = Observer(cfg, demo=True)
        announce_and_sync(observer)
        feed_demo(observer)
        result = observer.snapshot(100.012)
        self.assertEqual(result['patches'][0]['body_frame'], 'test_fixture/contact_panel_a')
        self.assertNotIn('joint_state', result)
        self.assertNotIn('robot_variant', result)

    def test_more_than_four_regions_has_no_platform_specific_cap(self):
        cfg = copy.deepcopy(self.config)
        extra = copy.deepcopy(cfg['nodes'][0])
        extra.update(patch_id='fixture_panel', interface='can_skin_test',
                     uid='123456789012345678901234', body_frame='fixture_panel')
        cfg['nodes'].append(extra)
        observer = Observer(cfg, demo=True)
        announce_and_sync(observer)
        feed_demo(observer)
        self.assertEqual(observer.snapshot(100.012)['expected_taxels'], 92)

    def test_empty_or_ambiguous_frame_name_rejected(self):
        for name in ('', 'unlabelled panel'):
            cfg = copy.deepcopy(self.config)
            cfg['nodes'][0]['body_frame'] = name
            with self.assertRaises(ValueError):
                Observer(cfg, demo=True)

    def test_unused_channel_cannot_become_valid(self):
        p = self.observer.patches[0]
        f = Frame(15, 1, 1, 1010, p.config_crc, tuple([0]*5+[255]*23),
                  (2000, 2000), 0, 0, 31, 5, 0)
        self.assertEqual(self.observer.ingest(p.interface, 0x201, f.encode(), 100.012), 'rejected')
        self.assertEqual(self.observer.snapshot(100.012)['patches'][0]['valid_mask'], 0)

    def test_partial_failure_only_counts_installed_taxels(self):
        feed_demo(self.observer)
        p = self.observer.patches[0]
        f = Frame(15, 2, 1, 1020, p.config_crc, tuple([0, 0, 0]+[255]*25),
                  (2000, 2000), 8, 0, 7, 5, 0)
        self.observer.ingest(p.interface, 0x201, f.encode(), 100.022)
        row = self.observer.snapshot(100.022)['patches'][0]
        self.assertEqual(row['unavailable_mask'], 8)
        self.assertEqual(row['disabled_mask'], ((1<<28)-1) & ~15)
        self.assertEqual(row['reason'], 'touch_channels_unavailable')
        self.assertFalse(row['health_ok'])

    def test_overload_is_preserved_as_contact_or_fault(self):
        p = self.observer.patches[0]
        f = Frame(15, 1, 1, 1010, p.config_crc, tuple([254, 0, 0, 0]+[255]*24),
                  (2000, 2000), 0, 1, 15, 5, 0)
        self.observer.ingest(p.interface, 0x201, f.encode(), 100.012)
        snapshot = self.observer.snapshot(100.012)
        self.assertEqual(snapshot['patches'][0]['contact_or_fault_mask'], 1)
        self.assertEqual(snapshot['features'][56], 1.0)

    def test_reboot_invalidates_immediately_before_new_data(self):
        feed_demo(self.observer)
        p = self.observer.patches[0]
        payload = ANNOUNCE.pack(VERSION, 0xa1, 1, bytes.fromhex(p.uid), 2, p.config_crc, 7, 10, 0)
        self.observer.ingest(p.interface, 0x301, payload, 100.020)
        self.assertFalse(self.observer.snapshot(100.020)['patches'][0]['fresh'])

    def test_duplicate_packet_never_refreshes_age(self):
        feed_demo(self.observer)
        feed_demo(self.observer, now=100.020)
        self.assertEqual(self.observer.snapshot(100.020)['valid_taxels'], 0)

    def test_unknown_regional_node_invalidates_region_only(self):
        feed_demo(self.observer)
        interface = self.observer.patches[0].interface
        self.observer.ingest(interface, 0x208, b'x', 100.020)
        rows = self.observer.snapshot(100.020)['patches']
        self.assertTrue(all(not p['fresh'] for p in rows if p['interface'] == interface))
        self.assertTrue(all(p['fresh'] for p in rows if p['interface'] != interface))

    def test_temperature_expiry_includes_time_held(self):
        p = self.observer.patches[0]
        f = Frame(15, 1, 1, 1010, p.config_crc, tuple([0]*4+[255]*24),
                  (2400, 2500), 0, 0, 15, 240, 0)
        self.observer.ingest(p.interface, 0x201, f.encode(), 100.012)
        self.assertEqual(self.observer.snapshot(100.012)['patches'][0]['temperature_C'], [24, 25])
        row = self.observer.snapshot(100.025)['patches'][0]
        self.assertTrue(row['fresh'])
        self.assertEqual(row['temperature_C'], [None, None])
        self.assertEqual(row['reason'], 'temperature_unavailable')
        self.assertFalse(row['health_ok'])

    def test_bad_identity_same_boot_cannot_reuse_previous_sync_permission(self):
        feed_demo(self.observer)
        p = self.observer.patches[0]
        gate = self.observer.gates[(p.interface, p.node_id)]
        payload = ANNOUNCE.pack(VERSION, 0xa1, p.node_id, bytes.fromhex('aa' * 12),
                                1, p.config_crc, 7, 10, 0)
        self.assertEqual(self.observer.ingest(p.interface, 0x301, payload, 100.020), 'rejected')
        self.assertIsNone(gate.boot)
        with self.assertRaises(ValueError):
            gate.request_sync(999, 100.021)
        feed_demo(self.observer, sequence=2, capture_ms=1020, now=100.022)
        self.assertFalse(self.observer.snapshot(100.022)['patches'][0]['fresh'])
        announce_and_sync(self.observer, now=101.0)
        feed_demo(self.observer, now=101.012)
        self.assertTrue(self.observer.snapshot(101.012)['patches'][0]['fresh'])

    def test_cached_observation_expires_at_sync_deadline(self):
        # Still-recent capture accepted just before the two-and-a-half-second deadline.
        feed_demo(self.observer, capture_ms=3490, now=102.492)
        self.assertTrue(self.observer.snapshot(102.500)['patches'][0]['fresh'])
        row = self.observer.snapshot(102.500)['patches'][0]
        self.assertLessEqual(row['valid_until_monotonic_s'], 102.502)
        row = self.observer.snapshot(102.503)['patches'][0]
        self.assertFalse(row['fresh'])
        self.assertEqual(row['reason'], 'time_sync_expired')

    def test_region_fault_revokes_pending_nonce(self):
        p = self.observer.patches[0]
        gate = self.observer.gates[(p.interface, p.node_id)]
        gate.request_sync(789, 100.020)
        self.observer.fail_region(p.interface, 'socket_overflow')
        self.assertIsNone(gate.pending)
        reply = SYNC_REPLY.pack(VERSION, 0x52, p.node_id, 789, 1, 1020, 1021, p.config_crc, 0)
        self.assertEqual(self.observer.ingest(p.interface, 0x381, reply, 100.022), 'rejected')
        self.assertIsNone(gate.sync)

    def test_bad_sync_revokes_old_mapping_and_pending_request(self):
        feed_demo(self.observer)
        p = self.observer.patches[0]
        gate = self.observer.gates[(p.interface, p.node_id)]
        gate.request_sync(789, 100.020)
        reply = SYNC_REPLY.pack(VERSION, 0x52, p.node_id, 790, 1, 1020, 1021, p.config_crc, 0)
        self.assertEqual(self.observer.ingest(p.interface, 0x381, reply, 100.022), 'rejected')
        self.assertIsNone(gate.pending)
        self.assertIsNone(gate.sync)
        self.assertFalse(self.observer.snapshot(100.022)['patches'][0]['fresh'])

    def test_all_installed_channels_failed_is_fresh_but_unavailable(self):
        p = self.observer.patches[0]
        f = Frame(15, 1, 1, 1010, p.config_crc, (255,) * 28,
                  (2400, 2500), p.expected_mask, 0, 0, 5, 0)
        self.observer.ingest(p.interface, 0x201, f.encode(), 100.012)
        row = self.observer.snapshot(100.012)['patches'][0]
        self.assertTrue(row['fresh'])
        self.assertEqual(row['unavailable_mask'], p.expected_mask)
        self.assertEqual(row['reason'], 'touch_channels_unavailable')
        self.assertFalse(row['health_ok'])


class TransportTest(unittest.TestCase):
    def setUp(self):
        self.observer = Observer(config(), demo=True)
        announce_and_sync(self.observer)
        feed_demo(self.observer)
        self.interface = self.observer.patches[0].interface
        self.transport = Transport.__new__(Transport)
        self.transport.observer = self.observer
        self.transport.dropped = {self.interface: 0}

    def test_error_and_truncated_frame_invalidate_coverage(self):
        for raw, flags in [(struct.pack('=I', CAN_ERR_FLAG), 0), (b'', 0),
                           (b'\0'*72, socket.MSG_CTRUNC), (b'\0'*16, 0)]:
            self.transport.receive(self.interface, raw, [], flags, 100.020)
            self.assertFalse(self.observer.snapshot(100.020)['patches'][0]['fresh'])

    def test_socket_overflow_invalidates_region(self):
        ancillary = [(socket.SOL_SOCKET, SO_RXQ_OVFL, struct.pack('=I', 1))]
        self.transport.receive(self.interface, b'\0'*72, ancillary, 0, 100.020)
        self.assertEqual(self.observer.gates[(self.interface,1)].reason, 'socket_overflow')

    def test_preflight_rejects_motor_five_megabit_setting(self):
        row = {'mtu':72,'flags':['UP'],'linkinfo':{'info_kind':'can','info_data':{
            'state':'ERROR-ACTIVE','bittiming':{'bitrate':1000000},'data_bittiming':{'bitrate':5000000}}}}
        with patch('subprocess.run') as run:
            run.return_value.stdout = json.dumps([row])
            with self.assertRaises(ValueError):
                check_interface('can_skin_la')
            row['linkinfo']['info_data']['data_bittiming']['bitrate']=2000000
            run.return_value.stdout = json.dumps([row])
            self.assertEqual(check_interface('can_skin_la')['mtu'],72)

    def test_dropped_periodic_sync_reply_retries_without_waiting_two_seconds(self):
        cfg = config()
        cfg['nodes'] = cfg['nodes'][:1]
        observer = Observer(cfg, demo=True)
        announce_and_sync(observer)
        p = observer.patches[0]
        key = (p.interface, p.node_id)
        transport = Transport.__new__(Transport)
        transport.observer = observer
        sock = Mock()
        transport.sockets = {p.interface: sock}
        transport.next_sync = {key: 102.0}
        with patch('select.select', return_value=([], [], [])), patch('secrets.randbits', side_effect=[1, 2]):
            transport.poll(102.0)
            transport.poll(102.010)
            self.assertEqual(sock.send.call_count, 1)
            transport.poll(102.021)
        self.assertEqual(sock.send.call_count, 2)
        self.assertEqual(observer.gates[key].pending[0], 2)


if __name__ == '__main__':
    unittest.main()
