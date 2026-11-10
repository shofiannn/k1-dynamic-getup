import gymnasium as gym
import numpy as np

import k1_env
from k1_env.mujoco_simulator.simulator import tf

gym.register_envs(k1_env)
env = gym.make("k1-standup-v0")
u = env.unwrapped
ds = u.options["desired_state"]
q_t = np.clip(np.copy(ds[: len(u.dofs)]), u.range_low, u.range_high)

print("tinggi jatuh (m) | tilt akhir (deg) | tinggi trunk akhir (m)")
for z in (0.45, 0.5, 0.55, 0.6, 0.7, 0.8):
    u.sim.reset()
    u.apply_control(q_t, True)
    u.sim.step()
    T = tf.rotation_matrix(ds[-1], [0, 1, 0])
    T[:3, 3] = [0, 0, z]
    u.sim.set_T_world_site("trunk", T)
    for _ in range(round(2.0 / u.sim.dt)):
        u.sim.step()
    print(f"{z:>14.2f}   | {np.rad2deg(u.get_tilt()):+14.1f}   | {u.trunk_site.xpos[2]:.3f}")
