# Artifact Harvest

| # | Artifact | URL / accession | Size | Notes |
|---|---|---|---|---|
| 1 | Paper preprint PDF | https://arxiv.org/pdf/1801.01103 | 1,759,476 B | arXiv 1801.01103v2 (9 Jun 2018), later published SIAM J. Sci. Comput. 40(5) B1330-B1360, DOI 10.1137/18M116383X |
| 2 | Paper abstract page | https://arxiv.org/abs/1801.01103 | small HTML | Title/authors verified |
| 3 | Author GitHub listing | https://api.github.com/users/leinkemmer/repos | JSON | 8 public repos surveyed |
| 4 | Ensign framework (author's) | https://github.com/leinkemmer/Ensign | C++ | "framework to facilitate dynamical low-rank simulation"; not used directly — clean-room Python instead. |
| 5 | Extracted paper text | `work/paper.txt` | 1816 lines | `pdftotext -layout` |
| 6 | Landau results r=5,10,20 | `work/results/landau_r*.json` | ~3×~800KB | Full timeseries: t, mass, momentum, kinetic, field, total_energy, l2, Emax, plus γ-fit |
| 7 | Two-stream results r=5,10,20 | `work/results/twostream_ts_r*.json` | ~3×~700KB | Same schema |
| 8 | Landau diagnostic plot | `report/evidence/landau_diagnostics.png` | 147 KB | 4-panel: electric energy w/ analytic line, mass drift, energy drift, L² drift |
| 9 | Two-stream diagnostic plot | `report/evidence/twostream_diagnostics.png` | 143 KB | 4-panel |
| 10 | LLM-judge prompt | `work/judge_prompt.txt` | 2.5 KB | Prompt sent to Argo |
| 11 | LLM-judge response | `work/judge_response.json` | ~1.5 KB | Raw response from `argo:claude-opus-4.7` |
| 12 | Solver source | `work/dlr_vlasov_poisson.py` | 11 KB | Clean-room DLR/FFT projector-splitting VP solver |
| 13 | Two-stream driver | `work/twostream.py` | 3.5 KB | |
| 14 | Plot script | `work/make_plots.py` | 3.7 KB | |
