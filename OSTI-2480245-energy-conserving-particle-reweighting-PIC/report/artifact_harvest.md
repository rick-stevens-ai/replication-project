# Artifact Harvest

| Artifact | Source | Details |
|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/2480245 | 5,503,298 bytes, PDF 1.5, 5 pages (journal 2-col reflow ~31 logical pages). Fetched via uicgpu (OSTI purl times out from CherryRd directly). Saved `work/paper.pdf`. |
| Extracted text | `pdftotext -layout` on paper.pdf | `work/paper.txt`, 1582 lines. Method Eqs 2–16 + Test 4.1/4.2 parameters recovered cleanly. |
| DOI | 10.1016/j.jcp.2024.113454 | *Journal of Computational Physics* (2024). Report id SAND2024-16128J. |

## Code / data availability
- **Aleph** (the PIC-DSMC code implementing the method): Sandia National Laboratories proprietary/export-controlled. **NOT publicly available.** No GitHub/Zenodo/OSTI code artifact accompanies the paper.
- No supplementary datasets released. The Test-4.2 cross sections are from the public Morgan database (LXCat) and the comparison tool Bolsig+ is freely available, but the paper ships no reproduction package.
- Consequence: full end-to-end rerun impossible without Aleph. Replication strategy = reimplement the mathematically-specified operators (Eqs 4–12) and verify their stated invariants + the Test-4.2 scaling structure. All numbers in this report are from our own reimplementation (`work/reweight.py` + tests), not from the paper.

## Checksums
```
paper.pdf : 5503298 bytes
```
