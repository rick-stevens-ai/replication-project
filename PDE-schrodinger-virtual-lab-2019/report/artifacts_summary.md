# Artifacts Summary

## Inputs pulled

| Artifact | URL / origin | Size | sha256 (paper) / commit | Notes |
|---|---|---:|---|---|
| paper.pdf | copied from sibling `PDE-Figueiras-Schrodinger-BPM-splitstep-2018/work/figueiras.pdf` (originally IOP OA) | 2,248,218 B | `034a26a1f606e6b1f5c5a0135a89d45c0ef137b5e763cabb10a190d67e933486` | Same paper as sibling (identity confirmed by sha256) |
| pyNLSE/bpm repo | https://github.com/pyNLSE/bpm.git | ~1 MB | `96d945b` (HEAD; last README fix); paper release is `916c502` "v.2" | Cloned into `work/bpm/` |
| notes_code.pdf | bundled in the repo (`work/bpm/doc/notes_code.pdf`) | 351,353 B | — | Authors' companion install + usage notes |

## Outputs produced

### Extraction
| File | Size | Method |
|---|---:|---|
| `extraction/marker.md` | 43,675 B / 656 lines | `pdftotext -layout` (poppler 26.06.0). Fallback because marker-pdf install failed on Python 3.14 (numpy pin conflict). |
| `extraction/nougat.mmd` | 38,884 B / 912 lines | `pymupdf` block extraction with heuristic heading detection (`work/pdf_to_mmd.py`). Not equivalent to Meta's nougat; documented in failure_analysis.md. |

### Simulation runs

12 example configurations executed end-to-end. Each produced (i) 100–300 PNG frames in `work/runs/<Ex>_<dim>/fig000.png…figNNN.png`, (ii) a final `.npy` of the final ψ, (iii) a density-time contour PNG, (iv) a JSON diagnostic in `work/diag/<Ex>_<dim>.json` (also copied to `report/evidence/`).

| Example | dim | Nx | dt | steps | wall (s) | PNGs | initial N | final N | rel drift | notes |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Rectangular_Barrier_1D | 1D | 1600 | 1e-4 | 60000 | 23.0 | 102 | 5.01326 | 4.93110 | −1.64e-02 | absorb loss OK |
| Sech2_Pot_1D | 1D | 2000 | 1e-3 | 200000 | 49.7 | 102 | 18.79971 | 18.16994 | −3.35e-02 | reflectionless s=10 |
| Double_Well_1D | 1D | 600 | 1e-3 | 30000 | 42.9 | 302 | 1.77245 | 1.77244 | −7.48e-06 | |
| Diffraction_Slit_1D | 1D | 1000 | 1e-4 | 4000 | 17.2 | 102 | 1.02000 | 1.01999 | −1.34e-05 | |
| Interference_Gaussians_1D | 1D | 1000 | 1e-3 | 4000 | 16.4 | 102 | 1.25331 | 1.24510 | −6.55e-03 | |
| Soliton_Emission_A_1D | 1D | 1200 | 1e-4 | 150000 | 84.6 | 302 | 2.98090 | 2.98090 | **+3.60e-11** | absorb=0, machine-precision conservation |
| Solitons_in_phase_1D | 1D | 500 | 1e-3 | 5000 | 20.1 | 102 | 3.99982 | 3.99982 | **+7.60e-13** | absorb=0, roundoff |
| Solitons_phase_opp_1D | 1D | 500 | 1e-3 | 5000 | 19.0 | 102 | 3.99981 | 3.99981 | **+7.25e-13** | absorb=0, roundoff |
| Thomas_Fermi_1D | 1D | 1000 | 5e-4 | 30000 | 48.9 | 302 | 2303.98567 | 2303.98567 | **+4.68e-12** | absorb=0, roundoff |
| Gaussian_Beam_2D | 2D | 300 | 1e-3 | 10000 | 94.3 | 203 | 1.00000 | 1.00000 | −2.16e-12 | packet doesn't reach absorb |
| Vortex_2D | 2D | 300 | 1e-3 | 10000 | 97.6 | 203 | 1.00000 | 1.00000 | −1.03e-10 | |
| Collapse_2D | 2D | 500 | 5e-3 | 1400 | 90.7 | 143 | 5.84183 | 5.84183 | **+2.72e-13** | absorb=0, roundoff, NLSE |

### Reflectionless sweep

7 runs; identical grid (Nx=4000, xmax=150, dt=0.001, tmax=80, absorb_coeff=20); identical initial Gaussian; V=−s(s+1)/(2 cosh²x) with s ∈ {1, 2, 3, 10, 0.5, 1.5, 2.5}. Results in `work/diag/reflectionless_sweep.json` (also copied to `report/evidence/reflectionless_sweep.json`).

### LLM-judge outputs

`report/evidence/evidence_judges.json` — 6 model outputs:
- argo:gpt-5.2 → PARTIAL (9.08 s wall)
- argo:gemini-2.5-pro → REPLICATED (24.17 s)
- argo:claude-opus-4.7 → ERROR (HTTP 502, transient)
- argo:gpt-4.1 → REPLICATED
- argo:gpt-4o → REPLICATED
- argo:o3 → REPLICATED

### Representative figures copied to evidence/

For each of the 9 most illustrative examples: `<Example>_initial.png` (first frame) and `<Example>_final.png` (last frame). See `report/evidence/`.

## File inventory (final)

```
PDE-schrodinger-virtual-lab-2019/
├── paper.pdf                                # (1) 2.2 MB
├── extraction/
│   ├── marker.md                            # (2) 43 kB via pdftotext (marker fallback)
│   └── nougat.mmd                           # (3) 38 kB via pymupdf (nougat fallback)
├── report/
│   ├── REPORT.md                            # main report (this replication's canonical)
│   ├── REPORT.tex                           # (4) LaTeX version
│   ├── brief.md
│   ├── attempt_log.md
│   ├── artifact_harvest.md
│   ├── artifacts_summary.md                 # (7)
│   ├── workflow.md                          # (6)
│   ├── open_questions.json                  # (5)
│   ├── failure_analysis.md                  # (8)
│   └── evidence/
│       ├── evidence_judges.json             # 6 LLM judge results
│       ├── <Example>_<dim>.json (12)        # per-run diagnostics
│       ├── reflectionless_sweep.json
│       ├── <Example>_initial.png / _final.png (~18)
│       └── ...
└── work/
    ├── .venv/                               # local python 3.14 venv
    ├── bpm/                                 # clone of github.com/pyNLSE/bpm
    │   ├── bpm.py 1D.py 2D.py README.md doc/notes_code.pdf
    │   ├── examples1D/*.py
    │   └── examples2D/*.py
    ├── runs/                                # PNG output per example
    │   └── <Example>_<dim>/fig*.png
    ├── diag/                                # JSON diagnostics (mirrored into evidence/)
    ├── run_example.py                       # headless driver
    ├── test_reflectionless_sweep.py         # targeted s-sweep
    ├── pdf_to_mmd.py                        # nougat fallback
    ├── judge.py / judge_retry.py / judge_extra.py    # LLM judge harnesses
    └── (misc SyntaxWarning-free .pyc files)
```

## Checksums (paper)

`sha256(paper.pdf) = 034a26a1f606e6b1f5c5a0135a89d45c0ef137b5e763cabb10a190d67e933486`

## Provenance chain

Paper → IOP (2018 OA, CC-BY 3.0) → sibling replication's `work/figueiras.pdf` (Rick's earlier download, retained sha256) → this dir's `paper.pdf` (byte-identical copy). Code → LIA2 group page → `github.com/pyNLSE/bpm` → clone at commit `96d945b`. LLM judges → Argo proxy on `localhost:44497` (rick-stevens-ai account, key `stevens`) → underlying providers (Argonne LLM gateway).
