import numpy as np
import lightkurve as lk
import matplotlib.pyplot as plt

print("1. Mengambil data TOI-5603 (TIC 224293782)...")
search = lk.search_lightcurve("TIC 224293782", mission="TESS", author="QLP")
lc_raw = search.download_all().stitch().remove_nans().normalize()

# Membersihkan outlier dan meratakan kurva cahaya
lc_clean = lc_raw[(lc_raw.flux.value > 0.95) & (lc_raw.flux.value < 1.05)]
lc_clean = lc_clean.remove_outliers(sigma_lower=5, sigma_upper=3)
lc_flat = lc_clean.flatten(window_length=101)

# Parameter transit TOI-5603.01
period = 0.5736183
t0 = 2635.46355

# 2. Lipat kurva cahaya untuk Primary Transit (Fase 0.0)
folded_primary = lc_flat.fold(period=period, epoch_time=t0)

# 3. Lipat kurva cahaya untuk Secondary Eclipse (Fase 0.5)
# Kita geser T0 sebanyak 0.5 * periode agar gerhana sekunder berada di pusat 0.0
t_secondary = t0 + (0.5 * period)
folded_secondary = lc_flat.fold(period=period, epoch_time=t_secondary)

# Binning data untuk mereduksi noise
bin_size = 0.003  # ~4.3 menit
binned_primary = folded_primary.bin(time_bin_size=bin_size)
binned_secondary = folded_secondary.bin(time_bin_size=bin_size)

# 4. Plot Perbandingan Berdampingan (Side-by-Side)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

# Panel Kiri: Gerhana Primer (Transit Utama)
ax1.scatter(folded_primary.time.value, folded_primary.flux.value, c='lightgray', alpha=0.3, s=8)
ax1.plot(binned_primary.time.value, binned_primary.flux.value, c='crimson', lw=2.2, label='Binned Transit')
ax1.axvline(0, color='blue', linestyle=':', alpha=0.7, label='Transit Center (Phase 0.0)')
ax1.set_xlim(-0.06, 0.06)
ax1.set_ylim(0.997, 1.003)
ax1.set_title("Primary Transit (Planet di Depan Bintang)")
ax1.set_xlabel("Waktu Relatif (Hari)")
ax1.set_ylabel("Normalized Flux")
ax1.legend(loc='lower right')
ax1.grid(True, linestyle="--", alpha=0.4)

# Panel Kanan: Gerhana Sekunder (Fase 0.5)
ax2.scatter(folded_secondary.time.value, folded_secondary.flux.value, c='lightgray', alpha=0.3, s=8)
ax2.plot(binned_secondary.time.value, binned_secondary.flux.value, c='forestgreen', lw=2.2, label='Binned Phase 0.5')
ax2.axvline(0, color='purple', linestyle=':', alpha=0.7, label='Secondary Center (Phase 0.5)')
ax2.set_xlim(-0.06, 0.06)
ax2.set_title("Secondary Eclipse Check (Objek di Belakang Bintang)")
ax2.set_xlabel("Waktu Relatif (Hari)")
ax2.legend(loc='lower right')
ax2.grid(True, linestyle="--", alpha=0.4)

plt.suptitle("Pemeriksaan Gerhana Sekunder - TOI-5603.01 (TIC 224293782)", fontsize=13)
plt.tight_layout()

print("Selesai! Menampilkan perbandingan...")
plt.show()