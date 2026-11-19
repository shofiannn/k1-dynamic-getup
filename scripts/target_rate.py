import gymnasium as gym
import numpy as np

import k1_env

gym.register_envs(k1_env)
env = gym.make("k1-standup-v0")
u = env.unwrapped
ok, bad = 0, []
for seed in range(30):
    env.reset(seed=seed, options={"target": True, "use_cache": False})
    tilt = float(np.rad2deg(u.get_tilt()))
    z = float(u.trunk_site.xpos[2])
    if abs(tilt) < 20 and z > 0.4:
        ok += 1
    else:
        bad.append((seed, round(tilt, 1), round(z, 3)))
print(f"berdiri: {ok}/30")
print("gagal (seed, tilt, tinggi):", bad)
