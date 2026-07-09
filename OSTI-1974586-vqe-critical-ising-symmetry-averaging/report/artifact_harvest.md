# Artifact Harvest

| Artifact | Source | Size | Checksum (MD5) | Notes |
|---|---|---|---|---|
| paper.pdf | https://www.osti.gov/servlets/purl/1974586 | 1,347,662 B | 131ff7c062bfb6993df7c222f7aaae49 | OSTI OA PDF (= arXiv:2210.15053v2). Downloaded via uicgpu proxy (CherryRd timed out on osti.gov). |
| paper.txt | `pdftotext -layout paper.pdf` on uicgpu | 65,393 B | — | Full text extracted; no OCR needed (born-digital PDF). |

**Public code:** No dedicated artifact repo was cited in the OA text for this arXiv/PRA version. The matchgate/Gaussian-fermion and free-fermion techniques are standard and were reimplemented from the paper's equations (Eq. 3, Eq. 4) + textbook Jordan-Wigner. No external data was required — the benchmark model is analytically defined.

**Data reused from paper:** NONE beyond the analytic target value `-4/π` and the model Hamiltonian Eq.(3)/(4). All numbers in this replication were computed fresh.

**Reference physics targets taken from paper (for comparison only):**
- Infinite-volume energy density = `-4/π` (Fig. 2 caption, p.4).
- Symmetry averaging reduces correlation-function error by ~2 orders of magnitude, <1e-7 at D=6 (Sec. V, p.4).
- Exact variational circuits need `p` rounds for `2p` spins (Sec. III / QAOA discussion).
