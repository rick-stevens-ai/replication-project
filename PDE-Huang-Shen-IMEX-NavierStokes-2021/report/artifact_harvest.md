# Artifact Harvest

| Artifact | Source | Size | Checksum (MD5) | Notes |
|---|---|---|---|---|
| `hs2021.pdf` | https://arxiv.org/pdf/2103.11025v1 (Open Access, arXiv) | 1.82 MB | 52bd37265ba9f5bf0050e5ceea672837 | Full preprint = published SIAM J. Numer. Anal. version (DOI 10.1137/21M1404144) |
| `hs2021.txt` | `pdftotext -layout hs2021.pdf` | 1755 lines | — | extracted text used for scheme/params |

**No external code artifact.** The paper provides no public code repository; the replication solver was implemented entirely from scratch from the equations in the paper (Fourier-spectral SAV/BDFk).

**Reference numbers taken from paper (Example 1, Section 3.3, Figure 1):**
- Domain Ω=(0,2)², periodic; ν=1; T=1; 40×40 Fourier modes.
- Manufactured exact solution (velocity + pressure) and the stated qualitative claim: velocity & pressure H¹ errors show the **expected order-k convergence** for BDFk, k=1,2,3,4. (Paper reports these as log-log plots, not a numeric table; the verifiable quantity is the convergence *order/slope* per scheme.)

**Tool versions:** Python 3 + NumPy (FFT), SymPy (forcing verification), Matplotlib (plot). Argo proxy (localhost:44497) for LLM judges — free endpoints only.
