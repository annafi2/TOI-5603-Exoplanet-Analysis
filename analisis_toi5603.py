import lightkurve as lk
import matplotlib.pyplot as plt

print("1. Mengunduh SEMUA sektor observasi TOI-5603 (Sektor 21, 41, 48, 75)...")

search = lk.search_lightcurve("TIC 224293782", mission="TESS", author="QLP")
print(search)


lc_collection = search.download_all()
lc_raw = lc_collection.stitch().remove_nans().normalize()

print("2. Membersihkan noise dan meratakan kurva (detrending)...")

lc_clean = lc_raw[(lc_raw.flux.value > 0.95) & (lc_raw.flux.value < 1.05)]
lc_clean = lc_clean.remove_outliers(sigma_lower=5, sigma_upper=3)


lc_flat = lc_clean.flatten(window_length=101)


period = 0.5736183
t0 = 2635.46355

print("3. Melipat seluruh data gabungan (phase folding)...")
folded_lc = lc_flat.fold(period=period, epoch_time=t0)


plt.figure(figsize=(10, 5))
ax = folded_lc.scatter(c='silver', alpha=0.2, s=8, label="Data Semua Sektor TESS")


folded_lc.bin(time_bin_size=0.004).plot(ax=ax, color='crimson', lw=2.5, label="Binned Transit Profile (Semua Sektor)")

plt.xlim(-0.06, 0.06)
plt.ylim(0.997, 1.003)
plt.axvline(0, color='blue', linestyle=':', alpha=0.7, label="Transit Center (Fase 0)")

plt.title(f"TOI-5603.01 Multi-Sector Phase Fold (P = {period:.5f} d, Depth ~ 0.067%)")
plt.xlabel("Waktu Relatif terhadap Transit Tengah (Hari)")
plt.ylabel("Normalized Flux")
plt.legend(loc='lower right')
plt.grid(True, linestyle="--", alpha=0.4)

print("Selesai! Menampilkan kurva multi-sektor...")
plt.show()