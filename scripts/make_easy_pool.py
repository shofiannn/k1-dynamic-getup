"""Membuat kumpulan posisi awal 'mudah' (duduk/berlutut) dari file mentah.

Pemakaian: python scripts/make_easy_pool.py TINGGI_BERDIRI_M
"""
import pickle
import sys

import gymnasium as gym
import mujoco
import numpy as np

import k1_env

H = float(sys.argv[1])
gym.register_envs(k1_env)
env = gym.make("k1-standup-v0")
u = env.unwrapped
raw = pickle.load(open("k1_env/env/standup_initial_configurations_raw.pkl", "rb"))
easy = []
for qpos, ctrl in raw:
    u.sim.data.qpos[:] = qpos
    u.sim.data.qvel[:] = 0
    mujoco.mj_forward(u.sim.model, u.sim.data)
    tilt = abs(np.rad2deg(u.get_tilt()))
    if tilt < 60 and u.trunk_site.xpos[2] < 0.85 * H:
        easy.append([qpos, ctrl])
out = "k1_env/env/standup_initial_configurations_easy.pkl"
pickle.dump(easy, open(out, "wb"))
print("posisi mudah:", len(easy), "->", out)
