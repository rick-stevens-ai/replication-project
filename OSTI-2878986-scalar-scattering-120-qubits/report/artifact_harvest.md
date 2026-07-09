# Artifact Harvest — OSTI 2878986

| Artifact | Source URL | Local path | Size | Checksum (md5) |
|---|---|---|---|---|
| OSTI PDF | https://www.osti.gov/servlets/purl/2878986 | `work/osti_2878986.pdf` | 4 449 627 B | `df33f156ee65de17500211038061c74a` |
| Extracted text | (derived, `pdftotext -layout`) | `work/osti_2878986.txt` | 1 703 152 B | — |
| arXiv e-print source tarball | https://arxiv.org/src/2411.02486 | `uicgpu:/tmp/2411.02486.src` | 5 028 913 B (gzip) | `1e30921c8928ead413624473b7088aae` |
| arXiv abstract page | https://arxiv.org/abs/2411.02486 | (viewed, not saved) | — | — |
| DOI record | https://doi.org/10.1103/qr72-51v1 | (viewed via arXiv metadata) | — | — |

## What we harvested from the arXiv source

Contents of `uicgpu:/tmp/arxiv_src/`:

```
00README.json               209 B    (arXiv submission metadata)
main_v3.tex           203 386 B     LaTeX source
preamble.tex            1 732 B     package preamble
main_v3.bbl           156 266 B     bibliography (compiled)
graphics/                 (dir, 18 PDF figures + 1 PNG logo)
```

Notable graphics filenames (correspond to paper figures):
- `scattering_heatmap_l_0.pdf`, `scattering_heatmap_l_2.pdf`, `scattering_heatmap_small.pdf` (Fig. 9 and 11)
- `results_by_time.pdf` (Fig. 10)
- `single_vs_two_wp_free.pdf`, `single_vs_two_wp_int.pdf`
- `time_evolution_circ_step.pdf`, `circuit_elements.pdf`, `full_circuit.pdf`
- `trot_vs_variational_fidelity.pdf`, `center_tracking.pdf`
- `exact_vs_variational_l_0.pdf`, `exact_vs_variational_l_2.pdf`
- `t_8_l_0_mitigation.pdf`
- `e_k_v_k_wp_prep_convergence.pdf`, `scalable_variational_circuits_procedure.pdf`
- `vac_prep_figs.pdf`, `map_to_qubits.pdf`
- `IQuSLogo.png`

**Data & code availability.** The arXiv source is TeX + figures only. No repo link in the paper text (checked with grep). No supplementary Zenodo, no GitHub, no Qiskit notebook or ancillary files. The 00README.json is not a data manifest, just arXiv housekeeping. This makes it impossible to bit-reproduce the paper's 120-qubit device runs or the MPS reference — we can only rebuild the model from the equations and compare qualitative predictions.

## Compute artifacts we produced

Under `report/evidence/`:

- `replication_results_L6_v2.json`, `replication_results_L6_sanity.json`, `replication_results_L8_main.json` — full numerical results for each (L, λ).
- `claim_verdicts.json` — C1..C5 per-claim scoring.
- `free_vs_int_summary.json` — per-time-step peak summary.
- `fig_scattering_heatmap_replication.png` — replication analog of paper Fig. 9 (heatmap of ⟨ϕ²⟩ − ⟨ϕ²⟩_vac vs t, j for both λ).
- `fig_peak_amplitude_vs_time.png` — collision peak magnitude vs time for both λ.
- `fig_dispersion.png` — analytic free-scalar dispersion vs closed-form.
- `llm_judge_verdict.json` — Argo (claude-opus-4.8) verdict summary.

Under `work/`:

- `replicate_scalar_scattering.py` — main simulator.
- `compare_free_vs_int.py` — claim scoring.
- `make_figures.py` — plotting.
