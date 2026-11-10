import sys

import mujoco
import numpy as np

# pemakaian: python pd_test.py scene.xml NAMA_SENDI TARGET_RAD
m = mujoco.MjModel.from_xml_path(sys.argv[1])
d = mujoco.MjData(m)
m.opt.gravity[:] = 0  # tanpa gravitasi: kita hanya menguji respons motor
name, target = sys.argv[2], float(sys.argv[3])
adr = m.jnt_qposadr[m.joint(name).id]
d.ctrl[m.actuator(name).id] = target
mujoco.mj_forward(m, d)
hist = []
for _ in range(int(1.0 / m.opt.timestep)):
    mujoco.mj_step(m, d)
    hist.append(d.qpos[adr])
hist = np.array(hist)
reach = np.where(np.abs(hist) >= 0.9 * abs(target))[0]
t90 = reach[0] * m.opt.timestep if len(reach) else float("nan")
over = (np.abs(hist).max() - abs(target)) / abs(target) * 100
print(f"{name}: target {target} | nilai akhir {hist[-1]:.3f} | lewatan {over:.1f}% | waktu 90%: {t90:.3f} s")
