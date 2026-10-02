# Animasi Pipeline AR (Feature Detection → Tracking → Plane Detection → Object Placement)

Script Python untuk membuat **GIF animasi** yang menjelaskan alur kerja Augmented Reality (AR) secara step-by-step. Dibuat untuk tugas Mini Implementasi, Opsi 2 (Animasi/GIF).

## Output

| Item | Nilai |
|------|-------|
| File | `AR_Pipeline_Animation.gif` |
| Durasi | 14 detik (looping) |
| Resolusi | 800 x 450 px |
| Frame rate | 12 FPS (168 frame) |

## Alur yang Ditampilkan

| Waktu | Tahap | Yang terlihat di animasi |
|-------|-------|--------------------------|
| 0 – 2 dtk | Kamera / dunia nyata | Tampilan kamera "LIVE" berisi ruangan (dinding, bingkai, tanaman, lantai kayu) dan kotak fokus. |
| 2 – 5 dtk | **Feature Detection** | Garis scan menyapu dari kiri ke kanan. Titik kuning muncul di sudut dan tekstur yang dilewati, lengkap dengan penghitung titik. |
| 5 – 8 dtk | **Tracking** | Titik berubah hijau, kamera bergoyang, jejak gerak (motion trail) dan jaring antar titik muncul. |
| 8 – 11 dtk | **Plane Detection** | Titik di lantai ditandai cyan, titik di dinding diredupkan, lalu grid plane melebar dari tengah dan muncul label "Plane terdeteksi". |
| 11 – 14 dtk | **Object Placement** | Efek tap di layar, lalu kubus 3D jatuh dan menempel di plane, lengkap dengan bayangan dan label. |

Komponen animasi sesuai soal: kamera/dunia nyata, titik feature, plane (grid), dan objek 3D.

## Cara Kerja Kode

**1. Render per frame.** Fungsi `render(i)` menggambar satu frame berdasarkan waktu `t = i / FPS`. Tahap yang aktif ditentukan dari list `STAGES`. Semua gambar dibuat di ukuran 2x (supersampling) lalu diperkecil dengan LANCZOS supaya garis dan lingkaran halus (anti-aliasing).

**2. Pemandangan palsu dengan perspektif.** Fungsi `fl(u, v)` mengubah koordinat lantai (`u` = kiri-kanan, `v` = jauh-dekat) menjadi koordinat layar dengan efek perspektif. Fungsi ini dipakai untuk menggambar papan lantai, titik feature di lantai, grid plane, dan posisi objek 3D, sehingga semuanya konsisten.

**3. Feature points.** Ada 34 titik: 12 di dinding (sudut bingkai dan pot) dan 22 di lantai (sambungan papan). Waktu munculnya bergantung pada posisi horizontal titik, jadi titik menyala tepat saat garis scan melewatinya.

**4. Tracking.** Fungsi `amp(t)` dan `off(t)` menghasilkan goyangan kamera (sinus) yang diterapkan ke seluruh scene dan semua titik. Jejak gerak digambar dari posisi titik saat ini ke posisinya 0,45 detik sebelumnya. Jaring hijau menghubungkan tiap titik dengan 2 tetangga terdekat.

**5. Plane detection.** Grid 8 x 6 sel dibuat di atas lantai. Sel muncul berurutan dari pusat (`CU, CV`) ke luar berdasarkan jarak, sehingga terlihat seperti bidang yang "ditemukan" sedikit demi sedikit.

**6. Object placement.** Kubus digambar isometrik lewat fungsi `cube()`. Animasi jatuh dan skala memakai easing `easeOutBack` (sedikit memantul), sedangkan bayangan memakai `easeOutCubic`. Karena objek memakai koordinat lantai yang sama, ia tetap menempel di plane saat kamera bergoyang.

**7. Transisi dan UI.** Flash putih singkat dan teks judul fade-in muncul di awal tiap tahap. Pill progress di atas berubah dari abu-abu (belum) ke biru (aktif) ke hijau centang (selesai). Ada juga bar progress waktu dan chip info di dalam layar kamera.

**8. Export GIF.** Palet warna dibuat dari beberapa frame kunci (maks. 255 warna), lalu dipakai untuk semua frame supaya warna tidak berkedip. Frame disimpan dengan Pillow (`save_all=True`, `loop=0`).

## Pengaturan yang Bisa Diubah

| Yang ingin diubah | Di mana |
|-------------------|---------|
| Durasi / FPS | `DUR`, `FPS` (baris 4) |
| Waktu mulai, judul, dan teks penjelasan tiap tahap | list `STAGES` |
| Label pill progress | list `PILLS` |
| Posisi objek 3D | `CU, CV` |
| Ukuran dan warna kubus | fungsi `cube()` |
| Ukuran grid plane | `U0, U1, V0, V1, NU, NV` |
| Kekuatan goyangan kamera | fungsi `amp(t)` |

## Tools

Python 3 dan [Pillow](https://pypi.org/project/pillow/). Seluruh animasi digambar lewat kode tanpa aset eksternal.
