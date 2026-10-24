import math
import random
import unittest
from dataclasses import replace

from software.skin_protocol import Frame, MASK
from software.skin_events import Reporter
from software.skin_wrench import aggregate, change_axes, cross, project, shift_origin, virtual_force


def frame(t, value=0, **kwargs):
    f = Frame(15, (t // 10) & 65535, 1, t & 0xffffffff, 123,
              (value,) * 28, (2500, 2500), 0, 0, MASK, 0, 0)
    return replace(f, **kwargs)


class Events(unittest.TestCase):
    def send(self, r, f, mask=0, success=True):
        p = r.consider(f, mask, (f.capture_ms + 5) & 0xffffffff)
        if p:
            r.complete(p, success)
        return p

    def test_idle_half_frames_with_full_values(self):
        r = Reporter()
        sent = [self.send(r, frame(t)) for t in range(0, 1000, 10)]
        self.assertEqual(sum(p is not None for p in sent), 50)
        self.assertTrue(all(len(p.frame.encode()) == 64 for p in sent if p))

    def test_periodic_comparator_same_samples(self):
        r = Reporter(mode='periodic')
        self.assertEqual(sum(self.send(r, frame(t)) is not None for t in range(0, 1000, 10)), 100)

    def test_threshold_compares_last_sent_not_last_sample(self):
        r = Reporter()
        self.send(r, frame(0))
        self.assertIsNone(self.send(r, frame(10, 3)))
        self.assertEqual(self.send(r, frame(20, 4)).reason, 'touch_delta')

    def test_contact_edge_bypasses_small_delta(self):
        r = Reporter()
        self.send(r, frame(0))
        self.assertEqual(self.send(r, frame(10, 1), 1).reason, 'contact_transition')
        self.assertEqual(self.send(r, frame(20, 1), 1).reason, 'active_contact')
        self.assertEqual(self.send(r, frame(30), 0).reason, 'contact_transition')

    def test_fault_not_hidden_by_delta(self):
        r = Reporter()
        self.send(r, frame(0))
        self.assertEqual(self.send(r, frame(10, flags=7)).reason, 'health_transition')
        self.assertEqual(self.send(r, frame(20, flags=7)).reason, 'ongoing_fault')

    def test_open_and_overload_retained(self):
        r = Reporter()
        self.send(r, frame(0))
        f = frame(10, intensity=(255,) + (0,)*27, valid_mask=MASK ^ 1, open_mask=1, overload_mask=2)
        p = self.send(r, f)
        self.assertEqual(p.frame.open_mask, 1)
        self.assertEqual(p.frame.overload_mask, 2)

    def test_failed_transmission_does_not_advance_baseline(self):
        r = Reporter()
        self.send(r, frame(0))
        self.send(r, frame(10, 10), success=False)
        self.assertEqual(r.last.frame.capture_ms, 0)
        p = self.send(r, frame(20, 9))
        self.assertEqual(p.reason, 'retry_latest_snapshot')
        self.assertEqual(r.last.frame.intensity[0], 9)

    def test_pending_tx_requires_explicit_resolution(self):
        r = Reporter()
        p = r.consider(frame(0), 0, 5)
        with self.assertRaises(RuntimeError):
            r.consider(frame(10), 0, 15)
        r.complete(p, False)
        self.assertIsNotNone(self.send(r, frame(20)))

    def test_temperature_and_invalid_transition(self):
        r = Reporter()
        self.send(r, frame(0))
        self.assertEqual(self.send(r, frame(10, temperatures=(2550, 2500))).reason, 'temperature_delta')
        self.assertEqual(self.send(r, frame(20, temperatures=(-32768, 2500))).reason, 'health_transition')

    def test_capture_wrap(self):
        r = Reporter()
        self.send(r, frame(0xfffffff0))
        self.assertIsNone(self.send(r, frame(0xfffffffa)))
        self.assertEqual(self.send(r, frame(0x100000004)).reason, 'absolute_refresh')

    def test_ongoing_thermal_fault_sends_every_scan(self):
        for kwargs in ({'temperature_age_ms': 300},
                       {'temperatures': (-32768, 2500)},
                       {'temperatures': (9000, 2500)}):
            with self.subTest(kwargs=kwargs):
                r = Reporter()
                self.send(r, frame(0, **kwargs))
                self.assertEqual(self.send(r, frame(10, **kwargs)).reason, 'ongoing_fault')
                self.assertEqual(self.send(r, frame(20, **kwargs)).reason, 'ongoing_fault')

    def test_pending_snapshot_defensively_copies_channels(self):
        r = Reporter()
        channels, temperatures = [0] * 28, [2500, 2500]
        proposal = r.consider(frame(0, intensity=channels, temperatures=temperatures), 0, 5)
        channels[0], temperatures[0] = 50, 8000
        self.assertEqual(proposal.frame.intensity[0], 0)
        r.complete(proposal, True)
        self.assertEqual(r.last.frame.temperatures[0], 2500)

    def test_new_epoch_forces_absolute_state(self):
        r = Reporter()
        self.send(r, frame(0))
        self.assertEqual(self.send(r, frame(0, boot=2)).reason, 'initial_or_new_epoch')

    def test_expired_snapshot_not_enqueued(self):
        with self.assertRaises(ValueError):
            Reporter().consider(frame(0), 0, 30)

    def test_receiver_missed_event_recovers_absolute_value(self):
        r = Reporter()
        self.send(r, frame(0))
        self.send(r, frame(10, 20))  # CAN TX completed; pretend host lost it
        self.assertIsNone(self.send(r, frame(20, 20)))
        recovered = self.send(r, frame(30, 20))
        self.assertEqual(recovered.frame.intensity, (20,) * 28)


class Wrenches(unittest.TestCase):
    def test_off_center_force_moment(self):
        self.assertEqual(aggregate([((.2, 0, 0), (0, 5, 0))]), (0, 5, 0, 0, 0, 1))

    def test_opposite_contacts_cancel_force_not_couple(self):
        w = aggregate([((1, 0, 0), (0, 1, 0)), ((-1, 0, 0), (0, -1, 0))])
        self.assertEqual(w, (0, 0, 0, 0, 0, 2))

    def test_shift_and_rotation_are_distinct(self):
        w = (0, 1, 0, 0, 0, 0)
        r = ((0, -1, 0), (1, 0, 0), (0, 0, 1))
        self.assertEqual(change_axes(w, r), (-1, 0, 0, 0, 0, 0))
        self.assertEqual(shift_origin(w, (1, 0, 0)), (0, 1, 0, 0, 0, 1))

    def test_aggregate_matches_point_jacobians_randomized(self):
        rng = random.Random(2019)
        for _ in range(100):
            axes = [(0, 0, 1), (0, 1, 0), (1, 0, 0)]
            origins = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in axes]
            link_origin = tuple(rng.uniform(-1, 1) for _ in range(3))
            contacts = [(tuple(rng.uniform(-.2, .2) for _ in range(3)),
                         tuple(rng.uniform(-2, 2) for _ in range(3))) for _ in range(28)]
            columns = [cross(z, tuple(a-b for a, b in zip(link_origin, o))) + z for z, o in zip(axes, origins)]
            j = tuple(zip(*columns))
            aggregated = project(j, aggregate(contacts))
            direct = [0.] * 3
            for r, f in contacts:
                p = tuple(a+b for a, b in zip(link_origin, r))
                for k, (z, o) in enumerate(zip(axes, origins)):
                    tangent = cross(z, tuple(a-b for a, b in zip(p, o)))
                    direct[k] += sum(a*b for a, b in zip(tangent, f))
            for a, b in zip(aggregated, direct):
                self.assertAlmostEqual(a, b, places=11)

    def test_virtual_work_identity(self):
        j = ((0, 1), (1, 0), (0, 0), (0, 0), (0, 0), (1, 1))
        w, qdot = (1, 2, 0, 0, 0, 3), (.2, -.1)
        tau = project(j, w)
        velocity = [sum(a*b for a, b in zip(row, qdot)) for row in j]
        self.assertAlmostEqual(sum(a*b for a, b in zip(tau, qdot)), sum(a*b for a, b in zip(w, velocity)))

    def test_virtual_force_direction_and_cap(self):
        self.assertEqual(virtual_force(254, (0, 0, 1), 5, 2), (0, 0, -2))
        with self.assertRaises(ValueError):
            virtual_force(255, (0, 0, 1), 5, 2)

    def test_reject_reflection_nan_bad_jacobian(self):
        with self.assertRaises(ValueError):
            change_axes((0,)*6, ((-1, 0, 0), (0, 1, 0), (0, 0, 1)))
        with self.assertRaises(ValueError):
            aggregate([((math.nan, 0, 0), (0, 1, 0))])
        with self.assertRaises(ValueError):
            project(((0,),) * 5, (0,) * 6)


if __name__ == '__main__':
    unittest.main()
