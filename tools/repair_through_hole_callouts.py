#!/usr/bin/env python3
"""Separate technical glyph sequences from RTL translated through-hole qualifiers."""
from pathlib import Path
import argparse,collections,json,re
import pymupdf as fitz
from repair_pdf_technical_glyphs import glyph_overlay,sha
CJK=re.compile(r'[\u3400-\u9fff]')

def main(plan_path,root,source_root,backup_dir):
    records=json.loads(plan_path.read_text());group=collections.defaultdict(list)
    for r in records:group[r['destination_path']].append(r)
    backup_dir.mkdir(parents=True,exist_ok=True);report=[]
    font_dir=Path('/usr/share/fonts/truetype/noto')
    css="@font-face{font-family:H;src:url(NotoSansHebrew-Regular.ttf)} body{margin:0} div{font-family:H;font-size:10pt;line-height:1;direction:rtl;text-align:left;color:#111}"
    for idx,(name,rows) in enumerate(group.items()):
        dst=root/name;before=sha(dst);(backup_dir/f'{idx:03d}.pdf').write_bytes(dst.read_bytes())
        sd=fitz.open(source_root/rows[0]['source_path']);dd=fitz.open(dst);pages=collections.defaultdict(list)
        for r in rows:pages[r['page']-1].append(r)
        details=[]
        for pno,rs in pages.items():
            sp=sd[pno];dp=dd[pno];origrot=dp.rotation;dp.set_rotation(0);sp.set_rotation(0)
            original=[]
            for b in sp.get_text('rawdict')['blocks']:
                for l in b.get('lines',[]):
                    for s in l['spans']:original.append(s)
            replacements=[];glyphs=[];redacts=[]
            for r in rs:
                match=[s for s in original if all(abs(a-b)<.01 for a,b in zip(s['bbox'],r['span']['bbox'])) and ''.join(c['c'] for c in s['chars'])==r['span']['text']]
                if len(match)!=1:raise ValueError(f'Ambiguous source span: {r}')
                s=match[0];box=fitz.Rect(s['bbox']);technical=[dict(c,size=s['size'],source_font=s['font']) for c in s['chars'] if not c['c'].isspace() and not CJK.search(c['c'])]
                chinese=[c for c in s['chars'] if CJK.search(c['c'])]
                if not technical or not chinese:raise ValueError('Unexpected mixed span')
                affected=[]
                for b in dp.get_text('dict')['blocks']:
                    for l in b.get('lines',[]):
                        for d in l['spans']:
                            if 'NotoSans' in d['font'] and fitz.Rect(d['bbox']).intersects(box):affected.append(d)
                if not affected:raise ValueError(f'No translated target: {name} page {pno+1}')
                for d in affected:
                    rect=fitz.Rect(d['bbox'])
                    if tuple(rect) not in redacts:dp.add_redact_annot(rect,fill=None);redacts.append(tuple(rect))
                label='עובר במלואו' if '\u5b8c\u5168' in r['span']['text'] else 'עובר'
                # Use the original qualifier's horizontal allocation, separate from numeric syntax.
                left=min(c['bbox'][0] for c in chinese);right=max(c['bbox'][2] for c in chinese);baseline=chinese[0]['origin'][1]
                labelrect=fitz.Rect(left,baseline-10.7,right,baseline+4)
                replacements.append((labelrect,label));glyphs.extend(technical)
                details.append({'page':pno+1,'source_bbox':list(box),'technical_text':''.join(c['c'] for c in technical),'technical_characters':len(technical),'qualifier_hebrew':label,'qualifier_rect':list(labelrect)})
            dp.apply_redactions(images=0,graphics=0,text=0)
            pdf,svg=glyph_overlay(sp,glyphs);ov=fitz.open(stream=pdf,filetype='pdf');dp.show_pdf_page(dp.rect,ov,0,overlay=True)
            for c in glyphs:dp.insert_text(tuple(c['origin']),c['c'],fontsize=c['size'],fontname='RepairSearch',fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',render_mode=3)
            for rect,label in replacements:
                spare,scale=dp.insert_htmlbox(rect,'<div>'+label+'</div>',css=css,archive=fitz.Archive(str(font_dir)),scale_low=.45)
                if spare<0:raise ValueError(f'Qualifier does not fit: {name}')
            dp.set_rotation(origrot)
            ov.save(backup_dir/f'{idx:03d}_page_{pno+1}_glyphs.pdf')
        tmp=dst.with_suffix('.through.tmp.pdf');dd.save(tmp,garbage=4,deflate=True);dd.close();sd.close();tmp.replace(dst)
        report.append({'source_path':rows[0]['source_path'],'destination_path':name,'source_sha256':sha(source_root/rows[0]['source_path']),'before_sha256':before,'after_sha256':sha(dst),'callouts':details})
        (root/'hardware/provenance/pdf_through_hole_repair_report.json').write_text(json.dumps({'schema_version':1,'method':'Original technical glyph shapes/transforms; qualifier alone rendered in Hebrew inside original Chinese-label region. Only translated text is redacted; drawing vector paths preserved.','files':report},ensure_ascii=True,indent=2)+'\n')
    print({'files':len(report),'callouts':sum(len(r['callouts']) for r in report)})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--plan',type=Path,required=True);p.add_argument('--root',type=Path,required=True);p.add_argument('--source-root',type=Path,required=True);p.add_argument('--backup-dir',type=Path,required=True);a=p.parse_args();main(a.plan,a.root,a.source_root,a.backup_dir)
