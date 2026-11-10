import pickle

import gymnasium as gym
import mujoco
import numpy as np

import k1_env

gym.register_envs(k1_env)
env = gym.make("k1-standup-v0")
u = env.unwrapped


def run(label, **options):
    env.reset(options=options)
    tilt0 = np.rad2deg(u.get_tilt())
    total = 0.0
    for _ in range(20):
        _, r, _, _, _ = env.step(np.zeros(5))
        total += r
    print(f"{label:>7}: tilt awal {tilt0:+7.1f} deg | reward rata-rata/langkah {total / 20:.3f} | tinggi badan {u.trunk_site.xpos[2]:.3f} m")


run("target", target=True, use_cache=False)
for name in ("prone", "supine"):
    u.initial_config = pickle.load(open(f"data/eval_{name}.pkl", "rb"))
    run(name, use_cache=True)

# uji tanda kemiringan: putar badan +90 derajat di sumbu y
u.sim.data.qpos[3:7] = [np.cos(np.pi / 4), 0, np.sin(np.pi / 4), 0]
mujoco.mj_forward(u.sim.model, u.sim.data)
print("uji tanda: tilt =", round(float(np.rad2deg(u.get_tilt())), 1), "(harus +90)")
