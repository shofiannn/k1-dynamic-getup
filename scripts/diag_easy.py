"""Diagnosis: apakah policy bisa berdiri kalau mulai dari posisi duduk/berlutut (kumpulan 'mudah')?

Pemakaian: python scripts/diag_easy.py PATH_MODEL [JUMLAH_POSISI]
"""
import pickle
import sys

import gymnasium as gym
import numpy as np
from sbx import CrossQ

import k1_env

gym.register_envs(k1_env)
model = CrossQ.load(sys.argv[1])
n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
env = gym.make("k1-standup-v0")
u = env.unwrapped
pool = pickle.load(open("k1_env/env/standup_initial_configurations_easy.pkl", "rb"))
idx = np.linspace(0, len(pool) - 1, n).astype(int)
for k, j in enumerate(idx):
    u.initial_config = [pool[j]]
    obs, _ = env.reset(seed=int(j), options={"use_cache": True})
    zs, tilts = [], []
    while True:
        action, _ = model.predict(obs, deterministic=True)
        obs, _, done, trunc, _ = env.step(action)
        zs.append(float(u.trunk_site.xpos[2]))
        tilts.append(float(np.rad2deg(u.get_tilt())))
        if done or trunc:
            break
    print(f"mudah #{j}: z_awal={zs[0]:.3f} z_maks={max(zs):.3f} z_akhir={zs[-1]:.3f} tilt_akhir={tilts[-1]:.1f}")
