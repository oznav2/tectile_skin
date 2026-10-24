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
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print('Repository checks passed: portable local links, English filenames, no Chinese text, no submodules, reproducible estimates.')
