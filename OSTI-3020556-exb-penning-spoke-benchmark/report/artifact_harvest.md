# Artifact Harvest

All artifacts fetched through the `uicgpu` proxy (`source ~/env.sh`); CherryRd times out on osti.gov / arxiv.org directly.

| Artifact | Source URL | Size | MD5 | Notes |
|---|---|---|---|---|
| OSTI OA PDF (target paper) | https://www.osti.gov/servlets/purl/3020556 | 2,248,946 B | `be1c310af9afc45c53ecf4cef200634e` | Powis et al 2026, PSST 35 025002; DOI 10.1088/1361-6595/ae3985 |
| Ref [93] PDF (formula source) | https://arxiv.org/pdf/1805.04438 | 3,121,824 B | `6f7769ad37a960cd8d0bd88b37c041b9` | Powis, Carlsson, Kaganovich, Raitses, Smolyakov 2018, "Scaling of Spoke Rotation Frequency within a Penning Discharge" (Phys. Plasmas 25, 072110). Contains Eq. 3–4. |

Local copies: `work/osti_3020556.pdf`, `work/ref93_powis2018_arxiv1805.04438.pdf`.

No proprietary data, no external datasets required — the replication target is a closed-form analytic formula evaluated on parameters read directly from the paper's Table 1 and Section 3.

## Key parameters (paper Table 1 + Sec 3, p.9)
- helium-4 ion mass mᵢ = 7291.712 mₑ (= 4.000 amu, verified)
- radial electric field Eᵣ ≈ 100 V/m
- gradient length scale Lₙ = 7.1 mm
- domain length Lₓ = Lᵧ = 5.0×10⁻² m (half-width 25 mm)
- applied magnetic field B = 100 G = 0.01 T
- injection radius R_inj = 5.0×10⁻³ m
- measured spoke frequency: 43.2 kHz (mean period 23.1 µs); min/max 41.1–46.1 kHz
- paper's stated analytic prediction: ~53 kHz
