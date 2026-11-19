"""Menghitung kondisi awal (kemiringan dan tinggi badan) tiap posisi uji, untuk analisis kegagalan.

Pemakaian: python scripts/failure_features.py
Keluaran: results/features.csv (postur, nomor, tilt0, z0)
"""
import csv
import pickle

import gymnasium as gym
import mujoco
import numpy as np

import k1_env

gym.register_envs(k1_env)
env = gym.make("k1-standup-v0")
u = env.unwrapped
rows = []
for posture in ("prone", "supine"):
    pool = pickle.load(open(f"data/eval_{posture}.pkl", "rb"))
    for idx, (qpos, ctrl) in enumerate(pool):
        u.sim.data.qpos[:] = qpos
        u.sim.data.qvel[:] = 0
        mujoco.mj_forward(u.sim.model, u.sim.data)
        rows.append([posture, idx, float(np.rad2deg(u.get_tilt())), float(u.trunk_site.xpos[2])])
with open("results/features.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["posture", "idx", "tilt0", "z0"])
    w.writerows(rows)
print("tersimpan: results/features.csv |", len(rows), "posisi")
