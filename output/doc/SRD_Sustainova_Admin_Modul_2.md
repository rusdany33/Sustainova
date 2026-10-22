# Software Requirements Document Sustainova Admin

ID SRD-SUSTAINOVA-ADMIN-202210370311406 | Versi 1.0 | 15 Oktober 2026

Rusdany Maestro | NIM 202210370311406 | Kelas C

## Tujuan dan sumber kebutuhan

Dokumen kebutuhan ini dikonsolidasikan pada 15 Oktober 2026 untuk mendukung analisis LAB SESSION Modul 2. Dasarnya adalah Test Plan revisi menu v1.2, arahan pengelompokan menu dan search/filter dari praktikan, serta UI dan source code yang tersedia. Dokumen ini tidak menyatakan bahwa seluruh kebutuhan sudah lolos eksekusi atau telah disetujui asisten.

## Cakupan

Role utama Admin. Tiga autentikasi wajib dan lima menu utama: Dashboard, Kelola Berita, Kelola Program, Pesan, Profil. Register merupakan jalur publik sebelum autentikasi dan membuat akun user. CRUD/search/filter diperlakukan sebagai subfitur. Kelola akun berarti profil akun sendiri, bukan CRUD semua pengguna.

## Kebijakan interpretasi

Search/filter berarti pencarian sebagian teks pada atribut daftar, dengan trim dan tanpa membedakan kapital. Ini bukan klaim filter dropdown terpisah. Baris berita/program yang sedang diedit tetap ditampilkan sesuai implementasi. Status pesan yang digunakan adalah new/read/replied; label replied tidak membuktikan pengiriman email.

Batas gambar form adalah 5 x 1024 x 1024 byte; JPG/JPEG, PNG, GIF dan WebP. Batas tersebut pada UI belum menjadi bukti validasi backend. Required poster/tanggal/deskripsi program dirujuk dari controller tambahProgram meskipun tanda wajib pada UI belum seragam. Peserta >= 0 dirujuk dari min form; nol diperlakukan sebagai nilai yang perlu diverifikasi, bukan otomatis tidak valid.

Form Register memakai minimum password 6 karakter; reset memakai minimum 8 karakter dan maksimum 72 byte UTF-8 di backend. Kedua alur dibedakan. Frontend reset membatasi 72 karakter; perbedaan karakter dan byte perlu dipertimbangkan pada data non-ASCII.

Route UI admin membatasi role admin; sebagian endpoint API admin juga mengizinkan editor. RQ-002 tidak mengklaim semua API eksklusif admin; matriks hak API yang lebih ketat memerlukan keputusan asisten. Profil hanya memvalidasi nama/email wajib dan format email pada form; validasi tambahan yang belum ditetapkan tidak dikarang.

## Kebutuhan fungsional

### F-01 Login

**RQ-001** Sistem harus menerima login akun admin dengan email terdaftar dan password benar, serta menolak input kosong, email tidak valid dan kredensial salah.

Prioritas High. Risiko terkait R-01.

Sumber: frontend/src/page/auth/login.vue; backend-js/src/controllers/authControllers.js (loginUser).

**RQ-002** Sistem harus mengarahkan menu admin ke halaman yang benar dan mempertahankan akses saat refresh jika sesi sah; halaman terlindungi harus menolak sesi kosong, kedaluwarsa atau role yang tidak diizinkan.

Prioritas High. Risiko terkait R-01.

Sumber: frontend/src/router/index.js (beforeEach); frontend/src/components/AccountMenu.vue; backend-js/src/middlewares/authorization.js.

**RQ-003** Logout harus menghapus sesi lokal sehingga halaman terlindungi meminta login kembali.

Prioritas High. Risiko terkait R-01.

Sumber: frontend/src/utils/auth.js (logout); frontend/src/components/AccountMenu.vue (signOut).

### F-02 Register

**RQ-004** Registrasi publik dengan seluruh isian valid dan email baru harus membuat akun user, bukan admin.

Prioritas High. Risiko terkait konsistensi fungsi dan keterpakaian.

Sumber: frontend/src/page/auth/register.vue; backend-js/src/controllers/authControllers.js (registerUser).

**RQ-005** Form Register harus memvalidasi nama minimal 3 karakter, format email, telepon 10-15 digit setelah normalisasi, alamat minimal 10 karakter, password minimal 6 karakter dan konfirmasi yang cocok; email duplikat ditolak backend.

Prioritas High. Risiko terkait konsistensi fungsi dan keterpakaian.

Sumber: frontend/src/page/auth/register.vue (validateField); backend-js/src/controllers/authControllers.js (registerUser).

### F-03 Forgot Password

**RQ-006** Permintaan Forgot Password harus memvalidasi email, mengirim tautan ke akun terdaftar dan memberi pesan generik untuk email berformat sah; pengiriman ulang mengikuti cooldown 60 detik.

Prioritas High. Risiko terkait R-02.

Sumber: frontend/src/page/auth/forgotPass.vue; backend-js/src/controllers/passwordResetController.js (requestReset).

**RQ-007** Token reset hanya boleh dipakai sebelum 30 menit dan satu kali; token tidak valid, kedaluwarsa atau terpakai harus ditolak.

Prioritas High. Risiko terkait R-02.

Sumber: backend-js/src/controllers/passwordResetController.js (requestReset, resetPassword).

**RQ-008** Password reset harus minimal 8 karakter, maksimal 72 byte UTF-8 dan konfirmasinya cocok; reset berhasil mengakhiri sesi lama.

Prioritas High. Risiko terkait R-02.

Sumber: frontend/src/page/auth/resetPassword.vue; backend-js/src/controllers/passwordResetController.js (resetPassword).

### F-04 Dashboard

**RQ-009** Dashboard harus menampilkan total program, berita dan pesan sesuai data yang berhasil dimuat.

Prioritas Medium. Risiko terkait konsistensi fungsi dan keterpakaian.

Sumber: frontend/src/page/admin/dashboard.vue (fetchDashboardData); backend-js/src/controllers/admin/adminControllers.js (dashboard, getContactMessages).

**RQ-010** Dashboard harus menampilkan ringkasan program dan berita terbaru serta daftar pesan, dengan navigasi ke menu pengelolaan.

Prioritas Medium. Risiko terkait konsistensi fungsi dan keterpakaian.

Sumber: frontend/src/page/admin/dashboard.vue; backend-js/src/controllers/admin/adminControllers.js (dashboard).

### F-05 Kelola Berita

**RQ-011** Kelola Berita harus menampilkan daftar berita dan membedakan keadaan data kosong dari kegagalan memuat data.

Prioritas Medium. Risiko terkait konsistensi fungsi dan keterpakaian.

Sumber: frontend/src/page/admin/kelola/berita.vue (fetchBeritaData, loadError).

**RQ-012** Admin harus dapat menambah berita dengan judul minimal 5 karakter dan konten minimal 10 karakter setelah trim, tanggal publikasi dan cover wajib; unggahan melalui form menerima JPG/PNG/GIF/WebP maksimal 5 x 1024 x 1024 byte.

Prioritas High. Risiko terkait R-04.

Sumber: frontend/src/page/admin/tambah/berita.vue (submitForm, handleCoverUpload); backend-js/src/controllers/admin/tambahControllers.js (tambahBerita).

**RQ-013** Admin harus dapat menyimpan perubahan berita termasuk penggantian cover, atau membatalkan edit tanpa mengubah data tersimpan.

Prioritas High. Risiko terkait R-05.

Sumber: frontend/src/page/admin/kelola/berita.vue (startEdit, cancelEdit, saveEdit); backend-js/src/controllers/admin/adminControllers.js (editBerita).

**RQ-014** Admin harus dapat menghapus berita yang dipilih setelah konfirmasi; pembatalan tidak menghapus berita.

Prioritas High. Risiko terkait R-05.

Sumber: frontend/src/page/admin/kelola/berita.vue (deleteHandler); backend-js/src/controllers/admin/adminControllers.js (deleteBerita).

**RQ-015** Search/filter Kelola Berita harus menyaring daftar berdasarkan kecocokan sebagian judul, ringkasan, kategori atau tanggal; abaikan kapital dan spasi tepi, sediakan reset serta jumlah hasil. Baris yang sedang diedit tetap terlihat.

Prioritas Medium. Risiko terkait konsistensi fungsi dan keterpakaian.

Sumber: frontend/src/page/admin/kelola/berita.vue (query, filteredItems); frontend/src/components/admin/SearchToolbar.vue.

### F-06 Kelola Program

**RQ-016** Kelola Program harus menampilkan daftar program dan membedakan data kosong dari kegagalan memuat data.

Prioritas Medium. Risiko terkait konsistensi fungsi dan keterpakaian.

Sumber: frontend/src/page/admin/kelola/program.vue (fetchProgramData, loadError).

**RQ-017** Admin harus dapat menambah program dengan nama, deskripsi, status, peserta, tanggal mulai/selesai dan poster wajib; peserta mengikuti batas form >= 0, tanggal mulai tidak melewati tanggal selesai, serta poster form berjenis gambar yang diizinkan maksimal 5 x 1024 x 1024 byte.

Prioritas High. Risiko terkait R-03, R-04.

Sumber: frontend/src/page/admin/tambah/program.vue (submitForm, handlePosterUpload); backend-js/src/controllers/admin/tambahControllers.js (tambahProgram).

**RQ-018** Admin harus dapat menyimpan perubahan program termasuk peserta, status, tanggal dan poster, atau membatalkan edit tanpa perubahan data tersimpan.

Prioritas High. Risiko terkait R-03, R-05.

Sumber: frontend/src/page/admin/kelola/program.vue (startEdit, cancelEdit, saveEdit); backend-js/src/controllers/admin/adminControllers.js (editProgram).

**RQ-019** Admin harus dapat menghapus program yang dipilih setelah konfirmasi; pembatalan tidak menghapus program.

Prioritas High. Risiko terkait R-05.

Sumber: frontend/src/page/admin/kelola/program.vue (deleteProgram); backend-js/src/controllers/admin/adminControllers.js (deleteProgram).

**RQ-020** Search/filter Kelola Program harus menyaring sebagian nama, deskripsi, status, peserta atau tanggal; abaikan kapital/spasi tepi, sediakan reset dan jumlah hasil; baris aktif edit tetap terlihat.

Prioritas Medium. Risiko terkait konsistensi fungsi dan keterpakaian.

Sumber: frontend/src/page/admin/kelola/program.vue (query, filteredItems); frontend/src/components/admin/SearchToolbar.vue.

### F-07 Pesan

**RQ-021** Menu Pesan harus memuat daftar dan detail pesan; membuka detail menandai pesan read dan memperbarui jumlah pesan baru, sedangkan kegagalan muat ditampilkan sebagai error.

Prioritas High. Risiko terkait R-06.

Sumber: frontend/src/page/admin/kelola/messages.vue (loadMessages, viewMessage, unreadCount); backend-js/src/controllers/admin/adminControllers.js (getContactMessageDetail).

**RQ-022** Admin harus dapat memperbarui status pesan menjadi new, read atau replied; status di luar pilihan itu harus ditolak.

Prioritas High. Risiko terkait R-06.

Sumber: frontend/src/page/admin/kelola/messages.vue (updateStatus); backend-js/src/controllers/admin/adminControllers.js (updateMessageStatus).

**RQ-023** Admin harus dapat menghapus pesan terpilih setelah konfirmasi; pembatalan tidak menghapus pesan.

Prioritas High. Risiko terkait R-05.

Sumber: frontend/src/page/admin/kelola/messages.vue (deleteMessage); backend-js/src/controllers/admin/adminControllers.js (deleteContactMessage).

**RQ-024** Search/filter Pesan harus menyaring sebagian nama/email pengirim, subjek, topik, isi atau status/label status; abaikan kapital/spasi tepi dan sediakan reset serta jumlah hasil.

Prioritas Medium. Risiko terkait konsistensi fungsi dan keterpakaian.

Sumber: frontend/src/page/admin/kelola/messages.vue (query, filteredItems); frontend/src/components/admin/SearchToolbar.vue.

### F-08 Profil

**RQ-025** Profil harus menampilkan data akun admin yang sedang login dan tautan akses cepat menuju menu pengelolaannya.

Prioritas High. Risiko terkait R-10.

Sumber: frontend/src/page/profile.vue (onMounted); backend-js/src/controllers/client/clientControllers.js (getUserProfile).

**RQ-026** Admin harus dapat memperbarui nama, email, telepon, username dan alamat akun sendiri; nama/email wajib dan email berformat sah pada form; perubahan tersimpan setelah refresh.

Prioritas High. Risiko terkait R-10.

Sumber: frontend/src/page/profile.vue (updateProfile); backend-js/src/controllers/client/clientControllers.js (updateUserProfile).

**RQ-027** Batal pada form Profil harus menutup edit tanpa mengirim perubahan ke server.

Prioritas Medium. Risiko terkait konsistensi fungsi dan keterpakaian.

Sumber: frontend/src/page/profile.vue (Cancel).

## Perbedaan dan konfirmasi yang masih diperlukan

Validasi server untuk peserta, tanggal, ukuran/jenis unggahan dan profil belum setara dengan batas UI; kondisi desain menetapkan aspek yang harus diperiksa, bukan klaim implementasi benar. Kosakata status program pada form tambah dan edit berbeda; daftar status bisnis tunggal perlu dikonfirmasi sebelum menurunkan kasus nilai spesifik.

Sumber README menyebut status pesan resolved, sedangkan UI/controller memakai replied; desain ini memakai UI/controller yang sedang tersedia. Persetujuan proyek dari Modul 1 tidak dianggap otomatis sebagai persetujuan setiap aturan kebutuhan baru.

## Pengendalian perubahan

Jika aturan asisten berubah, perbarui RQ terkait, lalu telusuri seluruh FS, TCond dan CI pada TTM. Sumber tetap menggunakan ID RQ yang sama apabila maknanya tidak berubah; kebutuhan baru diberi ID baru.