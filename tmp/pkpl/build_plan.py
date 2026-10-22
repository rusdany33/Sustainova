from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
from lxml import etree as E
import hashlib, json
root=Path(r'C:\laragon\www\SUSTAINOVATA-main')
src=Path(r'D:\PKPL\Test Plan Template.docx')
out=root/'output/doc/PKPL_Modul_1_Test_Plan_Admin_Rusdany_202210370311406.docx'
out.parent.mkdir(parents=True,exist_ok=True)
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W='{'+ns['w']+'}'
z=ZipFile(src); tree=E.fromstring(z.read('word/document.xml')); body=tree.find('w:body',ns)
ps=body.findall('w:p',ns); ts=body.findall('w:tbl',ns)
def textset(el,text):
    texts=el.findall('.//w:t',ns)
    if texts:
        texts[0].text=text
        texts[0].set('{http://www.w3.org/XML/1998/namespace}space','preserve')
        for t in texts[1:]:t.text=''
    else:
        p=el if el.tag==W+'p' else el.find('w:p',ns)
        r=E.SubElement(p,W+'r'); E.SubElement(r,W+'t').text=text
def fill(i,rows):
    table=ts[i]; old=table.findall('w:tr',ns)
    for r in old[1:]:table.remove(r)
    for vals in rows:
        row=deepcopy(old[1])
        for cell,val in zip(row.findall('w:tc',ns),vals):textset(cell,str(val))
        table.append(row)
        pr=row.find('w:trPr',ns)
        if pr is None:pr=E.Element(W+'trPr');row.insert(0,pr)
        E.SubElement(pr,W+'cantSplit')
    hp=old[0].find('w:trPr',ns)
    if hp is None: hp=E.Element(W+'trPr');old[0].insert(0,hp)
    E.SubElement(hp,W+'tblHeader')
date='5 Oktober 2026'; name='Rusdany maestro'; version='Baseline commit 9adad2b per 5 Oktober 2026'
textset(ps[15],'Sustainova Web Role Admin')
fill(0,[('Identifikasi Test Plan','TP-SUSTAINOVA-MOD1-202210370311406'),('Nama Aplikasi','Sustainova'),('Versi','1.0'),('Peran yang Dipilih untuk Diuji','Admin, konsisten sampai UAP'),('Nama Praktikan',name),('NIM','202210370311406'),('Kelas','C'),('Tanggal Dibuat',date),('Tanggal Terakhir Diperbarui',date),('Status','Draf siap review asisten')])
body.remove(ts[1])
fill(2,[('1.0',date,name,'Penyusunan konteks, cakupan admin, risiko, kriteria, lingkungan, jadwal Modul 1 dan luaran berdasarkan template serta sumber aplikasi.')])
fill(3,[('Nama Aplikasi','Sustainova'),('Platform','Web'),('Versi',version+'; perubahan lokal perlu dibekukan sebelum demo.'),('URL Deployment / Akses','http://localhost:5173; login /login; dashboard /admin/dashboard'),('Tumpukan Teknologi','Vue 3, Vue Router 4, Vite 6, Bootstrap 5; Node.js, Express 5, MySQL melalui mysql2; JWT dan bcrypt.'),('Deskripsi Singkat','Aplikasi informasi keberlanjutan untuk program, berita dan publikasi. Admin mengelola program, berita dan pesan kontak serta memantau ringkasan dashboard.')])
features=[
('Login','Autentikasi','F-01 Masuk dengan akun admin; kredensial benar memberi akses dashboard, kredensial salah ditolak.'),
('Register','Autentikasi','F-02 Pendaftaran publik sebelum login; email baru diproses, email duplikat ditolak. Akun baru berperan user, bukan admin; admin disiapkan melalui seed. Ini tidak mengubah role utama pengujian.'),
('Forgot Password','Autentikasi','F-03 Permintaan reset akun admin melalui email lokal dan simpan password baru; token sekali pakai, kedaluwarsa 30 menit, sesi lama berakhir.'),
('Dashboard admin','Tambahan','F-04 Menampilkan total program, jurnal dan berita serta tiga data terbaru setiap kategori.'),
('Tambah program','Tambahan','F-05 Menyimpan nama, deskripsi, peserta, status, tanggal dan poster; data muncul pada daftar.'),
('Daftar dan ubah program','Tambahan','F-06 Membaca daftar dan menyimpan perubahan; jumlah peserta dan status dapat dibandingkan sebelum dan sesudah.'),
('Hapus program','Tambahan','F-07 Menghapus data sementara setelah konfirmasi; pembatalan tidak menghapus dan data terhapus hilang dari daftar.'),
('Tambah berita','Tambahan','F-08 Menyimpan judul, kategori, ringkasan, isi, tanggal terbit dan cover.'),
('Daftar dan ubah berita','Tambahan','F-09 Membaca daftar serta mengubah berita; data baru tetap terlihat setelah pemuatan ulang.'),
('Hapus berita','Tambahan','F-10 Menghapus berita sementara setelah konfirmasi; berita lain tetap tersedia.'),
('Kelola pesan kontak','Tambahan','F-11 Melihat daftar dan detail, mengubah status new/read/replied serta menghapus pesan sementara; status tidak valid ditolak.')]
fill(4,[(i+1,n,k,d) for i,(n,k,d) in enumerate(features)])
fill(5,[('1','Alur author dan editor, review jurnal dan kolaborasi','Di luar role admin. Akun pembanding hanya digunakan untuk memastikan batas akses, bukan menguji alur bisnis role lain.'),('2','CRUD publikasi melalui UI admin','File komponennya tersedia, tetapi rute publikasi admin belum didaftarkan pada router. Tidak dihitung sebagai fitur demo admin.'),('3','Produksi, pengiriman email publik dan uji beban besar','Lingkungan yang disiapkan lokal; SMTP lokal digunakan. Detail pengujian modul berikutnya belum ditetapkan.')])
fill(6,[('Nama Peran','Admin'),('Deskripsi Peran','Mengelola konten program dan berita, menangani pesan kontak dan memantau dashboard. Akun admin berasal dari seed database.'),('Fitur yang Dapat Diakses','F-01, F-03 sampai F-11; F-02 adalah jalur autentikasi publik wajib proyek. Register tidak memberikan hak admin.'),('Alasan Pemilihan','Admin menyediakan CRUD, input teks/angka/tanggal/berkas, perubahan status dan otorisasi. Kombinasi ini memberi bahan pengujian sampai UAP. Perbedaan role pada platform Web tidak menjadikan produk berbeda untuk registrasi.')])
fill(7,[('Asumsi','Akun admin@test.com dari seed tersedia pada database uji; email reset dapat dibaca melalui Mailpit. Data sementara diberi awalan PKPL-M1.'),('Asumsi','README.md, LOCAL-SETUP.md, UI dan source code menjadi sumber kebutuhan awal. Perilaku serta aturan bisnis dikonfirmasi kepada asisten; SRS dilengkapi pada Modul 2.'),('Batasan','Fokus role admin; registrasi publik dicakup hanya sebagai syarat autentikasi proyek. Tidak ada perubahan role melalui registrasi.'),('Batasan','Uji dilakukan pada database lokal yang dicadangkan. Jangan menghapus data asli; baseline commit dan perubahan lokal dicatat sebelum demo.'),('Batasan','Jadwal demo 7 Oktober 2026; tautan registrasi dan keunikan produk Web harus diverifikasi bersama asisten. Dokumen tidak menyatakan persetujuan asisten sudah diberikan.')])
risks=[
('R-01','Batas otorisasi tidak sesuai kebutuhan: endpoint /api/admin juga mengizinkan editor; akses UI dan API dapat berbeda.','Produk',5,3,'Konfirmasi matriks izin dengan asisten, bandingkan akses tanpa token dan akun pembanding, pastikan data admin hanya dapat diubah role yang disepakati.'),
('R-02','Reset password gagal karena SMTP tidak tersedia, token dapat digunakan ulang atau sesi lama masih aktif.','Produk',5,3,'Siapkan Mailpit dan migrasi reset; periksa email, token sekali pakai/kedaluwarsa dan penolakan sesi lama menggunakan akun admin sementara.'),
('R-03','Input program tidak konsisten: peserta negatif/nol atau rentang tanggal terbalik dapat tersimpan.','Produk',4,4,'Sepakati batas peserta dan tanggal; bandingkan validasi UI/API serta data tersimpan. Dahulukan pemeriksaan nilai nol, negatif dan urutan tanggal.'),
('R-04','Unggahan berkas tidak dibatasi backend; fileFilter menerima semua berkas tanpa batas ukuran meskipun UI menyebut maksimum 5 MB.','Produk',4,4,'Gunakan berkas sementara; konfirmasi jenis/ukuran yang diizinkan, catat perbedaan UI/backend sebagai incident dan rencanakan validasi server serta pembersihan file.'),
('R-05','Ubah/hapus konten menyebabkan data dan berkas tidak sinkron atau data asli hilang.','Produk',5,3,'Cadangkan database dan folder unggahan; gunakan data berawalan PKPL-M1, periksa persistensi dan pembersihan, siapkan pemulihan cadangan.'),
('R-06','Status pesan tidak mencerminkan keadaan terbaru; detail mengubah status read tetapi respons dapat membawa status sebelumnya.','Produk',3,4,'Bandingkan status pada detail, daftar setelah refresh dan database; gunakan pesan sementara dan cek perubahan new/read/replied.'),
('R-07','Demo terganggu karena MySQL, backend, frontend atau Mailpit tidak aktif.','Proyek',4,3,'Lakukan pemeriksaan health dan login sebelum demo, jalankan JALANKAN.cmd, siapkan log serta langkah pemulihan layanan lokal.'),
('R-08','Registrasi terlambat, produk Web duplikat atau pemahaman source belum cukup saat demo.','Proyek',4,3,'Isi baris registrasi resmi setelah tautan tersedia, validasi UNQ-1 bersama asisten dan latihan penjelasan source serta alasan risiko sebelum 7 Oktober.')]
fill(8,[(rid,desc,kind,d,l,d*l,m) for rid,desc,kind,d,l,m in risks])
textset(ps[52],'Dasar skor: dampak 1 kosmetik, 2 gangguan kecil, 3 fungsi sebagian terganggu, 4 fitur utama/demo terhambat, 5 akses akun atau integritas data terancam. Kemungkinan 1 sangat jarang, 2 rendah, 3 sedang, 4 tinggi karena indikasi pada kode, 5 hampir pasti. Skor awal merupakan estimasi perencanaan, bukan angka hasil eksekusi. R-03/R-04 mendapat kemungkinan 4 karena validasi server perlu diperiksa; R-01/R-02/R-05 berdampak 5 karena menyangkut izin, akun atau kehilangan data. Urutan: 16 (R-03/R-04), 15 (R-01/R-02/R-05), lalu 12 (R-06/R-07/R-08).')
fill(9,[('Pendekatan Pengujian','Belum ditetapkan; dilengkapi pada modul berikutnya. Perencanaan Modul 1 mendahulukan fitur berisiko tinggi dan bukti yang dapat ditelusuri.'),('Tingkat Pengujian','Belum ditetapkan; dilengkapi pada modul berikutnya.'),('Jenis Pengujian Utama','Belum ditetapkan; dilengkapi pada modul berikutnya.'),('Fitur Berprioritas Tinggi','F-05/F-06 dan unggahan F-08/F-09 (R-03/R-04, 16); akses admin, reset dan penghapusan (R-01/R-02/R-05, 15).')])
fill(10,[('Arah dan Teknik Pengujian','Belum ditetapkan','Dilengkapi setelah materi terkait dipelajari pada modul berikutnya.')])
fill(11,[('Kriteria Masuk','Baseline build dicatat; MySQL terhubung; UI, API dan Mailpit aktif; akun admin dan data sementara tersedia; scope dan aturan bisnis disepakati; cadangan dibuat.'),('Kriteria Keluar','Modul 1: seluruh bagian wajib lengkap, minimal lima risiko dinilai, baris registrasi resmi dan 13 item kesiapan diperiksa asisten, serta demo selesai. Siklus berikutnya: semua kasus yang disepakati dieksekusi; tidak ada incident kritis/tinggi terbuka tanpa keputusan asisten.'),('Kriteria Lolos','Hasil aktual sesuai hasil yang diharapkan pada kebutuhan yang disepakati; pesan, status, data tersimpan dan izin sesuai. Modul 1 tidak menyatakan semua fitur telah lolos.'),('Kriteria Gagal','Hasil berbeda dari kebutuhan, akses tidak sah, data tidak tersimpan/konsisten, error atau aplikasi berhenti. Langkah, input, hasil aktual dan bukti dicatat sebagai incident.'),('Pengujian Ulang','Setelah perbaikan, ulangi kasus yang gagal dengan input dan prasyarat sama; bandingkan hasil serta kaitkan bukti dengan ID incident.'),('Pengujian Regresi','Setelah perubahan, periksa kembali login admin, akses dashboard, CRUD program/berita dan status pesan. Perubahan autentikasi juga mencakup reset dan validitas sesi.')])
fill(11,[('Kriteria Masuk','Build dicatat; MySQL, UI, API dan Mailpit aktif; akun/data sementara siap; scope disepakati; cadangan tersedia.'),('Kriteria Keluar','Modul 1: dokumen lengkap, risiko dinilai, registrasi dan 13 item direview asisten, demo selesai. Siklus berikutnya: seluruh kasus disepakati dieksekusi; incident kritis/tinggi ditutup atau diputuskan asisten.'),('Kriteria Lolos','Hasil aktual, persistensi data dan izin sesuai kebutuhan yang disepakati. Modul 1 belum menyatakan seluruh fitur lolos.'),('Kriteria Gagal','Hasil menyimpang, akses tidak sah, data tidak konsisten atau error; input, langkah, hasil dan bukti dicatat sebagai incident.'),('Pengujian Ulang','Ulangi kasus gagal setelah perbaikan dengan input/prasyarat sama; tautkan hasil ke incident.'),('Pengujian Regresi','Setelah perubahan, periksa login, dashboard, CRUD program/berita dan status pesan; perubahan autentikasi juga memerlukan reset dan validitas sesi.')])
fill(12,[('Jenis Perangkat','Laptop HP 15'),('Processor','AMD Ryzen 5 5500U with Radeon Graphics'),('RAM','Sekitar 8 GB terpasang; terdeteksi 7,87 GB memori fisik'),('Sistem Operasi','Windows 11 Home versi 10.0.26200')])
fill(13,[('Browser','Chrome atau Edge desktop; versi aktual dicatat saat demo','Akses UI dan pemeriksaan respons melalui DevTools'),('Runtime dan database','Node.js; Express 5; MySQL lokal Laragon; versi runtime dicatat saat baseline','Menjalankan API dan menyimpan data'),('Alat Dokumentasi','Microsoft Word; dokumen DOCX berdasarkan template laboratorium','Test Plan dan revisi'),('Alat Tangkapan Layar','Snipping Tool Windows','Bukti layar saat demo dan modul lanjutan'),('Email lokal','Mailpit http://localhost:8025; SMTP 127.0.0.1:1025','Membaca tautan reset password')])
fill(13,[('Browser','Chrome/Edge; versi dicatat saat demo','UI dan DevTools'),('Runtime dan database','Node.js, Express 5, MySQL Laragon; versi dicatat saat baseline','API dan penyimpanan'),('Dokumentasi','Microsoft Word','Test Plan dan revisi'),('Tangkapan layar','Snipping Tool Windows','Bukti demo'),('Email lokal','Mailpit localhost:8025; SMTP :1025','Tautan reset')])
fill(14,[('Jaringan','Loopback localhost untuk UI/API/database/SMTP; internet diperlukan untuk spreadsheet registrasi resmi.'),('Backend / API','REST Express http://localhost:3000/api; MySQL 127.0.0.1:3306 database sustainova. Health /api/health harus mengembalikan database connected.'),('URL Dasar Pengujian','http://localhost:5173; Mailpit http://localhost:8025')])
fill(15,[('Akun Uji Valid','Akun admin dari seed; akun admin sementara untuk reset agar password seed tidak berubah. Kredensial lokal disimpan di catatan operasional, bukan bukti publik.'),('Akun Uji Tidak Valid','Email tidak terdaftar, password salah, kolom kosong dan token tidak berlaku; akun pembanding untuk penolakan akses.'),('Contoh Data Input','Program dengan teks, peserta, status, tanggal dan poster; berita dengan kategori/isi/cover; pesan dengan status new/read/replied; email registrasi unik. Semua data sementara memakai awalan PKPL-M1.'),('Data Uji Tambahan','Belum ditetapkan; kumpulan nilai dan kasus rinci dilengkapi pada modul berikutnya.')])
fill(16,[('Modul 1','5 Oktober: analisis aplikasi dan penyusunan Test Plan/risiko; 6 Oktober: review, registrasi dan latihan; 7 Oktober: pemeriksaan layanan dan demo.','5 sampai 7 Oktober 2026','Dokumen Test Plan dan entri registrasi proyek'),*[(m,'Belum ditetapkan','Belum ditetapkan','Belum ditetapkan') for m in ['Modul 2','Modul 3','Modul 4','Modul 5','Modul 6','UAP']]])
fill(17,[('Modul 1','Dokumen Test Plan','DOCX','Siap review asisten; revisi mengikuti hasil demo'),('Modul 1','Entri Lembar Registrasi Proyek beserta 13 item kesiapan','Google Sheets resmi laboratorium','Belum diisi; tautan registrasi perlu tersedia dan UNQ-1 perlu diperiksa'),*[(m,'Belum ditetapkan','Belum ditetapkan','Belum ditetapkan') for m in ['Modul 2','Modul 3','Modul 4','Modul 5','Modul 6','UAP']]])
textset(ps[33],'Sumber kebutuhan awal: README.md, LOCAL-SETUP.md, frontend/src/router/index.js, halaman autentikasi/admin, backend-js/src/routes/adminRoutes.js, uploadFile.js dan controller terkait. Sumber ini digunakan untuk menyusun cakupan; aturan bisnis yang belum eksplisit dikonfirmasi kepada asisten. SRS belum wajib selesai pada Modul 1 dan dilengkapi bertahap pada Modul 2.')
textset(ps[38],'Cakupan mencakup 11 fitur: tiga autentikasi wajib dan delapan fitur tambahan. Operasi tambah, ubah dan hapus mempunyai input, proses serta hasil berbeda. Register adalah jalur publik proyek sebelum autentikasi, sedangkan role under test tetap Admin.')
textset(ps[62],'Arah dan teknik pengujian dipertahankan sebagai Belum ditetapkan untuk Modul 1 sesuai template laboratorium.')
parts={i.filename:z.read(i.filename) for i in z.infolist()}
parts['word/document.xml']=E.tostring(tree,xml_declaration=True,encoding='UTF-8',standalone=True)
if 'word/settings.xml' in parts:
    settings=E.fromstring(parts['word/settings.xml']); uf=settings.find('w:updateFields',ns)
    if uf is None:uf=E.SubElement(settings,W+'updateFields')
    uf.set(W+'val','true');parts['word/settings.xml']=E.tostring(settings,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(out,'w') as dest:
    for i in z.infolist():dest.writestr(i,parts[i.filename])
contract={'reference':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'section':'Letter portrait 8.5 x 11 inch; all margins 1 inch; geometry preserved','slots':'Body paragraph 15 subtitle; tables 0,2-17 edited; table 1 reference instruction removed as allowed; glossary tables 18-19 preserved; instructions kept or clarified. Added rows clone source body row.','preserve_only':[i.filename for i in z.infolist() if i.filename not in ['word/document.xml','word/settings.xml']],'styles':'Source Title, Subtitle, Heading 1, Heading 2, normal preserved byte for byte; table grids and cell properties cloned; heading, footer and numbering parts preserved','render':'Packaged renderer unavailable because LibreOffice absent; Word native PDF export attempted for actual template and final QA.'}
(root/'tmp/pkpl/artifact.md').write_text(json.dumps(contract,indent=2),encoding='utf-8')
with ZipFile(out) as final:
    assert all(final.read(p)==parts[p] for p in contract['preserve_only'])
print(out)
