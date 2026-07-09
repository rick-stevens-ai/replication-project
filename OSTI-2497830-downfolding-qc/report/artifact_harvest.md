# Artifact Harvest — OSTI-2497830

| # | Artifact | URL / Accession | Size / Info | Where kept |
|---|---|---|---|---|
| 1 | Paper PDF (Fermilab accepted MS, PhysRevApplied) | https://www.osti.gov/servlets/purl/2497830 | 2,173,727 B (≈ 2.17 MB) | `work/osti_2497830.pdf` |
| 2 | Paper plain-text extraction | (local, via `pdftotext -layout`) | 997 lines | `work/osti_2497830.txt` |
| 3 | Ca2CuO3 downfolded-model parameters (Appendix C.1) | Paper §III.A + Appendix C.1 | t = −0.491 eV, U = 3.578 eV, V = 0.903 eV | `work/ca2cuo3_ed.py` (encoded) |
| 4 | WTe2 downfolded-model parameters (Appendix C.2) | Paper Appendix C.2 | 4×4 hopping/on-site/off-site matrices, 4 bands | `work/osti_2497830.txt` (extracted) |
| 5 | SrVO3 downfolded-model parameters (Appendix C.3) | Paper Appendix C.3 | tₙₙ = −0.263, U = 3.527, V = 0.649 eV (band 1) | `work/srvo3_charge_order.py` (encoded) |
| 6 | Paper Table I / II results (DMRG + VQE energies + fidelities) | Paper §III + Table I / II | Ca2CuO3: 6.005 / 6.028 eV, F=99.3%; WTe2: 115.029 / 115.097 eV, F=96.2%; SrVO3: −105.383 / −105.365 eV, F=31.8% | in this report |
| 7 | Ca2CuO3 ED reproduction script | (this replication) | 8,224 B | `work/ca2cuo3_ed.py` |
| 8 | Ca2CuO3 ED result JSON | (this replication) | E0 + spin correlations | `report/evidence/ca2cuo3_ed_results.json` |
| 9 | SrVO3 sanity-check script | (this replication) | 6,996 B | `work/srvo3_charge_order.py` |
| 10 | SrVO3 sanity-check JSON | (this replication) | E0, site occupancies, Φ at 3 U/V settings | `report/evidence/srvo3_ed_results.json` |

**Public code from the authors:** none released. The 3 authors (Alvertis@NASA Ames/KBR, Khan@UIUC, Tubman@NASA Ames) do not link a Zenodo/GitHub repo for this paper. Their tensor-network VQE machinery is described in their Ref. [39] (Khan, Clark, Tubman, arXiv:2310.12965), and the underlying tensor operations use the `ITensor` package (Ref. [58]).

**Software dependencies for full reproduction of the authors' pipeline (not run here):**
- Quantum ESPRESSO (DFT starting point, PBE functional, ONCV pseudopotentials from Pseudo Dojo)
- Wannier90 (maximally localized Wannier functions)
- wan2respack + RESPACK (cRPA screened Coulomb integrals)
- ITensor (tensor-network / MPS/MPO)
- their own tensor-network VQE code (unpublished as of the paper)

**Software used in this replication:**
- Python 3, NumPy 2.4.3, SciPy 1.18.0 (Lanczos via `scipy.sparse.linalg.eigsh`)
- No GPU needed for the 63,504-dim ED — ran in 0.82 s on CherryRd laptop.
