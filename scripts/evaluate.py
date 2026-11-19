"""Evaluasi policy pada posisi awal UJI (tidak pernah dilihat saat training).

Pemakaian:
    python scripts/evaluate.py PATH_MODEL TINGGI_BERDIRI_M [JUMLAH_EPISODE [MULAI_DARI]]
Contoh (data "dev", untuk mengambil keputusan di Fase C):
    python scripts/evaluate.py logs/a0/crossq/k1-standup-v0_1/best_model.zip 0.52 30 0
Contoh (evaluasi final di Fase D, memakai sisa data uji):
    python scripts/evaluate.py logs/a0/crossq/k1-standup-v0_1/best_model.zip 0.52 100 30
"""
import csv
import math
import os
import pickle
import sys

import gymnasium as gym
import numpy as np
from sbx import CrossQ

import k1_env

gym.register_envs(k1_env)
model_path, height = sys.argv[1], float(sys.argv[2])
max_eps = int(sys.argv[3]) if len(sys.argv) > 3 else 100
start = int(sys.argv[4]) if len(sys.argv) > 4 else 0
HOLD = 20  # langkah berturut-turut (20 x 0,05 detik = 1 detik)
model = CrossQ.load(model_path)
env = gym.make("k1-standup-v0")
u = env.unwrapped
dt = u.options["dt"]
target_tilt = float(np.rad2deg(u.options["desired_state"][-1]))


def standing(obs):
    tilt = float(np.rad2deg(u.get_tilt()))
    z = float(u.trunk_site.xpos[2])
    qdot = float(np.linalg.norm(obs[5:10]))
    return abs(tilt - target_tilt) < 20 and z > 0.85 * height and qdot < 1.0


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (c - h, c + h)


os.makedirs("results", exist_ok=True)
tag = model_path.replace("/", "_").replace(".zip", "") + f"_from{start}"
rows = []
for posture in ("prone", "supine"):
    pool = pickle.load(open(f"data/eval_{posture}.pkl", "rb"))[start:start + max_eps]
    times, ok = [], 0
    for i, cfg in enumerate(pool):
        u.initial_config = [cfg]
        obs, _ = env.reset(seed=i, options={"use_cache": True})
        run, t_stand, step = 0, None, 0
        while True:
            action, _ = model.predict(obs, deterministic=True)
            obs, _, done, trunc, _ = env.step(action)
            step += 1
            run = run + 1 if standing(obs) else 0
            if run >= HOLD and t_stand is None:
                t_stand = (step - HOLD + 1) * dt
                break
            if done or trunc:
                break
        ok += t_stand is not None
        if t_stand is not None:
            times.append(t_stand)
        reason = "success" if t_stand is not None else ("terminated" if done else "timeout")
        rows.append([posture, start + i, int(t_stand is not None), t_stand if t_stand is not None else "", reason])
    lo, hi = wilson(ok, len(pool))
    med = float(np.median(times)) if times else float("nan")
    print(f"{posture:>6}: berhasil {ok}/{len(pool)} = {100 * ok / max(1, len(pool)):.1f}% (CI95 {100 * lo:.1f}-{100 * hi:.1f}%) | median time-to-stand {med:.2f} s")
with open(f"results/eval_{tag}.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["posture", "episode", "success", "time_to_stand_s", "end_reason"])
    w.writerows(rows)
print("CSV:", f"results/eval_{tag}.csv")
