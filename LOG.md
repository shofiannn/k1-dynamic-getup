# Log proyek K1 Dynamic Getting Up

## Fase B (selesai 10 Nov)
- Pose berdiri target: h = 0,5 rad (pinggul -28,6 deg, lutut 57,3 deg, pergelangan -28,6 deg)
- Tinggi jatuh pose target: 0,55 m (jatuh dari 0,8 m membuat robot roboh)
- Tinggi berdiri H = 0,494 m
- reward_check: target 0,9-1,0 | prone 0,15-0,25 | supine 0,25 | tanda tilt +90
- Data awal: prone ~1745, supine ~1285 (uji: 349 dan 257)
- JAX: CPU di training uji pertama (fps rata-rata 43), GPU aktif sesudah pasang jax[cuda12]
- fps GPU (sesudah belajar mulai, hitung dari selisih tabel): sekitar 20; rata-rata di tabel (75-83) menyesatkan karena termasuk fase acak
