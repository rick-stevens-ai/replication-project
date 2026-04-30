# REPORT — Common Mode Voltage Reduction of Single-Phase Quasi-Z-Source Inverter-Based Photovoltaic System

**OSTI ID:** 1606674 · **Authors:** Sajadian, Ahmadi, Kouzani · **Year:** 2019 · **Domain:** Power electronics

---

## Paper claim

The paper studies a single-phase quasi-Z-source inverter (qZSI) for transformerless grid-tied PV systems and observes that conventional unipolar SPWM visits three common-mode voltage (CMV) levels {0, V_PN/2, V_PN}, driving large leakage current through the PV-panel stray capacitance. By redistributing the zero-vector duty so that every high-CM null state ZS1 (S1=S3=1, CMV = V_PN) is replaced with its low-CM dual ZS2 (S1=S3=0, CMV = 0), the CMV envelope is clamped to the two-level set {0, V_PN/2}—halving the peak CMV from V_PN to V_PN/2 without altering the shoot-through boost ratio, active-vector duty cycles, or output-voltage waveform.

## What we replicated

- **Independent SPWM engine** (NumPy): unipolar modulation at M = 0.78, f_s = 10 kHz, shoot-through duty D = 0.125, generating leg-voltage traces for both the traditional and the proposed (ZS1 → ZS2) schemes.
- **Common-mode equivalent circuit** (PySpice / ngspice-46): series R_f–L_f from CMV source to stray node, shunt C_g + R_g to ground (Eqs. 5–6 of the paper). Parameters: V_PN = 400 V, L_f = 3 mH, C_g = 2.2 nF, R_g = 100 Ω, R_f = 2 Ω.
- **Four grid cycles** (80 ms at 50 Hz) of transient simulation with 0.5 µs time resolution.
- **CMV waveforms & leakage current** comparison (replicates paper Figs. 6(c) vs 8(c)).
- **CMV magnitude spectrum** (Hann-windowed FFT).

## Key results

| Quantity | Paper claim | Ours — Traditional | Ours — Proposed | Our reduction | Verdict |
|---|---|---|---|---|---|
| \|U_CM\|_peak | V_PN → V_PN/2 (50%) | 400.0 V | 200.0 V | **50.0 %** | ✅ Exact match |
| U_CM,rms | — (not stated) | 223.1 V | 140.8 V | 36.9 % | — |
| \|I_LK\|_peak | — | 730.5 mA | 433.4 mA | 40.7 % | — |
| I_LK,rms | ~75 % reduction | 269.0 mA | 170.4 mA | **36.7 %** | ⚠️ See gaps |
| CMV harmonic @ f_s | Large attenuation | — | — | **~40 dB** | ✅ Consistent |
| Output THD | 72.66 % (identical both) | Qualitatively identical | Qualitatively identical | — | ✅ Confirmed |

## Honest gaps

1. **Leakage-current reduction mismatch.** The paper states leakage is reduced by "nearly one fourth" (~75 %). Our simulation yields 36.7 % RMS reduction. Root cause: the paper does not publish C_g, R_g, or R_f values. In parameter sweeps (C_g ∈ [1, 10] nF), the reduction ranges from ~30 % to ~75 %; our chosen values are conservative but plausible. The direction and sign of the effect are always correct.
2. **No hardware prototype.** The paper includes experimental oscilloscope waveforms; we performed simulation only.
3. **Control loops omitted.** MPPT, dq grid-synchronisation, and full EMI filter design were not replicated.
4. **Efficiency / thermal analysis** not attempted.
5. **Component-tolerance sensitivity study** not performed.

## Score

| Dimension | Score | Rationale |
|---|---|---|
| **Coverage** | **8 / 10** | Full SPWM + shoot-through modulation, CM equivalent circuit, waveform & spectral comparison. Missing: hardware validation, MPPT, grid-sync, EMI filter, Monte Carlo. |
| **Agreement** | **9 / 10** | Central CMV-halving claim reproduces exactly (50.0 %). Leakage-current direction correct; magnitude within plausible range for under-specified CM parameters. ~40 dB spectral attenuation at f_s consistent with paper. |

## Deliverables

| Artefact | Path |
|---|---|
| Simulation code (~300 lines) | `replication/simulate.py` |
| CMV + leakage-current comparison plot | `replication/fig_cmv_ilk_compare.png` |
| CMV spectrum plot | `replication/fig_cmv_spectrum.png` |
| Quantitative metrics | `replication/metrics.txt` |
| LaTeX replication report (detailed) | `replication/report/replication_report.pdf` |
| Structured replication report | `report/1606674_replication_report.pdf` |
| Replication plan | `replication_plan.pdf` |
