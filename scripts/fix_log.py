import pathlib
import re
import shutil

p = pathlib.Path("LOG.md")
text = p.read_text()
assert "## Jadwal" not in text, "LOG.md sudah dirapikan sebelumnya"
shutil.copy(p, "LOG.md.bak")

parts = re.split(r"(?m)^(?=## )", text)
title = parts[0].strip() or "# Log proyek K1 Dynamic Getting Up"
sections = {}
for s in parts[1:]:
    m = re.match(r"## Fase ([A-E])", s)
    if m:
        sections[m.group(1)] = s.split("\n", 1)[1].strip("\n") if "\n" in s else ""
    else:
        sections.setdefault("lain", "")
        sections["lain"] += s

jadwal = {
    "A": ("Sabtu 31 Okt - Senin 2 Nov", "setup dan baseline FRASA", "dicatat Selasa 10 Nov"),
    "B": ("Kamis 5 Nov - Minggu 8 Nov", "model K1, pose berdiri, posisi awal, reward, training uji", "selesai nyata: Selasa 10 Nov"),
    "C": ("Senin 9 Nov - Minggu 15 Nov", "training, kurikulum, dua postur", "mulai nyata: Selasa 10 Nov, geser sekitar 1 hari"),
    "D": ("Senin 16 Nov - Kamis 19 Nov", "evaluasi dan analisis kegagalan", "belum dimulai"),
    "E": ("Jumat 20 Nov - Selasa 24 Nov", "video demo, README, laporan, pengumpulan", "belum dimulai"),
}
out = [title, "", "## Jadwal", "| Fase | Jadwal | Isi | Status |", "| --- | --- | --- | --- |"]
for k, (tgl, isi, st) in jadwal.items():
    out.append(f"| {k} | {tgl} | {isi} | {st} |")
out.append("")
for k, (tgl, isi, st) in jadwal.items():
    out.append(f"## Fase {k}: {isi} ({tgl}; {st})")
    body = sections.get(k, "").strip("\n")
    out.append(body if body else "- (belum ada catatan)")
    out.append("")
if sections.get("lain", "").strip():
    out.append(sections["lain"].strip("\n"))
    out.append("")
p.write_text("\n".join(out))
print("LOG.md dirapikan; cadangan: LOG.md.bak")
