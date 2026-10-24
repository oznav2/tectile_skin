#!/usr/bin/env python3
"""Record or verify exact delivered bytes for every mapped hardware source file.

This checks file identity/completeness only, not physical manufacturing validity.
Use --write after an intentional, reviewed change to imported hardware assets.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = ROOT / 'hardware/provenance'


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def current_inventory():
    source = json.loads((PROVENANCE / 'file_manifest.json').read_text())
    records = []
    for row in source['files']:
        target = ROOT / row['destination_path']
        if not target.is_file():
            raise ValueError(f'Missing source-mapped file: {row["destination_path"]}')
        records.append({
            'source_path': row['source_path'],
            'source_sha256': row['source_sha256'],
            'destination_path': row['destination_path'],
            'delivered_sha256': sha256(target),
            'delivered_bytes': target.stat().st_size,
        })
    if len(records) != 550 or len({row['destination_path'] for row in records}) != 550:
        raise ValueError('The pinned source must map to 550 distinct delivered files')
    return {
        'schema_version': 1,
        'source_repository': source['source_repository'],
        'source_commit': source['source_commit'],
        'source_file_count': len(records),
        'scope': 'Final source-mapped files after translation, reidentification and documented repairs; supporting project files are versioned by Git.',
        'files': records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    destination = PROVENANCE / 'delivery_inventory.json'
    actual = current_inventory()
    if args.write:
        destination.write_text(json.dumps(actual, ensure_ascii=True, indent=2) + '\n')
        print('Recorded final hashes for all 550 mapped hardware files.')
    else:
        if not destination.is_file():
            raise SystemExit('Missing recorded delivery inventory; review assets before --write.')
        recorded = json.loads(destination.read_text())
        if actual != recorded:
            old = {row['destination_path']: row for row in recorded['files']}
            changed = [row['destination_path'] for row in actual['files'] if old.get(row['destination_path']) != row]
            raise SystemExit('Hardware inventory mismatch: ' + ', '.join(changed))
        print('All 550 source-mapped hardware files match their recorded delivered hashes.')


if __name__ == '__main__':
    main()
