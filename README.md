# K1 Dynamic Getting Up

Proyek akhir: melatih kebijakan RL agar robot humanoid Booster K1 (simulator MuJoCo) bangun dari jatuh tengkurap (prone) dan telentang (supine). Pendekatan: adaptasi pipeline FRASA (Rhoban, MIT) untuk K1, dilatih dengan CrossQ, ditambah bonus reward padat dan kurikulum posisi awal.

**Hasil jujur: tidak ada kebijakan yang berhasil berdiri (0/100 pada prone dan supine untuk semua model yang diuji).** Repo ini mendokumentasikan percobaan, diagnosis kegagalan, dan cara mengulanginya.

## Ringkasan hasil

Evaluasi final: 100 posisi uji per postur (indeks 30 sampai 129 dari data uji, tidak pernah dilihat saat training). Data "dev" (30 posisi pertama) dipakai untuk keputusan selama percobaan.

Kriteria berhasil: kemiringan badan dalam 20 derajat dari tegak, tinggi badan di atas 0,85 x 0,494 m (0,42 m), norma kecepatan sendi di bawah 1 rad/s, ditahan 1 detik. Waktu bangun (time-to-stand) tidak dapat dilaporkan karena tidak ada keberhasilan.

| Run | Konfigurasi | Langkah | Prone | Supine |
| --- | --- | --- | --- | --- |
| A0 | reward dasar FRASA | 1 juta | 0/100 | 0/100 |
| A1 (3 seed) | A0 + bonus tinggi 0,3 + bonus tegak 0,3 | 1 juta | 0/300 | 0/300 |
| A1 panjang | seperti A1, seed 0 | 6 juta | 0/100 | 0/100 |
| C2 | A1 + kurikulum posisi awal mudah | 1,2 juta | 0/100 | 0/100 |
| C3 | bonus tinggi 1,5 saja + posisi mudah | 1,2 juta | 0/100 | 0/100 |
| C4 | bonus tinggi 1,0 + bonus tegak 1,0 + posisi mudah | 2 juta | 0/100 | 0/100 |

Rangkuman tabel lengkap: `results/final_table.txt` dan `results/summary.md`.

## Temuan diagnosis

- A0, A1, A1 panjang, C2, dan C4 berakhir di posisi duduk tegak dengan kaki lurus ke depan (tinggi badan maksimum sekitar 0,12 sampai 0,17 m, ambang berdiri 0,42 m), lalu diam. Ini kemungkinan optimum lokal: duduk tegak sudah memberi sebagian besar bonus ketegakan.
- C3 (bonus tinggi saja) menaikkan tinggi badan sampai 0,47 m pada supine, tetapi dengan badan miring (tilt sekitar -57 sampai -67 derajat): robot jongkok membungkuk dan berulang naik-turun; pada prone membentuk huruf V terbalik. Ini contoh reward hacking: tinggi dikejar tanpa berdiri tegak.
- Kurikulum posisi mudah (C2) tidak menolong, karena posisi "mudah" kita sudah rendah (tinggi sekitar 0,12 m).
- Dugaan penyebab (belum diuji): bentuk reward, kekakuan PD motor yang kami perkirakan sendiri (kp = batas torsi / 0,5), dan kontrol hanya lima sendi sagital simetris.

## Isi repo

- `k1_env/`: environment MuJoCo K1 (diadaptasi dari FRASA), dengan opsi reward Fase C (bonus tinggi, bonus tegak, kurikulum posisi awal).
- `tools/`: pembuat model dan environment K1, patch Fase C.
- `scripts/`: evaluasi (`evaluate.py`), perekaman video (`record.py`), analisis (`analyze_results.py`), diagnosis (`diag_rollout.py`, `diag_easy.py`), pembuat demo (`make_demo.py`), pembuat konfigurasi (`make_run_config.py`).
- `hyperparams/`: konfigurasi training (a0, a1, c2 sampai c4).
- `models/`: checkpoint `final_s0.zip` (A1, seed 0) dan `c3_s0.zip`.
- `docs/`: video (`demo.mp4`, klip kasus gagal) dan catatan.
- `LOG.md`: catatan kerja bertanggal.

## Mengulang percobaan

Dari folder repo, dengan venv aktif:

    python scripts/make_run_config.py a1 --fast height_bonus=0.3 upright_bonus=0.3 target_height=0.494
    python train_sbx.py --algo crossq --env k1-standup-v0 --conf hyperparams/a1.yml -f logs/a1 -n 1000000 --seed 0
    python scripts/evaluate.py models/final_s0.zip 0.494 100 30
    MUJOCO_GL=egl python scripts/record.py models/final_s0.zip prone 30 90 docs/klip.mp4

## Keterbatasan

- Hanya simulasi; tidak ada uji di robot nyata.
- Anggaran komputasi satu laptop (RTX 2050 4 GB); satu seed untuk C2 sampai C4.
- Parameter motor K1 adalah perkiraan.
- Kurikulum dua tahap seperti HumanUP tidak diimplementasikan; yang diuji hanya kurikulum posisi awal.

## Rujukan

- FRASA (Gaspard dkk., 2024), arXiv:2410.08655, https://github.com/Rhoban/frasa
- HumanUP (He dkk., 2025), arXiv:2502.12152
- Booster Gym (Wang dkk., 2025), arXiv:2506.15132
- CrossQ (Bhatt dkk., ICLR 2024)

## Catatan kontrol (dari kode)

- Lima sendi sagital dikendalikan: siku, bahu, pinggul, lutut, pergelangan kaki (pitch). Perintah dari sisi kiri dicerminkan ke kanan.
- Mode kontrol: kecepatan sendi, batas 2 pi rad/detik, langkah 0,05 detik (perubahan maksimum 0,314 rad per langkah).
- Sendi roll dan yaw tidak dikendalikan.
