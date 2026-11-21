import pathlib

p = pathlib.Path("k1_env/env/standup_env.py")
t = p.read_text()
assert "upright_gate" not in t, "sudah dipatch"

old1 = '"target_height": 0.5,'
assert t.count(old1) == 1
t = t.replace(old1, '"upright_gate": False,  # True: bonus tegak dikalikan fraksi tinggi\n            "target_height": 0.5,')

old2 = "            reward += self.options['upright_bonus'] * 0.5 * (1.0 + np.cos(tilt_err))\n"
assert t.count(old2) == 1
new2 = (
    "            gate = 1.0\n"
    "            if self.options['upright_gate']:\n"
    "                gate = min(1.0, max(0.0, self.trunk_site.xpos[2] / self.options['target_height']))\n"
    "            reward += self.options['upright_bonus'] * gate * 0.5 * (1.0 + np.cos(tilt_err))\n"
)
t = t.replace(old2, new2)
p.write_text(t)
print("OK: patch upright_gate diterapkan")
