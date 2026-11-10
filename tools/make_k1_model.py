#!/usr/bin/env python3
"""Membuat model K1 versi "siap-FRASA" dari K1_22dof.xml milik Booster.

Pemakaian:
    python make_k1_model.py <K1_22dof.xml> <folder_keluaran>
"""
import pathlib
import shutil
import sys
import xml.etree.ElementTree as ET

KP_DIV = 0.5     # kp = batas torsi / 0.5 rad (tebakan awal, disetel di Hari 6)
KV_RATIO = 0.05  # kv = 0.05 * kp (tebakan awal, disetel di Hari 6)


def clean(name):
    """aaleft_shoulder_pitch_joint -> left_shoulder_pitch; world_joint -> root."""
    if name == "world_joint":
        return "root"
    if name.startswith("aa"):
        name = name[2:]
    if name.endswith("_joint"):
        name = name[: -len("_joint")]
    return name


def main(src, out):
    src, out = pathlib.Path(src), pathlib.Path(out)
    tree = ET.parse(src)
    root = tree.getroot()

    # 1. Rename semua sendi, catat rentang sudutnya
    ranges = {}
    for j in root.iter("joint"):
        new = clean(j.get("name"))
        j.set("name", new)
        if j.get("range"):
            ranges[new] = j.get("range")

    # 2. Ganti motor torsi -> motor posisi (PD), seperti FRASA
    act = root.find("actuator")
    for m in list(act):
        assert m.tag == "motor", m.tag
        name = clean(m.get("name"))
        frc = float(m.get("forcerange").split()[1])
        kp = frc / KP_DIV
        kv = kp * KV_RATIO
        pos = ET.Element(
            "position",
            name=name,
            joint=clean(m.get("joint")),
            kp=f"{kp:g}",
            kv=f"{kv:g}",
            ctrlrange=ranges[name],
            forcerange=m.get("forcerange"),
        )
        act.remove(m)
        act.append(pos)

    # 3. Lantai: nama "floor" (dipakai kode FRASA) dan gesekan nyata (condim 3)
    n_floor = 0
    for g in root.iter("geom"):
        if g.get("name") == "ground":
            g.set("name", "floor")
            g.set("condim", "3")
            g.set("friction", "0.8 0.005 0.0001")
            n_floor += 1
    assert n_floor == 1

    # 4. Site "trunk" di badan utama (dipakai untuk menghitung kemiringan badan)
    n_trunk = 0
    for b in root.iter("body"):
        if b.get("name") == "trunk":
            ET.SubElement(b, "site", name="trunk", pos="0 0 0", size="0.01")
            n_trunk += 1
    assert n_trunk == 1

    # 5. Sensor giroskop harus bernama "gyro"
    n_gyro = 0
    for s in root.iter("gyro"):
        s.set("name", "gyro")
        n_gyro += 1
    assert n_gyro == 1

    out.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src.parent / "meshes", out / "meshes", dirs_exist_ok=True)
    ET.indent(tree)
    tree.write(out / "scene.xml", encoding="utf-8", xml_declaration=False)
    print("OK ->", out / "scene.xml")
    print("sendi:", len(ranges), " motor posisi:", len(list(act)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
