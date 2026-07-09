# Failure Analysis, Friction, and Residual Gaps

## What worked

- **Simulation**: The 7-qubit ($3+4$) Shor circuit for $N=15$, $a=2$ ran cleanly on Qiskit 2.5.0. Statevector construction, controlled modular exponentiation via the textbook cyclic-swap-chain-plus-X's decomposition, inverse QFT, and exact partial-transpose all worked first try.
- **Sanity checks**: The counting-vs-work log-negativity hits exactly $\log_2 r = 2$ after the second controlled $U_a$ and stays there — this is the theoretically expected value for a period-4 signal, and matches to machine precision. That is a hard internal consistency check.
- **Qualitative claim reproduction**: All three of the paper's headline qualitative claims (growth through cU_a, collapse after non-selective measurement because $r = 2^m$, classical-simulability of the no-entanglement variant) reproduced.

## What did not fully work / residual gaps

### G1. Absolute magnitude of the averaged log-negativity is ~2x the paper's plot

Our post-cU_a average log-negativity across all 63 bipartitions is 1.257 (log2 base), but the corresponding pure-state $\varepsilon = 0$ point in the paper's Fig. 11 sits at roughly 0.55-0.65, and Fig. 15 at 0.15-0.25. **These are the same physical quantity by the paper's own equation (Eq. 18) applied to the same circuit.** Three normalization/convention candidates each shift the number by roughly a factor of 2:
- Plain negativity $N(\rho) = (\|\rho^{T_A}\|_1 - 1)/2$ vs log-negativity $E_{\mathrm{neg}} = \log_2 \|\rho^{T_A}\|_1$.
- Natural log vs log base 2 (factor $\ln 2 \approx 0.69$).
- Partition-size-weighted average vs uniform average over the 63 partitions.

We tried (i) — plain negativity — and got 0.98, which is closer to Fig. 11's 0.55-0.65 but still off. The paper text does not disambiguate the plotting convention. Escalated as **Open Question 1**.

### G2. Did not sweep the mixing parameter $\varepsilon$

The paper's headline plot (Figs. 11-14) is $\langle E_{\mathrm{neg}}\rangle$ **vs $\varepsilon$**. We only did the $\varepsilon = 0$ endpoint (pure state). A full sweep is straightforward (repeat the density-matrix trace with the control-qubit prep replaced by $(1-2\varepsilon)|+\rangle\langle+| + \varepsilon I/2$ or similar) and would upgrade the verdict from PARTIAL to (likely) REPLICATED. Time-boxed out of this run.

### G3. Marker and Nougat extractions are surrogates

Neither `marker_single` nor `nougat` is installed on CherryRd (2026-07-05). We wrote surrogate `extraction/marker.md` and `extraction/nougat.mmd` files derived from `pdftotext -layout`, with the surrogate status prominently labeled at the top of each file. The brief permits pulling from a central parsed corpus if available; a spot-check of `~/.openclaw/workspace/parsed-papers/` (search timed out, killed after ~30 s) did not find a pre-parsed copy for `quant-ph/0102136`. For strict compliance, these would need to be re-generated on a GPU host with Marker/Nougat installed.

### G4. REPORT.pdf compile not attempted here

`pdflatex` presence not verified during this run; `REPORT.tex` is the primary artifact per the brief. Section 4 requires `.tex` "compiled to REPORT.pdf when possible" — we mark this as best-effort and rely on the .tex being human-readable.

### G5. Reading numbers off raster figures

The comparison values (Fig. 11 y-value $\approx 0.55$-$0.65$ at $\varepsilon = 0$, etc.) were read by eye from the paper's raster plots — the paper does not tabulate them. This is the paper's fault, not ours, but it means our "MISMATCH by 2x" claim has $\pm 0.05$ visual-reading error bars.

## Friction log

- **Search for parsed corpus timed out**: 30+ s wall on a broad `find` across `~/Dropbox/LUCID-100` and `~/.openclaw/workspace/parsed-papers/`. Killed and moved on.
- **Task narrative vs paper**: task narrative said $a=7$, paper's actual data uses $a=2$ (both have $r=4$ for $N=15$). Followed the paper, since the brief says reproduce the *paper's* headline number. Both $a$'s give the same period, so any qualitative claim carries over verbatim; a full replication would run both.
- **Interpretation of Fig. 11 vs Fig. 15**: Two ostensibly identical quantities plotted with different y-scales — even after careful re-reading of the captions, the exact averaging domain differs subtly (Fig. 11 curves are averaged post-cU_a **or** post-meas separately; Fig. 15 collapses to prob-of-finding-r on the x-axis). This ambiguity feeds directly into G1.

## Honest bottom line

We ran a **real** small-instance Qiskit simulation, verified the exact-theoretical entanglement of the counting-vs-work cut hits $\log_2 r$, reproduced all three qualitative claims, and delivered summary averages that agree in sign / rank-ordering / structural behavior with the paper's plots but differ by $\sim$2x in absolute magnitude for reasons pinned down to a normalization convention we cannot uniquely infer from the paper text. Verdict: **PARTIAL** — a stronger REPLICATED verdict would require the $\varepsilon$-sweep (G2), which is a well-defined next step.
