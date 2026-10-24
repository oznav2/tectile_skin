#!/usr/bin/env python3
"""Recreate two technical table PNGs from reviewed structured Hebrew transcription.

No generative image operation, electrical recalculation or source-archive mutation.
Unknown original units remain unknown. Small English circuit thumbnails are kept
as exact source crops because their low-resolution annotations cannot be reliably
transcribed. Only the two named PNG members may change in the destination ZIP.
Requires PyMuPDF and Pillow, plus Noto Sans Hebrew and DejaVu Sans fonts.
"""
import argparse
import hashlib
import html
import io
import json
import os
from pathlib import Path
import re
import tempfile
import zipfile

import pymupdf as fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PROVENANCE = ROOT/'hardware/provenance'
DATA = PROVENANCE/'impedance_tables_data.json'
OUTPUT = PROVENANCE/'impedance_tables'
FONT_HE = Path('/usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf')
FONT_LATIN = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def rgb(color):
    return tuple(int(color[i:i+2],16)/255 for i in (1,3,5))


class Drawing:
    def __init__(self,width,height,title):
        self.doc=fitz.open()
        self.page=self.doc.new_page(width=width,height=height)
        self.doc.set_metadata({'title':title,'author':'ROBOSKIN Hebrew technical transcription',
                               'subject':'Source manufacturing values transcribed; not recalculated or independently qualified'})
        self.archive=fitz.Archive(str(FONT_HE.parent))
        self.archive.add(str(FONT_LATIN.parent))
        self.css=f'''@font-face {{font-family:he;src:url({FONT_HE.name});}}
                    @font-face {{font-family:latin;src:url({FONT_LATIN.name});}}
                    * {{font-family:he,latin;}}'''
        self.rect((0,0,width,height),'#ffffff')

    def rect(self,box,fill='#ffffff',stroke=None):
        self.page.draw_rect(fitz.Rect(box),fill=rgb(fill),color=rgb(stroke) if stroke else None,width=.6)

    def text(self,box,text,size=17,align='center',color='#183358',rtl=None):
        if text is None:
            return
        if rtl is None:
            rtl=bool(re.search(r'[\u0590-\u05ff]',text))
        direction='rtl' if rtl else 'ltr'
        # Keep explicit Latin tokens in their own directional runs inside Hebrew.
        # Tokenize raw text before generating markup so <br> is never rewritten.
        lines=[]
        for line in text.split('\n'):
            pieces=[];position=0
            if rtl:
                for match in re.finditer(r'[A-Za-z0-9][A-Za-z0-9_./%×±~+()* -]*',line):
                    pieces.append(html.escape(line[position:match.start()]))
                    pieces.append('<span dir="ltr">'+html.escape(match[0])+'</span>')
                    position=match.end()
            pieces.append(html.escape(line[position:]))
            lines.append(''.join(pieces))
        encoded='<br>'.join(lines)
        body=f'<div dir="{direction}" style="font-size:{size}px;line-height:1.18;text-align:{align};color:{color};">{encoded}</div>'
        spare,scale=self.page.insert_htmlbox(fitz.Rect(box),body,css=self.css,archive=self.archive,scale_low=1)
        if spare<0:
            raise ValueError('Text does not fit: '+repr(text))

    def save(self,stem):
        self.doc.subset_fonts()
        pdf=OUTPUT/(stem+'.pdf')
        self.doc.save(pdf,garbage=4,deflate=True)
        png=OUTPUT/(stem+'.png')
        self.page.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(png)
        return {'pdf':str(pdf.relative_to(ROOT)), 'png':str(png.relative_to(ROOT)),
                'png_sha256':sha(png.read_bytes()),'pdf_sha256':sha(pdf.read_bytes())}


def stackup(data):
    d=Drawing(1720,1130,'ROBOSKIN - Hebrew layer stackup transcription')
    d.text((30,25,1690,65),'ROBOSKIN | מבנה שכבות',30)
    d.text((30,70,1690,105),'תמלול עברי של טבלת המקור; ערכי ייצור נשמרו ללא חישוב מחדש',17)
    widths=[145,170,475,145,145]
    xs=[30]
    for width in widths:xs.append(xs[-1]+width)
    headers=['שם שכבה','סוג חומר','פרטי חומר','עובי (mil)','עובי (mm)']
    y=140
    for col,title in enumerate(headers):
        d.rect((xs[col],y,xs[col+1],y+60),'#edf2f8','#cbd4df')
        d.text((xs[col]+6,y+12,xs[col+1]-6,y+56),title,19)
    d.text((1160,140,1690,180),'טווח העובי הכולל',20)
    d.text((1160,180,1690,215),data['total_thickness_range'],23,rtl=False)
    y+=60
    for row in data['rows']:
        height=130 if len(row['mil'])==3 else 70
        for col in range(5):d.rect((xs[col],y,xs[col+1],y+height),'#ffffff','#dce2e9')
        layer=row.get('layer_he',row['layer'])
        d.text((xs[0]+6,y+height/2-16,xs[1]-6,y+height-4),layer,18)
        d.text((xs[1]+6,y+height/2-16,xs[2]-6,y+height-4),row['material_he'],18)
        if row.get('parameters_note_he'):
            d.text((xs[2]+6,y+height/2-28,xs[3]-6,y+height/2),row['parameters'],18,rtl=False)
            d.text((xs[2]+6,y+height/2+2,xs[3]-6,y+height-3),row['parameters_note_he'],15)
        else:
            d.text((xs[2]+6,y+height/2-16,xs[3]-6,y+height-4),row['parameters'],18,rtl=False)
        for col,key in [(3,'mil'),(4,'mm')]:
            txt='\n'.join(row[key])
            d.text((xs[col]+6,y+(height-len(row[key])*25)/2,xs[col+1]-6,y+height-3),txt,18,rtl=False)
        # Each diagram band remains aligned to its table row; not a scale drawing.
        band_y0=y+12
        band_y1=y+height-12
        d.rect((1310,band_y0,1645,band_y1),row['color'])
        if row['layer'] in ('L2/L3','L4/L5'):
            a,b=row['layer'].split('/')
            d.text((1165,y+10,1295,y+height-5),a+'\n|\n'+b,19,rtl=False)
        else:d.text((1165,y+height/2-16,1295,y+height-4),layer,17)
        y+=height
    d.text((30,985,1690,1020),'תאים ריקים נשמרו ריקים; סדר ערכי הנחושת והליבה בתוך L2/L3 ובתוך L4/L5 נשמר.',16)
    d.text((30,1025,1690,1060),'האיור הצבעוני משייך שכבות לשורות ואינו שרטוט בקנה מידה. H/HOZ ו־H/H נשמרו כסימוני מקור.',16)
    return d.save('Impedance_Stackup.he')


def impedance(data,source_png):
    d=Drawing(2320,1100,'ROBOSKIN - Hebrew controlled impedance transcription')
    d.text((30,20,2290,62),'ROBOSKIN | טבלת עכבה מבוקרת',30)
    d.text((30,70,1150,112),data['source_item_number']+' | '+data['manufacturer_stackup_code'],24,rtl=False)
    d.text((1180,70,2290,112),data['special_label_he']+' | עובי לוח מוגמר '+data['finished_board_thickness'],23)
    d.text((30,118,700,150),'סבולת עכבה: '+data['impedance_tolerance']+' (יחידה לא מצוינת במקור)',17)
    d.text((720,118,2290,150),'תוויות ממשק המקור: נעיצה | חישוב עכבה לפי רוחב מוליך | חישוב | ביטול נעיצה',16)
    widths=[135,310,105,135,135,145,145,190,170,195,230]
    xs=[30]
    for width in widths:xs.append(xs[-1]+width)
    headers=['עכבה נדרשת\n(ohm)','סוג עכבה','שכבת אות','שכבת ייחוס\nעליונה','שכבת ייחוס\nתחתונה','רוחב מוליך\nW1','מרווח מוליכים\nS1','מרחק מוליך לנחושת\nD1','עכבה מחושבת\nלאחור','הערות','איור מקור']
    y=175
    for col,title in enumerate(headers):
        d.rect((xs[col],y,xs[col+1],y+75),'#edf2f8','#cbd4df')
        d.text((xs[col]+5,y+9,xs[col+1]-5,y+72),title,17)
    y+=75
    source=Image.open(io.BytesIO(source_png)).convert('RGB')
    crops=[]
    for index,row in enumerate(data['rows']):
        height=87
        vals=[row['required_ohm'],data['mode_he'][row['mode']],row['layer'],row['upper_reference'],row['lower_reference'],row['W1'],row['S1'],row['D1'],row['reverse_impedance']]
        for col in range(len(widths)):d.rect((xs[col],y,xs[col+1],y+height),'#ffffff','#dce2e9')
        for col,value in enumerate(vals):
            if col==5:d.rect((xs[col]+30,y+25,xs[col+1]-30,y+61),'#edf5e6')
            d.text((xs[col]+6,y+29,xs[col+1]-6,y+height-5),value,19 if col!=1 else 17)
        d.text((xs[9]+8,y+16,xs[10]-8,y+43),'הערה ריקה',14,color='#6b7685')
        d.text((xs[9]+8,y+46,xs[10]-8,y+77),row['remarks_counter'],17,rtl=False)
        crop=source.crop(row['source_diagram_crop_xyxy'])
        buf=io.BytesIO();crop.save(buf,format='PNG');raw=buf.getvalue()
        # Preserve the tiny English source diagram; do not invent blurred labels.
        name=f'impedance_diagram_{index+1:02}.png';(OUTPUT/name).write_bytes(raw)
        d.page.insert_image(fitz.Rect(xs[10]+65,y+8,xs[11]-65,y+height-8),stream=raw,keep_proportion=True)
        crops.append({'row':index+1,'source_crop_xyxy':row['source_diagram_crop_xyxy'],'crop_sha256':sha(raw),'path':str((OUTPUT/name).relative_to(ROOT))})
        y+=height
    d.text((30,973,2290,1003),'יחידות W1/S1/D1 אינן מצוינות בתמונה: לא הונחו mil או mm. גם ל־0.5 לא הוספה יחידה.',17)
    d.text((30,1010,2290,1042),'התא הריק בשורה הראשונה נשאר ריק; / נשמר בנפרד. 0/100 הוא מונה שדה הערות ריק, ולא נתון חשמלי.',17)
    d.text((30,1048,2290,1080),'האיורים הזעירים באנגלית נשמרו מן המקור; סימנים מטושטשים לא הומצאו. נתוני הטבלה הועתקו ללא חישוב מחדש.',16)
    result=d.save('Impedance_Traces.he');result['source_diagram_crops']=crops
    return result


def atomic_write(path,data):
    with tempfile.NamedTemporaryFile(dir=path.parent,prefix='.'+path.name+'.',delete=False) as temp:
        temp.write(data);temporary=Path(temp.name)
    try:os.replace(temporary,path)
    finally:temporary.unlink(missing_ok=True)


def validate_rendered_cells(data):
    """Check values in their individual output cells, including true blanks."""
    checks=0
    with fitz.open(OUTPUT/'Impedance_Stackup.he.pdf') as doc:
        page=doc[0];xs=[30,175,345,820,965,1110];y=200
        for row in data['stackup']['rows']:
            height=130 if len(row['mil'])==3 else 70
            for col,key in [(3,'mil'),(4,'mm')]:
                text=page.get_textbox(fitz.Rect(xs[col],y,xs[col+1],y+height))
                assert re.findall(r'\d+\.\d+',text)==row[key]
                checks+=1
            params=page.get_textbox(fitz.Rect(xs[2],y,xs[3],y+height))
            assert row['parameters'].replace(' ','') in params.replace(' ','').replace('\n','')
            if row['layer'] is None:
                assert not page.get_textbox(fitz.Rect(xs[0],y,xs[1],y+height)).strip()
            y+=height
    with fitz.open(OUTPUT/'Impedance_Traces.he.pdf') as doc:
        page=doc[0];xs=[30]
        for width in [135,310,105,135,135,145,145,190,170,195,230]:xs.append(xs[-1]+width)
        for index,row in enumerate(data['impedance']['rows']):
            y=250+87*index
            for col,key in [(0,'required_ohm'),(2,'layer'),(3,'upper_reference'),(4,'lower_reference'),(5,'W1'),(6,'S1'),(7,'D1'),(8,'reverse_impedance')]:
                assert page.get_textbox(fitz.Rect(xs[col],y,xs[col+1],y+87)).strip()==(row[key] or '')
                checks+=1
    return checks


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True,help='Unmodified original hardware checkout')
    ap.add_argument('--apply',action='store_true')
    args=ap.parse_args()
    data=json.loads(DATA.read_text())
    OUTPUT.mkdir(parents=True,exist_ok=True)
    source_archive=args.source/data['source_archive_path']
    source_images={}
    with zipfile.ZipFile(source_archive) as z:
        for info in z.infolist():
            if info.filename.lower().endswith(('.png','.jpg','.jpeg')):
                raw=z.read(info)
                source_images[sha(raw)]={'member':info.filename,'bytes':raw}
    for key in ('stackup','impedance'):
        if data[key]['source_image_sha256'] not in source_images:
            raise ValueError('Expected source screenshot hash not found: '+key)
    assert len(data['stackup']['rows'])==9 and len(data['impedance']['rows'])==8
    assert data['impedance']['rows'][0]['S1'] is None
    source_trace=source_images[data['impedance']['source_image_sha256']]['bytes']
    assets={'stackup':stackup(data['stackup']),'impedance':impedance(data['impedance'],source_trace)}
    cell_checks=validate_rendered_cells(data)
    replacements={data[k]['destination_member']:(ROOT/assets[k]['png']).read_bytes() for k in assets}
    destination=ROOT/data['destination_archive_path']
    before=destination.read_bytes()
    with zipfile.ZipFile(io.BytesIO(before)) as z:
        old_hashes={n:sha(z.read(n)) for n in z.namelist()}
        assert set(replacements)<=set(old_hashes)
        buffer=io.BytesIO()
        with zipfile.ZipFile(buffer,'w') as out:
            out.comment=z.comment
            for info in z.infolist():out.writestr(info,replacements.get(info.filename,z.read(info)))
    after=buffer.getvalue()
    with zipfile.ZipFile(io.BytesIO(after)) as z:
        assert z.testzip() is None
        assert set(z.namelist())==set(old_hashes)
        preserved={n:sha(z.read(n))==h for n,h in old_hashes.items() if n not in replacements}
        assert all(preserved.values())
        assert all(z.read(n)==v for n,v in replacements.items())
    if args.apply:
        atomic_write(destination,after)
        assert sha(destination.read_bytes())==sha(after)
    report={'schema_version':1,'applied':args.apply,'destination_archive':data['destination_archive_path'],
            'original_source_archive_sha256':sha(source_archive.read_bytes()),'before_archive_sha256':sha(before),'final_archive_sha256':sha(after),
            'structured_data_sha256':sha(DATA.read_bytes()),'font_sha256':{p.name:sha(p.read_bytes()) for p in (FONT_HE,FONT_LATIN)},
            'rendered_individual_value_or_blank_cells_checked':cell_checks,
            'replaced_png_members':[{'name':data[k]['destination_member'],'source_member':source_images[data[k]['source_image_sha256']]['member'],
                                     'source_image_sha256':data[k]['source_image_sha256'],'output_sha256':sha(replacements[data[k]['destination_member']]),'asset':assets[k]}for k in assets],
            'unchanged_other_members':preserved,'all_other_members_including_gerber_and_drill_byte_identical':all(preserved.values()),
            'no_electrical_recalculation':True,'source_archive_unmodified':True,
            'limitations':data['transcription_notes_he']}
    (PROVENANCE/'impedance_tables_report.json').write_text(json.dumps(report,ensure_ascii=True,indent=2)+'\n')
    print(json.dumps({'applied':args.apply,'replaced_pngs':len(replacements),'unchanged_other_members':len(preserved),'all_other_bytes_preserved':all(preserved.values())}))


if __name__=='__main__':main()
