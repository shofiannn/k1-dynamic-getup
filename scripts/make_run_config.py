"""Membuat file konfigurasi training.

Pemakaian:
    python scripts/make_run_config.py NAMA [--fast] [opsi=nilai ...]

Contoh:
    python scripts/make_run_config.py a0
    python scripts/make_run_config.py a1 height_bonus=0.3 upright_bonus=0.3 target_height=0.52
"""
import sys

import yaml

name = sys.argv[1]
fast = "--fast" in sys.argv
opts = {}
for a in sys.argv[2:]:
    if a.startswith("--"):
        continue
    k, v = a.split("=", 1)
    opts[k] = yaml.safe_load(v)

cfg = {
    "n_timesteps": 1000000,
    "policy": "MlpPolicy",
    "learning_rate": 0.001,
    "buffer_size": 1000000,
    "batch_size": 256,
    "n_envs": 16,
    "gamma": 0.99,
    "ent_coef": "auto",
    "train_freq": 4,
    "gradient_steps": 64 if fast else 512,
    "learning_starts": 100000,
    "policy_kwargs": "dict(net_arch=[384, 256])",
}
if opts:
    cfg["env_kwargs"] = {"options": opts}
out = f"hyperparams/{name}.yml"
with open(out, "w") as f:
    yaml.safe_dump({"k1-standup-v0": cfg}, f, sort_keys=False)
print("ditulis:", out)
print(open(out).read())
