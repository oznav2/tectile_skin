#!/usr/bin/env python3
"""Replace the nontechnical CMF product banner, retaining source attribution pages."""
from pathlib import Path
import hashlib,json
import pymupdf as fitz
ROOT=Path(__file__).resolve().parents[1]
FONT=Path('/usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    manifest=json.loads((ROOT/'hardware/provenance/file_manifest.json').read_text());report=[]
    css="@font-face {font-family: Hebrew; src: url(NotoSansHebrew-Regular.ttf);} @font-face {font-family:Latin; src:url(NotoSans-Regular.ttf);} body {margin:0;} div {font-family:Hebrew,Latin; font-size:10pt; line-height:1; color:white; direction:rtl; text-align:left;}"
    for rec in manifest['files']:
        path=ROOT/rec['destination_path']
        if not path.name.endswith('CMF_specification.pdf'):continue
        doc=fitz.open(path);page=doc[0];boxes=page.search_for('RP1')
        if not boxes:doc.close();continue
        if not all(30<b.x0<60 and 25<b.y0<47 and b.x1<65 for b in boxes):
            raise ValueError(f'Unexpected banner location: {path}: {boxes}')
        before=sha(path);rect=fitz.Rect(35,29,310,49)
        blue=tuple(c/255 for c in (31,78,139))
        page.add_redact_annot(rect,fill=blue)
        page.apply_redactions(images=0,graphics=0,text=0)
        spare,scale=page.insert_htmlbox(fitz.Rect(37.5,30,305,47.5),'<div>ROBOSKIN - מפרט גימור חלקי מעטפת (CMF)</div>',css=css,archive=fitz.Archive(str(FONT.parent)),scale_low=1)
        if spare<0:raise ValueError('Banner does not fit')
        tmp=path.with_suffix('.banner.tmp.pdf');doc.save(tmp,garbage=4,deflate=True);doc.close();tmp.replace(path)
        report.append({'destination_path':rec['destination_path'],'page':1,'rectangle':list(rect),'before_sha256':before,'after_sha256':sha(path),'scope':'Nontechnical product banner only; technical drawing and source-attribution pages retained.'})
    result={'schema_version':1,'changed_files':len(report),'files':report}
    (ROOT/'hardware/provenance/cmf_product_banner_repair.json').write_text(json.dumps(result,ensure_ascii=True,indent=2)+'\n')
    print('Rebranded CMF banners:',len(report))
if __name__=='__main__':main()
