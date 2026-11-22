"""Evaluasi dua ukuran pada data uji final: ketat (tilt 20) dan longgar (tilt TOL).

Pemakaian: python scripts/eval_relaxed.py PATH_MODEL [TOL_DERAJAT=45] [JUMLAH=100] [MULAI=30]
"""
import pickle
import sys

import gymnasium as gym
import numpy as np
from sbx import CrossQ

import k1_env

gym.register_envs(k1_env)
model = CrossQ.load(sys.argv[1])
tol = float(sys.argv[2]) if len(sys.argv) > 2 else 45.0
n = int(sys.argv[3]) if len(sys.argv) > 3 else 100
start = int(sys.argv[4]) if len(sys.argv) > 4 else 30
H, HOLD = 0.494, 20
env = gym.make("k1-standup-v0")
u = env.unwrapped
dt = u.options["dt"]
tt = float(np.rad2deg(u.options["desired_state"][-1]))


def ok(obs, tilt_tol):
    tilt = float(np.rad2deg(u.get_tilt()))
    z = float(u.trunk_site.xpos[2])
    qd = float(np.linalg.norm(obs[5:10]))
    return abs(tilt - tt) < tilt_tol and z > 0.85 * H and qd < 1.0


for posture in ("prone", "supine"):
    pool = pickle.load(open(f"data/eval_{posture}.pkl", "rb"))[start:start + n]
    strict = relaxed = 0
    times = []
    for i, cfg in enumerate(pool):
        u.initial_config = [cfg]
        obs, _ = env.reset(seed=i, options={"use_cache": True})
        rs = rr = 0
        step = 0
        got_s = got_r = False
        while True:
            action, _ = model.predict(obs, deterministic=True)
            obs, _, done, trunc, _ = env.step(action)
            step += 1
            rs = rs + 1 if ok(obs, 20.0) else 0
            rr = rr + 1 if ok(obs, tol) else 0
            if rs >= HOLD:
                got_s = True
            if rr >= HOLD and not got_r:
                got_r = True
                times.append((step - HOLD + 1) * dt)
            if done or trunc:
                break
        strict += got_s
        relaxed += got_r
    med = float(np.median(times)) if times else float("nan")
    print(f"{posture:>6}: ketat {strict}/{len(pool)} | longgar(tilt<{tol:.0f}) {relaxed}/{len(pool)} | median waktu longgar {med:.2f} s")
