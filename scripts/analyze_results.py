"""Rekap hasil evaluasi final: per seed, gabungan, kategori kegagalan, dan contoh episode.

Pemakaian (dari folder repo):
    python scripts/analyze_results.py
    python scripts/analyze_results.py "pola/berkas/*.csv"
Tanpa argumen, memakai results/eval_models_final_s*_from30.csv.
Keluaran: tabel di layar, results/summary.md, results/success_by_posture.png.
Kalau results/features.csv ada (dari failure_features.py), ikut dibuat tabel menurut kondisi awal.
"""
import csv
import glob
import math
import pathlib
import re
import statistics
import sys
from collections import Counter, defaultdict

NL = chr(10)  # karakter baris baru
pattern = sys.argv[1] if len(sys.argv) > 1 else "results/eval_models_final_s*_from30.csv"
files = sorted(glob.glob(pattern))
if not files:
    sys.exit(f"Tidak ada berkas cocok dengan pola: {pattern}")


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (c - h, c + h)


rows = []  # (seed, postur, nomor_episode, berhasil, waktu, alasan)
for f in files:
    m = re.search(r"_s(\d+)_", f)
    seed = m.group(1) if m else pathlib.Path(f).stem
    for r in csv.DictReader(open(f)):
        t = float(r["time_to_stand_s"]) if r["time_to_stand_s"] else None
        rows.append((seed, r["posture"], int(r["episode"]), int(r["success"]), t, r["end_reason"]))

seeds = sorted({r[0] for r in rows})
postures = ("prone", "supine")
out = []
out.append("Berkas dibaca: " + str(len(files)) + " (" + ", ".join(pathlib.Path(f).name for f in files) + ")")
out.append("")
out.append("## Hasil per seed dan postur")
out.append("")
out.append("| Seed | Postur | Berhasil | Success rate | CI 95% (Wilson) | Median time-to-stand (s) | Terbalik/terhenti | Habis waktu |")
out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
per = defaultdict(dict)
for s in seeds:
    for p in postures:
        sub = [r for r in rows if r[0] == s and r[1] == p]
        n, k = len(sub), sum(r[3] for r in sub)
        lo, hi = wilson(k, n)
        times = [r[4] for r in sub if r[3] and r[4] is not None]
        med = f"{statistics.median(times):.2f}" if times else "-"
        c = Counter(r[5] for r in sub)
        per[p][s] = (k, n)
        out.append(f"| {s} | {p} | {k}/{n} | {100 * k / max(1, n):.1f}% | {100 * lo:.1f}-{100 * hi:.1f}% | {med} | {c['terminated']} | {c['timeout']} |")

out.append("")
out.append("## Gabungan semua seed")
out.append("")
out.append("Tiap seed adalah run terpisah. CI gabungan hanya perkiraan kasar karena semua seed memakai posisi awal uji yang sama.")
out.append("")
out.append("| Postur | Rata-rata antar seed | Simpangan baku antar seed | Gabungan | CI 95% gabungan |")
out.append("| --- | --- | --- | --- | --- |")
for p in postures:
    rates = [100 * k / max(1, n) for k, n in per[p].values()]
    K = sum(k for k, _ in per[p].values())
    N = sum(n for _, n in per[p].values())
    lo, hi = wilson(K, N)
    sd = f"{statistics.stdev(rates):.1f}%" if len(rates) > 1 else "-"
    out.append(f"| {p} | {statistics.mean(rates):.1f}% | {sd} | {K}/{N} | {100 * lo:.1f}-{100 * hi:.1f}% |")

out.append("")
out.append("## Contoh episode untuk video (nomor posisi uji, dipakai di record.py)")
out.append("")
for s in seeds:
    for p in postures:
        sub = [r for r in rows if r[0] == s and r[1] == p]
        succ = sorted([r for r in sub if r[3]], key=lambda r: r[4])[:3]
        fails = [r for r in sub if not r[3]][:4]
        out.append(f"- seed {s}, {p}: sukses tercepat {[r[2] for r in succ]} | gagal {[(r[2], r[5]) for r in fails]}")

feat_path = pathlib.Path("results/features.csv")
if feat_path.exists():
    feats = {(r["posture"], int(r["idx"])): (float(r["tilt0"]), float(r["z0"])) for r in csv.DictReader(open(feat_path))}
    out.append("")
    out.append("## Success rate menurut kondisi awal (gabungan seed)")
    out.append("")
    out.append("| Postur | Kondisi awal | Berhasil | Success rate |")
    out.append("| --- | --- | --- | --- |")
    bins = [
        ("kemiringan 60-90 derajat", lambda t, z: 60 <= abs(t) < 90),
        ("kemiringan 90-120 derajat", lambda t, z: 90 <= abs(t) < 120),
        ("kemiringan di atas 120 derajat", lambda t, z: abs(t) >= 120),
        ("badan rendah (tinggi di bawah 0,10 m)", lambda t, z: z < 0.10),
        ("badan agak tinggi (0,10 m atau lebih)", lambda t, z: z >= 0.10),
    ]
    for p in postures:
        for name, cond in bins:
            sel = [r for r in rows if r[1] == p and (p, r[2]) in feats and cond(*feats[(p, r[2])])]
            if sel:
                k = sum(r[3] for r in sel)
                out.append(f"| {p} | {name} | {k}/{len(sel)} | {100 * k / len(sel):.1f}% |")

text = NL.join(out)
print(text)
pathlib.Path("results").mkdir(exist_ok=True)
pathlib.Path("results/summary.md").write_text(text + NL)
print("Tersimpan: results/summary.md")

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    width = 0.8 / max(1, len(seeds))
    for i, s in enumerate(seeds):
        vals = [100 * per[p][s][0] / max(1, per[p][s][1]) for p in postures]
        ax.bar([j + i * width for j in range(2)], vals, width, label=f"seed {s}")
    ax.set_xticks([j + width * (len(seeds) - 1) / 2 for j in range(2)])
    ax.set_xticklabels(["prone (tengkurap)", "supine (telentang)"])
    ax.set_ylabel("success rate (%)")
    ax.set_ylim(0, 100)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig("results/success_by_posture.png", dpi=150)
    print("Tersimpan: results/success_by_posture.png")
except Exception as e:  # grafik bersifat opsional
    print("Grafik dilewati:", e)
