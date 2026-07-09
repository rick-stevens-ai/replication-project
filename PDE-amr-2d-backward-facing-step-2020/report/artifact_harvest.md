# Artifact Harvest

## Primary paper (paywalled)
- **DOI**: 10.1142/S0219876220410121  (World Scientific, Int. J. Comp. Methods, 2020)
- **Title**: Accuracy Verification of a 2D Adaptive Mesh Refinement Method Using Backward-Facing Step Flow of Low Reynolds Numbers
- **Authors**: Zhenquan Li, Miao Li
- **S2 paperId**: 09d810e147c2604883286a775e195576f7d3a0e0  |  MAG 3035175284  |  CorpusId 209068510
- **Access attempts (all failed for full text)**:
  - `doi.org/10.1142/s0219876220410121` -> WSPC -> HTTP 403 Cloudflare bot challenge
  - `api.unpaywall.org/v2/10.1142/s0219876220410121` -> `is_oa=False`, 0 OA locations
  - `arxiv.org/search/?query=Li+Li+2020+adaptive+mesh+refinement+backward+facing+step` -> 0 hits
  - ResearchGate profile `Zhenquan-Li` reachable but PDF not openly linked
  - Zenodo / OSTI: nothing indexed under this DOI
- **Recovered content**: verbatim abstract + tldr + metadata via Semantic Scholar (S2)
  - `work/s2_paper.json`  (S2 API response, 2.4 kB)
  - `work/paper_metadata.md`  (curated metadata block)
  - `paper.pdf`  (2.7 kB abstract-only stand-in generated with reportlab)
  - `extraction/marker.md`  (stand-in: abstract with `STAND-IN` header)
  - `extraction/nougat.mmd`  (stand-in: same)

## Companion / benchmark reference data (public)

- **Armaly et al. 1983** experimental x_r/S(Re) at ER=1.94 (backward-facing step), J. Fluid
  Mech. 127:473-496.  10-point table hard-coded in `work/reference_data.py`
  (representative published values).
- **Erturk 2008** numerical x_r/S(Re) at ER=2.00, Comp. Fluids 37(6):633-655 (stream-function
  vorticity finite-difference reference solutions).  10-point table hard-coded in
  `work/reference_data.py`.
- Combined machine-readable dump: `report/evidence/reference_bfs_data.json`.

## Code artifacts (all in `work/`)

| File | LOC | Role |
|---|---|---|
| `bfs_psi_omega.py` | ~330 | 2D BFS solver: stream-function/vorticity, hybrid convection, sparse LU psi-Poisson, RK2 |
| `amr_sweep.py`     | ~85  | Multi-grid driver for BFS refinement runs (unused in final due to solver limitation) |
| `vdamr_synthetic.py` | ~230 | Manufactured-analytical-psi VDAMR verifier (independent test of paper's method claim) |
| `vdamr_analysis.py` | ~90 | Post-processor: self-convergence order + monotonicity of flag_frac |
| `reference_data.py` | ~80 | Curated Armaly1983 + Erturk2008 reference tables + Re-convention conversion |

Total: ~815 LOC of independent Python.

## Data artifacts

- `report/evidence/synthetic_v2/vdamr_synthetic.json`  (6-grid manufactured sweep)
- `report/evidence/synthetic_v2/vdamr_synthetic.csv`
- `report/evidence/synthetic_v2/vdamr_analysis.json`  (convergence-order summary)
- `report/evidence/synthetic/vdamr_synthetic.{json,csv}`  (v1 sweep with different vortex params, for provenance)
- `report/evidence/nsrun/Re{50,100,200}_dx01.{json,npz}`  (BFS-NS runs at dx=0.1)
- `report/evidence/nsrun/refine_Re50_dx{0.25,0.15,0.10,0.075}.{json,npz}`  (Re=50 mesh-refinement)
- `report/evidence/reference_bfs_data.json`  (Armaly + Erturk consolidated)
- `report/evidence/smoke/*` (initial diagnostic runs)
- `report/evidence/llm_judge_result.json`  (Argo Opus 4.8 verdict)

## Sizes / checksums

- All NPZ dumps < 300 kB each (~13 files, total ~2 MB)
- JSON summaries < 20 kB each
- paper.pdf: 2 759 bytes
