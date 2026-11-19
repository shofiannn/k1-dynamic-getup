"""Grafik reward evaluasi selama training.

Pemakaian: python scripts/plot_eval.py KELUARAN.png logs/a0/crossq/k1-standup-v0_1 [folder_lain ...]
"""
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

for folder in sys.argv[2:]:
    d = np.load(f"{folder}/evaluations.npz")
    plt.plot(d["timesteps"], d["results"].mean(axis=1), label=folder.split("/")[1])
plt.xlabel("langkah training")
plt.ylabel("reward evaluasi rata-rata")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig(sys.argv[1], dpi=120)
print("grafik tersimpan:", sys.argv[1])
