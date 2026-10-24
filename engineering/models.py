#!/usr/bin/env python3
"""Reproducible design accounting. Predictions, not measurements or quotations."""
from pathlib import Path
import csv
import json
import math

ROOT = Path(__file__).resolve().parent


def calculate():
    with (ROOT / 'cost_inputs.csv').open() as f:
        rows = list(csv.DictReader(f))
    materials = sum(float(r['quantity']) * float(r['unit_usd_1000_patches']) for r in rows)
    low = sum(float(r['quantity']) * float(r['low_unit_usd']) for r in rows)
    high = sum(float(r['quantity']) * float(r['high_unit_usd']) for r in rows)
    # 120 lamination + 60 electrical + 120 attended calibration + 45 final seconds.
    labor_s, labor_per_h = 345, 24
    # Electrical station 60s; mechanical station 240s. Includes amortization/utilities.
    machine_s, machine_per_h = 300, 12
    process = labor_s * labor_per_h / 3600 + machine_s * machine_per_h / 3600
    yield_rate, rework_per_start = .95, .50
    patch = round((materials + process + rework_per_start) / yield_rate, 2)
    # Keep currency conversion explicit: planning conversion, NOT a market quote.
    gateway_each = 400
    def installed(n, spare_fraction=.10):
        regions = math.ceil(n / 8)
        # Isolated lab gateway + regional distributor/harness/box; one reusable PSU.
        shared = regions * (gateway_each + 67) + 300 + (100 if regions > 4 else 0)
        return {'patches': n, 'regions': regions, 'shared_usd': shared,
                'installed_usd': n * patch + shared,
                'installed_with_spares_usd': (n + math.ceil(n * spare_fraction)) * patch + shared}
    # Deliberately padded no-error airtime envelope, not an exact CAN-FD simulator.
    nominal_bits = 80
    fast_bits = math.ceil((64 * 8 + 40) * 1.25) + 20
    airtime = nominal_bits / 1e6 + fast_bits / 2e6
    rb, eol, vref = 22000, 100000, 3.3
    code = lambda r, bias=rb: 4095 * r / (bias + r)
    idle_min = code(eol * .8, rb * 1.01)
    idle_max = code(eol * 1.2, rb * .99)
    r_thevenin = 1 / (1 / (rb * 1.01) + 1 / (eol * 1.2))
    # Project budget 3uA entire selected path, 10 counts other electrical errors.
    # Conservative: attribute aggregate leakage through the entire 1k + 4.7k path.
    idle_error = 3e-6 * (r_thevenin + 5700 * 1.01) / 3.1 * 4095 + 10
    opened_min = 4095 - (3e-6 * (rb + 5700) * 1.01 / 3.1 * 4095 + 10)
    ntc_i = vref / (39000 + 10000)
    temperature_example = {'ntc_current_uA_at_25C': ntc_i * 1e6,
                           'ntc_dissipation_uW_at_25C': ntc_i**2 * 10000 * 1e6,
                           'ntc_code_at_25C': code(10000, 39000)}
    copper_density = 8960
    direct_wire_kg = 2240 * 2 * 2 * .032 * 1e-6 * copper_density
    # Geometric strain for a flex layer at outer surface (not a cable life prediction).
    result = {
        'materials_usd': round(materials, 4), 'material_low_high_usd': [round(low, 2), round(high, 2)],
        'labor_seconds_per_patch': labor_s, 'machine_seconds_per_patch': machine_s,
        'process_usd': process, 'yield': yield_rate, 'patch_usd': round(patch, 4),
        'robot_scenarios': [installed(n) for n in (8, 16, 36, 80)],
        'bus_airtime_bound_us_no_errors': airtime * 1e6,
        'bus_8nodes_100Hz_utilization': airtime * 8 * 100,
        'bus_plus_20_diagnostic_frames_per_s': airtime * (8 * 100 + 20),
        'scan_seven_channels_8addresses_us': 8 * (250 + 7 * 2 * (160.5 + 12.5) / 8),
        'idle_adc_nominal': code(eol), 'idle_adc_tolerance': [idle_min, idle_max],
        'idle_error_bound_counts': idle_error, 'open_adc_lower_bound': opened_min,
        'open_threshold': 3900, 'reference_codes': [4095 * x for x in (.25, .4, .6, .75)],
        'temperature': temperature_example,
        '24AWG_2m_loop_ohm_20C': .336,
        '24AWG_2m_loop_ohm_50C': .336 * (1 + .00393 * 30),
        'direct_2240_individual_2m_32AWG_pairs_bare_copper_kg': direct_wire_kg,
        'one_patch_active_area_m2': 28 * .023**2,
        'eighty_patch_active_area_m2_before_overlap': 80 * 28 * .023**2,
        'retail_film_24_5mm_squares_per_11_5x13inch_sheet': math.floor(11.5 * 25.4 / 24.5) * math.floor(13 * 25.4 / 24.5),
        'full_patch_groups_from_retail_film': (math.floor(11.5 * 25.4 / 24.5) * math.floor(13 * 25.4 / 24.5)) // 28,
        'parallel_calibration_28cells_at_20N_total_N': 28 * 20,
        '95percent_zero_failure_lower_reliability_n30': .05**(1/30),
        'n_for_99percent_reliability_95confidence_zero_failures': math.ceil(math.log(.05) / math.log(.99))
    }
    assert idle_max + idle_error < 3900 < opened_min
    assert result['bus_plus_20_diagnostic_frames_per_s'] < .40
    assert result['scan_seven_channels_8addresses_us'] < 5000
    return result


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2))
