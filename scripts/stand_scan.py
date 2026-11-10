import sys

import mujoco
import numpy as np

m = mujoco.MjModel.from_xml_path(sys.argv[1])
dt = m.opt.timestep


def qadr(n):
    return m.jnt_qposadr[m.joint(n).id]


print("hip_pitch knee ankle | tilt akhir (deg) | tinggi (m) | geser x (m)")
for h in (0.3, 0.5, 0.7):
    d = mujoco.MjData(m)
    d.qpos[2] = 0.7
    for side in ("left", "right"):
        for n, v in (("hip_pitch", -h), ("knee_pitch", 2 * h), ("ankle_pitch", -h)):
            d.qpos[qadr(f"{side}_{n}")] = v
            d.ctrl[m.actuator(f"{side}_{n}").id] = v
    mujoco.mj_forward(m, d)
    x0 = d.qpos[0]
    for _ in range(int(3.0 / dt)):
        mujoco.mj_step(m, d)
    R = d.site("trunk").xmat
    tilt = np.rad2deg(-np.arctan2(R[6], R[8]))
    print(f"{-h:+.2f}     {2 * h:+.2f}  {-h:+.2f} | {tilt:+8.1f}        | {d.qpos[2]:.3f}     | {d.qpos[0] - x0:+.3f}")
