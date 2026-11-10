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
