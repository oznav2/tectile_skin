import unittest
from dataclasses import replace
from software.skin_protocol import Frame, Gate, ANNOUNCE, SYNC_REPLY, MASK, delta32

UID = '0102030405060708090a0b0c'
CFG = 0x12345678


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.gate = Gate(UID, 1, CFG)
        self.gate.announce(ANNOUNCE.pack(2, 0xa1, 1, bytes.fromhex(UID), 7, CFG, 7, 10, 0))
        self.gate.request_sync(1234, 10.0)
        self.gate.accept_sync(SYNC_REPLY.pack(2, 0x52, 1, 1234, 7, 1000, 1001, CFG, 0), 10.004)
        self.frame = Frame(15, 100, 7, 1010, CFG, (0,) * 28,
                           (2500, 2600), 0, 0, MASK, 20, 0)

    def test_round_trip(self):
        self.assertEqual(Frame.decode(self.frame.encode()), self.frame)
        self.assertEqual(len(self.frame.encode()), 64)

    def test_rejected_identity_cannot_resync_with_old_epoch(self):
        other_uid = bytes.fromhex('ff' * 12)
        self.gate.accept(self.frame.encode(), 10.015)
        self.gate.request_sync(4567, 10.016)
        bad = ANNOUNCE.pack(2, 0xa1, 1, other_uid, 7, CFG, 7, 10, 0)
        with self.assertRaises(ValueError):
            self.gate.announce(bad)
        self.assertIsNone(self.gate.boot)
        self.assertIsNone(self.gate.pending)
        self.assertIsNone(self.gate.sync)
        with self.assertRaisesRegex(ValueError, 'announce first'):
            self.gate.request_sync(5678, 10.017)
        with self.assertRaises(ValueError):
            self.gate.accept(self.frame.encode(), 10.018)
        self.assertFalse(self.gate.coverage_available(10.019))

    def test_malformed_announcement_revokes_identity(self):
        self.gate.accept(self.frame.encode(), 10.015)
        with self.assertRaises(ValueError):
            self.gate.announce(b'bad')
        self.assertIsNone(self.gate.boot)
        self.assertFalse(self.gate.coverage_available(10.016))

    def test_last_good_sample_cannot_outlive_sync(self):
        near_expiry = replace(self.frame, capture_ms=3495)
        result = self.gate.accept(near_expiry.encode(), 12.499)
        self.assertLessEqual(result['valid_until_monotonic_s'], 12.504)
        self.assertTrue(self.gate.coverage_available(12.500))
        self.assertFalse(self.gate.coverage_available(12.505))

    def test_valid(self):
        result = self.gate.accept(self.frame.encode(), 10.015)
        self.assertEqual(result['temperature_C'], [25.0, 26.0])
        self.assertTrue(self.gate.coverage_available(10.020))
        self.assertFalse(self.gate.coverage_available(10.060))

    def test_delayed_packet_fresh_reception_does_not_help(self):
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.gate.accept(self.frame.encode(), 10.200)
        self.assertFalse(self.gate.coverage_available(10.200))

    def test_duplicate_invalidates(self):
        self.gate.accept(self.frame.encode(), 10.015)
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.gate.accept(self.frame.encode(), 10.016)
        self.assertFalse(self.gate.coverage_available(10.016))

    def test_boot_mismatch(self):
        with self.assertRaisesRegex(ValueError, 'boot'):
            self.gate.accept(replace(self.frame, boot=8).encode(), 10.015)

    def test_zero_boot_epoch_rejected(self):
        with self.assertRaisesRegex(ValueError, 'boot_epoch'):
            self.gate.announce(ANNOUNCE.pack(2, 0xa1, 1, bytes.fromhex(UID), 0, CFG, 7, 10, 0))

    def test_future_capture_rejected(self):
        with self.assertRaisesRegex(ValueError, 'future'):
            self.gate.accept(replace(self.frame, capture_ms=1100).encode(), 10.015)

    def test_config_mismatch(self):
        with self.assertRaisesRegex(ValueError, 'config'):
            self.gate.accept(replace(self.frame, config_crc=0).encode(), 10.015)

    def test_overload_is_retained(self):
        f = replace(self.frame, overload_mask=1, intensity=(254,) + (0,) * 27)
        self.assertEqual(self.gate.accept(f.encode(), 10.015)['contact_or_fault_mask'], 1)

    def test_open_cannot_be_valid(self):
        with self.assertRaisesRegex(ValueError, 'open'):
            self.gate.accept(replace(self.frame, open_mask=1).encode(), 10.015)

    def test_invalid_sentinel(self):
        f = replace(self.frame, open_mask=1, valid_mask=MASK ^ 1, intensity=(255,) + (0,) * 27)
        self.assertEqual(self.gate.accept(f.encode(), 10.015)['valid_mask'], MASK ^ 1)

    def test_temperature_age_and_disconnect(self):
        f = replace(self.frame, temperature_age_ms=300)
        self.assertEqual(self.gate.accept(f.encode(), 10.015)['temperature_C'], [None, None])

    def test_temperature_age_includes_transport(self):
        f = replace(self.frame, temperature_age_ms=249)
        self.assertEqual(self.gate.accept(f.encode(), 10.015)['temperature_C'], [None, None])

    def test_all_cells_invalid_means_no_coverage(self):
        f = replace(self.frame, valid_mask=0, intensity=(255,) * 28)
        self.gate.accept(f.encode(), 10.015)
        self.assertFalse(self.gate.coverage_available(10.016))

    def test_downstream_deadline_is_capture_based(self):
        result = self.gate.accept(self.frame.encode(), 10.035)
        self.assertLess(result['valid_until_monotonic_s'], 10.050)

    def test_capability_mismatch_removes_coverage(self):
        self.gate.accept(self.frame.encode(), 10.015)
        with self.assertRaises(ValueError):
            self.gate.announce(ANNOUNCE.pack(2, 0xa1, 1, bytes.fromhex(UID), 7, CFG, 0, 10, 0))
        self.assertFalse(self.gate.coverage_available(10.016))

    def test_bank_diagnostic(self):
        with self.assertRaisesRegex(ValueError, 'bank'):
            self.gate.accept(replace(self.frame, diagnostics=1).encode(), 10.015)

    def test_sync_expiration(self):
        with self.assertRaisesRegex(ValueError, 'expired'):
            self.gate.accept(self.frame.encode(), 13.0)

    def test_delayed_sync_rejected(self):
        self.gate.request_sync(99, 11.0)
        with self.assertRaisesRegex(ValueError, 'round-trip'):
            self.gate.accept_sync(SYNC_REPLY.pack(2, 0x52, 1, 99, 7, 2000, 2001, CFG, 0), 11.200)

    def test_nonce_checked(self):
        self.gate.request_sync(99, 11.0)
        with self.assertRaisesRegex(ValueError, 'identity'):
            self.gate.accept_sync(SYNC_REPLY.pack(2, 0x52, 1, 98, 7, 2000, 2001, CFG, 0), 11.004)

    def test_sequence_wrap(self):
        self.gate.accept(replace(self.frame, sequence=65535).encode(), 10.015)
        self.gate.accept(replace(self.frame, sequence=0, capture_ms=1020).encode(), 10.025)

    def test_uptime_wrap(self):
        self.assertEqual(delta32(2, 0xfffffffe), 4)
        self.gate.request_sync(99, 20.0)
        self.gate.accept_sync(SYNC_REPLY.pack(2, 0x52, 1, 99, 7, 0xfffffffe, 0xffffffff, CFG, 0), 20.004)
        self.gate.accept(replace(self.frame, capture_ms=8).encode(), 20.015)

    def test_truncation_and_version(self):
        with self.assertRaises(ValueError):
            Frame.decode(self.frame.encode()[:-1])
        with self.assertRaises(ValueError):
            Frame.decode(bytes([1]) + self.frame.encode()[1:])

    def test_bad_announce_invalidates_existing_data(self):
        self.gate.accept(self.frame.encode(), 10.015)
        with self.assertRaises(ValueError):
            self.gate.announce(ANNOUNCE.pack(2, 0xa1, 1, bytes(12), 7, CFG, 7, 10, 0))
        self.assertFalse(self.gate.coverage_available(10.016))


if __name__ == '__main__':
    unittest.main()
