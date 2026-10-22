# Panduan demo LAB SESSION Modul 2 Sustainova Admin

Rusdany Maestro | 202210370311406 | Kelas C | 15 Oktober 2026

## Dokumen yang digunakan

- Test Plan revisi v1.2 menetapkan delapan fitur utama dan risiko. Susunan mengikuti menu: Login, Register, Forgot Password, Dashboard, Kelola Berita, Kelola Program, Pesan, Profil.
- SRD_Sustainova_Admin_Modul_2.md memuat 27 kebutuhan ber-ID, sumber setiap kebutuhan, dan perbedaan aturan yang perlu diperhatikan. Dokumen ini dikonsolidasikan untuk Modul 2; bukan klaim adanya SRS terpisah yang sudah disetujui sebelumnya.
- TDS/TTM LAB mengisi template sampai Bagian 5: Requirements, Feature Sets, Test Conditions, Coverage Items, dan Test Traceability Matrix. Bagian 6 teknik tidak diisi sesuai batas modul.

## Arti hubungan yang perlu dipahami

Requirement menjelaskan perilaku yang harus disediakan. Feature Set mengelompokkan kebutuhan yang berkaitan. Test Condition menyatakan keadaan/aspek yang perlu diperiksa. Coverage Item menentukan bagian/properti yang dicakup. TTM mencatat hubungan ID semuanya agar tidak ada kebutuhan yang terlewat dan perubahan dapat ditelusuri.

Contoh utama adalah search/filter berita:

| Elemen | ID dan penjelasan |
|---|---|
| Requirement | RQ-015: pencarian sebagian teks dengan normalisasi kapital/spasi tepi, reset dan jumlah hasil. |
| Feature Set | FS-005: Kelola Berita. Search/filter bukan fitur utama kesembilan. |
| Test Condition | TCond-029: kata kunci cocok dan normalisasi; TCond-030: tidak cocok/kosong/reset; TCond-031: jumlah hasil dan baris yang sedang diedit. |
| Coverage Item | CI-015: kata kunci, normalisasi, jumlah hasil dan reset berita. |
| TTM | Tiga baris RQ-015 menautkan FS-005 ke tiga kondisi tersebut dan CI-015. |

Contoh lain: RQ-020 -> FS-006 -> TCond-041/TCond-042/TCond-043 -> CI-020 untuk search/filter program. RQ-024 -> FS-007 -> TCond-049/TCond-050 -> CI-024 untuk pesan. RQ-026 -> FS-008 -> TCond-052/TCond-053 -> CI-026 untuk perubahan profil.

## Urutan presentasi

1. Perkenalkan aplikasi Web Sustainova dan role Admin. Register merupakan jalur publik wajib yang membuat akun user; role utama pengujian tidak berubah.
2. Tunjukkan Test Plan revisi menu. Jelaskan 3 autentikasi + 5 menu = 8 fitur utama. CRUD, status, unggahan dan search/filter menjadi subfitur.
3. Buka SRD. Pilih RQ-015 dan tunjukkan sumber aturan pencarian pada kode serta arahan fitur aslab yang disampaikan praktikan.
4. Buka Bagian 1 TDS untuk melihat requirement yang sama. Lanjutkan ke FS-005 pada Bagian 2.
5. Tunjukkan tiga kondisi terkait pada Bagian 3. Jelaskan kondisi adalah aspek pengujian, belum langkah/input konkret test case.
6. Tunjukkan CI-015 pada Bagian 4. Bedakan objek cakupan dari uraian kondisi.
7. Tunjukkan tiga hubungan RQ-015 pada Bagian 5 TTM. Baca ID dua arah: dari kebutuhan ke kondisi, atau dari kondisi kembali ke sumber kebutuhannya.
8. Jelaskan prioritas: High untuk akses, akun, validasi penting, persistensi/hapus; Medium untuk pencarian, daftar dan ringkasan. Tidak perlu memaksa semua kondisi menjadi High.
9. Tunjukkan ringkasan 27 RQ, 8 FS, 54 TCond, 27 CI dan 54 hubungan TTM. Semua kebutuhan yang dipilih memiliki hubungan; ini bukan bukti semua pengujian sudah dieksekusi atau lolos.
10. Jelaskan bahwa jika aturan berubah, RQ, kondisi, CI, dan hubungan TTM yang terdampak diperbarui bersama.

## Letak source saat aslab meminta

| Aspek | File dan fungsi yang dicari |
|---|---|
| Search berita | frontend/src/page/admin/kelola/berita.vue: query dan filteredItems |
| Search program | frontend/src/page/admin/kelola/program.vue: query dan filteredItems |
| Search pesan | frontend/src/page/admin/kelola/messages.vue: query dan filteredItems |
| Reset pencarian dan jumlah hasil | frontend/src/components/admin/SearchToolbar.vue |
| Rute dan guard | frontend/src/router/index.js: router.beforeEach |
| Profil | frontend/src/page/profile.vue: updateProfile; backend-js/src/controllers/client/clientControllers.js: updateUserProfile |
| CRUD berita/program | backend-js/src/controllers/admin/tambahControllers.js dan adminControllers.js |
| Status pesan | backend-js/src/controllers/admin/adminControllers.js: updateMessageStatus |

Tekan Ctrl+P pada editor untuk membuka nama file, lalu Ctrl+F untuk mencari fungsi. Search/filter saat ini berjalan pada daftar yang dimuat frontend, bukan endpoint search khusus. Baris program/berita aktif edit sengaja tetap terlihat saat pencarian.

## Hal yang harus dijelaskan dengan tepat

- Test Plan dan SRD memiliki fungsi berbeda. Test Plan mengatur lingkup/rencana; SRD mencatat kebutuhan sebagai test basis.
- Filter yang didesain adalah penyaringan kata kunci, bukan dropdown filter baru.
- Profil mengelola akun sendiri; bukan pengelolaan semua akun pengguna.
- Pesan replied adalah status, bukan bukti bahwa email telah dikirim.
- Poster program wajib menurut controller. Kegagalan simpan tanpa poster pada latihan sebelumnya tidak boleh langsung disimpulkan sebagai bug database.
- Backend unggahan belum setara dengan pembatasan UI. Daftar status program pada tambah/edit juga berbeda. Kondisi desain memeriksa perilaku; bukan klaim seluruh implementasi sudah benar.
- Persetujuan proyek dan checklist spreadsheet yang pernah dibaca tidak otomatis berarti dokumen kebutuhan/TDS ini telah dinilai. Jangan mengarang tanggal atau nama pemeriksa.

## Pemetaan rubrik

| Komponen | Bobot | Bukti |
|---|---:|---|
| TDS | 35% | Bagian 1-4; kebutuhan jelas, delapan FS, kondisi dan prioritas sesuai cakupan. |
| TTM | 30% | Bagian 5; seluruh RQ/FS/TCond/CI terhubung tanpa ID yatim. |
| Dokumentasi | 15% | Template laboratorium dipakai sampai Bagian 5; ID dan nama konsisten. |
| Demo dan penjelasan | 20% | Latihan penelusuran di atas dijelaskan dengan kata sendiri. |

Dokumen membantu memenuhi kriteria; hasil penilaian tetap bergantung pada review aslab dan pemahaman saat demo.
