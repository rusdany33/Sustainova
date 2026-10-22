from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from copy import deepcopy
p=Path(r'C:\laragon\www\SUSTAINOVATA-main\output\doc\PKPL_Modul_1_Test_Plan_Admin_Rusdany_202210370311406.docx')
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}; W='{'+ns['w']+'}'
with ZipFile(p) as z:
    infos=z.infolist(); parts={i.filename:z.read(i.filename) for i in infos}
t=E.fromstring(parts['word/document.xml'])
replacements={
'Rusdany maestro':'Rusdany Maestro',
'1.0':'1.1',
'Draf siap review asisten':'Siap review Test Plan; proyek telah disetujui asisten',
'Jadwal demo 7 Oktober 2026; tautan registrasi dan keunikan produk Web harus diverifikasi bersama asisten. Dokumen tidak menyatakan persetujuan asisten sudah diberikan.':'Demo 7 Oktober 2026. Proyek sudah terdaftar pada tab C baris 20 dan disetujui asisten berdasarkan konfirmasi praktikan. Checklist tercatat 12/13; REQ-1 masih FALSE. Persetujuan proyek tidak berarti Test Plan sudah dinilai.',
'Registrasi terlambat, produk Web duplikat atau pemahaman source belum cukup saat demo.':'Perubahan cakupan setelah persetujuan tidak tercatat atau sumber kebutuhan awal belum ditautkan pada registrasi.',
'Isi baris registrasi resmi setelah tautan tersedia, validasi UNQ-1 bersama asisten dan latihan penjelasan source serta alasan risiko sebelum 7 Oktober.':'Registrasi tab C baris 20 tersedia; UNQ-1 TRUE. Tautkan sumber kebutuhan awal untuk REQ-1, catat perubahan scope dan latihan demo sebelum 7 Oktober.',
'Belum diisi; tautan registrasi perlu tersedia dan UNQ-1 perlu diperiksa':'Terdaftar pada tab C baris 20; proyek disetujui menurut praktikan. Checklist 12/13; REQ-1 perlu diperbarui setelah sumber kebutuhan awal direview.',
}
def setp(el,value):
    texts=el.findall('.//w:t',ns)
    if texts:
        texts[0].text=value
        for n in texts[1:]:n.text=''
for par in t.findall('.//w:p',ns):
    val=''.join(par.itertext()) if False else ''.join(x.text or '' for x in par.findall('.//w:t',ns))
    if val in replacements:setp(par,replacements[val])
tables=t.find('w:body',ns).findall('w:tbl',ns)
# Preserve initial revision version; add a separate truthful revision record.
rev=tables[1]; first=rev.findall('w:tr',ns)[1]; setp(first.findall('w:tc',ns)[0],'1.0')
new=deepcopy(first)
for cell,val in zip(new.findall('w:tc',ns),['1.1','5 Oktober 2026','Rusdany Maestro','Mencatat registrasi kelas C baris 20, konfirmasi persetujuan proyek dari praktikan, checklist 12/13 dan tindak lanjut REQ-1.']):setp(cell,val)
rev.append(new)
parts['word/document.xml']=E.tostring(t,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(p,'w') as z:
    for i in infos:z.writestr(i,parts[i.filename])
guide=p.parent/'Panduan_Demo_dan_Registrasi_Modul_1.md'
s=guide.read_text(encoding='utf-8').replace('Rusdany maestro','Rusdany Maestro')
s=s.replace('Tautan spreadsheet belum diberikan, sehingga registrasi belum dikerjakan.','Registrasi ditemukan pada tab C baris 20. Proyek sudah disetujui asisten berdasarkan konfirmasi praktikan; kolom status/pemeriksa pada spreadsheet masih kosong.')
s=s.replace('Isi spreadsheet resmi, verifikasi UNQ-1 dan catat hasil pemeriksaan asisten. Tautan spreadsheet belum diberikan, sehingga registrasi belum dikerjakan.','Perbarui hanya informasi praktikan yang perlu dilengkapi pada baris 20. UNQ-1 sudah TRUE; persetujuan proyek telah dikonfirmasi praktikan.')
s=s.replace('Belum dapat dipastikan tanpa spreadsheet resmi/asisten. Role berbeda pada Web bukan produk berbeda.','UNQ-1 tercatat TRUE pada tab C baris 20. Role berbeda pada Web bukan produk berbeda.')
s=s.replace('Isi spreadsheet resmi, verifikasi UNQ-1 dan catat hasil pemeriksaan asisten. Registrasi ditemukan','Lengkapi informasi praktikan yang masih diperlukan pada baris 20; UNQ-1 sudah TRUE. Registrasi ditemukan')
notice='''## Status registrasi dan persetujuan terbaru

Pada 5 Oktober 2026, entri Rusdany Maestro, NIM 202210370311406, Sustainova Web ditemukan pada tab **C baris 20** di [spreadsheet resmi](https://docs.google.com/spreadsheets/d/1jlCOf2GXIOOpdJOK1X0zS1bMAMTlGdtQsbxrkM2y3Rk/edit?gid=1740208238#gid=1740208238). Praktikan mengonfirmasi proyek sudah disetujui asisten. Kolom status, pemeriksa dan catatan asisten masih kosong pada pembacaan ini; dokumen tidak mengarang nama pemeriksa atau tanggal persetujuan.

Checklist **12/13**: PRJ-1 sampai RDY-6 semuanya TRUE; **REQ-1 pada AE20 masih FALSE**. README.md, LOCAL-SETUP.md, UI serta route/controller sudah diidentifikasi sebagai sumber kebutuhan awal dalam Test Plan. SRS belum wajib selesai pada Modul 1. Tindak lanjutnya adalah mencatat sumber tersebut pada registrasi dan menyesuaikan REQ-1 sesuai hasil review; spreadsheet tidak diubah dalam pembaruan dokumen ini.

Kolom F20 (lima fitur tambahan) dan H20 (catatan praktikan) masih kosong. Bahan fitur dan kebutuhan awal di bagian berikut dapat digunakan untuk melengkapinya. Kolom AG20 menampilkan seluruh kode sebagai belum terpenuhi meskipun 12 kolom bernilai TRUE; gunakan nilai checkbox S20:AE20 dan progres AF20 sebagai bukti pembacaan, serta sampaikan ketidaksesuaian rumus AG20 kepada pengelola bila diperlukan.

'''
s=s.replace('## Pemetaan rubrik Table 7.1',notice+'## Pemetaan rubrik Table 7.1')
guide.write_text(s,encoding='utf-8')
print(p)
