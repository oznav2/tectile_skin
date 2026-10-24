#!/usr/bin/env python3
"""Restore selected collateral PDF text deletions using original vector glyphs.

The visible repair consists exclusively of original glyph outlines and affine
transforms. An invisible Unicode layer restores searchability at each original
baseline. No surrounding source text, geometry or branding is imported.
Run only with a reviewed plan; source and pre-repair hashes are checked.
"""
from pathlib import Path
import argparse, copy, hashlib, json, re
import xml.etree.ElementTree as ET
import pymupdf as fitz

NS='http://www.w3.org/2000/svg'; XL='http://www.w3.org/1999/xlink'
ET.register_namespace('', NS); ET.register_namespace('xlink', XL)

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def glyph_overlay(page, chars):
    page.set_rotation(0)
    root=ET.fromstring(page.get_svg_image(text_as_path=True))
    ids={e.get('id'):e for e in root.iter() if e.get('id')}
    parents={c:p for p in root.iter() for c in p}
    uses=[e for e in root.iter() if e.tag==f'{{{NS}}}use' and e.get('data-text') is not None]
    selected=[]
    for char in chars:
        x,y=char['origin']; found=[]
        for e in uses:
            if e.get('data-text')!=char['c']:continue
            m=re.fullmatch(r'matrix\(([^)]+)\)',e.get('transform',''))
            if not m:continue
            v=[float(z) for z in re.split('[, ]+',m[1]) if z]
            if len(v)==6 and abs(v[4]-x)<.05 and abs(v[5]-y)<.05:found.append(e)
        if len(found)!=1:raise ValueError(f'Glyph must match exactly once: {char}: {len(found)}')
        selected.append(found[0])
    out=ET.Element(f'{{{NS}}}svg', {k:v for k,v in root.attrib.items() if k in ('width','height','viewBox','version')})
    defs=ET.SubElement(out,f'{{{NS}}}defs'); done=set()
    for e in selected:
        ident=e.get(f'{{{XL}}}href','').removeprefix('#')
        if ident not in done:defs.append(copy.deepcopy(ids[ident]));done.add(ident)
        chain=[]; node=parents.get(e)
        while node is not None and node is not root:
            if node.tag==f'{{{NS}}}g':chain.append(node)
            node=parents.get(node)
        target=out
        for group in reversed(chain):
            # Clip groups are unnecessary for isolated complete glyph outlines.
            attrs={k:v for k,v in group.attrib.items() if k not in ('clip-path','id')}
            if attrs:target=ET.SubElement(target,f'{{{NS}}}g',attrs)
        target.append(copy.deepcopy(e))
    svg=ET.tostring(out,encoding='utf-8',xml_declaration=True)
    with fitz.open(stream=svg,filetype='svg') as s:
        return s.convert_to_pdf(),svg

def apply(plan_path,root,source_root,backup,report_path):
    plan=json.loads(plan_path.read_text()); result=[]; backup.mkdir(parents=True,exist_ok=True)
    font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    for index,rec in enumerate(plan['files']):
        src=source_root/rec['source_path'];dst=root/rec['destination_path']
        if sha(src)!=rec['source_sha256']:raise ValueError(f'Source hash changed: {src}')
        if sha(dst)!=rec['before_sha256']:raise ValueError(f'Destination hash changed: {dst}')
        backup_path=backup/f'{index:03d}.pdf';backup_path.write_bytes(dst.read_bytes())
        sd=fitz.open(src);dd=fitz.open(dst);glyphs=0; overlays=[]
        for pstr,cs in rec['pages'].items():
            pno=int(pstr)-1; dp=dd[pno];rotation=dp.rotation;dp.set_rotation(0)
            pdf,svg=glyph_overlay(sd[pno],cs)
            overlay=fitz.open(stream=pdf,filetype='pdf')
            if abs(overlay[0].rect.width-dp.rect.width)>.1 or abs(overlay[0].rect.height-dp.rect.height)>.1:
                raise ValueError(f'Page dimensions changed: {dst} page {pstr}')
            dp.show_pdf_page(dp.rect,overlay,0,overlay=True)
            for c in cs:
                dp.insert_text(tuple(c['origin']),c['c'],fontsize=c['size'],fontname='RepairSearch',fontfile=font_path,render_mode=3,overlay=True)
            dp.set_rotation(rotation);glyphs+=len(cs)
            overlay_path=backup/f'{index:03d}_page_{pstr}_glyphs.pdf';overlay.save(overlay_path)
            overlays.append({'page':int(pstr),'glyphs':len(cs),'overlay_sha256':sha(overlay_path)})
        temp=dst.with_suffix('.repair.tmp.pdf');dd.save(temp,garbage=4,deflate=True);dd.close();sd.close();temp.replace(dst)
        result.append({'source_path':rec['source_path'],'destination_path':rec['destination_path'],'source_sha256':rec['source_sha256'],'before_sha256':rec['before_sha256'],'after_sha256':sha(dst),'restored_glyphs':glyphs,'pages':overlays})
    report={'schema_version':1,'method':'Original glyph outlines and original affine transforms restored as vector paths; an invisible Unicode layer records character origins for search/positional checks. No surrounding drawing geometry, source-language text or branding restored.','files':result,'restored_files':len(result),'restored_glyphs':sum(r['restored_glyphs'] for r in result)}
    report_path.write_text(json.dumps(report,ensure_ascii=True,indent=2)+'\n')
    print(json.dumps({'files':len(result),'glyphs':report['restored_glyphs']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--plan',type=Path,required=True);p.add_argument('--root',type=Path,required=True);p.add_argument('--source-root',type=Path,required=True);p.add_argument('--backup-dir',type=Path,required=True);p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();apply(a.plan,a.root,a.source_root,a.backup_dir,a.report)
