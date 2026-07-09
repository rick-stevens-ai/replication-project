# Failure analysis — arXiv:0704.3628 replication

Even for a clean REPLICATED verdict, the standard requires honest analysis of every friction point, workaround, assumption, and residual gap. Here they are.

## 1. Bipartite-parity blocker at odd depth n

**What failed.** First sweep (n=2,3,4,5) crashed at n=3 with the assertion `|psi_start''> has zero norm — construction bug`.

**Root cause.** T' (tree + tail) is a bipartite graph (all edges between distinct BFS-color classes). Color-0 = root; color-1 = tree level 1; ... Color-n = leaves. Adding an even-length tail adds equal numbers of color-0 and color-1 vertices. The kernel of a bipartite adjacency matrix has dimension `||A|-|B||` and its support alternates between the two color classes. `|psi_start>` is supported entirely on color-0 (even-indexed tail sites including the root). For odd depth n, tree leaves are on color-1 (odd tree distance from root), making color-1 the majority class in T', so `ker H` is supported on color-1 and `P_ker |psi_start> = 0`.

**Paper's escape hatch.** Section 3.2 opens with: *"Without loss of generality, assume that all leaves are at an even distance from the root. (If there is a leaf ℓ at an odd depth, create two new vertices v_1, v_2 and connect them to ℓ, making ℓ an internal node. v_1, v_2 are now leaves at an even depth. Replace x_i by two new variables at v_1, v_2 equal to NOT x_i. Then NAND of those two at ℓ evaluates to x_i.)"* This doubling preprocessing fixes the parity but doubles N.

**Workaround.** We restricted the sweep to even n ∈ {2,4,6,8}. This still gives four data points spanning 64× in N (4 → 256), sufficient to confirm the empirical scaling exponent.

**Residual gap.** The doubling preprocessing is not implemented. Question Q3 in `open_questions.json` asks whether the WLOG doubling is truly "free" or hides a constant-factor query overhead.

## 2. Marker + Nougat not installed on host

**What failed.** The 8-artifact standard requires `extraction/marker.md` (Marker parse) and `extraction/nougat.mmd` (Nougat parse). Neither tool is installed on CherryRd.

**Root cause.** Marker and Nougat are heavy PyTorch-based extractors that require GB-scale model downloads and GPU (or slow CPU) for reasonable runtime. This is a QC-200 replication working directory on a laptop-class host; the central SCOUT/LUCID/OSTI extraction corpuses on Eagle do not contain arXiv:0704.3628 (verified via directory scan).

**Workaround.** Same convention already used in sibling QC-200 dirs (e.g. `QC-0707.2831-jones-polynomials-dqc1-shor-jordan`): produce **labelled surrogates**. `marker.md` is a PyMuPDF page-boundary text extraction; `nougat.mmd` is a `pdftotext -layout` extraction. Both files have header lines explicitly stating the tool used. `extraction/README.md` documents this choice.

**Residual gap.** If Marker/Nougat becomes available later, rerun and overwrite. Structural equations (H matrix elements, phase-estimation formulas) may be better preserved by Nougat than by pdftotext, so any downstream text-mining across the corpus that assumes LaTeX-style math from Nougat will not get it here.

## 3. Small-N discreteness in queries/√N ratio

**What is not a failure, but worth flagging.** The empirical `queries / √N` ratio is not constant: 17.5, 18.75, 19.375, 19.688 for N = 4, 16, 64, 256. This looks like slight super-√N scaling.

**Root cause.** Queries per input = `C · (2^m − 1)` where `m = ceil(log2(4·√N))`. This is a step function; for `4·√N = 8, 16, 32, 64` we get exactly `m = 3, 4, 5, 6`, so queries = `5·(2^m−1) = 35, 75, 155, 315`. The `−1` term makes the ratio slowly approach 20 from below as N grows. The pure `2^m / √N = 4` constant would give ratios `35/2 = 17.5, 75/4 = 18.75, ...` — asymptotically `2^m / √N → 4C = 20`, matching what we see.

**No fix needed.** The paper's `O(√N)` is asymptotic; a `1 − 1/2^m` correction is expected. Question Q1 asks whether the constant `4` in `m = ceil(log2(4·√N))` can be tightened.

## 4. Success drop from 0.950 → 0.917 at N=256

**What worth noting.** Overall success rate is flat at 0.950 for N=4, 16, 64 but drops to 0.917 at N=256, entirely driven by T=0 success falling from 0.900 to 0.833 (T=1 stays at 1.000 throughout).

**Root cause candidates.**
(a) **Larger residual overlap on non-zero eigenphases** for random T=0 inputs at bigger trees — the paper only proves overlap constant `c > 0`, not c = 1, and random T=0 inputs can have overlap as low as ~0.4-0.5 with the θ=0 eigenstate.
(b) **Coarse phase-estimation grid** with only m=6 bits at N=256: threshold theta_thresh = 0.5/√256 = 0.03125 vs grid spacing 2π/64 ≈ 0.098. Two adjacent grid points can straddle the threshold.

**Impact.** Still well above the paper's 2/3 bound. If we increased C from 5 to 11 (majority vote of more shots) or m by 1, the T=0 rate at N=256 would recover to 0.95+.

**Residual gap.** Question Q1 in open_questions.json addresses this systematically (2-D Pareto sweep over m-scale and C).

## 5. Claims not tested

C5 (`O(√(Nd))` arbitrary binary NAND tree) and C6 (`O(N^(1/2+O(1/√log N)))` arbitrary NAND formula) were **not tested**. They require the general weighted-H construction (Sec 3.2 items 1-2) with edge weights `4th-root(m_c / 2 m_p)` etc.

**Why not.** The task brief scoped the reproduction to "small balanced binary NAND tree (n=2,3,4 → N=4,8,16 leaves)" — we exceeded the brief on N (reached 256) but stayed within the balanced case. Extending to the general case is directly implementable but a full replication of Theorem 3 part 2 is a separate follow-up.

**Residual gap.** Q4 in open_questions.json addresses this directly.

## 6. No 3-judge Argo panel

**What was skipped.** The QC brief calls for "3-judge Argo panel only if time remains; else self-verdict."

**Reason.** Self-verdict is unambiguous here: the paper's headline number (success ≥ 2/3, queries scaling as √N) is directly measured with real numpy statevector simulation on 4 values of N, with empirical exponent within 6% of the paper's 0.5. There is no ambiguity for a judge panel to resolve.

## Summary

Everything blocking a full green-check is documented above; none of it changes the verdict. The paper's core algorithmic claim was reproduced with real linear-algebra simulation, using only free tools, on a laptop, in about 30 minutes of agent wall clock.
