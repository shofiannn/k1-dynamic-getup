#!/usr/bin/env python3
"""Menyalin kode FRASA menjadi paket k1_env untuk robot Booster K1.

Pemakaian:
    python make_k1_env.py <folder_frasa_original> <folder_repo_k1>
"""
import pathlib
import shutil
import sys

src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])

ignore = shutil.ignore_patterns("__pycache__", "*.pkl", "model", "*.egg-info")
shutil.copytree(src / "frasa_env", dst / "k1_env", ignore=ignore, dirs_exist_ok=True)
for f in ["hyperparams"]:
    shutil.copytree(src / f, dst / f, dirs_exist_ok=True)
for f in ["train_sbx.py", "enjoy_sbx.py", "standup_generate_initial.py", "test_env.py", "setup.py", "pyproject.toml"]:
    shutil.copy(src / f, dst / f)
shutil.copy(src / "LICENSE", dst / "LICENSE-FRASA.txt")  # lisensi MIT FRASA wajib disertakan

# 1. Ganti nama di semua file teks
for p in list(dst.rglob("*.py")) + list(dst.rglob("*.yml")):
    if "tools" in p.parts:
        continue
    t = p.read_text()
    t = t.replace("frasa_env", "k1_env").replace("FRASAEnv", "K1Env").replace("frasa-standup-v0", "k1-standup-v0")
    p.write_text(t)


# 2. Perubahan terarah (setiap perubahan harus tepat satu kali ketemu)
def edit(path, old, new):
    p = dst / path
    t = p.read_text()
    assert t.count(old) == 1, f"{path}: '{old}' ditemukan {t.count(old)} kali"
    p.write_text(t.replace(old, new))


env = "k1_env/env/standup_env.py"
edit(env, 'self.dofs = ["elbow", "shoulder_pitch", "hip_pitch", "knee", "ankle_pitch"]',
     'self.dofs = ["elbow_pitch", "shoulder_pitch", "hip_pitch", "knee_pitch", "ankle_pitch"]')
edit(env, 'self.trunk_body = "torso_2023"', 'self.trunk_body = "trunk"')
edit(env, "T_world_trunk[:3, 3] = [0, 0, 0.4]", "T_world_trunk[:3, 3] = [0, 0, 0.8]")
edit("k1_env/env/standup.py", 'options["truncate_duration"] = 5.0', 'options["truncate_duration"] = 10.0')

# 3. Perbaikan kompatibilitas MuJoCo baru (yang kamu temui di Hari 1)
sim = "k1_env/mujoco_simulator/simulator.py"
t = (dst / sim).read_text()
t = t.replace("for id in np.argwhere(selector):", "for id in np.flatnonzero(selector):")
t = t.replace("mj_contactForce(self.model, self.data, id, forcetorque)", "mj_contactForce(self.model, self.data, int(id), forcetorque)")
(dst / sim).write_text(t)

# 4. Hasil generator posisi awal disimpan ke file "_raw" (mentah); nanti dipilah prone/supine
edit("standup_generate_initial.py",
     "filename: str = env.unwrapped.get_initial_config_filename()",
     'filename: str = env.unwrapped.get_initial_config_filename().replace(".pkl", "_raw.pkl")')
print("OK: paket k1_env dibuat di", dst)
