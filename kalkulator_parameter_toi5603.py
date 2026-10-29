import math
import csv

def hitung_dan_ekspor_eksoplanet(nama_planet, tic_id, period_hari, depth_fraction, r_star_surya, teff_star, m_star_surya):
    """
    Menghitung parameter fisis eksoplanet dan mengekspor hasilnya ke CSV dan Markdown.
    """
    # ---------------------------------------------------------
    # 1. PERHITUNGAN ASTROFISIKA
    # ---------------------------------------------------------
    # Radius Planet
    rp_over_rstar = math.sqrt(depth_fraction)
    rp_surya = r_star_surya * rp_over_rstar
    rp_bumi = rp_surya * 109.2
    rp_jupiter = rp_surya * 9.73

    # Estimasi Massa Teoretis (Chen & Kipping 2017)
    mp_bumi = 0.97 * (rp_bumi ** 1.89)
    mp_jupiter = mp_bumi / 317.8

    # Orbit (Hukum III Kepler)
    period_tahun = period_hari / 365.25
    a_au = (m_star_surya * (period_tahun ** 2)) ** (1.0 / 3.0)
    a_km = a_au * 149597870.7

    # Semi-Amplitudo Kecepatan Radial (RV)
    k_rv = 28.4 * (period_hari ** (-1.0 / 3.0)) * mp_jupiter * (m_star_surya ** (-2.0 / 3.0))

    # Radiasi & Temperatur Kesetimbangan
    r_star_km = r_star_surya * 695700.0
    teq_a0 = teff_star * math.sqrt(r_star_km / (2.0 * a_km))
    teq_a03 = teq_a0 * ((1.0 - 0.3) ** 0.25)
    
    l_star = (r_star_surya ** 2) * ((teff_star / 5778.0) ** 4)
    insolasi = l_star / (a_au ** 2)

    # ---------------------------------------------------------
    # 2. STRUKTUR DATA TABEL
    # Format: [Kategori, Nama Parameter, Simbol, Nilai, Satuan, Keterangan]
    # ---------------------------------------------------------
    tabel_data = [
        ["Geometri", "Rasio Radius", "Rp / R*", f"{rp_over_rstar:.5f}", "-", "Akar dari kedalaman transit"],
        ["Geometri", "Radius Planet (Bumi)", "Rp", f"{rp_bumi:.2f}", "R_Earth", "Ukuran relatif thd Bumi"],
        ["Geometri", "Radius Planet (Jupiter)", "Rp", f"{rp_jupiter:.3f}", "R_Jup", "Kelas Sub-Saturn / Gas Giant"],
        ["Massa", "Massa Teoretis (Bumi)", "Mp", f"{mp_bumi:.1f}", "M_Earth", "Relasi empiris Chen & Kipping (2017)"],
        ["Massa", "Massa Teoretis (Jupiter)", "Mp", f"{mp_jupiter:.3f}", "M_Jup", "Perkiraan massa analitis"],
        ["Orbit", "Sumbu Semi-Mayor", "a", f"{a_au:.5f}", "AU", "Jarak orbit via Hukum Kepler III"],
        ["Orbit", "Jarak ke Pusat Bintang", "a", f"{a_km:,.0f}", "km", "Orbit sangat rapat (USP)"],
        ["Spektroskopi", "Semi-Amplitudo RV", "K", f"{k_rv:.2f}", "m/s", "Goyangan bintang target deteksi"],
        ["Termal", "Insolasi Relatif", "S", f"{insolasi:,.0f}", "S_Earth", "Fluks radiasi dibanding Bumi"],
        ["Termal", "Temperatur Ekuilibrium (A=0)", "Teq", f"{teq_a0:.0f}", "Kelvin", "Model albedo nol & panas merata"],
        ["Termal", "Temperatur Ekuilibrium (A=0.3)", "Teq", f"{teq_a03:.0f}", "Kelvin", "Model albedo atmosferik tipikal"],
    ]

    # Cetak ringkasan singkat ke terminal
    print(f"\nPerhitungan selesai untuk {nama_planet}!")
    print(f"Radius: {rp_bumi:.2f} R_Earth | Massa: {mp_bumi:.1f} M_Earth | a: {a_au:.5f} AU | K: {k_rv:.2f} m/s")

    # ---------------------------------------------------------
    # 3. FUNGSI EKSPOR KE CSV
    # ---------------------------------------------------------
    nama_csv = "parameter_fisis_toi5603.csv"
    with open(nama_csv, mode="w", newline="", encoding="utf-8") as f_csv:
        writer = csv.writer(f_csv)
        # Tulis Header Kolom
        writer.writerow(["Kategori", "Parameter", "Simbol", "Nilai", "Satuan", "Keterangan"])
        # Tulis Seluruh Baris Data
        writer.writerows(tabel_data)
    print(f"[v] Berhasil mengekspor tabel ke CSV : {nama_csv}")

    # ---------------------------------------------------------
    # 4. FUNGSI EKSPOR KE MARKDOWN
    # ---------------------------------------------------------
    nama_md = "catatan_parameter_toi5603.md"
    with open(nama_md, mode="w", encoding="utf-8") as f_md:
        f_md.write(f"# Laporan Karakterisasi Fisis: {nama_planet}\n\n")
        f_md.write(f"- **ID Katalog:** TIC {tic_id}\n")
        f_md.write(f"- **Periode Orbit:** {period_hari} hari (~{period_hari*24:.1f} jam)\n")
        f_md.write(f"- **Kedalaman Transit:** {depth_fraction*100:.3f}%\n")
        f_md.write(f"- **Radius Bintang ($R_*$):** {r_star_surya} $R_\\odot$\n")
        f_md.write(f"- **Suhu Bintang ($T_{{eff}}$):** {teff_star:.0f} K\n\n")
        f_md.write("## Tabel Parameter Turunan\n\n")
        
        # Header Tabel Markdown
        f_md.write("| Kategori | Parameter | Simbol | Nilai | Satuan | Keterangan |\n")
        f_md.write("| :--- | :--- | :---: | :---: | :---: | :--- |\n")
        
        # Isi Baris Tabel
        for kat, param, symb, val, unit, note in tabel_data:
            f_md.write(f"| {kat} | {param} | `{symb}` | {val} | {unit} | {note} |\n")
        
        f_md.write("\n> *Catatan: Nilai massa dan kecepatan radial dihitung secara empiris analitis untuk keperluan perencanaan observasi lanjutan dan validasi statistik.* \n")
        
    print(f"[v] Berhasil mengekspor catatan ke MD  : {nama_md}\n")

# =============================================================
# EKSEKUSI DATA TOI-5603.01
# =============================================================
if __name__ == "__main__":
    hitung_dan_ekspor_eksoplanet(
        nama_planet="TOI-5603.01",
        tic_id="224293782",
        period_hari=0.5736183,
        depth_fraction=0.00067,
        r_star_surya=2.12,
        teff_star=6712.0,
        m_star_surya=1.45
    )