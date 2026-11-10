import sys

import mujoco
import numpy as np

m = mujoco.MjModel.from_xml_path(sys.argv[1])
d = mujoco.MjData(m)
print("nq =", m.nq, "| nv =", m.nv, "| nu =", m.nu)
print("massa total (kg):", round(float(m.body_mass.sum()), 3))
print("timestep (s):", m.opt.timestep)
print("geom nomor 0:", mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_GEOM, 0))
print("--- sendi ---")
for i in range(m.njnt):
    print(i, mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_JOINT, i), np.round(m.jnt_range[i], 3))
print("--- motor: nama | kp | kv | batas torsi ---")
for i in range(m.nu):
    print(i, mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_ACTUATOR, i),
          m.actuator_gainprm[i, 0], -m.actuator_biasprm[i, 2], m.actuator_forcerange[i])
mujoco.mj_forward(m, d)
print("kontak di pose awal:", d.ncon)

ok = True
for _ in range(int(3.0 / m.opt.timestep)):
    mujoco.mj_step(m, d)
    if not np.isfinite(d.qpos).all():
        ok = False
        break
print("jatuh bebas 3 detik:", "AMAN" if ok else f"NAN pada detik {d.time:.3f}")
print("tinggi badan akhir (m):", round(float(d.qpos[2]), 3), "| kontak akhir:", d.ncon)
