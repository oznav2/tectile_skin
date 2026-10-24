#!/usr/bin/env python3
"""Translate reviewed STEP display strings without changing non-string bytes.

Read original sources only for geometry comparison; translate current imported
files so previous branding changes remain intact. No CAD kernel regeneration is
claimed. Dry-run by default; --apply atomically replaces STEP files and STEP ZIP
members, leaving every other ZIP member's content unchanged.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = ROOT/'hardware/provenance'
STRINGS = re.compile(rb"'(?:[^']|'')*'", re.S)
CJK = re.compile(r'[\u3400-\u9fff]')
OLD_ID = re.compile(r'YCL\.[A-Z]\d+')
NEW_ID = re.compile(r'ROBOSKIN\.\d+')


def decode_literal(raw):
    body = raw[1:-1].replace(b"''", b"'")
    try:
        text = body.decode('utf-8')
    except UnicodeDecodeError:
        text = body.decode('gb18030', errors='strict')
    for kind, codec in [('2', 'utf-16-be'), ('4', 'utf-32-be')]:
        text = re.sub(r'\\X'+kind+r'\\([0-9A-Fa-f]+)\\X0\\',
                      lambda m: bytes.fromhex(m[1]).decode(codec), text)
    return text


def encode_literal(text):
    result = []
    for chunk in re.findall(r'[\x00-\x7f]+|[^\x00-\x7f]+', text):
        result.append(chunk.replace("'", "''") if chunk.isascii() else
                      '\\X2\\'+chunk.encode('utf-16-be').hex().upper()+'\\X0\\')
    return ("'"+''.join(result)+"'").encode('ascii')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def localize(current, original, filename, translations, registry):
    if STRINGS.sub(b"''", current) != STRINGS.sub(b"''", original):
        raise ValueError(f'Existing non-string geometry differs from original: {filename}')
    inverse = {value:key for key,value in registry.items()}
    changes = 0
    def replace(match):
        nonlocal changes
        raw = match[0]
        if raw.isascii() and b'\\X2\\' not in raw and b'\\X4\\' not in raw and b'YCL.' not in raw:
            return raw
        text = decode_literal(raw)
        is_name = bool(re.search(rb'FILE_NAME\s*\(\s*$', current[max(0,match.start()-60):match.start()], re.I))
        if is_name and CJK.search(text):
            new = filename
        elif CJK.search(text):
            key = NEW_ID.sub(lambda m: inverse.get(m[0],m[0]), text)
            if key not in translations:
                raise ValueError('Unreviewed STEP label: '+repr(key))
            new = translations[key]
        else:
            new = text
        new = OLD_ID.sub(lambda m: registry.get(m[0],m[0]), new)
        if CJK.search(new):
            raise ValueError('Chinese remains after translation')
        if new == text:
            return raw
        changes += 1
        return encode_literal(new)
    final = STRINGS.sub(replace, current)
    if STRINGS.sub(b"''", final) != STRINGS.sub(b"''", original):
        raise AssertionError('Localization changed non-string STEP bytes')
    remaining = 0
    for match in STRINGS.finditer(final):
        raw = match[0]
        if not raw.isascii() or b'\\X2\\' in raw or b'\\X4\\' in raw:
            remaining += bool(CJK.search(decode_literal(raw)))
    if remaining:
        raise AssertionError('Residual decoded Chinese label')
    return final, {'source_sha256':digest(original), 'before_sha256':digest(current),
                   'final_sha256':digest(final), 'translated_display_strings':changes,
                   'non_string_geometry_unchanged':True, 'decoded_chinese_labels_remaining':0,
                   'native_cad_regenerated':False, 'hebrew_cad_rendering_verified':False}


def atomic_write(path, content):
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.'+path.name+'.', delete=False) as temp:
        temp.write(content)
        temp.flush()
        os.fsync(temp.fileno())
        temporary = Path(temp.name)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True, help='Unmodified source hardware checkout')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    translations = json.loads((PROVENANCE/'step_translation_map.json').read_text())
    registry = {p['upstream_part_id']:p['roboskin_id'] for p in json.loads((PROVENANCE/'part_registry.json').read_text())['parts']}
    manifest = json.loads((PROVENANCE/'file_manifest.json').read_text())
    checks = []
    for item in manifest['files']:
        path = ROOT/item['destination_path']
        source = args.source/item['source_path']
        if path.suffix.lower() in ('.step','.stp'):
            final, check = localize(path.read_bytes(), source.read_bytes(), path.name, translations, registry)
            if args.apply:
                atomic_write(path, final)
                if digest(path.read_bytes()) != check['final_sha256']:
                    raise AssertionError('Written file verification failed')
            checks.append({'path':item['destination_path'], **check})
        elif path.suffix.lower()=='.zip':
            original_zip = zipfile.ZipFile(source)
            current_zip = zipfile.ZipFile(path)
            targets = [n for n in current_zip.namelist() if n.lower().endswith(('.step','.stp'))]
            original_targets = [n for n in original_zip.namelist() if n.lower().endswith(('.step','.stp'))]
            if not targets:
                original_zip.close(); current_zip.close(); continue
            if len(targets) != 1 or len(original_targets) != 1:
                raise ValueError('Ambiguous ZIP STEP mapping: '+str(path))
            member = targets[0]
            final, check = localize(current_zip.read(member), original_zip.read(original_targets[0]),
                                    Path(member).name, translations, registry)
            if args.apply:
                buf = io.BytesIO()
                untouched = {}
                with zipfile.ZipFile(buf,'w') as result:
                    result.comment = current_zip.comment
                    for info in current_zip.infolist():
                        data = current_zip.read(info)
                        if info.filename != member:
                            untouched[info.filename] = digest(data)
                        result.writestr(info, final if info.filename==member else data)
                current_zip.close()
                atomic_write(path, buf.getvalue())
                with zipfile.ZipFile(path) as written:
                    assert written.testzip() is None
                    assert digest(written.read(member))==check['final_sha256']
                    assert all(digest(written.read(n))==h for n,h in untouched.items())
            current_zip.close(); original_zip.close()
            checks.append({'path':item['destination_path'], 'member':member,
                           'other_zip_members_unchanged':True, **check})
    report = {'schema_version':2, 'source_commit':manifest['source_commit'],
              'applied':args.apply, 'checks':checks,
              'scope':'Every mapped standalone STEP and STEP-containing ZIP member; display strings only. Non-string bytes compared with original source, no CAD regeneration or Hebrew CAD rendering claim.',
              'translation_map_sha256':digest((PROVENANCE/'step_translation_map.json').read_bytes())}
    if args.apply:
        atomic_write(PROVENANCE/'step_geometry_checks.json', (json.dumps(report,ensure_ascii=True,indent=2)+'\n').encode())
    print(json.dumps({'applied':args.apply,'documents':len(checks),
                      'translated_strings':sum(c['translated_display_strings']for c in checks),
                      'non_string_checks_passed':sum(c['non_string_geometry_unchanged']for c in checks),
                      'decoded_chinese_labels_remaining':sum(c['decoded_chinese_labels_remaining']for c in checks)}))


if __name__=='__main__':
    main()
