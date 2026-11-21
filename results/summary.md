Berkas dibaca: 3 (eval_models_final_s0_from30.csv, eval_models_final_s1_from30.csv, eval_models_final_s2_from30.csv)

## Hasil per seed dan postur

| Seed | Postur | Berhasil | Success rate | CI 95% (Wilson) | Median time-to-stand (s) | Terbalik/terhenti | Habis waktu |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | prone | 0/100 | 0.0% | 0.0-3.7% | - | 3 | 97 |
| 0 | supine | 0/100 | 0.0% | 0.0-3.7% | - | 2 | 98 |
| 1 | prone | 0/100 | 0.0% | 0.0-3.7% | - | 3 | 97 |
| 1 | supine | 0/100 | 0.0% | 0.0-3.7% | - | 3 | 97 |
| 2 | prone | 0/100 | 0.0% | 0.0-3.7% | - | 4 | 96 |
| 2 | supine | 0/100 | 0.0% | 0.0-3.7% | - | 1 | 99 |

## Gabungan semua seed

Tiap seed adalah run terpisah. CI gabungan hanya perkiraan kasar karena semua seed memakai posisi awal uji yang sama.

| Postur | Rata-rata antar seed | Simpangan baku antar seed | Gabungan | CI 95% gabungan |
| --- | --- | --- | --- | --- |
| prone | 0.0% | 0.0% | 0/300 | 0.0-1.3% |
| supine | 0.0% | 0.0% | 0/300 | 0.0-1.3% |

## Contoh episode untuk video (nomor posisi uji, dipakai di record.py)

- seed 0, prone: sukses tercepat [] | gagal [(30, 'timeout'), (31, 'timeout'), (32, 'terminated'), (33, 'timeout')]
- seed 0, supine: sukses tercepat [] | gagal [(30, 'timeout'), (31, 'timeout'), (32, 'timeout'), (33, 'timeout')]
- seed 1, prone: sukses tercepat [] | gagal [(30, 'timeout'), (31, 'timeout'), (32, 'terminated'), (33, 'timeout')]
- seed 1, supine: sukses tercepat [] | gagal [(30, 'timeout'), (31, 'timeout'), (32, 'timeout'), (33, 'timeout')]
- seed 2, prone: sukses tercepat [] | gagal [(30, 'timeout'), (31, 'timeout'), (32, 'timeout'), (33, 'timeout')]
- seed 2, supine: sukses tercepat [] | gagal [(30, 'timeout'), (31, 'timeout'), (32, 'timeout'), (33, 'timeout')]
