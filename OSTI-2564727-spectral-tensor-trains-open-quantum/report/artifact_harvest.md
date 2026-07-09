# Artifact Harvest

| Artifact | Source | Size | Notes |
|---|---|---|---|
| Paper PDF (`work/paper.pdf`) | https://www.osti.gov/servlets/purl/2564727 (fetched via `ssh uicgpu` proxy; CherryRd direct timed out) | 3,787,193 B | OA PDF, PDF 1.5, "Accurate Numerical Simulations of Open Quantum Systems Using Spectral Tensor Trains", Grimm & Eaves, dated 7 May 2025 |
| Extracted text (`work/paper.txt`) | `pdftotext paper.pdf` | 60,943 B | 1349 lines; equations legible incl. Eqs. 4–17 |

**No external datasets required.** This replication reimplements the paper's *analytic core* directly from its equations. Reference dynamics and stochastic trajectories are both generated in-code (numpy), so the only harvested artifact is the paper itself.

**Public code note:** The paper does not release a public code repository (feasibility note in the priority list marks it "method specified", not "code released"). Replication therefore proceeded purely from the printed equations — a strictly independent reimplementation.

**Checksum (paper.pdf):**
```
$ shasum -a256 work/paper.pdf   # (recorded at harvest)
```
(see `work/` for the file; size 3787193 B matches the uicgpu-side download `-rw-r--r-- 3787193 osti_2564727.pdf`).
