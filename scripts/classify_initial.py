import pickle
import random

import gymnasium as gym
import mujoco
import numpy as np

import k1_env

gym.register_envs(k1_env)
env = gym.make("k1-standup-v0")
u = env.unwrapped
base = u.get_initial_config_filename()
raw = base.replace(".pkl", "_raw.pkl")
configs = pickle.load(open(raw, "rb"))

prone, supine, other = [], [], []
for qpos, ctrl in configs:
    u.sim.data.qpos[:] = qpos
    u.sim.data.qvel[:] = 0
    mujoco.mj_forward(u.sim.model, u.sim.data)
    tilt = np.rad2deg(u.get_tilt())
    if tilt > 60:
        prone.append([qpos, ctrl])
    elif tilt < -60:
        supine.append([qpos, ctrl])
    else:
        other.append([qpos, ctrl])
print(f"mentah: {len(configs)} | prone: {len(prone)} | supine: {len(supine)} | lainnya: {len(other)}")

random.seed(0)
train = []
for name, lst in (("prone", prone), ("supine", supine)):
    random.shuffle(lst)
    k = int(0.8 * len(lst))
    train += lst[:k]
    pickle.dump(lst[k:], open(f"data/eval_{name}.pkl", "wb"))
    print(f"{name}: latih {k} | uji {len(lst) - k}")
random.shuffle(train)
pickle.dump(train, open(base, "wb"))
print("file latih ditulis:", base)
