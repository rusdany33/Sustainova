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
