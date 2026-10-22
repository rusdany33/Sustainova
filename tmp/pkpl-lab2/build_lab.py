from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
from lxml import etree as E
import hashlib,json,re
from design_data import features,req,conds
root=Path(r'C:\laragon\www\SUSTAINOVATA-main');tmp=root/'tmp/pkpl-lab2';out=root/'output/doc'
src_plan=Path(r'D:\PKPL\PKPL_Modul_1_Test_Plan_Admin_Rusdany_202210370311406.docx')
src_tds=Path(r'D:\PKPL\Test Design Specification & TTM Template.docx')
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};W='{'+ns['w']+'}'
def readzip(path):
 with ZipFile(path) as z: return z.infolist(),{i.filename:z.read(i.filename) for i in z.infolist()}
def settext(el,value):
 texts=el.findall('.//w:t',ns)
 if texts:
  texts[0].text=str(value);texts[0].set('{http://www.w3.org/XML/1998/namespace}space','preserve')
  for x in texts[1:]:x.text=''
 else:
  p=el if el.tag==W+'p' else el.find('w:p',ns)
  rr=E.SubElement(p,W+'r');E.SubElement(rr,W+'t').text=str(value)
def para_settings(p,keep=False,page=False):
 pr=p.find('w:pPr',ns)
 if pr is None:pr=E.Element(W+'pPr');p.insert(0,pr)
 for tag,active in [('keepNext',keep),('pageBreakBefore',page)]:
  if active and pr.find('w:'+tag,ns) is None:E.SubElement(pr,W+tag)
def fill(table,rows,widths=None):
 old=table.findall('w:tr',ns)
 for rr in old[1:]:table.remove(rr)
 for vals in rows:
  rr=deepcopy(old[1])
  for c,v in zip(rr.findall('w:tc',ns),vals):settext(c,v)
  pr=rr.find('w:trPr',ns)
  if pr is None:pr=E.Element(W+'trPr');rr.insert(0,pr)
  if pr.find('w:cantSplit',ns) is None:E.SubElement(pr,W+'cantSplit')
  table.append(rr)
 hp=old[0].find('w:trPr',ns)
 if hp is None:hp=E.Element(W+'trPr');old[0].insert(0,hp)
 header=hp.find('w:tblHeader',ns)
 if header is None:header=E.SubElement(hp,W+'tblHeader')
 header.set(W+'val','true')
 if widths:
  grid=table.find('w:tblGrid',ns)
  for c,w in zip(grid,widths):c.set(W+'w',str(w))
  for rr in table.findall('w:tr',ns):
   for c,w in zip(rr.findall('w:tc',ns),widths):
    cp=c.find('w:tcPr',ns);cw=cp.find('w:tcW',ns)
    if cw is None:cw=E.SubElement(cp,W+'tcW')
    cw.set(W+'w',str(w));cw.set(W+'type','dxa')
def writezip(dest,infos,parts,tree):
 parts=dict(parts);parts['word/document.xml']=E.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
 with ZipFile(dest,'w') as z:
  for i in infos:z.writestr(deepcopy(i),parts[i.filename])
 with ZipFile(dest) as z:
  assert all(z.read(k)==v for k,v in parts.items())

# Preserve source-derived page, typography, furniture, and all opaque package parts.
infos,parts=readzip(src_plan);tree=E.fromstring(parts['word/document.xml']);body=tree.find('w:body',ns);tables=body.findall('w:tbl',ns)
def cell(table,key,value):
 for rr in table.findall('w:tr',ns)[1:]:
  cs=rr.findall('w:tc',ns)
  if ''.join(cs[0].itertext())==key or ''.join(x.text or '' for x in cs[0].findall('.//w:t',ns))==key:settext(cs[1],value);return
 raise ValueError(key)
cell(tables[0],'Versi','1.2');cell(tables[0],'Tanggal Terakhir Diperbarui','15 Oktober 2026')
cell(tables[2],'Versi','Commit dasar 9adad2b dengan perubahan lokal per 15 Oktober 2026; rute dan search/filter mengacu pada checkout yang digunakan untuk desain Modul 2.')
cell(tables[2],'Deskripsi Singkat','Aplikasi informasi keberlanjutan. Admin memantau Dashboard, mengelola Berita, Program, Pesan dan Profil akun sendiri. Search/filter tersedia di daftar Berita, Program dan Pesan.')
desc=[
'F-01 Login akun admin; kredensial sah membuka dashboard, input tidak valid ditolak dan rute terlindungi memerlukan sesi yang sesuai.',
'F-02 Pendaftaran publik dengan validasi data dan email unik. Akun baru berperan user, bukan admin; admin disiapkan melalui seed.',
'F-03 Permintaan email dan reset password akun admin; token berlaku 30 menit dan sekali pakai, password baru tervalidasi serta sesi lama berakhir.',
'F-04 Menampilkan total Program, Berita dan Pesan, ringkasan program/berita terbaru, daftar pesan serta navigasi ke menu terkait.',
'F-05 Melihat, menambah, mengubah dan menghapus berita. Search/filter menyaring kata kunci pada judul, ringkasan, kategori atau tanggal, dengan reset dan jumlah hasil.',
'F-06 Melihat, menambah, mengubah dan menghapus program. Search/filter menyaring nama, deskripsi, status, peserta atau tanggal, dengan reset dan jumlah hasil.',
'F-07 Melihat daftar/detail, mengubah status new/read/replied dan menghapus pesan. Search/filter menyaring pengirim/email, subjek, topik, isi atau status, dengan reset dan jumlah hasil.',
'F-08 Melihat serta mengubah nama, email, telepon, username dan alamat akun admin sendiri; tersedia batal edit dan akses cepat ke menu admin.'
]
fill(tables[3],[(str(i+1),f[2],'Autentikasi' if i<3 else 'Tambahan',desc[i]) for i,f in enumerate(features)])
cell(tables[5],'Deskripsi Peran','Memantau dashboard, mengelola berita, program dan pesan kontak, serta memperbarui profil akun sendiri. Akun admin berasal dari seed database.')
cell(tables[5],'Fitur yang Dapat Diakses','F-01 dan F-03 sampai F-08. F-02 merupakan jalur registrasi publik wajib proyek dan tidak memberikan hak admin. CRUD dan search/filter adalah subfitur pada menu induknya.')
cell(tables[5],'Alasan Pemilihan','Delapan fitur utama terdiri atas tiga autentikasi dan lima menu admin. CRUD, validasi teks/angka/tanggal/berkas, search/filter dan perubahan status memberi variasi pengujian sampai UAP. Perbedaan role pada platform Web tidak membedakan produk untuk registrasi.')
cell(tables[8],'Fitur Berprioritas Tinggi','F-06 Kelola Program dan unggahan pada F-05/F-06 (R-03/R-04, 16); Login, Forgot Password serta ubah/hapus pada Kelola Berita, Kelola Program dan Pesan (R-01/R-02/R-05, 15). Search/filter dan Profil ditelusuri melalui R-09/R-10 (12).')
cell(tables[14],'Contoh Data Input','Program, berita dan pesan sementara berawalan PKPL-M1; profil akun admin uji; kata kunci cocok/tidak cocok, variasi kapital/spasi, serta pencarian kosong/reset pada tiga daftar.')
for p in body.findall('w:p',ns):
 text=''.join(x.text or '' for x in p.findall('.//w:t',ns))
 if text.startswith('Cakupan mencakup 11 fitur:'):
  settext(p,'Cakupan mencakup 8 fitur utama: Login, Register, Forgot Password, Dashboard, Kelola Berita, Kelola Program, Pesan dan Profil. Tambah, ubah, hapus, validasi, perubahan status dan search/filter dicakup sebagai subfitur pada menu induknya. Search/filter berbasis kata kunci tersedia pada Pesan, Kelola Program dan Kelola Berita. Register tetap jalur publik; role under test adalah Admin.')
 if text.startswith('Dasar skor:'):
  settext(p,'Dasar skor: dampak dan kemungkinan masing-masing berskala 1 (sangat rendah) sampai 5 (sangat tinggi); prioritas = dampak x kemungkinan. Skor adalah estimasi perencanaan. R-03/R-04 bernilai 16 karena variasi input dan unggahan perlu diperiksa; R-01/R-02/R-05 bernilai 15 karena menyangkut akses, akun atau integritas data. R-06 sampai R-10 bernilai 12. Mitigasi menjelaskan pemeriksaan dan tindakan pengurangan risiko.')
# Avoid empty pages caused by a standalone page-break paragraph after a full table.
plan_ps=body.findall('w:p',ns)
for i,p in enumerate(plan_ps):
 text=''.join(x.text or '' for x in p.findall('.//w:t',ns))
 if text=='DAFTAR ISI':
  para_settings(p,page=True)
  prev=p.getprevious()
  if prev is not None and prev.tag==W+'p' and not ''.join(x.text or '' for x in prev.findall('.//w:t',ns)) and prev.findall('.//w:br',ns):body.remove(prev)
 if text=='4. Lingkungan Pengujian':
  prev=p.getprevious()
  if prev is not None and prev.tag==W+'p' and not ''.join(x.text or '' for x in prev.findall('.//w:t',ns)):body.remove(prev)
rows=[]
for rr in tables[7].findall('w:tr',ns)[1:]:
 vals=[''.join(x.text or '' for x in c.findall('.//w:t',ns)) for c in rr.findall('w:tc',ns)]
 if vals[0]=='R-03': vals[1]='Input program tidak konsisten: peserta nol tidak tersimpan, peserta negatif lolos atau rentang tanggal terbalik tersimpan.'
 rows.append(vals)
rows.extend([
 ['R-09','Search/filter menampilkan data tidak sesuai kata kunci, jumlah hasil salah atau reset tidak memulihkan daftar.','Produk','4','3','12','Periksa tiap atribut pada Pesan, Kelola Program dan Kelola Berita; bandingkan hasil, kapital/spasi, pencarian kosong/reset dan baris yang sedang diedit.'],
 ['R-10','Perubahan Profil tidak tersimpan konsisten atau mengenai akun yang bukan milik admin yang login.','Produk','4','3','12','Gunakan akun admin sementara; bandingkan identitas akun dan nilai sebelum/sesudah refresh; periksa batal, validasi nama/email dan persistensi.']])
fill(tables[7],rows)
rev=tables[1];new=deepcopy(rev.findall('w:tr',ns)[-1])
for c,v in zip(new.findall('w:tc',ns),['1.2','15 Oktober 2026','Rusdany Maestro','Menyelaraskan 8 fitur utama berdasarkan menu, memperbaiki deskripsi Profil/Berita/Pesan, menambahkan search/filter dalam tiga menu, memperbarui ID dan risiko terkait.']):settext(c,v)
rev.append(new)
plan_out=out/'PKPL_Modul_1_Test_Plan_Admin_Rusdany_202210370311406_Revisi_v1_2.docx'
writezip(plan_out,infos,parts,tree)

# Requirements baseline for Lab Session. No claim this is a previously approved SRS.
srd=['# Software Requirements Document Sustainova Admin',
'ID SRD-SUSTAINOVA-ADMIN-202210370311406 | Versi 1.0 | 15 Oktober 2026',
'Rusdany Maestro | NIM 202210370311406 | Kelas C',
'## Tujuan dan sumber kebutuhan',
'Dokumen kebutuhan ini dikonsolidasikan pada 15 Oktober 2026 untuk mendukung analisis LAB SESSION Modul 2. Dasarnya adalah Test Plan revisi menu v1.2, arahan pengelompokan menu dan search/filter dari praktikan, serta UI dan source code yang tersedia. Dokumen ini tidak menyatakan bahwa seluruh kebutuhan sudah lolos eksekusi atau telah disetujui asisten.',
'## Cakupan',
'Role utama Admin. Tiga autentikasi wajib dan lima menu utama: Dashboard, Kelola Berita, Kelola Program, Pesan, Profil. Register merupakan jalur publik sebelum autentikasi dan membuat akun user. CRUD/search/filter diperlakukan sebagai subfitur. Kelola akun berarti profil akun sendiri, bukan CRUD semua pengguna.',
'## Kebijakan interpretasi',
'Search/filter berarti pencarian sebagian teks pada atribut daftar, dengan trim dan tanpa membedakan kapital. Ini bukan klaim filter dropdown terpisah. Baris berita/program yang sedang diedit tetap ditampilkan sesuai implementasi. Status pesan yang digunakan adalah new/read/replied; label replied tidak membuktikan pengiriman email.',
'Batas gambar form adalah 5 x 1024 x 1024 byte; JPG/JPEG, PNG, GIF dan WebP. Batas tersebut pada UI belum menjadi bukti validasi backend. Required poster/tanggal/deskripsi program dirujuk dari controller tambahProgram meskipun tanda wajib pada UI belum seragam. Peserta >= 0 dirujuk dari min form; nol diperlakukan sebagai nilai yang perlu diverifikasi, bukan otomatis tidak valid.',
'Form Register memakai minimum password 6 karakter; reset memakai minimum 8 karakter dan maksimum 72 byte UTF-8 di backend. Kedua alur dibedakan. Frontend reset membatasi 72 karakter; perbedaan karakter dan byte perlu dipertimbangkan pada data non-ASCII.',
'Route UI admin membatasi role admin; sebagian endpoint API admin juga mengizinkan editor. RQ-002 tidak mengklaim semua API eksklusif admin; matriks hak API yang lebih ketat memerlukan keputusan asisten. Profil hanya memvalidasi nama/email wajib dan format email pada form; validasi tambahan yang belum ditetapkan tidak dikarang.',
'## Kebutuhan fungsional']
for f in features:
 srd+=['### '+f[0]+' '+f[2]]
 for r in req:
  if r['fs']!=f[1]:continue
  if f[1]=='FS-008' and r['risk']=='R-01':r['risk']='R-10'
  srd += ['**'+r['id']+'** '+r['description'], 'Prioritas '+r['priority']+'. Risiko terkait '+(r['risk'] or 'konsistensi fungsi dan keterpakaian')+'.', 'Sumber: '+r['source']+'.']
srd+=['## Perbedaan dan konfirmasi yang masih diperlukan',
'Validasi server untuk peserta, tanggal, ukuran/jenis unggahan dan profil belum setara dengan batas UI; kondisi desain menetapkan aspek yang harus diperiksa, bukan klaim implementasi benar. Kosakata status program pada form tambah dan edit berbeda; daftar status bisnis tunggal perlu dikonfirmasi sebelum menurunkan kasus nilai spesifik.',
'Sumber README menyebut status pesan resolved, sedangkan UI/controller memakai replied; desain ini memakai UI/controller yang sedang tersedia. Persetujuan proyek dari Modul 1 tidak dianggap otomatis sebagai persetujuan setiap aturan kebutuhan baru.',
'## Pengendalian perubahan',
'Jika aturan asisten berubah, perbarui RQ terkait, lalu telusuri seluruh FS, TCond dan CI pada TTM. Sumber tetap menggunakan ID RQ yang sama apabila maknanya tidak berubah; kebutuhan baru diberi ID baru.']
srd_path=out/'SRD_Sustainova_Admin_Modul_2.md';srd_path.write_text('\n\n'.join(srd),encoding='utf-8')

# Fill the supplied TDS template, Sections 1 through 5 only.
infos,parts=readzip(src_tds);tree=E.fromstring(parts['word/document.xml']);body=tree.find('w:body',ns)
ps=body.findall('w:p',ns);tables=body.findall('w:tbl',ns)
def addpara(before,text,pattern=None,keep=False,page=False):
 p=deepcopy(pattern if pattern is not None else ps[2]);settext(p,text);para_settings(p,keep,page);body.insert(body.index(before),p);return p
for p in ps[2:4]:body.remove(p)
for p in ps[5:13]:body.remove(p)
body.remove(ps[17]);body.remove(tables[3])
addpara(ps[1],'LAB SESSION Modul 2 | Sustainova Web | Role Admin')
addpara(ps[1],'Rusdany Maestro | 202210370311406 | Kelas C | 15 Oktober 2026')
addpara(ps[1],'ID TDS-SUSTAINOVA-ADMIN-MOD2-202210370311406 | Versi 1.0')
addpara(ps[1],'Dasar pengujian: SRD-SUSTAINOVA-ADMIN-202210370311406 versi 1.0 dan Test Plan revisi menu v1.2. Dokumen ini menetapkan kebutuhan, Feature Sets, Test Conditions, Coverage Items dan TTM untuk desain pengujian. Hasil eksekusi belum dinyatakan.')
addpara(ps[1],'Cakupan: tiga autentikasi wajib dan lima menu utama. Register adalah jalur publik; akun baru bukan admin. Search/filter berbasis kata kunci berada dalam Kelola Berita, Kelola Program dan Pesan. Alur author/editor, review publikasi dan administrasi seluruh pengguna tidak termasuk.')
addpara(ps[1],'Prioritas High: akses, akun, validasi utama dan integritas data; Medium: ringkasan, daftar dan pencarian. Risiko mengacu R-01 sampai R-10 pada Test Plan v1.2. Bagian teknik dan test case rinci tidak diisi karena batas Modul 2 adalah Bagian 5.')
for f in features:
 addpara(ps[4],f[0]+' '+f[2],pattern=ps[5],keep=True)
 for r in req:
  if r['fs']==f[1]:addpara(ps[4],r['id']+': '+r['description'])
para_settings(ps[4],keep=True,page=True)
for f in features:
 addpara(ps[13],f[1]+' - '+f[2],pattern=ps[5],keep=True)
 addpara(ps[13],'Objective: '+f[4],keep=True)
 addpara(ps[13],'Priority: '+f[3]+' | Traceability: '+', '.join(r['id'] for r in req if r['fs']==f[1]))
para_settings(ps[13],keep=True,page=True);para_settings(ps[14],keep=True,page=True);para_settings(ps[15],keep=True,page=True)
fill(tables[0],[(c['id'],c['fs'],c['description'],c['priority'],c['rq']) for c in conds],[1296,936,4068,936,1404])
fill(tables[1],[(r['ci'],r['coverage'],', '.join(c['id'] for c in conds if c['rq']==r['id']),r['priority'],r['id']) for r in req],[1008,2808,2448,936,1440])
settext(ps[16],'TTM menautkan setiap requirement pada Bagian 1 ke Feature Set, Test Condition dan Coverage Item terkait. Setiap baris merepresentasikan satu hubungan desain; bukan hasil uji Lolos/Gagal.')
fill(tables[2],[(c['rq'],c['fs'],c['id'],c['ci']) for c in conds],[1800,1800,2520,2520])
addpara(ps[18],f'Pemeriksaan kelengkapan: {len(req)}/{len(req)} requirement, {len(features)}/{len(features)} Feature Sets, {len(conds)}/{len(conds)} Test Conditions dan {len(req)}/{len(req)} Coverage Items memiliki hubungan pada TTM. Cakupan ini berlaku untuk kebutuhan yang dipilih, bukan bukti bahwa aplikasi bebas defect.')
addpara(ps[18],'Contoh penelusuran: RQ-015 menetapkan search/filter berita; dikelompokkan pada FS-005; diturunkan menjadi TCond-029 sampai TCond-031; aspek yang dicakup adalah CI-015. Hubungan ini memungkinkan perubahan aturan pencarian ditelusuri ke kondisi terkait.')
# Generate example references from actual data rather than hardcoding fragile IDs.
example=[c for c in conds if c['rq']=='RQ-015']
last_added=body[body.index(ps[18])-1]
settext(last_added,'Contoh penelusuran: RQ-015 menetapkan search/filter berita; dikelompokkan pada FS-005; diturunkan menjadi '+', '.join(c['id'] for c in example)+'; aspek yang dicakup adalah CI-015. Perubahan aturan pencarian ditelusuri melalui hubungan ini.')
tds_out=out/'PKPL_Modul_2_LAB_TDS_TTM_Admin_Rusdany_202210370311406.docx'
writezip(tds_out,infos,parts,tree)

# Referential integrity checks against data and exported OOXML.
assert len({r['id'] for r in req})==len(req)==27
assert len({c['id'] for c in conds})==len(conds)==54
assert {c['fs'] for c in conds}=={f[1] for f in features}
assert {c['rq'] for c in conds}=={r['id'] for r in req}
assert {c['ci'] for c in conds}=={r['ci'] for r in req}
for c in conds:
 r=next(r for r in req if r['id']==c['rq']);assert r['fs']==c['fs'] and r['ci']==c['ci']
for r in req:
 for item in r['source'].split('; '):
  path=item.split(' (')[0];assert (root/path).is_file(),path
with ZipFile(tds_out) as z:
 raw=z.read('word/document.xml').decode();assert '6. Test Design Technique Summary' not in raw
 assert 'ISBN' not in raw and 'librarians' not in raw
manifest={'requirements':len(req),'features':len(features),'conditions':len(conds),'coverage_items':len(req),'ttm_rows':len(conds),'orphan_ids':[],'sources':[str(src_plan),str(src_tds)],'output_files':[str(plan_out),str(tds_out),str(srd_path)]}
(tmp/'validation.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
contracts={
 'test_plan':{'reference':str(src_plan),'sha256':hashlib.sha256(src_plan.read_bytes()).hexdigest(),'geometry':'Source section/page geometry, styles, header/footer parts preserved. Tables 0,1,2,3,5,7,8,14 and 2 body paragraphs edited; rows R-09/R-10 and revision1.2 cloned; all other package parts unchanged.'},
 'tds':{'reference':str(src_tds),'sha256':hashlib.sha256(src_tds.read_bytes()).hexdigest(),'geometry':'Letter portrait, margins top/bottom1 inch left/right1.25 inch; source Cambria heading patterns and normal body reused. Three source table components filled, column grids adapted to descriptions within original table width; row cantSplit and repeated header added. Headings3-5 begin new pages.','slots':'Template sections1-5 filled. Section6 and its table removed per explicit Module2 limit. Paragraphs2/5 cloned to expand requirements/FS. Table0=54 conditions, table1=27coverage, table2=54TTMrows.','preservation':'Only word/document.xml modified; styles, numbering, theme, header/footer and relationships preserved byte-for-byte.'},
 'render':'Packaged renderer unavailable because soffice.exe absent. Native Word used for read-only PDF export; PDFs rasterized with pypdfium2 for visual QA.'}
(tmp/'artifact.md').write_text(json.dumps(contracts,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
