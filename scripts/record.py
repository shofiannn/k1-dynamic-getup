"""Merekam video episode ke file mp4 (tanpa jendela).

Pemakaian:
    MUJOCO_GL=egl python scripts/record.py PATH_MODEL POSTUR NOMOR_POSISI_UJI AZIMUTH KELUARAN.mp4
Contoh:
    MUJOCO_GL=egl python scripts/record.py logs/a0/crossq/k1-standup-v0_1/best_model.zip prone 0 90 docs/prone0.mp4
"""
import pickle
import sys

import gymnasium as gym
import imageio.v2 as imageio
import mujoco
import numpy as np
from sbx import CrossQ

import k1_env

gym.register_envs(k1_env)
model_path, posture, idx, az, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
model = CrossQ.load(model_path)
env = gym.make("k1-standup-v0")
u = env.unwrapped
u.initial_config = [pickle.load(open(f"data/eval_{posture}.pkl", "rb"))[idx]]
obs, _ = env.reset(seed=idx, options={"use_cache": True})
renderer = mujoco.Renderer(u.sim.model, 480, 640)
cam = mujoco.MjvCamera()
cam.distance, cam.azimuth, cam.elevation = 2.5, az, -10


def frame():
    cam.lookat[:] = [u.sim.data.qpos[0], 0, 0.4]
    renderer.update_scene(u.sim.data, cam)
    return renderer.render()


frames = [frame()]
while True:
    action, _ = model.predict(obs, deterministic=True)
    obs, _, done, trunc, _ = env.step(action)
    frames.append(frame())
    if done or trunc:
        break
imageio.mimsave(out, frames, fps=20)
print("video tersimpan:", out, "| jumlah frame:", len(frames))
