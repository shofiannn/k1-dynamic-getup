#!/usr/bin/env python3
"""Menambah fitur Fase C ke k1_env. Semua fitur MATI secara bawaan,
jadi perilaku Fase B tidak berubah sampai kamu menyalakannya lewat file konfigurasi.

Pemakaian (sekali saja, dari folder repo):
    python tools/patch_phase_c.py .
"""
import pathlib
import sys

dst = pathlib.Path(sys.argv[1])
path = dst / "k1_env/env/standup_env.py"
t = path.read_text()
assert "reg_ramp_steps" not in t, "file ini sudah pernah dipatch"


def sub(old, new, count=1):
    global t
    assert t.count(old) == count, f"'{old}' ditemukan {t.count(old)} kali, seharusnya {count}"
    t = t.replace(old, new)


# 1. import mujoco (dipakai untuk menyaring posisi awal)
sub("import gymnasium\nimport numpy as np\n", "import gymnasium\nimport mujoco\nimport numpy as np\n")

# 2. opsi baru (semua mati)
sub('            "previous_actions": 1,\n        }',
    '            "previous_actions": 1,\n'
    '            # --- Fase C (semua mati secara bawaan) ---\n'
    '            "reg_ramp_steps": 0,    # >0: bonus kehalusan naik 0 -> 1 selama sekian langkah total\n'
    '            "n_envs_hint": 16,      # jumlah env paralel, untuk memperkirakan langkah total\n'
    '            "easy_start_steps": 0,  # >0: kurikulum posisi awal selama sekian langkah total\n'
    '            "easy_start_frac": 0.5, # peluang awal memakai posisi mudah (duduk/berlutut)\n'
    '            "posture": "both",      # "both", "prone", atau "supine"\n'
    '            "height_bonus": 0.0,    # bobot bonus tinggi badan (padat)\n'
    '            "upright_bonus": 0.0,   # bobot bonus ketegakan badan (padat)\n'
    '            "target_height": 0.5,   # tinggi badan saat berdiri (dari reward_check.py)\n'
    '        }')

# 3. muat kumpulan posisi mudah dan saring postur, setelah file posisi awal dimuat
sub("                self.initial_config = pickle.load(f)\n",
    "                self.initial_config = pickle.load(f)\n"
    "\n"
    "        # --- Fase C ---\n"
    "        self.total_steps = 0\n"
    "        self.reg_scale = 1.0\n"
    "        self.easy_config = None\n"
    "        easy_path = initial_config_path.replace('.pkl', '_easy.pkl')\n"
    "        if os.path.exists(easy_path):\n"
    "            with open(easy_path, 'rb') as f:\n"
    "                self.easy_config = pickle.load(f)\n"
    "        if self.initial_config is not None and self.options['posture'] != 'both':\n"
    "            self.initial_config = self._filter_posture(self.initial_config, self.options['posture'])\n")

# 4. metode baru
sub("    def get_initial_config_filename(self) -> str:",
    "    def _filter_posture(self, configs, posture):\n"
    "        kept = []\n"
    "        for qpos, ctrl in configs:\n"
    "            self.sim.data.qpos[:] = qpos\n"
    "            self.sim.data.qvel[:] = 0\n"
    "            mujoco.mj_forward(self.sim.model, self.sim.data)\n"
    "            tilt = np.rad2deg(self.get_tilt())\n"
    "            if (posture == 'prone' and tilt > 60) or (posture == 'supine' and tilt < -60):\n"
    "                kept.append([qpos, ctrl])\n"
    "        return kept\n"
    "\n"
    "    def _pick_pool(self):\n"
    "        steps = self.total_steps * self.options['n_envs_hint']\n"
    "        ramp = self.options['easy_start_steps']\n"
    "        if self.easy_config and ramp > 0 and steps < ramp:\n"
    "            p_easy = self.options['easy_start_frac'] * (1.0 - steps / ramp)\n"
    "            if self.np_random.random() < p_easy:\n"
    "                return self.easy_config\n"
    "        return self.initial_config\n"
    "\n"
    "    def get_initial_config_filename(self) -> str:")

# 5. hitung langkah total dan skala kehalusan di awal setiap step
sub("    def step(self, action):\n        action = np.array(action)\n",
    "    def step(self, action):\n        action = np.array(action)\n"
    "\n"
    "        self.total_steps += 1\n"
    "        ramp = self.options['reg_ramp_steps']\n"
    "        self.reg_scale = 1.0 if ramp <= 0 else min(1.0, self.total_steps * self.options['n_envs_hint'] / ramp)\n")

# 6. skala bonus kehalusan (aksi kecil dan perubahan aksi kecil)
sub("reward += np.exp(-np.linalg.norm(action)) * 1e-1\n",
    "reward += np.exp(-np.linalg.norm(action)) * 1e-1 * self.reg_scale\n", count=2)
sub("reward += np.exp(-np.linalg.norm(action_variation)) * 5e-2\n",
    "reward += np.exp(-np.linalg.norm(action_variation)) * 5e-2 * self.reg_scale\n", count=3)

# 7. bonus padat (bobot 0 = mati), sesudah suku tabrakan
sub("        reward += np.exp(-self.sim.self_collisions()) * 1e-1\n",
    "        reward += np.exp(-self.sim.self_collisions()) * 1e-1\n"
    "\n"
    "        # --- Fase C: bonus padat (bobot 0 = mati) ---\n"
    "        if self.options['height_bonus'] > 0:\n"
    "            h = self.trunk_site.xpos[2] / self.options['target_height']\n"
    "            reward += self.options['height_bonus'] * min(1.0, max(0.0, h))\n"
    "        if self.options['upright_bonus'] > 0:\n"
    "            tilt_err = self.tilt_history[-1] - self.options['desired_state'][-1]\n"
    "            reward += self.options['upright_bonus'] * 0.5 * (1.0 + np.cos(tilt_err))\n")

# 8. pilih posisi awal lewat kumpulan yang tepat
sub("qpos, ctrl = random.choice(self.initial_config)", "qpos, ctrl = random.choice(self._pick_pool())")

path.write_text(t)
print("OK: patch Fase C diterapkan pada", path)
