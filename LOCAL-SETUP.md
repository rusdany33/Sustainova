# Menjalankan Sustainova di Laragon

Untuk pertama kali setelah clone dari GitHub, jalankan `npm install` di folder `backend-js` dan `frontend`. Salin `backend-js/.env.example` menjadi `backend-js/.env`, isi `JWT_SECRET` dengan nilai acak, dan sesuaikan konfigurasi database. Buat database `sustainova` lalu impor `db/sustainovata_db.sql` ke database kosong tersebut.

1. Aktifkan MySQL dengan **Start All** di Laragon.
2. Klik dua kali `JALANKAN.cmd`, atau jalankan `powershell -ExecutionPolicy Bypass -File .\start-local.ps1` dari folder proyek.
3. Website tersedia di http://localhost:5173. Backend tersedia di http://localhost:3000/api/health.

Database lokal: `sustainova`, host `127.0.0.1`, port `3306`, username `root`, password kosong. Konfigurasi dibaca dari `backend-js/.env`.

Akun bawaan SQL: `admin@test.com`, `editor@test.com`, dan `author@test.com`. Password ketiganya: `password123`.

Database sudah diimpor. Jangan impor ulang ke database yang sudah berisi tabel. Untuk instalasi baru dengan database kosong, impor `db/sustainovata_db.sql` setelah memilih database tujuan.

Log server tersedia di folder `logs`. Setelah mengubah kode backend, restart proses backend agar perubahan dimuat.

Verifikasi dari folder `backend-js`:

```powershell
npm run test-db
npm run test:integration
```

Tes integrasi membutuhkan backend aktif dan akun bawaan di atas. Tes membuat data sementara dengan nama unik lalu membersihkannya.

Verifikasi frontend dari folder `frontend`: `npm run build`.

## Lupa password

Jalankan `npm run migrate:password-reset` dari folder `backend-js` untuk database lama. Import SQL utama yang baru sudah mencakup tabel reset dan versi sesi.

Untuk Laragon, aktifkan Mailpit (SMTP `127.0.0.1:1025`, kotak masuk http://localhost:8025). Salin `frontend/.env.example` menjadi `frontend/.env.local` untuk menampilkan petunjuk kotak email lokal. Buka halaman lupa password, masukkan email akun, buka email di Mailpit, lalu gunakan tautannya untuk menyimpan password baru. Email lokal tidak diteruskan ke Gmail/Outlook.

Tautan berlaku 30 menit, sekali pakai. Password baru minimal 8 karakter; setelah reset semua sesi lama akun berakhir. Pengiriman ulang dibatasi 60 detik per akun dan endpoint reset dibatasi 20 percobaan per IP dalam 15 menit.

Untuk pengiriman ke email publik, isi `SMTP_HOST`, `SMTP_PORT`, `SMTP_SECURE`, `SMTP_USER`, `SMTP_PASSWORD`, dan `MAIL_FROM` dengan konfigurasi penyedia email. Isi `FRONTEND_URL` dengan alamat website HTTPS. Jangan commit `.env`. Konfigurasi transport mengacu pada [dokumentasi Nodemailer](https://nodemailer.com/smtp), dan alur token mengikuti [panduan OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html).

Tes lengkap reset melalui Mailpit: `npm run test:password-reset` dari folder backend. Tes menggunakan akun sementara dan menghapus akun serta email tes sesudah selesai.
