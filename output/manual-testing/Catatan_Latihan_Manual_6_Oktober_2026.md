# Catatan latihan manual Sustainova Admin

Tanggal 6 Oktober 2026. Lingkungan localhost:5173, backend localhost:3000. Tujuan: latihan observasi sebelum demo Modul 1, bukan laporan seluruh aplikasi lolos.

| ID | Langkah dan input | Harapan | Hasil aktual | Kesimpulan |
|---|---|---|---|---|
| M-01 | Login admin@test.com dengan password Salah123! | Akses ditolak | Alert Login gagal: Password salah; tetap pada login | Lolos untuk percobaan ini |
| M-02 | Login admin@test.com dengan password123, buka menu akun lalu Dashboard Admin | Akun admin dapat membuka dashboard | Login menuju beranda; menu menampilkan ADMIN dan dashboard dapat dibuka | Akses dashboard berhasil; angka ringkasan belum diverifikasi |
| M-03 | Buka Tambah Program, nama kosong, klik Simpan Program | Form tidak disimpan | Tetap pada form; fokus pada Nama Program | Validasi kosong terlihat; tidak membuktikan seluruh validasi server |
| M-04 | Nama PKPL-M1-LATIHAN-20261006; deskripsi Data sementara untuk latihan manual Rusdany.; status Aktif; peserta 10; mulai 2026-10-06; selesai 2026-10-07; poster kosong; klik Simpan Program | Jika poster opsional menurut kebutuhan, penyimpanan berhasil dan data muncul | Alert Terjadi kesalahan saat menyimpan program; tetap pada form. Console Error submitting form: AxiosError | Incident perlu ditelusuri; penyebab dan apakah terjadi perubahan database belum diverifikasi |

UI menampilkan angka dashboard 0, daftar program/berita kosong, dan pesan kosong pada sesi latihan ini. Jangan menyimpulkan database pasti kosong tanpa pemeriksaan lebih lanjut. Backend health merespons status ok dan database connected. Bukti API lulus tanggal sebelumnya tidak menggantikan hasil UI hari ini.

Screenshot alert JavaScript tidak dapat diambil oleh fasilitas screenshot browser yang tersedia. Pesan alert dicatat dari accessibility state. Screenshot 07 menunjukkan form setelah alert ditutup, bukan gambar alert itu sendiri.

Pengujian ubah dan hapus belum dilakukan karena penyimpanan gagal. Semua operasi berikut harus memakai data latihan yang dapat dikenali, bukan data asli. Jangan menulis Lolos untuk langkah yang belum dijalankan.

## Format catatan setiap percobaan

ID; fitur; kondisi awal; input; langkah; hasil yang diharapkan; hasil aktual; status Lolos/Gagal/Belum diuji/Perlu konfirmasi; bukti; tindak lanjut.

## Urutan latihan berikutnya

1. Ulangi login salah dan benar.
2. Buka dashboard, daftar program, daftar berita, pesan; catat apakah berhasil memuat data.
3. Coba nama program kosong dan peserta -1; amati penolakan form.
4. Coba simpan program dengan data normal seperti M-04; tambahkan poster kecil bila aturan yang disepakati mewajibkannya. Jika gagal, catat dan hentikan alur ubah/hapus; jangan mengarang keberhasilan.
5. Setelah data benar-benar tersedia, refresh daftar; ubah nama, peserta dan status; refresh lagi; bandingkan hasil dengan input.
6. Pada data latihan saja, coba hapus lalu pilih Batal; pastikan data masih ada. Kemudian hapus data latihan bila Anda memang ingin menghapusnya; pastikan data lain tidak terpengaruh.
7. Ulangi pola kosong/normal/ubah/hapus pada berita.
8. Siapkan satu pesan kontak dummy melalui halaman kontak. Buka sebagai admin, perhatikan perubahan new/read/replied dan hasil setelah refresh. Tidak perlu benar-benar mengirim balasan email kepada orang lain.
9. Register melalui halaman publik dengan identitas dummy dan email unik example.test; periksa duplikat dan konfirmasi password berbeda. Akun hasil registrasi adalah user, bukan admin.
10. Forgot Password dengan email akun uji; periksa kotak email Mailpit. Jika ingin mengganti password, lakukan sendiri pada akun sementara dan selesaikan login ulang. Jangan mengganti password admin seed untuk latihan ini.

## Hubungan hasil dengan risk register

Risiko adalah kemungkinan masalah yang direncanakan. Incident adalah kejadian yang ditemukan. M-04 merupakan incident penyimpanan yang perlu ditelusuri; tidak otomatis membuktikan risiko tanggal, unggahan atau otorisasi. Nilai dampak/kemungkinan dalam risk register adalah estimasi yang harus dijelaskan, bukan jumlah tes gagal.
