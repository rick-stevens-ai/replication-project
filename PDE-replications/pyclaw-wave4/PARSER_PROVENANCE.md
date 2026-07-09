# Parser Provenance — PyClaw Re-pass (Wave 4)

## Source PDF

- **Title:** PyClaw: Accessible, Extensible, Scalable Tools for Wave Propagation Problems
- **Authors:** Ketcheson, Mandli, Ahmadia, Alghamdi, Quezada de Luna, Parsani, Knepley, Emmett
- **Venue:** SIAM Journal on Scientific Computing, 2012 (Vol. 34, No. 4, pp. C210–C231)
- **DOI:** 10.1137/110856976
- **arXiv:** 1111.6583 v2 (12 May 2012)
- **URL fetched:** https://arxiv.org/pdf/1111.6583
- **Date fetched:** 2026-06-23
- **Local path:** `repass_paper/pyclaw_paper.pdf`
- **Size:** 2,743,918 bytes
- **SHA-256:** `94bb2a5ee4b21ef960518600758ca6132801eb209a2dc44cff3436cd8b26d18e`

## Parser

- **Tool:** `pdftotext` (Poppler), `-layout` flag
- **Path:** `/usr/local/bin/pdftotext`
- **Command:** `pdftotext -layout pyclaw_paper.pdf pyclaw_paper.layout.txt`
- **Output:** `repass_paper/pyclaw_paper.layout.txt` (991 lines)
- **No Marker/canonical corpus used.** PyClaw is a SISC software-paper PDF with
  tables and code listings; `pdftotext -layout` cleanly preserves the
  Table 5.1 timing grid, Table 7.1 Rossby-Haurwitz breakdown times, the
  shock-bubble post-shock state, and the Listing 1/2/3 code blocks.

## Verification

Spot-checked:
- Title and author block on line 1-5.
- Section headings (Introduction, Algorithms, Software design, Performance,
  Applications) at expected positions.
- Table 5.1 (Clawpack vs PyClaw timings on Xeon and BlueGene/P) parses with
  correct columns: Acoustics 28s/41s/1.5 Xeon, 192s/316s/1.6 PowerPC;
  Shallow Water 79s/99s/1.3 Xeon, 714s/800s/1.1 PowerPC.
- Listing 2 (2D Euler 4-wave Riemann problem) parses with
  `solver = pyclaw.ClawSolver2D ( riemann.rp2_euler_4wave )`.
- Section 7.2 shock-bubble post-shock state: behind shock `p = 5`,
  `ρ ≈ 2.82`, `v ≈ 1.61`, pre-shock `ρ = p = 1` (bubble: `ρ = 0.1`),
  γ = 1.4.
- Table 7.1 Rossby-Haurwitz breakdown: 100×50 — , 200×100 ≈ 34d,
  400×200 ≈ 45d, 800×400 ≈ 46d.
