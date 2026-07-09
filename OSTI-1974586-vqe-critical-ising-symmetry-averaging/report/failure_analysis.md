# Failure analysis — OSTI 1974586

Honest log of what failed, what was deliberately skipped, what could still be wrong,
and what would flip the verdict.

## 1. Hard failures encountered mid-run

### 1.1 CherryRd → osti.gov download timeout
- **What happened:** direct `curl https://www.osti.gov/servlets/purl/1974586` on CherryRd hung past the request deadline.
- **Root cause:** unresolved — likely upstream network / TLS handshake stall from CherryRd's residential ISP path to `osti.gov`. Not a firewall block (other OSTI PDFs later succeeded from CherryRd on retry).
- **Fix:** `ssh uicgpu` + `source ~/env.sh` (ALCF proxy), then `curl`. Succeeded first try.
- **Residual risk:** the PDF was fetched via a single non-primary host. MD5 (`131ff7c062bfb6993df7c222f7aaae49`) was recorded but NOT cross-verified against the arXiv PDF MD5 or an independent OSTI mirror. For a well-known preprint this is low risk but is a real single-source provenance gap.

### 1.2 (No other hard failures)
- pdftotext ran clean (born-digital PDF).
- Free-fermion diagonalization ran clean (deterministic linear algebra).
- Dense spin diagonalization for L ∈ {4, 8, 12} ran clean and agreed with the free-fermion result to machine precision.
- QAOA Nelder-Mead converged with 10 restarts at each depth.
- Symmetry-averaging trig identity verified exactly.
- Argo judge responded on first request; verdict PARTIAL.

## 2. Deliberate NOT-reproduced items

### 2.1 C6 — DMERA matchgate circuit + exp(-4.89 D) scaling
- **Why skipped:** requires the paper's appendix circuit parameters, a full matchgate contractor, and the paper's variational-optimization pipeline. Building that from scratch is a research-scale effort, not a reference-physics replication.
- **Consequence:** the paper's headline algorithmic contribution is UNVERIFIED by this replication. A reader who trusts the exact reference physics but wants to know whether DMERA really achieves the claimed exponential-in-depth error scaling gets no signal from this report.
- **What would flip the verdict from PARTIAL to REPRODUCED:** implement (or obtain from the authors) the DMERA matchgate circuit for L ∈ {16, 32, 64} at D ∈ {2, 4, 6}, minimize its energy on the critical TFIM, and confirm the exp(-4.89 D) slope with a fitted uncertainty.

### 2.2 C7 — full 4-orders combined (translational + KW) suppression on actual DMERA output
- **Why skipped:** downstream of C6 — cannot rerun without DMERA observables.
- **Consequence:** the ~4-orders figure is CONSISTENT with our mechanism-level check (C5 already delivers ~2 orders from KW alone; adding translational orbit averaging over ~L observables plausibly buys another ~1-2 orders) but is not independently confirmed at the reported magnitude.
- **What would flip:** same as 2.1, then run the translational-average pipeline on the DMERA output.

## 3. Weaknesses in what WAS reproduced

### 3.1 C5 mechanism check is a trig tautology
- The claim ``|sin(φ/2)| ≈ 2 orders at φ ≈ 1°`` is an exact identity. Verifying it does NOT verify that the paper's actual DMERA/KW observable pair sits at φ ≈ 1° on real output. The paper's `10^-7` figure at D=6 could still be off by orders of magnitude and our C5 pass would not catch it.
- **What would strengthen this:** produce the actual DMERA output for D ∈ {2, 4, 6}, measure the two KW-related observables, extract the empirical phase mismatch φ(D), and confirm it stays near 0/π across depth.

### 3.2 QAOA L=8 is at the boundary
- The exact-preparation threshold `p = L/2` is trivially reached at L=8 with p=4 by parameter counting; any QAOA-style ansatz becomes exact at that boundary. Our reproduction of "exact at p=4" does not test the paper's stronger claim that DMERA continues to outperform QAOA at L ≫ 2p.
- **What would strengthen this:** rerun the QAOA scan at L ∈ {16, 32} with p ∈ {2, 4, 6, 8} and confirm QAOA plateaus with large residual error, while DMERA continues to improve.

### 3.3 Single-judge scoring
- The LLM judge is a single Argo model (`argo:gpt-5.2`). Its PARTIAL concurrence with our own assessment is weak evidence — it is the only vote against ourselves.
- **What would strengthen this:** add a second independent judge (a different Argo model, or a free Sophia/CELS endpoint) and require concurrence. If they disagree, escalate to a human reviewer.

## 4. Provenance gaps (low severity, logged for completeness)

- Single-source PDF MD5 (see §1.1) — mitigate by cross-verifying against arXiv 2210.15053v2 MD5 on next run.
- `pdftotext` ran on uicgpu; the text file `1974586.txt` was consumed on CherryRd. Byte-level integrity was not re-checked after cross-host transfer. Low risk (rsync via Dropbox) but worth a sha256 audit on rerun.
- Judge verdict is non-deterministic (LLM temperature > 0). Only one poll was persisted. A robust protocol would poll N times and require majority concurrence.

## 5. Bugs we know we didn't hit but should have tested

- **Numerical instability of `eps(k) = 4|sin(k/2)|` near k=0** — irrelevant at even-sector momenta `(2m+1)π/L` (never hits k=0), but a naive PBC even-fermion sector would need care.
- **Nelder-Mead getting trapped in QAOA local minima** — mitigated by 10 restarts; not stress-tested with alternative optimizers (COBYLA, SPSA, BFGS with analytic gradient).
- **Endianness / bit-ordering in the Pauli-tensor construction** for the dense L-qubit Hamiltonian — implicitly tested by agreement with the free-fermion reference, but not unit-tested in isolation.

## 6. Overall failure-mode classification

- **Provenance:** LOW risk (single-source download, MD5 recorded, born-digital).
- **Reference physics:** VERY LOW risk (two-methods agreement to machine precision, expected CFT scaling reproduced).
- **Mechanism (C5):** LOW risk for the mechanism itself, MEDIUM risk that it is NOT dispositive of the paper's actual claimed suppression on real DMERA output.
- **Algorithmic contribution (C6/C7):** UNTESTED. This is the honest reason for PARTIAL.
- **Scoring:** MEDIUM risk (single LLM judge, non-deterministic).

Net: the replication is HONEST about what it did and did not verify, the verdict PARTIAL is warranted, and none of the failure modes above shift the conclusion.
