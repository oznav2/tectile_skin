"""Geometry/interface and physical mass-property checks; no hardware pass implied."""
import json
import math
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from added_inertia import combine_link, point_mass_delta
from generate_templates import PROFILES, profile, stencil

ASSETS = Path(__file__).resolve().parents[1] / 'assets' / 'mechanics'


class MechanicsTests(unittest.TestCase):
    def test_channel_layout_and_controller_capacity(self):
        for name, shape in PROFILES.items():
            data = profile(name, *shape)
            count = shape[0]*shape[1]
            self.assertEqual(data['active_mask'], (1 << count)-1)
            self.assertLessEqual(count, 28)
            self.assertEqual([site['index'] for site in data['sites']], list(range(count)))
            self.assertEqual(len({tuple(s['position_mm']) for s in data['sites']}), count)
            for site in data['sites']:
                self.assertLess(abs(site['position_mm'][0]), data['sensing_field_mm'][0]/2)
                self.assertLess(abs(site['position_mm'][1]), data['sensing_field_mm'][1]/2)

    def test_physical_units_and_axis_direction(self):
        data = profile('compact_2x2', 2, 2)
        root = ET.fromstring(stencil(data))
        self.assertEqual(root.get('width'), '76mm')
        self.assertEqual(root.get('height'), '91mm')
        circles = root.findall('{http://www.w3.org/2000/svg}circle')
        # SVG y grows down; mechanical +y must grow up. Channel 2 is above 0.
        self.assertLess(float(circles[2].get('cy')), float(circles[0].get('cy')))
        self.assertEqual(float(circles[1].get('cx'))-float(circles[0].get('cx')), 25)

    def test_saved_outputs_are_reproducible(self):
        data = json.loads((ASSETS/'panel_profiles.json').read_text())
        self.assertFalse(data['robot_specific_fit_validated'])
        self.assertIsNone(data['temperature_sensor_positions'])
        self.assertIsNone(data['sensor_tail_geometry'])
        for actual in data['profiles']:
            expected = profile(actual['profile_id'], *PROFILES[actual['profile_id']])
            self.assertEqual(actual, expected)
            self.assertEqual((ASSETS/(actual['profile_id']+'_template.svg')).read_text(), stencil(expected))

    def test_example_counts_and_coverage(self):
        counts = {'compact_2x2':2, 'compact_3x2':4, 'standard_7x4':2}
        examples = [(profile(name, *PROFILES[name]), quantity) for name, quantity in counts.items()]
        self.assertEqual(sum(len(p['sites'])*q for p, q in examples), 88)
        self.assertEqual(sum(p['physical_mm'][0]*p['physical_mm'][1]*q for p,q in examples), 62788)
        self.assertEqual(sum(p['sensing_field_mm'][0]*p['sensing_field_mm'][1]*q for p,q in examples), 55000)

    def test_parallel_axis_analytical_case(self):
        self.assertEqual(point_mass_delta(2, [1,0,0]), [[0,0,0],[0,2,0],[0,0,2]])
        zero = [[0.0]*3 for _ in range(3)]
        result = combine_link(1, [-1,0,0], zero,
                              [{'mass_kg':1, 'com_m':[1,0,0], 'inertia_at_com':zero}])
        self.assertEqual(result, {'mass_kg':2, 'com_m':[0,0,0], 'inertia_at_com':[[0,0,0],[0,2,0],[0,0,2]]})

    def test_intrinsic_inertia_and_translation_invariance(self):
        sphere = [[0.4,0,0],[0,0.4,0],[0,0,0.4]]
        result = combine_link(1, [100,-30,2], sphere,
                              [{'mass_kg':1, 'com_m':[100,-30,2], 'inertia_at_com':sphere}])
        self.assertEqual(result['com_m'], [100,-30,2])
        self.assertEqual(result['inertia_at_com'], [[0.8,0,0],[0,0.8,0],[0,0,0.8]])

    def test_reject_invalid_measured_properties(self):
        for mass in (-1, 0, math.nan, math.inf):
            with self.assertRaises(ValueError):
                point_mass_delta(mass, [0,0,0])
        for position in ([0,0], [0,0,math.nan]):
            with self.assertRaises(ValueError):
                point_mass_delta(1, position)
        tensors = ([[1,0,0],[0,1,0],[0,0,3]],  # Impossible principal moments.
                   [[1,.9,0],[.9,1,0],[0,0,.1]],  # Same issue in rotated axes.
                   [[1,.1,0],[0,1,0],[0,0,1]],  # Asymmetric.
                   [[1,0,0],[0,math.nan,0],[0,0,1]])
        for tensor in tensors:
            with self.assertRaises(ValueError):
                combine_link(1, [0,0,0], tensor, [])


if __name__ == '__main__':
    unittest.main()
