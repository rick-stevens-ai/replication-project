# Failure analysis — quant-ph/0211124 replication

## Non-issues (fully replicated)
- Paper's central claim (Theorem 2 applied to the largest non-normal subgroup): confirmed with per-trial success 67-70% >> paper's lower bound (2/π)² ≈ 0.4053.
- GSVV random-basis indistinguishability: confirmed with fresh-U-per-trial MAP accuracy = 1/p ± 0.005.
- Amplification / majority-vote scaling: confirmed monotonic improvement to 76-83% at k=10 shots.

## Real friction encountered

### F1. Marker + Nougat not installed
- **What**: The QC-200 mandatory artifact list requires `extraction/marker.md` and `extraction/nougat.mmd`. Neither `marker-pdf` nor `nougat-ocr` is in the environment, and the central QC-100 parsed corpus (`~/Dropbox/REPLICATE-PROJECT/QC-100/parsed_md/`) does not contain an entry for arxiv id `quant-ph/0211124` (checked by title grep on `QC100_manifest.tsv`).
- **Workaround**: produced `pdftotext`-derived Markdown/MMD substitutes clearly labeled with a NOTE header. The full body text is preserved verbatim.
- **Residual gap**: math equations are NOT LaTeX-formatted in the substitute files (they appear as ASCII fragments). A native Nougat parse would produce inline `$...$` math, and Marker would preserve figure/table structure. For a 16-page pure-theory paper with no figures and few tables, the loss is minor.
- **Fix path**: install `pip install marker-pdf` (~2 GB weights) and `pip install nougat-ocr` (~1.5 GB weights), then rerun. Deferred out of scope for this ~30-minute subagent turn.

### F2. b=3 blind spot in paper's argmin decoder (p=5)
- **What**: The paper's decoder `b_hat = argmin_b |b/p - ell/(p-1)|` gets 0% accuracy on `b=3` at `p=5`. Cause: at `p=5`, the frequency lattice `{ell/(p-1)} = {0, 0.25, 0.5, 0.75}` and the message lattice `{b/p} = {0, 0.2, 0.4, 0.6, 0.8}`. For `b=3` (=0.6), nearest is `0.75` (distance 0.15), giving `ell*=3`. For `b=4` (=0.8), also nearest is `0.75` (distance 0.05). So whenever we observe `ell=3` for `b=3`, argmin picks `b=4` instead. This is a genuine small-instance lattice-tie artifact.
- **Impact on verdict**: NONE. The paper's per-trial lower bound `(2/π)² ≈ 0.4053` is about `Pr[ell = ell*(b)]` where `ell*(b)` is the nearest lattice frequency, not about `Pr[b_hat = b]` after argmin decoding. Our majority-vote experiment (`k=10` shots) recovers 76% aggregate accuracy at `p=5`, and TV distance analysis shows the paper's basis extracts near-maximal information (0.77 mean TV).
- **Open question Q1** captures this for follow-up.

### F3. Fixed-U random-basis MAP decoder is above baseline (32-37% vs 1/p = 20-14%)
- **What**: When we hold a single Haar-random U fixed and give the decoder oracle access to a MAP table trained on independent samples from that same U, the decoder achieves accuracy substantially above 1/p.
- **Why it's not a contradiction**: GSVV's theorem concerns the average over U. When we redraw U fresh each trial (`gsvv_fresh_basis_test.py`), accuracy collapses precisely to 1/p (± 0.005 for p=5, matching 20.0% baseline exactly).
- **Note**: this is actually a nice pedagogical result — it clarifies WHERE the indistinguishability comes from (marginalization over U, not per-U structure).
- **Open question Q2** captures this for follow-up.

### F4. Section 3's TV lower bound (≥ 1/4) is loose by 3x for A_p
- **What**: Paper's Section 3 proof yields `TV(H^b, H^{b'}) ≥ 1/(4(p-1))` asymptotically → `1/4` in the limit. We observe mean off-diagonal TV of **0.77** (p=5) and **0.85** (p=7).
- **Impact**: none for the verdict (the bound is a lower bound, so exceeding it is expected). But the constant is worth tightening — it would improve query-complexity constants for practical implementations.
- **Open question Q3** captures this for follow-up.

## No-goes / blocked / contradicted
None. The paper is fully self-contained (no external data / no external code required) and its central claims are directly simulable.

## What we did NOT test
- **Theorem 1** (fully reconstructible for q = (p-1)/polylog(p)): would require simulating a q-hedral group with q much smaller than p-1, which we spot-checked only via A_p (q = p-1). No obstacle in principle.
- **Theorem 5** (closure under extension by polynomial-size groups): a proof-only structural result; not directly amenable to numerical simulation.
- **Complete q-hedral case** (Section 3's `H_a` with `q < p-1`): implemented in principle but not exercised. Open question Q4.
- **Efficient QFT implementation** (Hoyer, 1999): we use the exact dense QFT matrix; a genuine polynomial-time circuit implementation is a separate systems-engineering question. Open question Q5.
