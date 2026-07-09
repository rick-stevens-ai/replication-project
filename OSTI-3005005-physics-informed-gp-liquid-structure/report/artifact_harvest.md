# Artifact Harvest — OSTI-3005005

## Public artifacts pulled

| # | Artifact | URL | Size | Notes |
|---|----------|-----|------|-------|
| 1 | OSTI PDF (full paper) | https://www.osti.gov/servlets/purl/3005005 | 4,296,913 B (4.30 MB) | v1.4 PDF, 14 pages. Downloaded on uicgpu (Argonne proxy), scp'd to local. `sha256 = c1feb…` (see file). |
| 2 | JPCB DOI record | https://doi.org/10.1021/acs.jpcb.5c05024 | — | Published 2025-10-31; CC-BY 4.0 license, so redistribution/use is fine. |
| 3 | Authors' code repo (referenced, not pulled) | https://github.com/hoepfnergroup/LiquidStructureGP-Sullivan | — | Paper's Data Availability statement lists this repo; we deliberately did not clone it to keep the replication independent. Our implementation is written from scratch reading only the paper text. |
| 4 | Supporting Information (referenced, not pulled) | pubs.acs.org SI ZIP + PDF | — | SI includes tabulated hyperparameters, posterior means/covariances, and full detailed math. Would be helpful for tighter numerical comparison against the paper's exact argon/water numbers. |

## Public references cited by the paper (not pulled, cited for context)

- Yarnell et al. 1973 neutron scattering of liquid argon (ref 29 in the paper).
- Skinner et al. broadened X-ray liquid water (ref 23).
- TIP4P/2005f flexible water model (Gonzalez & Abascal, ref 44).

## Ground-truth data generated in this replication

- Percus-Yevick hard-sphere S(q) and g(r) computed analytically in `work/gp_liquid_structure.py` using Ashcroft-Lekner / Wertheim closed forms.
- σ_HS = 3.16 Å, ρ = 0.02125 Å⁻³ (paper's argon density), packing fraction η = 0.351.

## Files produced

| File | Bytes | Description |
|------|-------|-------------|
| `report/evidence/metrics.json` | ~1.5 KB | All numeric outcomes (RMSE, coverage, peak stats, hyperparameters). |
| `report/evidence/arrays.npz` | ~175 KB | Raw numeric arrays for the figures. |
| `report/evidence/gp_liquid_structure.png` | ~156 KB | S(q) and g(r) posterior figure. |
| `report/evidence/llm_judge.txt` | ~5 KB | argo:gpt-5 judge transcript. |
| `report/evidence/llm_judge_second.txt` | ~2 KB | argo:claude-sonnet-4.6 judge transcript. |
| `work/paper.pdf` | 4,296,913 B | The downloaded OSTI PDF. |
| `work/paper.txt` | ~69 KB | pymupdf text extraction. |
| `work/gp_liquid_structure.py` | ~21 KB | Full replication implementation. |
| `work/llm_judge.py` | ~4 KB | Argo LLM-judge harness. |
