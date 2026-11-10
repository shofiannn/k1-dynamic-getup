# Reward versi 0 (reward FRASA, tanpa perubahan)

Mode kontrol: velocity. Per langkah (0,05 detik):

R = exp(-20 * ||psi - psi_target||^2) + 0.1 * exp(-||a||) + 0.05 * exp(-||a_t - a_t-1||) + 0.1 * exp(-F_tabrakan)

- psi = [sudut 5 sendi, kemiringan badan], psi_target = pose berdiri K1 (lihat desired_state)
- a = aksi (kecepatan target sendi), F_tabrakan = gaya tabrakan antar bagian badan
- Maksimum per langkah sekitar 1,25
- Sumber: README dan standup_env.py milik FRASA (Rhoban), MIT License
