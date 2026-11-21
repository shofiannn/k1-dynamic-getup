Berkas dibaca: 1 (eval_logs_c2_s0_crossq_k1-standup-v0_1_k1-standup-v0_from0.csv)

## Hasil per seed dan postur

| Seed | Postur | Berhasil | Success rate | CI 95% (Wilson) | Median time-to-stand (s) | Terbalik/terhenti | Habis waktu |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | prone | 0/30 | 0.0% | -0.0-11.4% | - | 0 | 30 |
| 0 | supine | 0/30 | 0.0% | -0.0-11.4% | - | 2 | 28 |

## Gabungan semua seed

Tiap seed adalah run terpisah. CI gabungan hanya perkiraan kasar karena semua seed memakai posisi awal uji yang sama.

| Postur | Rata-rata antar seed | Simpangan baku antar seed | Gabungan | CI 95% gabungan |
| --- | --- | --- | --- | --- |
| prone | 0.0% | - | 0/30 | -0.0-11.4% |
| supine | 0.0% | - | 0/30 | -0.0-11.4% |

## Contoh episode untuk video (nomor posisi uji, dipakai di record.py)

- seed 0, prone: sukses tercepat [] | gagal [(0, 'timeout'), (1, 'timeout'), (2, 'timeout'), (3, 'timeout')]
- seed 0, supine: sukses tercepat [] | gagal [(0, 'timeout'), (1, 'timeout'), (2, 'timeout'), (3, 'timeout')]
