#!/usr/bin/env python3
"""Check portable links, file naming, reference coverage and checked-in estimates."""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from engineering.models import calculate
errors=[]
for p in ROOT.rglob('*'):
 if not p.is_file() or any(x in p.parts for x in ('.git','__pycache__','.venv')):continue
 rel=p.relative_to(ROOT)
 if not str(rel).isascii():errors.append(f'Non-English filename: {rel}')
 if p.suffix in ('.md','.json','.csv','.py','.svg','.scad','.net','.yml'):
  s=p.read_text()
  if re.search(r'[\u3400-\u9fff]',s):errors.append(f'Untranslated source text: {rel}')
  if p.suffix=='.md':
   for target in re.findall(r'\]\(([^)]+)\)',s):
    target=target.strip('<>').split('#')[0]
    if not target or re.match(r'\w+://|mailto:',target):continue
    if not (p.parent/unquote(target)).exists():errors.append(f'Broken local link: {rel} -> {target}')
index=json.loads((ROOT/'research/reference_index.json').read_text())
# The evidence register retains its original numbered sources.
refs=index['records']
nums=[x.get('number',x.get('id',x.get('ref'))) for x in refs]
if sorted(nums)!=list(range(1,85)):errors.append('Research register must contain references 1..84 exactly once')
saved=json.loads((ROOT/'engineering/model_results.json').read_text())
if saved!=calculate():errors.append('Stored engineering results differ from executable model')
if (ROOT/'.gitmodules').exists():errors.append('Standalone repository must not have submodules')
languages=json.loads((ROOT/'docs/languages.json').read_text())
for pair in languages['pairs']:
 he=ROOT/pair['hebrew'];en=ROOT/pair['english']
 if not he.is_file() or not en.is_file():
  errors.append(f'Missing language companion: {pair}');continue
 hs=he.read_text();es=en.read_text()
 if not hs.startswith('<div dir="rtl" lang="he">') or not re.search(r'[\u0590-\u05ff]',hs):
  errors.append(f'Primary document must be Hebrew with RTL layout: {pair["hebrew"]}')
 code=lambda s:re.findall(r'^```[^\n]*\n(.*?)^```',s,re.M|re.S)
 if code(hs)!=code(es):errors.append(f'Code blocks differ between language versions: {pair["hebrew"]}')
# CLAUDE.md is agent guidance, not project documentation.
primary={str(p.relative_to(ROOT)) for p in ROOT.rglob('*.md') if '.git' not in p.parts and not p.name.endswith(('.en.md','.he.md')) and str(p.relative_to(ROOT))!='CLAUDE.md'}
if primary!={p['hebrew'] for p in languages['pairs']}:errors.append('Language manifest does not cover all primary Markdown documents')
manifest=json.loads((ROOT/'hardware/provenance/file_manifest.json').read_text())
for row in manifest['files']:
 if not (ROOT/row['destination_path']).is_file():errors.append(f'Missing imported hardware file: {row["destination_path"]}')
if len(manifest['files'])!=550:errors.append('Pinned hardware source must account for all 550 source files')
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print('Repository checks passed: bilingual Markdown and code, portable links, English filenames, no Chinese text, all 550 source hardware files, no submodules, reproducible estimates.')
