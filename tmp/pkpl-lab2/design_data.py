"""Source-grounded requirements and test conditions for the Admin scope."""
features=[
('F-01','FS-001','Login','High','Memastikan login, sesi, rute menu dan logout admin sesuai hak akses.'),
('F-02','FS-002','Register','High','Memeriksa registrasi publik wajib proyek; akun baru tetap user, bukan admin.'),
('F-03','FS-003','Forgot Password','High','Memeriksa permintaan email, validitas token reset dan perubahan sesi admin.'),
('F-04','FS-004','Dashboard','Medium','Memeriksa ringkasan program, berita, pesan dan tautan menuju menu pengelolaan.'),
('F-05','FS-005','Kelola Berita','High','Memeriksa daftar, tambah, ubah, hapus dan search/filter berita.'),
('F-06','FS-006','Kelola Program','High','Memeriksa daftar, tambah, ubah, hapus dan search/filter program.'),
('F-07','FS-007','Pesan','High','Memeriksa daftar, detail, status, hapus dan search/filter pesan kontak.'),
('F-08','FS-008','Profil','High','Memeriksa profil dan perubahan informasi akun admin sendiri.')]
req=[];conds=[]
def add(fs,description,source,coverage,cases,priority='High',risk=''):
 rid=f'RQ-{len(req)+1:03}';ci=f'CI-{len(req)+1:03}'
 req.append(dict(id=rid,fs=f'FS-{fs:03}',description=description,source=source,coverage=coverage,ci=ci,priority=priority,risk=risk))
 for text in cases:
  conds.append(dict(id=f'TCond-{len(conds)+1:03}',rq=rid,fs=f'FS-{fs:03}',ci=ci,description=text,priority=priority))

add(1,'Sistem harus menerima login akun admin dengan email terdaftar dan password benar, serta menolak input kosong, email tidak valid dan kredensial salah.',
'frontend/src/page/auth/login.vue; backend-js/src/controllers/authControllers.js (loginUser)',
'Input email/password, respons login dan tujuan dashboard',[
'Email admin terdaftar dan password benar menghasilkan sesi admin serta tujuan /admin/dashboard.',
'Email/password kosong atau format email salah ditolak dengan informasi pada input terkait.',
'Email tidak terdaftar atau password salah ditolak tanpa membuat sesi login.'],risk='R-01')
add(1,'Sistem harus mengarahkan menu admin ke halaman yang benar dan mempertahankan akses saat refresh jika sesi sah; halaman terlindungi harus menolak sesi kosong, kedaluwarsa atau role yang tidak diizinkan.',
'frontend/src/router/index.js (beforeEach); frontend/src/components/AccountMenu.vue; backend-js/src/middlewares/authorization.js',
'Menu/rute admin, refresh dan pemeriksaan sesi',[
'Admin bersesi sah membuka Dashboard, Kelola Berita, Pesan, Profil dan Kelola Program melalui menu serta refresh URL tujuan.',
'Pengunjung tanpa sesi atau dengan sesi kedaluwarsa diarahkan ke login ketika membuka rute terlindungi.',
'Role pembanding non-admin tidak membuka halaman /admin; API tanpa token sah menolak akses.'],risk='R-01')
add(1,'Logout harus menghapus sesi lokal sehingga halaman terlindungi meminta login kembali.',
'frontend/src/utils/auth.js (logout); frontend/src/components/AccountMenu.vue (signOut)',
'Logout dan akses kembali setelah sesi dihapus',[
'Logout diikuti akses ulang/refresh halaman admin meminta login kembali.'],risk='R-01')
add(2,'Registrasi publik dengan seluruh isian valid dan email baru harus membuat akun user, bukan admin.',
'frontend/src/page/auth/register.vue; backend-js/src/controllers/authControllers.js (registerUser)',
'Registrasi berhasil dan role akun baru',[
'Data registrasi valid dan email unik membuat akun user serta mengarahkan pengguna ke login.'])
add(2,'Form Register harus memvalidasi nama minimal 3 karakter, format email, telepon 10-15 digit setelah normalisasi, alamat minimal 10 karakter, password minimal 6 karakter dan konfirmasi yang cocok; email duplikat ditolak backend.',
'frontend/src/page/auth/register.vue (validateField); backend-js/src/controllers/authControllers.js (registerUser)',
'Validasi tiap kolom Register dan keunikan email',[
'Setiap kolom wajib kosong atau panjang/format input tidak memenuhi aturan form ditolak tanpa registrasi.',
'Konfirmasi password berbeda ditolak; email yang sudah terdaftar tidak menghasilkan akun kedua.'])
add(3,'Permintaan Forgot Password harus memvalidasi email, mengirim tautan ke akun terdaftar dan memberi pesan generik untuk email berformat sah; pengiriman ulang mengikuti cooldown 60 detik.',
'frontend/src/page/auth/forgotPass.vue; backend-js/src/controllers/passwordResetController.js (requestReset)',
'Email permintaan reset, respons generik dan cooldown',[
'Email admin terdaftar berformat sah menerima tautan melalui Mailpit; email tidak terdaftar mendapat pesan generik yang sama tanpa tautan akun.',
'Email kosong/format salah ditolak; permintaan ulang sebelum 60 detik tidak mengirim email kedua.'],risk='R-02')
add(3,'Token reset hanya boleh dipakai sebelum 30 menit dan satu kali; token tidak valid, kedaluwarsa atau terpakai harus ditolak.',
'backend-js/src/controllers/passwordResetController.js (requestReset, resetPassword)',
'Masa berlaku dan pemakaian token reset',[
'Token sah dan belum terpakai dapat digunakan sebelum kedaluwarsa.',
'Token palsu, kedaluwarsa atau sudah dipakai tidak mengubah password.'],risk='R-02')
add(3,'Password reset harus minimal 8 karakter, maksimal 72 byte UTF-8 dan konfirmasinya cocok; reset berhasil mengakhiri sesi lama.',
'frontend/src/page/auth/resetPassword.vue; backend-js/src/controllers/passwordResetController.js (resetPassword)',
'Validasi password reset dan invalidasi sesi lama',[
'Password terlalu pendek, melebihi 72 byte atau konfirmasi berbeda ditolak tanpa perubahan password.',
'Reset valid memungkinkan login dengan password baru, menolak password lama dan membuat token sesi lama tidak berlaku.'],risk='R-02')
add(4,'Dashboard harus menampilkan total program, berita dan pesan sesuai data yang berhasil dimuat.',
'frontend/src/page/admin/dashboard.vue (fetchDashboardData); backend-js/src/controllers/admin/adminControllers.js (dashboard, getContactMessages)',
'Total program, berita dan pesan pada dashboard',[
'Total tiga kategori sesuai data sumber; keadaan tanpa data menunjukkan nol.',
'Setelah perubahan data berhasil, dashboard yang dimuat ulang memperbarui total kategori terkait.'],priority='Medium')
add(4,'Dashboard harus menampilkan ringkasan program dan berita terbaru serta daftar pesan, dengan navigasi ke menu pengelolaan.',
'frontend/src/page/admin/dashboard.vue; backend-js/src/controllers/admin/adminControllers.js (dashboard)',
'Tab ringkasan dan tautan Lihat Semua',[
'Tab Program/Berita menampilkan maksimal tiga data terbaru menurut urutan ID; tab Pesan menampilkan daftar yang dimuat.',
'Tautan Lihat Semua pada ringkasan membuka menu yang sesuai tanpa rute salah.'],priority='Medium')
add(5,'Kelola Berita harus menampilkan daftar berita dan membedakan keadaan data kosong dari kegagalan memuat data.',
'frontend/src/page/admin/kelola/berita.vue (fetchBeritaData, loadError)',
'Daftar berita, empty state dan load error',[
'Daftar berisi data atau pesan tanpa data sesuai respons berhasil; kegagalan API menunjukkan informasi gagal memuat.'],priority='Medium')
add(5,'Admin harus dapat menambah berita dengan judul minimal 5 karakter dan konten minimal 10 karakter setelah trim, tanggal publikasi dan cover wajib; unggahan melalui form menerima JPG/PNG/GIF/WebP maksimal 5 x 1024 x 1024 byte.',
'frontend/src/page/admin/tambah/berita.vue (submitForm, handleCoverUpload); backend-js/src/controllers/admin/tambahControllers.js (tambahBerita)',
'Form berita, tanggal dan unggahan cover',[
'Isian berita valid dan cover yang diizinkan menghasilkan berita yang terlihat setelah refresh.',
'Judul/konten kurang dari panjang minimum atau tanggal/cover wajib tidak tersedia membuat penambahan ditolak.',
'Form menolak cover dengan tipe tidak didukung atau ukuran di atas batas unggahan.'],risk='R-04')
add(5,'Admin harus dapat menyimpan perubahan berita termasuk penggantian cover, atau membatalkan edit tanpa mengubah data tersimpan.',
'frontend/src/page/admin/kelola/berita.vue (startEdit, cancelEdit, saveEdit); backend-js/src/controllers/admin/adminControllers.js (editBerita)',
'Edit, batal, persistensi dan cover berita',[
'Perubahan berita/cover yang disimpan tetap terlihat setelah refresh.',
'Batal edit mengembalikan nilai semula; kegagalan penyimpanan tidak ditampilkan sebagai keberhasilan.'],risk='R-05')
add(5,'Admin harus dapat menghapus berita yang dipilih setelah konfirmasi; pembatalan tidak menghapus berita.',
'frontend/src/page/admin/kelola/berita.vue (deleteHandler); backend-js/src/controllers/admin/adminControllers.js (deleteBerita)',
'Konfirmasi hapus dan identitas berita',[
'Konfirmasi hapus menghilangkan berita yang dipilih tanpa menghapus berita lain.',
'Batal pada konfirmasi mempertahankan data berita.'],risk='R-05')
add(5,'Search/filter Kelola Berita harus menyaring daftar berdasarkan kecocokan sebagian judul, ringkasan, kategori atau tanggal; abaikan kapital dan spasi tepi, sediakan reset serta jumlah hasil. Baris yang sedang diedit tetap terlihat.',
'frontend/src/page/admin/kelola/berita.vue (query, filteredItems); frontend/src/components/admin/SearchToolbar.vue',
'Kata kunci, normalisasi, jumlah hasil dan reset berita',[
'Saat tidak mengedit, kata kunci cocok pada tiap atribut pencarian hanya menampilkan berita yang sesuai; variasi kapital/spasi tepi memberi hasil sama.',
'Kata kunci tidak cocok menunjukkan nol hasil; kata kunci kosong, tombol hapus atau Escape memulihkan daftar.',
'Jumlah hasil sesuai baris yang tampil; baris berita aktif edit tetap terlihat saat kata kunci berubah.'],priority='Medium')
add(6,'Kelola Program harus menampilkan daftar program dan membedakan data kosong dari kegagalan memuat data.',
'frontend/src/page/admin/kelola/program.vue (fetchProgramData, loadError)',
'Daftar program, empty state dan load error',[
'Daftar program, pesan tanpa data dan pesan gagal memuat sesuai keadaan respons.'],priority='Medium')
add(6,'Admin harus dapat menambah program dengan nama, deskripsi, status, peserta, tanggal mulai/selesai dan poster wajib; peserta mengikuti batas form >= 0, tanggal mulai tidak melewati tanggal selesai, serta poster form berjenis gambar yang diizinkan maksimal 5 x 1024 x 1024 byte.',
'frontend/src/page/admin/tambah/program.vue (submitForm, handlePosterUpload); backend-js/src/controllers/admin/tambahControllers.js (tambahProgram)',
'Form program, peserta, rentang tanggal dan poster',[
'Data program lengkap dan poster sah menghasilkan program yang tersedia setelah refresh; nilai peserta nol dan positif diperiksa.',
'Nama kosong/spasi saja atau field wajib/poster tidak tersedia membuat penambahan ditolak.',
'Peserta negatif atau tanggal mulai setelah tanggal selesai ditolak pada form.',
'Poster bertipe tidak didukung atau melebihi batas ukuran ditolak form.'],risk='R-03, R-04')
add(6,'Admin harus dapat menyimpan perubahan program termasuk peserta, status, tanggal dan poster, atau membatalkan edit tanpa perubahan data tersimpan.',
'frontend/src/page/admin/kelola/program.vue (startEdit, cancelEdit, saveEdit); backend-js/src/controllers/admin/adminControllers.js (editProgram)',
'Edit program, status, peserta, poster dan batal',[
'Perubahan program termasuk peserta nol/status/tanggal atau poster tersimpan dan tetap tersedia setelah refresh.',
'Batal edit mengembalikan nilai semula; kegagalan simpan memberi informasi error.'],risk='R-03, R-05')
add(6,'Admin harus dapat menghapus program yang dipilih setelah konfirmasi; pembatalan tidak menghapus program.',
'frontend/src/page/admin/kelola/program.vue (deleteProgram); backend-js/src/controllers/admin/adminControllers.js (deleteProgram)',
'Konfirmasi hapus dan identitas program',[
'Konfirmasi hapus menghilangkan program terpilih tanpa menghapus program lain.',
'Batal pada konfirmasi mempertahankan data program.'],risk='R-05')
add(6,'Search/filter Kelola Program harus menyaring sebagian nama, deskripsi, status, peserta atau tanggal; abaikan kapital/spasi tepi, sediakan reset dan jumlah hasil; baris aktif edit tetap terlihat.',
'frontend/src/page/admin/kelola/program.vue (query, filteredItems); frontend/src/components/admin/SearchToolbar.vue',
'Kata kunci, normalisasi, jumlah hasil dan reset program',[
'Saat tidak mengedit, kecocokan pada setiap atribut pencarian menghasilkan program sesuai kata kunci termasuk variasi kapital/spasi tepi.',
'Kata kunci tidak cocok menghasilkan nol; kosong, tombol hapus atau Escape memulihkan daftar.',
'Jumlah hasil sesuai baris tampil dan program yang sedang diedit tetap terlihat ketika kata kunci berubah.'],priority='Medium')
add(7,'Menu Pesan harus memuat daftar dan detail pesan; membuka detail menandai pesan read dan memperbarui jumlah pesan baru, sedangkan kegagalan muat ditampilkan sebagai error.',
'frontend/src/page/admin/kelola/messages.vue (loadMessages, viewMessage, unreadCount); backend-js/src/controllers/admin/adminControllers.js (getContactMessageDetail)',
'Daftar/detail pesan, status read dan jumlah belum dibaca',[
'Daftar/detail menampilkan pengirim, subjek dan isi pesan yang sesuai; kosong dan gagal muat dibedakan.',
'Membuka pesan new mengubah status menjadi read dan memperbarui indikator setelah reload daftar.'],risk='R-06')
add(7,'Admin harus dapat memperbarui status pesan menjadi new, read atau replied; status di luar pilihan itu harus ditolak.',
'frontend/src/page/admin/kelola/messages.vue (updateStatus); backend-js/src/controllers/admin/adminControllers.js (updateMessageStatus)',
'Transisi status pesan dan penolakan status ilegal',[
'Perubahan ke setiap status yang diizinkan bertahan setelah pemuatan ulang daftar; replied tidak dianggap bukti email terkirim.',
'Permintaan API dengan status di luar new/read/replied ditolak tanpa perubahan status.'],risk='R-06')
add(7,'Admin harus dapat menghapus pesan terpilih setelah konfirmasi; pembatalan tidak menghapus pesan.',
'frontend/src/page/admin/kelola/messages.vue (deleteMessage); backend-js/src/controllers/admin/adminControllers.js (deleteContactMessage)',
'Konfirmasi hapus dan identitas pesan',[
'Konfirmasi hapus menghilangkan pesan terpilih; Batal mempertahankannya dan pesan lain tidak terpengaruh.'],risk='R-05')
add(7,'Search/filter Pesan harus menyaring sebagian nama/email pengirim, subjek, topik, isi atau status/label status; abaikan kapital/spasi tepi dan sediakan reset serta jumlah hasil.',
'frontend/src/page/admin/kelola/messages.vue (query, filteredItems); frontend/src/components/admin/SearchToolbar.vue',
'Kata kunci, status, normalisasi dan reset pesan',[
'Kata kunci pada setiap atribut pencarian, termasuk label status, menampilkan pesan yang cocok dengan normalisasi kapital/spasi tepi.',
'Kata kunci tidak cocok menghasilkan nol; kosong, tombol hapus atau Escape memulihkan daftar dan jumlah hasil yang sesuai.'],priority='Medium')
add(8,'Profil harus menampilkan data akun admin yang sedang login dan tautan akses cepat menuju menu pengelolaannya.',
'frontend/src/page/profile.vue (onMounted); backend-js/src/controllers/client/clientControllers.js (getUserProfile)',
'Data profil akun sendiri dan akses cepat',[
'Nama, email, telepon, alamat dan role sesuai akun admin; tautan akses cepat membuka menu yang benar.'],risk='R-01')
add(8,'Admin harus dapat memperbarui nama, email, telepon, username dan alamat akun sendiri; nama/email wajib dan email berformat sah pada form; perubahan tersimpan setelah refresh.',
'frontend/src/page/profile.vue (updateProfile); backend-js/src/controllers/client/clientControllers.js (updateUserProfile)',
'Isian profil, validasi dasar dan persistensi akun sendiri',[
'Perubahan profil valid tersimpan pada akun admin sendiri dan tetap terlihat setelah refresh.',
'Nama/email kosong atau email tidak berformat sah ditolak form; kegagalan API memberi informasi error.'],risk='R-01')
add(8,'Batal pada form Profil harus menutup edit tanpa mengirim perubahan ke server.',
'frontend/src/page/profile.vue (Cancel)',
'Batal edit profil dan data tersimpan',[
'Batal edit diikuti refresh mempertahankan data profil tersimpan sebelum perubahan.'],priority='Medium')
