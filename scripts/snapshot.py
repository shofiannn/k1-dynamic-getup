import sys

import imageio.v2 as imageio
import mujoco
import numpy as np

m = mujoco.MjModel.from_xml_path(sys.argv[1])
d = mujoco.MjData(m)
mujoco.mj_forward(m, d)
renderer = mujoco.Renderer(m, 480, 360)
frames = []
for azimuth in (0, 90, 180, 270):
    cam = mujoco.MjvCamera()
    cam.lookat[:] = [0, 0, 0.8]
    cam.distance = 3.0
    cam.azimuth = azimuth
    cam.elevation = -10
    renderer.update_scene(d, cam)
    frames.append(renderer.render())
imageio.imwrite(sys.argv[2], np.hstack(frames))
print("gambar tersimpan:", sys.argv[2])
