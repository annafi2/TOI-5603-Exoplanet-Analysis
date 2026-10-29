# Photometric Vetting & Physical Characterization of USP Candidate TOI-5603.01 (TIC 224293782)

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Library-Lightkurve](https://img.shields.io/badge/Library-Lightkurve-orange.svg)](https://docs.lightkurve.org/)
[![Mission-TESS](https://img.shields.io/badge/Mission-NASA%20TESS-red.svg)](https://tess.mit.edu/)
[![Status-Planet%20Candidate](https://img.shields.io/badge/Disposition-Planet%20Candidate-yellow.svg)](https://exofop.ipac.caltech.edu/tess/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A Python pipeline that reduces TESS photometry of the ultra-short-period (USP) exoplanet candidate **TOI-5603.01** (**TIC 224293782**), runs photometric vetting tests, and derives its physical parameters analytically.

---

## 🔭 Target Overview

**TOI-5603.01** is a USP sub-Saturn/Neptunian candidate orbiting an F-type star. Its orbital period is $13.77\text{ hours}$ ($P = 0.57362\text{ days}$). The planet orbits at $0.0153\text{ AU}$ and receives extreme irradiation and tidal forcing, which makes it a useful target for studies of atmospheric evolution and tidal decay.

### Stellar & Planetary Parameters Summary

| Parameter | Symbol | Value | Unit | Source / Note |
| :--- | :---: | :---: | :---: | :--- |
| **Target Identifier** | - | TIC 224293782 | - | ExoFOP-TESS / MAST |
| **Effective Temperature** | $T_{\text{eff}}$ | $6712 \pm 144$ | $\text{K}$ | ExoFOP Host Catalog |
| **Surface Gravity** | $\log g$ | $3.94 \pm 0.09$ | $\text{cgs}$ | Stellar Atmosphere Fit |
| **Stellar Radius** | $R_*$ | $2.12 \pm 0.12$ | $R_\odot$ | TESS Input Catalog (TIC v8.2) |
| **Stellar Mass (Derived)** | $M_*$ | $\approx 1.45$ | $M_\odot$ | F-type Main-Sequence / Subgiant |
| **Orbital Period** | $P$ | $0.5736183$ | $\text{days}$ | Multi-Sector Phase Folding |
| **Transit Epoch** | $T_0$ | $2459635.46355$ | $\text{BJD}$ | TESS Science Processing (SPOC/QLP) |
| **Transit Depth** | $\delta$ | $\sim 0.067 - 0.114$ | $\%$ | Lightkurve Flattening / Binning |
| **Planetary Radius** | $R_p$ | $\approx 5.99$ | $R_\oplus$ | $\approx 0.534\ R_{\text{Jup}}$ |
| **Theoretical Mass** | $M_p$ | $\approx 28.6$ | $M_\oplus$ | Chen & Kipping (2017) Scaling |
| **Semi-Major Axis** | $a$ | $0.01529$ | $\text{AU}$ | Kepler's Third Law ($\approx 2.29 \times 10^6\text{ km}$) |
| **RV Semi-Amplitude** | $K$ | $\approx 2.40$ | $\text{m/s}$ | Circular Orbit Prediction |
| **Equilibrium Temp (A=0)**| $T_{\text{eq}}$ | $\approx 3810$ | $\text{K}$ | Full Heat Redistribution |

---

## 🧪 Photometric Vetting & Diagnostic Tests

Four tests check the candidate against astrophysical false positives: grazing eclipsing binaries, blended eclipsing binaries, and background stellar contaminants.

### 1. Multi-Sector Phase Folding & Detrending
The pipeline pulls multi-sector full-frame and target-pixel data from MAST, removes instrumental systematics, and flattens the light curve with a Savitzky-Golay or moving polynomial filter. Folding at $P = 0.5736183\text{ d}$ produces a symmetric, U-shaped transit with no V-shaped features.

### 2. Odd-Even Transit Depth Test
The script groups transits by integer cycle index $N$ and measures the depth of each group:
* **Even Transits ($N = 0, 2, 4, \dots$):** Depth $\delta_{\text{even}} \approx 0.114\%$
* **Odd Transits ($N = 1, 3, 5, \dots$):** Depth $\delta_{\text{odd}} \approx 0.113\%$
* **Depth Difference:** $\Delta\delta \approx 0.001\%$ ($10\text{ ppm}$)

The depths match, as expected from a single occulting body. A binary with unequal stars would alternate deep primary and shallow secondary eclipses.

### 3. Secondary Eclipse Search (Phase 0.5)
Tidal circularization drives the eccentricity of a USP orbit toward zero ($e \approx 0$), so a secondary eclipse falls at phase $0.5$. Phase-folding the light curve with an offset of $\Delta \phi = 0.5$ shows:
* A flat normalized flux baseline at phase $0.5$.
* No thermal or optical dip, which rules out a self-luminous low-mass stellar companion such as an M dwarf.

### 4. Centroid Offset & Ground-Based Follow-up (TFOP / MuSCAT2)
* **TIC Contamination Ratio:** $0.001157$ ($< 0.12\%$), so the photometric aperture is uncrowded.
* **Multi-Band Photometry:** MuSCAT2 on the 1.52 m Telescopio Carlos Sánchez observed the target in $g, r, i, z_s$. The signal stays on the target aperture, which rules out nearby eclipsing binaries (NEBs).

---

## 📁 Repository Structure

```text
TOI-5603-Exoplanet-Analysis/
├── odd_even_test.py               # Odd-Even transit depth comparison script
├── secondary_eclipse_test.py      # Phase 0.5 secondary occultation diagnostics
├── kalkulator_parameter_toi5603.py # Physical parameter & RV amplitude calculator
├── parameter_fisis_toi5603.csv    # Exported tabulated astrophysical properties
├── catatan_parameter_toi5603.md   # Detailed characterization report
├── .gitignore                     # Git tracking exclusions
└── README.md                      # Project documentation and summary
```

---

## 🚀 Getting Started

### Prerequisites

Install Python 3.9 or newer, then install the dependencies:

```bash
pip install lightkurve astropy matplotlib numpy
```

### Running the Vetting Scripts

1. **Odd-even diagnostic:**
   ```bash
   python odd_even_test.py
   ```
2. **Secondary eclipse inspection:**
   ```bash
   python secondary_eclipse_test.py
   ```
3. **Analytical parameters and exported tables:**
   ```bash
   python kalkulator_parameter_toi5603.py
   ```

---

## 📊 Formulas

### Transit Depth & Radius Ratio
The transit depth gives the planetary radius from the occulted stellar area:
$$\frac{R_p}{R_*} = \sqrt{\delta}$$

### Semi-Major Axis (Kepler's Third Law)
With $M_p \ll M_*$:
$$a = \left( \frac{G M_* P^2}{4\pi^2} \right)^{1/3} \approx \left[ M_* (M_\odot) \times \left(\frac{P}{365.25\text{ d}}\right)^2 \right]^{1/3} \text{AU}$$

### Radial Velocity Semi-Amplitude ($K$)
The stellar reflex semi-amplitude sets the target for spectroscopic follow-up:
$$K \approx 28.4\text{ m/s} \times \left( \frac{P}{1\text{ d}} \right)^{-1/3} \left( \frac{M_p \sin i}{M_{\text{Jup}}} \right) \left( \frac{M_*}{M_\odot} \right)^{-2/3}$$

---

## 🔮 Roadmap

- [x] Multi-sector light curve extraction and detrending.
- [x] Odd-even depth consistency test.
- [x] Secondary eclipse check at phase 0.5.
- [x] Analytic physical and orbital parameter derivation.
- [ ] Statistical validation with the Bayesian framework `TRICERATOPS` ($FPP < 0.01$, $NFPP < 0.001$).
- [ ] Transit Timing Variations (TTV) analysis to search for external perturbers.
- [ ] Radial Velocity (RV) spectroscopic follow-up proposal.

---

## 📚 References & Acknowledgments

* **TESS:** NASA's Transiting Exoplanet Survey Satellite mission.
* **Lightkurve Collaboration:** Lightkurve: *Kepler and TESS Time Series Analysis in Python* (Lightkurve Collaboration, 2018).
* **Mass-Radius Scaling:** Chen, J., & Kipping, D. (2017). *Probabilistic Forecasting of the Masses and Radii of Other Worlds*. The Astrophysical Journal, 834(1), 17.
* **ExoFOP-TESS:** Data provided by the TESS Follow-up Observing Program Working Group.
