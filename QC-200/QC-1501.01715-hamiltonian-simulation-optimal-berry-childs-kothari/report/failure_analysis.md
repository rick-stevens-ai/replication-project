# Failure analysis — BCK 2015 replication

## What did NOT work / partial gaps

### 1. Marker + Nougat parses missing
- Neither `marker` nor `nougat` is installed on CherryRd.
- The paper (1501.01715) is not in the central corpus at `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/_LUCID100_ADMIN/marker_md_uicgpu_20260622/` or `marker_vs_nougat_20260622/`.
- **Mitigation:** produced `extraction/marker.md` and `extraction/nougat.mmd` as pdftotext-derived proxies with **explicit provenance headers** stating what they are and are not. No fabrication.
- **Residual gap:** a real Marker/Nougat run would preserve equation LaTeX at higher fidelity. If needed, a batched uicgpu run could regenerate these two files.

### 2. Full circuit construction not built
- The paper's full algorithm requires:
  - Block-encoding of $H$ via isometry $T$ and oracles $O_H, O_F$.
  - Quantum walk step $U = i S (2 T T^\dagger - I)$.
  - LCU `select`$(U^m)$ across $m \in \{-k, \dots, k\}$ ancilla-controlled powers.
  - Bessel-amplitude ancilla state prep.
  - Oblivious amplitude amplification (OAA).
  - Segment chaining.
- This is a $32 \times 32 \times (2k{+}1)$-dimensional statevector job in Qiskit — doable but heavy for a single subagent.
- **Scope decision:** we replaced the full circuit with a *numerical* check of the LCU-of-Bessel truncation on the walk-invariant eigenspace. This is exactly the object BCK's Lemma 8 bounds, so it is a faithful test of the headline scaling — but it does not exercise the ancilla state prep, OAA, or gate count.
- **Residual gap:** Claim C6 (full 2-qubit gate cost $O(\tau[n + \log^{5/2}(\tau/\eps)] \log/\log\log)$) is untested; Claim C3 (tradeoff variant, Thm 3 with parameter $\alpha$) is untested. Both would need the full circuit.

### 3. Averaging bug (caught + fixed in-run)
- First implementation of `bck_lcu_evolution` averaged both walk eigenspaces ($\mu_+$ and $\mu_-$ branches), giving $V_k \to \cos(m\theta)$-only content. Result: $\|V_k - e^{-iHt}\|$ plateaued at $\sim 1.0$ for all $k$.
- **Cause:** misread of paper eqs. 7-9. The Jacobi-Anger identity applied to a *single* walk-eigenspace branch already gives $e^{-iHt}$; averaging both destroys the imaginary parts that carry the actual time-evolution phase.
- **Fix:** switched to single-branch $\sum J_m(z) e^{im\theta}$. Convergence immediately dropped to machine precision by $k = 20$.
- **Lesson logged:** re-read the paper's identity carefully before assuming symmetrisation is needed. When BCK write "there is no need to distinguish the eigenspaces" (paper §2, after eq. 9), they mean *either* branch gives the answer, not that you should average them.

### 4. No 3-judge Argo panel
- The brief calls for a 3-judge Argo panel "if time remains; else self-verdict".
- Self-verdict was used since all three quantitative anchors matched the paper's formulas within expected constants.
- **Residual gap:** a full 3-judge panel could cross-check the verdict; this can be added in a follow-up run.

### 5. Only one Hamiltonian tested
- Only the 4-qubit XY chain with $J=1$ was tested. $\tau = 3$ is small.
- **Residual gap:** the paper's claims are asymptotic in $\tau$. Our confirmation of $c \approx 2.0$ in $k/[log(1/\eps)/\log\log(1/\eps)]$ across ten orders of magnitude of $\eps$ is strong evidence, but a $\tau$-sweep is missing. This is Open Question Q3.

## What DID work

- LCU-of-Bessel truncation converges to machine precision by $k = 20$ (Experiment A).
- $k(\eps)$ scaling matches $c \cdot \log(1/\eps)/\log\log(1/\eps)$ with stable $c \approx 2.0$ across $\eps \in [10^{-1}, 10^{-10}]$ (Experiment B). **Direct numerical confirmation of Thm 1.**
- BCK beats 2nd-order Trotter by $\sim 2.5\times$ query count at $\eps = 10^{-3}$ on this instance (Experiment C).
- All 8 artifacts were produced; extraction stubs are honestly labelled; no fabricated numerics.

## Overall

**Verdict: REPLICATED (partial).** The paper's headline scaling and LCU convergence are numerically confirmed; the full circuit and gate-cost claims (C3, C6) are out of scope for a single subagent. Nothing was contradicted, nothing was fabricated, no paid endpoints were used.
