# Artifact Harvest — OSTI 3366861

| # | Artifact | URL | Size (B) | Local path |
|---|---|---|---|---|
| 1 | Paper PDF | https://www.osti.gov/servlets/purl/3366861 | 2 781 106 | `paper.pdf`, `work/paper.pdf` |
| 2 | SCULPT source (git) | https://github.com/AMOS-experiment/CoInML.git | — (git clone) | uicgpu:~/sculpt-work/CoInML/ |
| 3 | D₂O sample dataset (zip) | https://zenodo.org/api/records/18478576/files/D2O_dataset.zip/content | 56 502 479 | uicgpu:~/sculpt-work/D2O_dataset.zip |
| 4 | D₂O per-state files (unzipped) | (from zip #3) | see below | uicgpu:~/sculpt-work/D2O_data/D2O_dataset/*.dat |
| 5 | Zenodo record metadata | https://zenodo.org/api/records/18478576 | ~10 000 | uicgpu:/tmp/zen.json |

## D₂O per-state files (from Zenodo)

| File | Bytes | Events | Quantum state |
|---|---|---|---|
| group1_3A2.dat | 24 194 514 | 181 468 | ³A₂ (triplet A₂) → O(³P) |
| group1_3B1.dat | 3 838 050 | 28 791 | ³B₁ (triplet B₁) → O(³P) |
| group1_3B2.dat | 42 807 621 | 320 972 | ³B₂ (triplet B₂) → O(³P) |
| group2_1A2.dat | 10 394 453 | 77 890 | ¹A₂ (singlet A₂) → O(¹D) |
| group2_1B1.dat | 3 351 029 | 25 100 | ¹B₁ (singlet B₁) → O(¹D) |
| group2_1B2.dat | 23 146 875 | 173 364 | ¹B₂ (singlet B₂) → O(¹D) |
| group2_2_1A1.dat | 13 587 732 | 101 704 | 2¹A₁ → O(¹D) |
| group3_3_1A1.dat | 5 866 414 | 43 831 | 3¹A₁ → O(¹S) |
| **TOTAL** | **127 186 688** | **953 120** | 8 states |

Each row = 15 float columns (px, py, pz for D1, D2, O, e1, e2) in atomic units. Header row present.

## Referenced but not pulled

- Reedy et al. 2018 (Ref. 34 in paper) — H₂O dication analysis used as ground-truth basis. Not needed for our replication (Zenodo files are already labeled by quantum state).
- Streeter et al. 2018 (Ref. 43) — theoretical slingshot-mechanism ab initio calcs. Cited as future work by paper, not needed for replication.
- Venkatachalam 2025 (Ref. 27), Li 2025 (Ref. 28) — concurrent ML-CEI papers, comparison only, not needed.
