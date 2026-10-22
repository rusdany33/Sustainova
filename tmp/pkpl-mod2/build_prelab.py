from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
from lxml import etree as E
import hashlib,json
src=Path(r'D:\PKPL\Test Design Specification & TTM Template.docx')
root=Path(r'C:\laragon\www\SUSTAINOVATA-main')
out=root/'output/doc/PKPL_Modul_2_PRELAB_TDS_TTM_Rusdany_202210370311406.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}; W='{'+ns['w']+'}'
with ZipFile(src) as z:
    infos=z.infolist();parts={i.filename:z.read(i.filename) for i in infos}
t=E.fromstring(parts['word/document.xml']);body=t.find('w:body',ns);ps=body.findall('w:p',ns);tables=body.findall('w:tbl',ns)
def settext(el,text):
    texts=el.findall('.//w:t',ns)
    if texts:
        texts[0].text=str(text)
        for x in texts[1:]:x.text=''
    else:
        p=el if el.tag==W+'p' else el.find('w:p',ns)
        r=E.SubElement(p,W+'r');E.SubElement(r,W+'t').text=str(text)
def insertpara(before,text):
    p=deepcopy(ps[2]);settext(p,text);body.insert(body.index(before),p)
def fill(table,rows):
    old=table.findall('w:tr',ns)
    for r in old[1:]:table.remove(r)
    for vals in rows:
        r=deepcopy(old[1])
        for c,v in zip(r.findall('w:tc',ns),vals):settext(c,v)
        pr=r.find('w:trPr',ns)
        if pr is None:pr=E.SubElement(r,W+'trPr')
        E.SubElement(pr,W+'cantSplit');table.append(r)
    hp=old[0].find('w:trPr',ns)
    if hp is None:hp=E.SubElement(old[0],W+'trPr')
    E.SubElement(hp,W+'tblHeader')
settext(ps[0],'TEST DESIGN SPECIFICATION (TDS)')
insertpara(ps[1],'PRE-LAB Modul 2 | Online Course Registration System')
insertpara(ps[1],'Rusdany Maestro | 202210370311406 | Kelas C | 14 Oktober 2026')
insertpara(ps[1],'Identifikasi dokumen: TDS-OCRS-PRELAB-202210370311406 | Versi 1.0')
insertpara(ps[1],'Dasar pengujian: studi kasus PRE-LAB pada Modul 2 halaman 15. Role: Mahasiswa. Sistem menyediakan pendaftaran mata kuliah yang masih tersedia dan peninjauan daftar mata kuliah yang sudah didaftarkan.')
requirements=[
('RQ-001','Sistem harus memungkinkan mahasiswa mendaftar pada mata kuliah yang masih memiliki kapasitas dan belum didaftarkan mahasiswa tersebut.'),
('RQ-002','Sistem harus menolak pendaftaran mata kuliah yang sudah mencapai kapasitas maksimum.'),
('RQ-003','Sistem harus mencegah mahasiswa mendaftar mata kuliah yang sama lebih dari satu kali.'),
('RQ-004','Sistem harus menampilkan daftar mata kuliah yang berhasil didaftarkan mahasiswa.'),
('RQ-005','Jika mahasiswa belum mendaftar mata kuliah apa pun, sistem harus menampilkan pesan bahwa belum ada data pendaftaran.')]
settext(ps[2],requirements[0][0]+': '+requirements[0][1]);settext(ps[3],requirements[1][0]+': '+requirements[1][1])
for rid,desc in requirements[2:]:insertpara(ps[4],rid+': '+desc)
settext(ps[5],'FS-001 - Pendaftaran Mata Kuliah')
settext(ps[6],'Objective: Memproses pendaftaran yang memenuhi kapasitas serta mencegah pendaftaran pada kelas penuh atau pendaftaran berulang.')
settext(ps[7],'Priority: High. Kegagalan berpotensi menghasilkan pendaftaran melampaui kapasitas atau data ganda.')
settext(ps[8],'Traceability: RQ-001, RQ-002, RQ-003')
settext(ps[9],'FS-002 - Daftar Mata Kuliah Terdaftar')
settext(ps[10],'Objective: Menampilkan mata kuliah yang berhasil didaftarkan dan informasi yang jelas ketika daftar masih kosong.')
settext(ps[11],'Priority: Medium. Mahasiswa memerlukan daftar untuk memeriksa hasil pendaftarannya; prioritas setelah integritas transaksi pendaftaran.')
settext(ps[12],'Traceability: RQ-004, RQ-005')
conditions=[
('TCond-001','FS-001','Pendaftaran pada mata kuliah yang masih memiliki kapasitas dan belum didaftarkan diterima.','High','RQ-001'),
('TCond-002','FS-001','Pendaftaran pada mata kuliah dengan kapasitas penuh ditolak dan tidak menambah pendaftaran.','High','RQ-002'),
('TCond-003','FS-001','Pendaftaran ulang mata kuliah yang sudah didaftarkan ditolak meskipun kapasitas masih tersedia.','High','RQ-003'),
('TCond-004','FS-001','Pendaftaran ditolak ketika mata kuliah sekaligus penuh dan sudah didaftarkan; tidak muncul pendaftaran tambahan.','High','RQ-002, RQ-003'),
('TCond-005','FS-002','Daftar menampilkan satu mata kuliah ketika mahasiswa memiliki satu pendaftaran berhasil.','Medium','RQ-004'),
('TCond-006','FS-002','Daftar menampilkan seluruh mata kuliah yang berhasil didaftarkan ketika terdapat beberapa pendaftaran.','Medium','RQ-004'),
('TCond-007','FS-002','Daftar tanpa pendaftaran menampilkan pesan bahwa belum ada data pendaftaran.','Medium','RQ-005')]
fill(tables[0],conditions)
coverage=[
('CI-001','Kapasitas tersedia, status belum terdaftar dan penerimaan pendaftaran','TCond-001','High','RQ-001'),
('CI-002','Kapasitas maksimum dan penolakan pendaftaran kelas penuh','TCond-002, TCond-004','High','RQ-002'),
('CI-003','Status sudah terdaftar dan pencegahan pendaftaran ganda','TCond-003, TCond-004','High','RQ-003'),
('CI-004','Daftar dengan satu pendaftaran berhasil','TCond-005','Medium','RQ-004'),
('CI-005','Kelengkapan daftar dengan beberapa pendaftaran berhasil','TCond-006','Medium','RQ-004'),
('CI-006','Daftar kosong dan pesan belum ada data pendaftaran','TCond-007','Medium','RQ-005')]
fill(tables[1],coverage)
settext(ps[16],'Matriks berikut menelusuri setiap requirement ke Feature Set, Test Condition dan Coverage Item. Satu requirement dapat memiliki beberapa kondisi; satu kondisi dapat memeriksa lebih dari satu requirement.')
ttm=[('RQ-001','FS-001','TCond-001','CI-001'),('RQ-002','FS-001','TCond-002','CI-002'),('RQ-002','FS-001','TCond-004','CI-002'),('RQ-003','FS-001','TCond-003','CI-003'),('RQ-003','FS-001','TCond-004','CI-003'),('RQ-004','FS-002','TCond-005','CI-004'),('RQ-004','FS-002','TCond-006','CI-005'),('RQ-005','FS-002','TCond-007','CI-006')]
fill(tables[2],ttm)
body.remove(ps[17]);body.remove(tables[3])
insertpara(ps[18],'Pemeriksaan kelengkapan desain: 5/5 requirement memiliki hubungan pada TTM; seluruh 7 Test Condition memiliki Coverage Item. Angka ini menunjukkan cakupan dokumentasi desain, bukan hasil eksekusi atau persentase pengujian yang lolos.')
insertpara(ps[18],'Contoh penelusuran: RQ-003 mencegah pendaftaran ganda; dikelompokkan dalam FS-001; diperiksa oleh TCond-003 dan TCond-004; aspek yang dicakup adalah CI-003.')
parts['word/document.xml']=E.tostring(t,xml_declaration=True,encoding='UTF-8',standalone=True)
contract={'reference':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'geometry':'Letter portrait; top/bottom 1 inch, left/right 1.25 inch; one section retained','slots':'Paragraphs 2-3 cloned for 5 requirements; paragraphs 5-12 filled for 2 Feature Sets; tables 0-2 filled; Section 6 and table 3 removed because requested PRE-LAB work is requirements/design/TTM only. Metadata and explanation clone normal source paragraphs.','preservation':'Only word/document.xml edited; all other ZIP parts preserved byte-for-byte. Table grids, fonts and paragraph roles retained; body rows cloned; headers repeated and rows kept together.','source_pages':'Module 2 page 15 PRE-LAB; headings and tables from retained template','render':'Packaged renderer fails: soffice.exe absent. Native Word PDF export and pypdfium2 rasterization used for visual verification.'}
(root/'tmp/pkpl-mod2/artifact.md').write_text(json.dumps(contract,indent=2),encoding='utf-8')
out.parent.mkdir(parents=True,exist_ok=True)
with ZipFile(out,'w') as z:
    for i in infos:z.writestr(i,parts[i.filename])
with ZipFile(out) as z:
    assert all(z.read(k)==v for k,v in parts.items())
assert {r[0] for r in requirements}=={r[0] for r in ttm}
assert {c[0] for c in conditions}=={r[2] for r in ttm}
for rq,fs,tc,ci in ttm:
    c=next(x for x in conditions if x[0]==tc);v=next(x for x in coverage if x[0]==ci)
    assert c[1]==fs and rq in c[4].split(', ') and tc in v[2].split(', ') and rq in v[4].split(', ')
print(out)
