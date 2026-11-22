# K1 Dynamic Getting Up

Proyek akhir: melatih kebijakan RL agar robot humanoid Booster K1 (simulator MuJoCo) bangun dari jatuh tengkurap (prone) dan telentang (supine). Pendekatan: adaptasi pipeline FRASA (Rhoban, MIT) untuk K1, dilatih dengan CrossQ, ditambah bonus reward padat, bonus tegak dengan gerbang tinggi, dan kurikulum posisi awal.

## Hasil singkat

- Konfigurasi reward **C5** menghasilkan kebijakan yang berdiri pada **satu dari tiga seed**: seed 2 berhasil **88/100 (prone, median 2,65 s)** dan **95/100 (supine, median 1,45 s)** pada 100 posisi uji final per postur (ukuran ketat).
- Seed 0 naik ke jongkok dalam yang stabil (0/100 ketat; 93/100 dan 77/100 pada ukuran longgar). Seed 1 hampir gagal total (1/100 dan 0/100).
- Semua konfigurasi lain (A0, A1 selama 1 dan 6 juta langkah, C2 sampai C4) 0/100.
- **Variasi antar seed sangat besar**; rata-rata tiga seed pada ukuran ketat sekitar 30% per postur.
- Posisi akhir seed 2 adalah berdiri dengan badan tegak dan lutut masih agak tertekuk, bukan kaki lurus penuh.

Prototipe kebijakan: `models/c5_s2.zip`. Demo: `docs/demo_final.mp4` (keberhasilan dan kasus gagal).

## Protokol evaluasi

Posisi awal uji tidak pernah dilihat saat training. Data "dev" (30 posisi pertama per postur) untuk keputusan selama percobaan; evaluasi final 100 posisi berikutnya per postur (indeks 30 sampai 129).

- **Ukuran ketat (utama):** kemiringan badan dalam 20 derajat dari tegak, tinggi badan di atas 0,85 x 0,494 m = 0,42 m, norma kecepatan sendi di bawah 1 rad/s, dipertahankan 1 detik.
- **Ukuran longgar (dilaporkan terpisah):** sama, tetapi kemiringan di bawah 45 derajat. Ambang ini dipilih setelah melihat hasil C5 (post hoc) dan bukan ukuran berdiri penuh.
- Waktu bangun adalah median detik dari awal episode sampai ukuran terpenuhi 1 detik penuh.

## Tabel hasil (final, 100 posisi per postur)

| Run | Konfigurasi | Langkah | Prone (ketat) | Supine (ketat) |
| --- | --- | --- | --- | --- |
| A0 | reward dasar FRASA | 1 juta | 0/100 | 0/100 |
| A1 (3 seed) | A0 + bonus tinggi 0,3 + bonus tegak 0,3 | 1 juta | 0/300 | 0/300 |
| A1 panjang | seperti A1, seed 0 | 6 juta | 0/100 | 0/100 |
| C2 | A1 + kurikulum posisi mudah | 1,2 juta | 0/100 | 0/100 |
| C3 | bonus tinggi 1,5 saja + posisi mudah | 1,2 juta | 0/100 | 0/100 |
| C4 | bonus tinggi 1,0 + bonus tegak 1,0 + posisi mudah | 2 juta | 0/100 | 0/100 |
| C5 seed 0 / 1 / 2 | bonus tinggi 1,0 + bonus tegak 2,0 digerbang tinggi + posisi mudah | 2 juta | 0 / 1 / 88 dari 100 | 0 / 0 / 95 dari 100 |

Ukuran longgar C5: seed 0 prone 93/100 (2,40 s), supine 77/100 (1,45 s); seed 1 1/100 dan 0/100; seed 2 sama dengan ukuran ketat. Pada data dev, seed 2: ketat 25/30 (prone) dan 28/30 (supine), konsisten dengan hasil final. Rincian: `results/final_table.txt`, `results/relaxed_table.txt`, `results/relaxed_dev_c5.txt`, `results/summary.md`.

## Temuan diagnosis

- A0, A1, A1 panjang, C2, dan C4 berakhir di posisi duduk tegak (tinggi badan maksimum 0,12 sampai 0,17 m): duduk tegak sudah memberi sebagian besar bonus tegak (optimum lokal). Menambah langkah sampai 6 juta tidak mengubah perilaku.
- C3 (bonus tinggi saja) mengejar tinggi tanpa tegak (reward hacking): jongkok membungkuk berulang pada supine, huruf V terbalik pada prone.
- C5 mengalikan bonus tegak dengan fraksi tinggi, sehingga bonus besar hanya saat badan sudah tinggi; ini membuka jalan ke berdiri, tetapi hasilnya sangat bergantung pada seed (penyebabnya belum diuji).
- Kurikulum posisi awal "mudah" kami ternyata rendah (tinggi awal sekitar 0,12 m), jadi manfaatnya sendiri belum terbukti.

## Catatan kontrol (dari kode)

- Lima sendi sagital dikendalikan: siku, bahu, pinggul, lutut, pergelangan kaki (pitch); perintah sisi kiri dicerminkan ke kanan. Sendi roll dan yaw tidak dikendalikan.
- Mode kontrol kecepatan sendi, batas 2 pi rad/detik, langkah 0,05 detik (perubahan maksimum 0,314 rad per langkah).
- Parameter motor (kp = batas torsi / 0,5, kv = 0,05 kp) adalah perkiraan, bukan data pabrikan.

## Isi repo

- `k1_env/`: environment MuJoCo K1 (diadaptasi dari FRASA) dengan opsi reward Fase C.
- `tools/`: pembuat model dan environment K1, patch Fase C (`patch_phase_c.py`) dan opsi `upright_gate` (`patch_gate.py`).
- `scripts/`: `evaluate.py`, `eval_relaxed.py` (dua ukuran), `record.py`, `analyze_results.py`, `diag_rollout.py`, `diag_easy.py`, `make_demo.py`, `make_run_config.py`, `make_easy_pool.py`.
- `hyperparams/`: konfigurasi training (a0, a1, c2 sampai c5).
- `models/`: checkpoint (`c5_s0`, `c5_s1`, `c5_s2`, `final_s0`, `c3_s0`).
- `docs/`: video dan catatan. `LOG.md`: catatan kerja bertanggal.

## Mengulang percobaan (C5)

Dari folder repo, dengan venv aktif:

    python scripts/make_easy_pool.py 0.494
    python scripts/make_run_config.py c5 --fast height_bonus=1.0 upright_bonus=2.0 upright_gate=true target_height=0.494 easy_start_steps=1200000 easy_start_frac=0.5
    python train_sbx.py --algo crossq --env k1-standup-v0 --conf hyperparams/c5.yml -f logs/c5_s2 -n 2000000 --seed 2
    python scripts/eval_relaxed.py models/c5_s2.zip 45 100 30
    MUJOCO_GL=egl python scripts/record.py models/c5_s2.zip prone 30 90 docs/klip.mp4

Satu run 2 juta langkah memakan sekitar 100 menit di laptop (RTX 2050 4 GB, simulasi di CPU).

## Keterbatasan

- Hanya simulasi; tidak ada uji di robot nyata atau uji ketahanan (gesekan, massa).
- Tiga seed untuk C5 dan satu seed untuk konfigurasi lain; variasi antar seed besar.
- C5 dipilih setelah beberapa percobaan reward (risiko seleksi), meski dievaluasi pada posisi uji terpisah dari data training.
- Ambang ukuran longgar dipilih setelah melihat hasil.
- Kurikulum dua tahap seperti HumanUP tidak diimplementasikan.

## Rujukan

- FRASA (Gaspard dkk., 2024), arXiv:2410.08655, https://github.com/Rhoban/frasa
- HumanUP (He dkk., 2025), arXiv:2502.12152
- Booster Gym (Wang dkk., 2025), arXiv:2506.15132
- CrossQ (Bhatt dkk., ICLR 2024)
