import unittest
from dataclasses import replace
from software.skin_events import Reporter
from software.skin_protocol import Frame


def compact(t, valid=15):
    return Frame(15, t // 10, 1, t, 123, (0,) * 4 + (255,) * 24,
                 (2500, 2500), 0, 0, valid, 0, 0)


class CompactProfiles(unittest.TestCase):
    def test_disabled_cells_do_not_trigger_fault_traffic(self):
        r = Reporter(expected_mask=15)
        sent = []
        for t in range(0, 1000, 10):
            p = r.consider(compact(t), 0, t)
            if p:
                sent.append(p)
                r.complete(p, True)
        self.assertEqual(len(sent), 50)
        self.assertNotIn('ongoing_fault', [p.reason for p in sent])

    def test_enabled_cell_failure_still_reports_every_scan(self):
        r = Reporter(expected_mask=15)
        p = r.consider(compact(0), 0, 0)
        r.complete(p, True)
        for t in (10, 20, 30):
            f = replace(compact(t, 14), intensity=(255, 0, 0, 0) + (255,) * 24)
            p = r.consider(f, 0, t)
            self.assertIsNotNone(p)
            r.complete(p, True)

    def test_disabled_channel_cannot_generate_contact(self):
        with self.assertRaises(ValueError):
            Reporter(expected_mask=15).consider(compact(0), 16, 0)

    def test_disabled_channel_cannot_become_valid(self):
        with self.assertRaises(ValueError):
            Reporter(expected_mask=7).consider(compact(0), 0, 0)

    def test_mask_must_be_nonempty_and_bounded(self):
        for mask in (0, -1, 1 << 28, True):
            with self.assertRaises(ValueError):
                Reporter(expected_mask=mask)
