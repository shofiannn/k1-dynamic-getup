# Log proyek K1 Dynamic Getting Up

## Jadwal
| Fase | Jadwal | Isi | Status |
| --- | --- | --- | --- |
| A | Sabtu 31 Okt - Senin 2 Nov | setup dan baseline FRASA | selesai |
| B | Kamis 5 Nov - Minggu 8 Nov | model K1, pose berdiri, posisi awal, reward, training uji | selesai |
| C | Senin 9 Nov - Minggu 15 Nov | training, kurikulum, dua postur | berjalan |
| D | Senin 16 Nov - Kamis 19 Nov | evaluasi dan analisis kegagalan | belum dimulai |
| E | Jumat 20 Nov - Selasa 24 Nov | video demo, README, laporan, pengumpulan | belum dimulai |

## Fase A: setup dan baseline FRASA (Sabtu 31 Okt - Senin 2 Nov)
- Sistem: Ubuntu 24.04.5 LTS, Python 3.12.3
- Laptop: Thin A15 B7UCX, GPU RTX 2050 4 GB, driver 595.99.02
- Lingkungan Python: ~/venv-getup
- Versi: mujoco 3.17.0, jax 0.12.0.1, sbx 0.28.0, rl_zoo3 2.9.2, gymnasium 1.0.0
- FRASA asli (Rhoban, MIT License) di-clone ke ~/getup-project/frasa_original; dipakai sebagai dasar k1_env
- Uji FRASA asli: test_env.py (robot Sigmaban jatuh), standup_generate_initial.py, training uji 120.000 langkah, enjoy_sbx.py
- Masalah yang ditemui dan solusinya:
  - mj_contactForce TypeError: np.argwhere diganti np.flatnonzero dan id dibungkus int() (sudah masuk tools/make_k1_env.py)
  - ModuleNotFoundError requests di enjoy_sbx.py: pip install requests
  - Error BadPixmap saat membuka viewer: jalankan dengan LIBGL_ALWAYS_SOFTWARE=1; untuk video pakai MUJOCO_GL=egl
- Repo GitHub: k1-dynamic-getup (akun shofiannn); login lewat gh auth login (token lama ditolak, diganti)
- JAX awalnya CPU saja; GPU aktif sesudah pip install -U "jax[cuda12]"

## Fase B: model K1, pose berdiri, posisi awal, reward, training uji (Kamis 5 Nov - Minggu 8 Nov)
- Pose berdiri target: h = 0,5 rad (pinggul -28,6 deg, lutut 57,3 deg, pergelangan -28,6 deg)
- Tinggi jatuh pose target: 0,55 m (jatuh dari 0,8 m membuat robot roboh)
- Tinggi berdiri H = 0,494 m
- reward_check: target 0,9-1,0 | prone 0,15-0,25 | supine 0,25 | tanda tilt +90
- Data awal: prone ~1745, supine ~1285 (uji: 349 dan 257)
- JAX: CPU di training uji pertama (fps rata-rata 43), GPU aktif sesudah pasang jax[cuda12]
- fps GPU (sesudah belajar mulai, hitung dari selisih tabel): sekitar 20; rata-rata di tabel (75-83) menyesatkan karena termasuk fase acak

## Fase C: training, kurikulum, dua postur (Senin 9 Nov - Minggu 15 Nov)
- (belum ada catatan)

## Fase D: evaluasi dan analisis kegagalan (Senin 16 Nov - Kamis 19 Nov)
- (belum ada catatan)

## Fase E: video demo, README, laporan, pengumpulan (Jumat 20 Nov - Selasa 24 Nov)
- (belum ada catatan)
- 19 Nov: reset pose target (use_cache=False) goyah: berdiri 19/30 pada tinggi lepas 0,55 m dan 10/30 pada 0,50 m. Tidak berdampak pada training/evaluasi karena keduanya memakai posisi awal dari berkas (cache). Dipertahankan 0,55 m.

## C9-C11: evaluasi A1 seed 0 (19 Nov)
- C9: prone 0/30, supine 0/30 (dev, H=0.494).
- C11: kedua posisi kategori C (terjebak): robot naik ke duduk tegak <1 detik lalu diam. Hipotesis: optimum lokal akibat bonus tinggi/ketegakan A1 (belum dibuktikan; bandingkan dengan A0).
rantai dimulai: Thu Nov 19 07:55:19 PM WIB 2026
run panjang A1 (6M langkah, seed 0) dimulai: Fri Nov 20 07:52:11 AM WIB 2026
A0 dev: prone 0/30, supine 0/30 (1M langkah, H=0.494)
C2 (kurikulum posisi mudah, 1.2M langkah, ramp 800k, seed 0) dimulai: Fri Nov 20 01:07:16 PM WIB 2026. a1_long 6M: prone 0/30, supine 0/30 (best dan final)
C2 dev: 0/30 dan 0/30; diagnosis: z_maks 0.12-0.16 m (ambang 0.42), bahkan dari posisi mudah. C3 (height_bonus=1.5, upright_bonus=0, 1.2M) dimulai: Fri Nov 20 03:39:18 PM WIB 2026
C3 (height 1.5, upright 0, 1.2M): z_maks supine 0.47-0.48 tapi tilt -57..-67; prone z 0.26 tilt 129 (tinggi tanpa tegak). C4 (height 1.0, upright 1.0, 2M) dimulai: Fri Nov 20 10:50:36 PM WIB 2026

## Evaluasi final D3 (22 Nov)
- 100 posisi uji per postur (data uji dari indeks 30), H=0.494, model akhir tiap run.
- final_s0, final_s1, final_s2 (A1, 1M), a0_s0 (A0, 1M), a1_long_6M, c2_s0 (kurikulum posisi mudah), c3_s0 (height 1.5), c4_s0 (height 1.0 + upright 1.0): semuanya 0/100 prone dan 0/100 supine (CI95 0.0-3.7%).
- Diagnosis: robot belajar duduk tegak (z_maks 0.12-0.17 m, ambang berdiri 0.42 m). C3 menaikkan z sampai 0.47 m pada supine tetapi dengan tubuh miring (tilt -57 sampai -67 derajat).
C5 (height 1.0, upright 2.0 digating tinggi, posisi mudah, 2M) dimulai: Sun Nov 22 12:49:53 AM WIB 2026
C5 seed 0 dev: ketat 0/30; final longgar (tilt<45): prone 93/100, supine 77/100. Rantai C5 seed 1 dan 2 dimulai: Sun Nov 22 01:08:39 PM WIB 2026
