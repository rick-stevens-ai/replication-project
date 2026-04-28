# Common Mode Voltage Reduction of Single-Phase Quasi-Z-Source Inverter-Based Photovoltaic System

- **OSTI ID:** 1606674
- **Rank:** #8
- **Replication Score:** 9/10

## Why This Paper
The paper presents a computational analysis of inverter modulation methods with clear equations, simulation outputs, and quantitative metrics, making it highly suitable for AI replication.

## Replication Plan
AI would implement the inverter topology and modulation schemes in circuit simulation software, reproduce equations and switching states, and generate quantitative results for CMV and leakage current under various scenarios.

## Status
- [x] Paper reviewed
- [x] Data identified
- [x] Code implemented
- [x] Results validated

## Replication Summary (2026-04-23, Ollie / OpenClaw)

**Independent implementation:** `replication/simulate.py`
- NumPy SPWM generator (unipolar, $M=0.78$, $f_s=10$ kHz, shoot-through $D=0.125$) producing leg-voltage traces for both the traditional and the proposed (ZS1$\to$ZS2) modulation.
- PySpice / ngspice-46 transient analysis of the common-mode equivalent circuit (Eq.~5–6 of the paper) with $L_f=3$ mH, $C_g=2.2$ nF, $R_g=100\,\Omega$, $R_f=2\,\Omega$.

**Key numerical results:**
| Quantity | Traditional | Proposed | Reduction |
|---|---|---|---|
| $\lvert U_\text{CM}\rvert_\text{peak}$ | 400.0 V | 200.0 V | **50.0 %** |
| $U_\text{CM,rms}$ | 223.1 V | 140.8 V | 36.9 % |
| $\lvert I_\text{LK}\rvert_\text{peak}$ | 730 mA | 433 mA | 40.7 % |
| $I_\text{LK,rms}$ | 269 mA | 170 mA | 36.7 % |

The CMV-halving claim reproduces **exactly** (the proposed scheme clamps CMV to $\{0,V_{PN}/2\}$ while the traditional scheme visits $\{0,V_{PN}/2,V_{PN}\}$). The switching-harmonic line at $f_s=10$ kHz in the CMV spectrum drops by $\sim$40 dB.

**Deliverables:**
- `replication/simulate.py` — full simulation code
- `replication/fig_cmv_ilk_compare.png` — CMV + leakage current comparison (replicates Fig. 6(c) vs 8(c))
- `replication/fig_cmv_spectrum.png` — CMV spectrum
- `replication/metrics.txt` — quantitative metrics
- `replication/report/replication_report.pdf` — LaTeX report

**Score: 4 / 5** — central claim reproduced exactly; leakage-current ratio within the range consistent with unspecified CM-path parameters; no experimental quantities attempted.
