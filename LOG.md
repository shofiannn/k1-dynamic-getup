# Log proyek K1 Dynamic Getting Up

## Fase B (selesai 10 Nov)
- Pose berdiri target: h = 0,5 rad (pinggul -28,6 deg, lutut 57,3 deg, pergelangan -28,6 deg)
- Tinggi jatuh pose target: 0,55 m (jatuh dari 0,8 m membuat robot roboh)
- Tinggi berdiri H = 0,494 m
- reward_check: target 0,9-1,0 | prone 0,15-0,25 | supine 0,25 | tanda tilt +90
- Data awal: prone ~1745, supine ~1285 (uji: 349 dan 257)
- JAX: CPU di training uji pertama (fps rata-rata 43), GPU aktif sesudah pasang jax[cuda12]
- fps GPU (sesudah belajar mulai, hitung dari selisih tabel): sekitar 20; rata-rata di tabel (75-83) menyesatkan karena termasuk fase acak

## Fase A (selesai, dicatat 10 Nov)
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
