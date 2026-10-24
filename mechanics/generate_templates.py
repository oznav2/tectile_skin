#!/usr/bin/env python3
"""Generate original, platform-neutral fit stencils and channel coordinates.

These are dimensional inspection aids, not conductive artwork or production CAD.
Only Python's standard library is needed.
"""
import json
from pathlib import Path

DESTINATION = Path(__file__).resolve().parents[1] / 'assets' / 'mechanics'
PITCH_MM = 25.0
PERIMETER_MM = 3.0
PROFILES = {'compact_2x2': (2, 2), 'compact_3x2': (3, 2), 'standard_7x4': (7, 4)}


def profile(name, columns, rows):
    sensing = [columns * PITCH_MM, rows * PITCH_MM]
    physical = [v + 2 * PERIMETER_MM for v in sensing]
    return {
        'profile_id': name, 'columns': columns, 'rows': rows,
        'pitch_mm': PITCH_MM, 'nominal_perimeter_mm': PERIMETER_MM,
        'physical_mm': physical, 'sensing_field_mm': sensing,
        'active_mask': (1 << (columns * rows)) - 1,
        'controller_contact_capacity': 28,
        'sites': [{'index': row * columns + column,
                   'position_mm': [(column - (columns - 1) / 2) * PITCH_MM,
                                   (row - (rows - 1) / 2) * PITCH_MM, 0.0],
                   'normal': [0.0, 0.0, 1.0]}
                  for row in range(rows) for column in range(columns)],
    }


def stencil(data):
    length, width = data['physical_mm']
    sx, sy = data['sensing_field_mm']
    # Margin and footer are page furniture, not part of the film.
    page_length, page_width = length + 20, width + 35
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{page_length:g}mm" height="{page_width:g}mm" viewBox="0 0 {page_length:g} {page_width:g}">',
             '<title>ROBOSKIN physical fit stencil; not electrode artwork</title>',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<rect x="10" y="10" width="{length:g}" height="{width:g}" rx="3" fill="none" stroke="black" stroke-width="0.2"/>',
             f'<rect x="13" y="13" width="{sx:g}" height="{sy:g}" fill="none" stroke="blue" stroke-width="0.15"/>']
    for site in data['sites']:
        x = 10 + length / 2 + site['position_mm'][0]
        y = 10 + width / 2 - site['position_mm'][1]
        parts += [f'<circle cx="{x:g}" cy="{y:g}" r="2" fill="none" stroke="green" stroke-width="0.2"/>',
                  f'<text x="{x+3:g}" y="{y+1:g}" font-family="sans-serif" font-size="3">{site["index"]}</text>']
    parts += [f'<path d="M10 {width+20:g} h25" stroke="black" stroke-width="0.5"/>',
              f'<text x="10" y="{width+25:g}" font-family="sans-serif" font-size="2.6">25 mm check | {data["profile_id"]}</text>',
              f'<text x="10" y="{width+30:g}" font-family="sans-serif" font-size="2.6">+x right; +y up; +z out of page</text>', '</svg>']
    return '\n'.join(parts) + '\n'


def main():
    DESTINATION.mkdir(parents=True, exist_ok=True)
    profiles = [profile(name, *shape) for name, shape in PROFILES.items()]
    payload = {'schema_version': 1, 'status': 'DIMENSIONAL_PROTOTYPE_NOT_MANUFACTURING_RELEASE',
               'coordinate_origin': 'center of nominal sensing field',
               'robot_specific_fit_validated': False,
               'temperature_sensor_positions': None,
               'sensor_tail_geometry': None,
               'profiles': profiles,
               'eight_panel_example': {
                   'compact_2x2': 2, 'compact_3x2': 4, 'standard_7x4': 2,
                   'contact_sites': 88, 'local_temperature_channels': 16,
                   'note': 'Arithmetic example only; panel locations and robot fit are not specified.'}}
    (DESTINATION / 'panel_profiles.json').write_text(json.dumps(payload, indent=2) + '\n')
    for data in profiles:
        (DESTINATION / (data['profile_id'] + '_template.svg')).write_text(stencil(data))
    print(f'Generated {len(profiles)} original stencils and profile definitions in {DESTINATION}')


if __name__ == '__main__':
    main()
