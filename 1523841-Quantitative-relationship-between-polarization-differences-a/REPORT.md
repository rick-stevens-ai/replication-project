# REPORT — Quantitative Relationship between Polarization Differences and the Zone-Averaged Shift Photocurrent

**OSTI ID:** 1523841 · **Authors:** Fregoso, Morimoto, Moore · **Year:** 2017  
**Domain:** Condensed Matter / Topological Response / Shift Current Photovoltaics  
**arXiv:** 1701.00172v2

---

## Paper claim (one paragraph)

The paper establishes that in a crystalline insulator the Brillouin-zone-averaged shift vector $\bar{R}_{cv}$ — the quantity that controls the frequency-integrated bulk photovoltaic (shift-current) response — is quantitatively determined by the Berry-phase polarization difference between conduction and valence bands plus an integer winding number: $e\,\bar{R}_{cv} = a\,(P_c - P_v) + W_{cv}\,e\,a$ (Eq. 9). The winding number $W_{cv} \in \mathbb{Z}$ originates from the interband dipole phase and changes by ±1 at topological transitions where the band gap closes. This identity generalizes to multi-band systems via Eq. 17 and is demonstrated analytically and numerically on the 1D Rice–Mele model (Fig. 1(b)), a three-band model (Sec. IV / Fig. 2), and 2D extensions (Sec. V).

## What we replicated

| Aspect | Status |
|--------|--------|
| **Central identity (Eq. 9)** on 1D Rice–Mele model | ✅ Verified to machine precision ($3.3 \times 10^{-16}$ max residual) |
| **Closed-form shift vector** (Eq. C5, d-vector formula) | ✅ Implemented and validated |
| **Analytic limits** (Eqs. D8–D9) at $k \to 0$ and $k \to \pi/a$ | ✅ Reproduced to $< 3 \times 10^{-16}$ |
| **Berry connections** from paper Eq. D4 | ✅ Used for gauge-consistent polarization calculation |
| **Fig. 1(b) reproduction** — $a(P_c - P_v)$, $e\bar{R}_{cv}$ (d-vector), and full numerical $e\bar{R}_{cv}$ vs. $\delta/t$ | ✅ Qualitative and quantitative match |
| **Winding-number discontinuity** ($\Delta W_{cv} = 1$) at gap-closing $\delta = 0$ | ✅ Observed as expected |
| **Multi-band extension** (Eq. 17 / Wilson-loop generalization) | ✅ Verified on 3-band trimer, 4-band coupled RM, and 1D BHZ-like models |

### Not reproduced

- 2D extension (Sec. V) and three-band example of Sec. IV / Fig. 2 from the original paper
- Explicit shift-conductivity spectrum $\sigma^{zzz}(\omega)$ (Eq. D16)
- Material-specific DFT+Wannier calculations (GeS, BaTiO₃, monolayer WS₂)
- Paper Figs. 2–4

## Key results (paper vs ours)

| Quantity | Paper | This work | Difference |
|----------|-------|-----------|------------|
| Shift-vector limit $R_{cv}(k\to 0)$, $\delta=0.3$, $\Delta=0.5$ | $-0.745356$ | $-0.745356$ | $2.2 \times 10^{-16}$ |
| Shift-vector limit $R_{cv}(k\to\pi)$, $\delta=0.3$, $\Delta=0.5$ | $-0.128624$ | $-0.128624$ | $5.6 \times 10^{-17}$ |
| Shift-vector limit $R_{cv}(k\to 0)$, $\delta=0.7$, $\Delta=0.5$ | $-0.319438$ | $-0.319438$ | $5.6 \times 10^{-17}$ |
| Shift-vector limit $R_{cv}(k\to\pi)$, $\delta=0.7$, $\Delta=0.5$ | $-0.203433$ | $-0.203433$ | $0$ |
| Shift-vector limit $R_{cv}(k\to 0)$, $\delta=-0.4$, $\Delta=0.5$ | $+0.559017$ | $+0.559017$ | $1.1 \times 10^{-16}$ |
| Shift-vector limit $R_{cv}(k\to\pi)$, $\delta=-0.4$, $\Delta=0.5$ | $+0.156174$ | $+0.156174$ | $2.8 \times 10^{-17}$ |
| Identity residual $e\bar{R}_{cv} - a(P_c - P_v)$ ($\delta > 0$, mean) | $0$ (exact) | $-7 \times 10^{-16}$ | Machine precision |
| Identity residual $e\bar{R}_{cv} - a(P_c - P_v)$ ($\delta < 0$, mean) | $0$ (exact) | $+7 \times 10^{-16}$ | Machine precision |
| Max pointwise deviation from integer | $0$ (exact) | $3.33 \times 10^{-16}$ | Machine precision |
| Winding-number jump at $\delta = 0$ | $\Delta W_{cv} = 1$ | $\Delta W_{cv} = 1$ | Exact match |
| Full numerical vs. d-vector $\|\bar{R}^{\text{num}} - \bar{R}^{\text{d-vec}}\|$ | $|W_{cv}| = 1$ | $1.00 \pm 10^{-3}$ | Consistent |

## Honest gaps

1. **No 2D or higher-dimensional tests.** The paper's Sec. V (2D extension) and parts of Sec. IV (three-band model shown in Fig. 2) were not replicated. These require multi-band smooth-gauge Berry connections in 2D, which is conceptually identical but more involved implementation work.

2. **No shift-conductivity spectrum.** The explicit $\sigma^{zzz}(\omega)$ spectrum from Eq. D16 was not computed — it is a downstream observable from the same shift vector and does not independently test the central identity.

3. **No material-specific calculations.** The paper's connection to real materials (GeS, BaTiO₃, WS₂) via DFT+Wannier was entirely outside scope. This is the dominant blocker (friction category F7: missing surrogate calculators).

4. **Multi-band extension uses new models, not the paper's three-band model.** The tier-lift verification used a custom 3-band trimer, 4-band coupled RM, and 1D BHZ-like model rather than the specific three-band model from the paper's Sec. IV.

5. **KSV gauge subtlety.** The paper's Bloch Hamiltonian uses half-angle arguments ($\cos(ka/2)$, $\sin(ka/2)$), making it $4\pi/a$-periodic. Naive King–Smith–Vanderbilt overlap products fail without a sewing matrix at the BZ boundary. This was resolved by using the paper's closed-form Berry connections (Eq. D4) directly.

## Score

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Coverage** | **8/10** | Core 1D identity, all analytic limits, Fig. 1(b), and winding structure reproduced. Multi-band extension adds beyond-paper verification. Missing: 2D model, three-band figure, material-specific DFT. |
| **Agreement** | **10/10** | Every reproduced quantity matches to machine precision ($\sim 10^{-16}$). No discrepancies found between our numerics and the paper's predictions. |

## Deliverables

| Artifact | Path |
|----------|------|
| Main replication code (Rice–Mele) | `replication/code/rice_mele.py` |
| Multi-band extension code | `replication/code/multiband_extension.py` |
| Fig. 1(b) reproduction | `replication/figures/fig1b_rice_mele.pdf` |
| Identity-check residual plot | `replication/figures/identity_check.pdf` |
| Band-structure plot | `replication/figures/bands.pdf` |
| Numerical data archive | `replication/figures/rice_mele_data.npz` |
| Detailed replication report (LaTeX) | `replication/report/replication_report.tex` |
| Compiled replication report | `replication/report/replication_report.pdf` |
| Compiled top-level report | `report/1523841_replication_report.pdf` |
| Replication plan | `replication_plan_1523841.pdf` |

**Runtime:** < 60 s on a laptop. Dependencies: Python 3, NumPy, Matplotlib only. $N_k = 4001$, 100 $\delta$-points.
