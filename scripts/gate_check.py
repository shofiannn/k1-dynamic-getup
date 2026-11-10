"""Pemeriksaan otomatis Gerbang Fase A dan B.

Pemakaian (dari folder repo, venv aktif):
    python scripts/gate_check.py
"""
import importlib.util
import os
import pathlib
import re
import subprocess
import sys

OK, BAD, WARN = "[LULUS]", "[GAGAL]", "[CEK]  "
results = []


def report(status, text, hint=""):
    results.append(status)
    print(f"{status} {text}")
    if hint and status != OK:
        print(f"         -> {hint}")


def has(mod):
    try:
        return importlib.util.find_spec(mod) is not None
    except Exception:
        return False


def run(cmd, timeout=600):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout + p.stderr)


print("=== FASE A ===")
report(OK if "venv-getup" in sys.prefix else BAD, f"venv aktif ({sys.prefix})",
       "jalankan: source ~/venv-getup/bin/activate")
for mod, hint in (("mujoco", "pip install mujoco"), ("jax", "pip install jax"), ("sbx", "pip install -e . di frasa"),
                  ("rl_zoo3", "pip install rl_zoo3"), ("gymnasium", "pip install gymnasium")):
    report(OK if has(mod) else BAD, f"paket {mod} terpasang", hint)
report(OK if has("frasa_env") or pathlib.Path("~/getup-project/frasa_original").expanduser().exists() else BAD,
       "FRASA asli ada di ~/getup-project/frasa_original",
       "ulangi Fase A (clone Rhoban/frasa)")
try:
    import jax
    devs = str(jax.devices())
    report(OK if "Cuda" in devs else WARN, f"JAX memakai: {devs}",
           "bukan GPU: training lebih lambat (pip install -U 'jax[cuda12]')")
except Exception as e:
    report(BAD, f"JAX error: {e}")

print("\n=== FASE B ===")
for f in ("tools/make_k1_model.py", "tools/make_k1_env.py", "scripts/check_model.py", "scripts/snapshot.py",
          "scripts/pd_test.py", "scripts/stand_scan.py", "scripts/classify_initial.py", "scripts/reward_check.py",
          "k1_env/mujoco_simulator/model/scene.xml", "docs/k1_4sisi.png", "hyperparams/crossq_smoke.yml"):
    report(OK if pathlib.Path(f).exists() else BAD, f"berkas {f}", "langkah pembuat berkas ini belum dikerjakan")
report(OK if pathlib.Path("LOG.md").exists() else WARN, "LOG.md ada", "buat LOG.md (catatan harian)")
report(OK if pathlib.Path("docs/reward.md").exists() else WARN, "docs/reward.md ada (B19)", "kerjakan B19")

try:
    import mujoco
    m = mujoco.MjModel.from_xml_path("k1_env/mujoco_simulator/model/scene.xml")
    mass = float(sum(m.body_mass))
    report(OK if (m.nq, m.nv, m.nu) == (29, 28, 22) else BAD, f"model K1: nq={m.nq} nv={m.nv} nu={m.nu} (harus 29/28/22)")
    report(OK if abs(mass - 19.67) < 0.2 else BAD, f"massa total {mass:.2f} kg (harus sekitar 19,67)")
    report(OK if m.geom(0).name == "floor" else BAD, f"geom nomor 0 bernama '{m.geom(0).name}' (harus floor)")
except Exception as e:
    report(BAD, f"model K1 gagal dimuat: {e}", "ulangi B5-B7")

try:
    import gymnasium as gym
    import numpy as np
    import k1_env
    gym.register_envs(k1_env)
    env = gym.make("k1-standup-v0")
    u = env.unwrapped
    ds = np.rad2deg(u.options["desired_state"])
    report(OK if not np.allclose(ds, [-49.5, 19.5, -52, 79, -36.5, 8.5], atol=0.1) else BAD,
           f"desired_state = {np.round(ds, 1).tolist()}", "pose Sigmaban belum diganti ke pose K1 (B15)")
    src = pathlib.Path("k1_env/env/standup_env.py").read_text()
    report(OK if "0.55 if target else 0.8" in src else BAD, "perbaikan tinggi jatuh pose target (0.55)",
           "jalankan perintah sed dari catatan temuan setelah B18")
    report(OK if u.options["truncate_duration"] == 10.0 else WARN, f"durasi episode {u.options['truncate_duration']} s (rencana 10)")
    import pickle
    n_tr = len(pickle.load(open(u.get_initial_config_filename(), "rb")))
    n_p = len(pickle.load(open("data/eval_prone.pkl", "rb")))
    n_s = len(pickle.load(open("data/eval_supine.pkl", "rb")))
    report(OK if n_p >= 100 and n_s >= 100 else BAD,
           f"data uji: prone {n_p}, supine {n_s}; data latih total {n_tr}  (perkiraan total per postur: {n_p * 5} / {n_s * 5}, target minimal 500)",
           "kumpulkan lebih banyak (B16) SEBELUM training dimulai")
except Exception as e:
    report(BAD, f"environment K1 gagal dibuat/dibaca: {e}", "kirim pesan error ini ke asisten")

print("\n(menjalankan reward_check.py, mohon tunggu...)")
try:
    rc, out = run([sys.executable, "scripts/reward_check.py"])
    print(out.strip()[-700:])
    g = lambda name: re.search(rf"{name}:\s+tilt awal\s+([+-]?[\d.]+) deg \| reward rata-rata/langkah ([\d.]+) \| tinggi badan ([\d.]+)", out)
    t, p, s = g("target"), g("prone"), g("supine")
    if t and p and s:
        report(OK if abs(float(t[1])) < 15 and float(t[2]) > 0.8 else BAD,
               f"target: tilt {t[1]} reward {t[2]} (harus tilt dekat 0, reward di atas 0,8)")
        report(OK if float(p[1]) > 60 and float(p[2]) <= 0.26 else BAD, f"prone: tilt {p[1]} reward {p[2]}")
        report(OK if float(s[1]) < -60 and float(s[2]) <= 0.26 else BAD, f"supine: tilt {s[1]} reward {s[2]}")
    else:
        report(BAD, "keluaran reward_check tidak terbaca", "jalankan manual: python scripts/reward_check.py")
    report(OK if "tilt = 90.0" in out else BAD, "uji tanda tilt = +90")
except Exception as e:
    report(BAD, f"reward_check gagal: {e}")

best = list(pathlib.Path("logs").glob("**/best_model.zip")) if pathlib.Path("logs").exists() else []
report(OK if best else WARN, f"hasil training uji: {len(best)} best_model.zip", "kerjakan B21 (fps masih perlu dicatat)")

rc, out = run(["git", "status", "--porcelain"])
report(OK if rc == 0 and not out.strip() else WARN, "semua perubahan sudah di-commit",
       "git add . && git commit -m '...' ; berkas belum disimpan: " + " ".join(out.split()[:6]))
rc, out = run(["git", "rev-list", "--count", "@{u}..HEAD"])
report(OK if rc == 0 and out.strip() == "0" else WARN, "semua komit sudah di-push ke GitHub", "jalankan: git push")

print("\n=== RINGKASAN ===")
print(f"lulus {results.count(OK)} | perlu dicek {results.count(WARN)} | gagal {results.count(BAD)}")
print("GERBANG:", "LULUS" if BAD not in results else "BELUM LULUS (lihat baris [GAGAL])")
