# MOLOKU — Next.js lokal

Website kebudayaan Maluku Utara dengan Next.js App Router dan React. Versi statis awal tetap tersedia di `dist/` sebagai arsip. Pengembangan aktif ada di `app/`, `components/`, dan `lib/`.

## Menjalankan

```powershell
cd D:\skripsi\kebudayaan\moloku
npm install
npm run dev
```

Buka http://localhost:3000. Untuk produksi lokal: `npm run build`, lalu `npm start`. Tes data dan filter: `npm test`.

## Halaman & fitur

- `/`: cerita pembuka, latar foto mengikuti scroll, progres membaca, koleksi pilihan.
- `/jelajahi`: pencarian teks, filter kategori/wilayah, urutan A–Z, reset, filter tersimpan di URL.
- `/budaya/[slug]`: detail cerita, rujukan, rekomendasi terkait, favorit, catatan pribadi, salin tautan, cetak.
- `/galeri`: foto dengan lightbox, tombol sebelumnya/selanjutnya, navigasi keyboard, konteks dan kredit.
- `/favorit`: cerita yang disimpan di browser dengan pencarian/filter.
- `/kuis`: lima pertanyaan bertahap, umpan balik, hasil, pembahasan, skor terbaik dan main ulang.
- `/tentang`: tujuan, sumber, kredit, penjelasan penyimpanan lokal.
- Halaman 404 untuk alamat yang tidak ditemukan.

Favorit, catatan, dan skor menggunakan localStorage. Tidak ada login, database, atau sinkronisasi lintas perangkat. Sumber konten di `lib/data.mjs`; foto dan kredit di `public/assets/`. Latar bergerak menggunakan 12 frame ilustrasi AI pesisir (bukan dokumentasi budaya), disimpan dalam atlas 3 × 4 di public/assets/culture-sequence/atlas.png. Prompt dan kredit ada di folder yang sama. Scroll menentukan frame, dengan transisi antarfame dan dukungan reduced motion. Hak foto mengikuti penerbit Indonesia Travel.

Pengerjaan versi ini hanya lokal. Manifest Sites dipertahankan sebagai identitas versi terdahulu; tidak ada publikasi otomatis pada `dev`, `build`, atau `start`.
