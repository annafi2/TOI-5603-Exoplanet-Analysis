import numpy as np
import lightkurve as lk
import matplotlib.pyplot as plt

# 1. Unduh dan siapkan data gabungan
print("1. Mengambil data TOI-5603...")
search = lk.search_lightcurve("TIC 224293782", mission="TESS", author="QLP")
lc_raw = search.download_all().stitch().remove_nans().normalize()

# Bersihkan noise instrumen dan ratakan kurva (detrending)
lc_clean = lc_raw[(lc_raw.flux.value > 0.95) & (lc_raw.flux.value < 1.05)]
lc_clean = lc_clean.remove_outliers(sigma_lower=5, sigma_upper=3)
lc_flat = lc_clean.flatten(window_length=101)

# Parameter kandidat TOI-5603.01
period = 0.5736183
t0 = 2635.46355

# 2. Hitung nomor transit untuk setiap titik pengamatan
# Rumus: N = round((t - T0) / P)
time_val = lc_flat.time.value
transit_number = np.round((time_val - t0) / period)

# Pisahkan mask transit genap dan ganjil
even_mask = (transit_number % 2 == 0)
odd_mask = (transit_number % 2 != 0)

lc_even = lc_flat[even_mask]
lc_odd = lc_flat[odd_mask]

# 3. Phase Folding masing-masing kelompok
print("2. Melipat kurva cahaya kelompok genap dan ganjil...")
folded_even = lc_even.fold(period=period, epoch_time=t0)
folded_odd = lc_odd.fold(period=period, epoch_time=t0)

# 4. Binning kurva untuk mengukur profil transit rata-rata
bin_size = 0.003  # ~4.3 menit
binned_even = folded_even.bin(time_bin_size=bin_size)
binned_odd = folded_odd.bin(time_bin_size=bin_size)

# 5. Estimasi kedalaman numerik sederhana di sekitar fase 0
mask_transit_window = lambda binned: (binned.time.value > -0.015) & (binned.time.value < 0.015)

depth_even = 1.0 - np.nanmin(binned_even[mask_transit_window(binned_even)].flux.value)
depth_odd = 1.0 - np.nanmin(binned_odd[mask_transit_window(binned_odd)].flux.value)

diff_depth = abs(depth_even - depth_odd)
ratio_depth = (depth_odd / depth_even) if depth_even > 0 else 0

print(f"\n--- HASIL PENGUKURAN KEDALAMAN ---")
print(f"Kedalaman Transit Genap (Even) : {depth_even * 100:.4f}% ({depth_even*1e6:.1f} ppm)")
print(f"Kedalaman Transit Ganjil (Odd) : {depth_odd * 100:.4f}% ({depth_odd*1e6:.1f} ppm)")
print(f"Selisih Kedalaman (|Even - Odd|): {diff_depth * 100:.4f}% ({diff_depth*1e6:.1f} ppm)")
print(f"Rasio Kedalaman (Odd / Even)   : {ratio_depth:.3f}")

# 6. Plot Perbandingan Kurva (Overlay)
plt.figure(figsize=(10, 5))

# Plot titik binned dan garis profil
plt.plot(binned_even.time.value, binned_even.flux.value, color='dodgerblue', lw=2.2, 
         label=f'Even Transits (Depth ~ {depth_even*100:.3f}%)')
plt.plot(binned_odd.time.value, binned_odd.flux.value, color='crimson', lw=2.2, linestyle='--',
         label=f'Odd Transits (Depth ~ {depth_odd*100:.3f}%)')

plt.xlim(-0.06, 0.06)
plt.ylim(0.997, 1.003)
plt.axvline(0, color='gray', linestyle=':', alpha=0.7)

plt.title("Odd-Even Transit Depth Test - TOI-5603.01")
plt.xlabel("Waktu Relatif terhadap Transit Tengah (Hari)")
plt.ylabel("Normalized Flux")
plt.legend(loc='lower right')
plt.grid(True, linestyle="--", alpha=0.4)

plt.show()