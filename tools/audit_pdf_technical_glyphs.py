from pathlib import Path
import re,json,math,hashlib,time
import pymupdf as fitz
import argparse
parser=argparse.ArgumentParser(description='Audit original technical text origins against adapted original PDF pages; ignores appended registers.')
parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--source-root',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args();ROOT=args.root;SRC=args.source_root
manifest=json.loads((ROOT/'hardware/provenance/file_manifest.json').read_text())
CJK=re.compile(r'[\u3400-\u9fff\uf900-\ufaff]')
BRAND=re.compile(r'(?:YCL\.|ROBOSKIN\.|RoboParty|Robo Party|RP1|Shanghai)',re.I)
# Broad intentional-text exclusions; all standalone numeric, dimension, material and symbol spans remain candidates.
NONT=re.compile(r'^(?:www\.|https?:|.*@)|Liner Measure|Chamfer|Angle|Limit|APPROV|DRAWN|CHECK|DRAWING|DATE|DESIGN',re.I)
summary={'schema_version':1,'source_commit':manifest['source_commit'],'method':'Compare every original page before appended registers. CJK-free nonbranding non-label source spans checked character-by-character against same character within 0.75pt origin in destination rawdict. No PDFs modified. Missing spans are review candidates: relocated text is not assumed preserved at manufacturing coordinate.','files':[],'missing_candidates':[],'started':time.time()}
def chars(page):
 out=[]; spans=[]
 for block in page.get_text('rawdict')['blocks']:
  for line in block.get('lines',[]):
   for span in line['spans']:
    cs=span.get('chars',[]); text=''.join(c['c'] for c in cs)
    spans.append({'text':text,'chars':cs,'bbox':span['bbox'],'font':span['font'],'size':span['size'],'dir':line['dir'],'line_text':''.join(''.join(c['c'] for c in z.get('chars',[])) for z in line['spans'])})
    out.extend(cs)
 return out,spans
for row in manifest['files']:
 if not row['source_path'].lower().endswith('.pdf'):continue
 sp=SRC/row['source_path']; dp=ROOT/row['destination_path']
 rec={'source_path':row['source_path'],'destination_path':row['destination_path']}
 if not sp.exists() or not dp.exists():rec['error']='missing file';summary['files'].append(rec);continue
 sd=fitz.open(sp);dd=fitz.open(dp)
 rec.update(source_pages=len(sd),destination_pages=len(dd),candidate_spans=0,missing_spans=0)
 if 'Architecture.pdf' in row['source_path']:
  rec['excluded']='Fully redrawn architecture; requires semantic audit, not positional comparison.';summary['files'].append(rec);continue
 for pno in range(min(len(sd),len(dd))):
  sc,ss=chars(sd[pno]);dc,ds=chars(dd[pno]);ix={}
  for c in dc:
   x,y=c['origin'];ix.setdefault((c['c'],round(x),round(y)),[]).append((x,y))
  def exists(c):
   x,y=c['origin'];k=c['c']
   for dx in (-1,0,1):
    for dy in (-1,0,1):
     for u,v in ix.get((k,round(x)+dx,round(y)+dy),[]):
      if abs(x-u)<=.75 and abs(y-v)<=.75:return True
   return False
  for s in ss:
   text=s['text'].strip()
   if not text or CJK.search(text) or BRAND.search(text) or NONT.search(text):continue
   # Retain all technical glyphs, including letters and graphical font-mapped codepoints.
   rec['candidate_spans']+=1
   missing=[c for c in s['chars'] if not c['c'].isspace() and not exists(c)]
   if not missing:continue
   rec['missing_spans']+=1
   area=fitz.Rect(s['bbox'])
   overlaps=[{'text':o['text'],'bbox':o['bbox']} for o in ss if CJK.search(o['text']) and area.intersects(fitz.Rect(o['bbox']))]
   summary['missing_candidates'].append({'source_path':row['source_path'],'destination_path':row['destination_path'],'page':pno+1,'span_text':s['text'],'line_text':s['line_text'],'bbox':s['bbox'],'font':s['font'],'size':s['size'],'dir':s['dir'],'missing_text':''.join(c['c'] for c in missing),'missing_chars':missing,'overlapping_original_chinese_spans':overlaps,'numeric':bool(re.search(r'\d',text)),'symbol_only':not bool(re.search(r'[A-Za-z\d]',text))})
 summary['files'].append(rec)
 sd.close();dd.close()
summary['duration_s']=round(time.time()-summary['started'],2)
summary['counts']={'pdfs':len(summary['files']),'source_pages':sum(r.get('source_pages',0) for r in summary['files']),'candidate_spans':sum(r.get('candidate_spans',0) for r in summary['files']),'missing_spans':len(summary['missing_candidates']),'affected_files':len({r['destination_path'] for r in summary['missing_candidates']}),'numeric_missing_spans':sum(r['numeric'] for r in summary['missing_candidates'])}
args.output.write_text(json.dumps(summary,ensure_ascii=True,indent=2)+'\n')
print(json.dumps(summary['counts']));print('duration',summary['duration_s'])
