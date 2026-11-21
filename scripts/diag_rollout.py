"""Diagnosis cepat: seberapa tinggi dan tegak robot pernah mencapai selama satu episode.

Pemakaian: python scripts/diag_rollout.py PATH_MODEL [JUMLAH_POSISI]
"""
import pickle
import sys

import gymnasium as gym
import numpy as np
from sbx import CrossQ

import k1_env

gym.register_envs(k1_env)
model = CrossQ.load(sys.argv[1])
n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
env = gym.make("k1-standup-v0")
u = env.unwrapped
tt = float(np.rad2deg(u.options["desired_state"][-1]))
print(f"tilt target = {tt:.1f} derajat | ambang berdiri: tinggi > {0.85 * 0.494:.3f} m")
for posture in ("prone", "supine"):
    pool = pickle.load(open(f"data/eval_{posture}.pkl", "rb"))[:n]
    for i, cfg in enumerate(pool):
        u.initial_config = [cfg]
        obs, _ = env.reset(seed=i, options={"use_cache": True})
        zs, tilts, acts = [], [], []
        while True:
            action, _ = model.predict(obs, deterministic=True)
            obs, _, done, trunc, _ = env.step(action)
            zs.append(float(u.trunk_site.xpos[2]))
            tilts.append(float(np.rad2deg(u.get_tilt())))
            acts.append(float(np.mean(np.abs(action))))
            if done or trunc:
                break
        print(f"{posture:>6} #{i}: langkah={len(zs)} z_awal={zs[0]:.3f} z_maks={max(zs):.3f} "
              f"z_akhir={zs[-1]:.3f} tilt_akhir={tilts[-1]:.1f} rata2|aksi|={np.mean(acts):.2f}")
