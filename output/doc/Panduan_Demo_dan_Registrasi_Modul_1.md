# Persiapan demo Modul 1 PKPL Sustainova Admin

Rusdany Maestro · 202210370311406 · Kelas C · Demo 7 Oktober 2026

## Status registrasi dan persetujuan terbaru

Pada 5 Oktober 2026, entri Rusdany Maestro, NIM 202210370311406, Sustainova Web ditemukan pada tab **C baris 20** di [spreadsheet resmi](https://docs.google.com/spreadsheets/d/1jlCOf2GXIOOpdJOK1X0zS1bMAMTlGdtQsbxrkM2y3Rk/edit?gid=1740208238#gid=1740208238). Praktikan mengonfirmasi proyek sudah disetujui asisten. Kolom status, pemeriksa dan catatan asisten masih kosong pada pembacaan ini; dokumen tidak mengarang nama pemeriksa atau tanggal persetujuan.

Checklist **12/13**: PRJ-1 sampai RDY-6 semuanya TRUE; **REQ-1 pada AE20 masih FALSE**. README.md, LOCAL-SETUP.md, UI serta route/controller sudah diidentifikasi sebagai sumber kebutuhan awal dalam Test Plan. SRS belum wajib selesai pada Modul 1. Tindak lanjutnya adalah mencatat sumber tersebut pada registrasi dan menyesuaikan REQ-1 sesuai hasil review; spreadsheet tidak diubah dalam pembaruan dokumen ini.

Kolom F20 (lima fitur tambahan) dan H20 (catatan praktikan) masih kosong. Bahan fitur dan kebutuhan awal di bagian berikut dapat digunakan untuk melengkapinya. Kolom AG20 menampilkan seluruh kode sebagai belum terpenuhi meskipun 12 kolom bernilai TRUE; gunakan nilai checkbox S20:AE20 dan progres AF20 sebagai bukti pembacaan, serta sampaikan ketidaksesuaian rumus AG20 kepada pengelola bila diperlukan.

## Pemetaan rubrik Table 7.1

| Bobot | Bukti yang disiapkan | Tindakan saat demo |
|---|---|---|
| Test Plan 40% | DOCX mengikuti template: identitas, revisi, konteks, cakupan, asumsi/batasan, strategi, lingkungan, jadwal, luaran | Jelaskan hubungan cakupan dengan risiko dan kriteria. Placeholder Modul 2–UAP serta teknik tetap dipertahankan sesuai template. |
| Analisis risiko 25% | Delapan risiko produk/proyek; dampak dan kemungkinan 1–5, prioritas hasil perkalian, mitigasi | Jelaskan mengapa validasi input/unggahan bernilai 16 dan risiko akun/data bernilai 15. Skor adalah perkiraan perencanaan; indikasi kode bukan hasil seluruh kasus uji. |
| Kesesuaian dan kesiapan 15% | Web, role Admin, 11 fitur, source tersedia dan pemeriksaan API lokal | Tunjukkan aplikasi berjalan dan masukkan 13 item ke baris spreadsheet resmi. Pastikan produk Web tidak didaftarkan mahasiswa lain. |
| Penjelasan demo 20% | Alur penjelasan berikut dan contoh konkret | Jelaskan dengan kata sendiri. Jangan hanya membaca dokumen atau menyatakan semua fitur sudah lolos. |

## Alur demo sekitar 8 sampai 10 menit

1. **Proyek dan role**: “Sustainova adalah aplikasi Web informasi keberlanjutan. Saya memilih Admin untuk mengelola program, berita dan pesan. Role ini konsisten sampai UAP.” Buka halaman login dan masuk dengan akun seed lokal `admin@test.com`, password `password123`. Kredensial ini untuk lingkungan lokal, jangan dimasukkan ke screenshot publik.
2. **Fitur minimum**: jelaskan 3 autentikasi + 8 fitur tambahan. Register membuat akun `user`; fitur ini merupakan jalur publik wajib proyek, bukan cara memperoleh hak admin. Admin disediakan melalui seed. Konfirmasi pemetaan ini dengan asisten. Buka dashboard, daftar program, tambah program, berita dan pesan. Publikasi admin tidak dihitung karena route UI belum terdaftar.
3. **Variasi input dan perilaku**: tunjukkan nama/deskripsi teks, jumlah peserta angka, tanggal, poster berkas, status program dan status pesan. Tambah/ubah/hapus memiliki proses serta keluaran tersendiri. Gunakan data sementara `PKPL-M1-*`; jangan menghapus data asli.
4. **Test Plan**: tunjukkan sumber kebutuhan awal README, LOCAL-SETUP dan source. Jelaskan SRS diselesaikan bertahap pada Modul 2; arah/teknik pengujian dan jadwal modul berikutnya sengaja belum ditetapkan sesuai template. Kriteria masuk memerlukan layanan, akun, data uji dan cadangan; kriteria keluar Modul 1 memerlukan dokumen, registrasi, pemeriksaan kesiapan serta demo.
5. **Risiko**: pilih R-04 sebagai contoh. UI menyebut batas 5 MB, tetapi `backend-js/src/utils/uploads.js` menerima semua berkas dan tidak menetapkan batas ukuran. Dampak 4 karena mengganggu konten/penyimpanan; kemungkinan 4 karena indikasi nyata pada kode; prioritas 4 × 4 = 16. Mitigasinya menyepakati aturan berkas, memeriksa respons server dan mencatat incident untuk perbaikan. Ini belum berarti semua skenario eksploitasi telah diuji.
6. **Kesiapan dan penutup demo**: buka source `frontend/src/page/admin/tambah/program.vue`, `backend-js/src/controllers/admin/adminControllers.js`, `backend-js/src/routes/adminRoutes.js` dan `backend-js/src/middlewares/authorization.js`. Jelaskan cabang input/status/otorisasi dan sumber kebutuhan. Tunjukkan baris registrasi, kekurangan yang belum ditutup serta tindak lanjut yang disepakati dengan asisten.

## Jawaban yang perlu dipahami

- **QA dan QC**: QA menyiapkan proses pencegahan kesalahan, misalnya Test Plan dan risk register. QC memeriksa produk, membandingkan hasil aktual dengan harapan dan melaporkan incident pada modul selanjutnya.
- **STLC dan SDLC**: analisis kebutuhan dan perencanaan pengujian dimulai saat kebutuhan/desain dibuat. Pengembangan berjalan bersama persiapan pengujian; setelah implementasi, pengujian menghasilkan umpan balik untuk perbaikan dan pengujian ulang.
- **Test basis**: README, catatan fitur dan perilaku yang disepakati. Contoh test condition: admin dapat mengubah status pesan menjadi nilai yang diizinkan. Test case kemudian memberikan input, langkah dan expected result konkret; belum menjadi luaran wajib Modul 1.
- **Risk produk dan proyek**: validasi unggahan adalah risiko produk. Layanan lokal mati atau registrasi duplikat adalah risiko proyek. Mitigasi harus menarget penyebab atau dampak masing-masing.
- **Retest dan regresi**: retest mengulang kasus gagal setelah perbaikan; regresi memeriksa fitur penting terkait agar perubahan tidak merusak perilaku sebelumnya.
- **Role admin dan izin editor**: backend saat ini mengizinkan admin dan editor pada route admin. Jangan mengklaim seluruh endpoint eksklusif admin. Cocokkan implementasi dengan aturan bisnis yang disetujui.

## Bahan salin ke baris registrasi resmi

Ini bahan persiapan, bukan pengganti spreadsheet laboratorium dan bukan formulir checklist terpisah yang perlu dikumpulkan.

| Bidang | Nilai |
|---|---|
| Nama | Rusdany Maestro |
| NIM | 202210370311406 |
| Kelas | C |
| Produk | Sustainova |
| Platform | Web |
| Role | Admin |
| Repository | https://github.com/rusdany33/Sustainova.git |
| Demo lokal | http://localhost:5173 |
| Teknologi | Vue 3, Vite 6, Bootstrap 5, Node.js, Express 5, MySQL, JWT, bcrypt |
| Fitur autentikasi | Login; Register publik; Forgot Password/reset akun admin |
| Fitur tambahan | Dashboard; tambah program; daftar/ubah program; hapus program; tambah berita; daftar/ubah berita; hapus berita; kelola pesan |
| Sumber kebutuhan awal | README.md; LOCAL-SETUP.md; UI dan source route/controller admin; aturan bisnis dikonfirmasi asisten |

Jangan menyalin semua status menjadi TRUE tanpa memeriksa bukti. Isi TRUE/FALSE pada 13 kolom resmi berikut.

| Kode | Dasar untuk mengisi status | Yang masih perlu dipastikan |
|---|---|---|
| PRJ-1 | Source tersedia dan panduan struktur disiapkan | Anda harus mampu menjelaskan pengembangan atau pemahaman proyek secara langsung. |
| PRJ-2 | Health API database connected; frontend HTTP 200; 53 pemeriksaan API lulus pada 5 Oktober 2026 | Jalankan kembali sebelum demo; pastikan UI dan Mailpit dapat ditunjukkan. |
| PRJ-3 | CRUD program/berita dan status pesan memberi interaksi serta hasil tersimpan | Tunjukkan hasil aktual pada demo. |
| ROL-1 | Admin dipilih pada semua bagian Test Plan | Pertahankan sampai UAP. |
| FTR-1 | 11 fitur dicantumkan pada bagian 1.2 | Konfirmasi penerimaan cakupan autentikasi publik oleh asisten. |
| FTR-2 | Source login, register, forgotPass dan reset-password tersedia | Peragakan reset dengan Mailpit pada akun admin sementara. |
| FTR-3 | 8 tambahan memiliki fungsi dan contoh hasil yang jelas | Tunjukkan alur yang dipilih dan jangan menghitung route publikasi admin yang belum ada. |
| UNQ-1 | Produk dipilih pada platform Web | UNQ-1 tercatat TRUE pada tab C baris 20. Role berbeda pada Web bukan produk berbeda. |
| RDY-3 | Peserta angka, teks, email, tanggal dan validasi UI tersedia | Pastikan aturan kebutuhan dapat dijelaskan; detail teknik belum ditetapkan dalam Test Plan Modul 1. |
| RDY-4 | Source route, controller, middleware dan Vue tersedia | Tunjukkan source nyata dan pahami percabangan. |
| RDY-5 | `backend-js/tests/integration.js` sudah dapat menjalankan alur API otomatis | Otomasi UI dan pilihan teknik modul selanjutnya belum ditetapkan. |
| RDY-6 | CRUD program/berita dan status pesan tersedia | Gunakan data sementara serta bukti persistensi. |
| REQ-1 | README, LOCAL-SETUP, UI dan source telah diidentifikasi sebagai kebutuhan awal | Konfirmasi perilaku bisnis; SRS belum wajib selesai Modul 1. |

## Pemeriksaan operasional sebelum 7 Oktober

1. Aktifkan MySQL Laragon dan jalankan `JALANKAN.cmd`; periksa API health dan UI.
2. Aktifkan Mailpit, verifikasi migration password-reset dan sediakan akun admin sementara. Skrip reset umum sudah lulus 19 pemeriksaan; demo reset melalui UI dengan akun admin tetap perlu dilakukan.
3. Cadangkan database dan folder unggahan. Siapkan program/berita/pesan sementara untuk demonstrasi.
4. Lengkapi informasi praktikan yang masih diperlukan pada baris 20; UNQ-1 sudah TRUE. Registrasi ditemukan pada tab C baris 20. Proyek sudah disetujui asisten berdasarkan konfirmasi praktikan; kolom status/pemeriksa pada spreadsheet masih kosong.
5. Review tanggal, versi browser/runtime dan status dokumen. Ubah menjadi Final setelah review/registrasi dan revisi yang diperlukan selesai; tambah riwayat revisi jika isinya berubah.

## Catatan verifikasi awal

Pada 5 Oktober 2026, `GET /api/health` merespons status ok dan database connected, frontend lokal merespons HTTP 200, dan `node tests/integration.js` menghasilkan `PASS: 53 API checks`. Skrip mencakup login, registrasi, akses terlarang, CRUD program/berita serta alur proyek lainnya, menggunakan data unik dan cleanup. Hasil ini merupakan pemeriksaan awal kesiapan API, bukan laporan bahwa semua fitur admin, seluruh validasi UI atau alur reset password sudah lulus. Baseline repository: commit `9adad2b`; perubahan lokal `frontend/index.html` sudah ada sebelum tugas ini dan tidak diubah.

`node tests/password-reset.js` juga menghasilkan `PASS: 19 password reset checks, SMTP delivery, expiry, replay, race, password change and session invalidation.` Skrip menggunakan akun sementara berperan user dan membersihkannya, sehingga hasil ini memverifikasi layanan reset umum, belum menggantikan demo UI reset akun admin. Log awal memuat peringatan koneksi timeout; pemeriksaan database berikutnya dan seluruh assertion skrip berhasil. Jangan menyatakan keseluruhan aplikasi bebas defect dari hasil dua skrip ini.
