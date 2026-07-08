# Failure Analysis — Honest Critique

## Identity check
The paper cited in REPORT.md is:
> Childs, Maslov, Nam, Ross, Su, "Toward the first quantum simulation
> with quantum speedup," PNAS 115 (38), 9456–9461 (2018),
> arXiv:1711.10980.

The slug "Childs2018" matches. The queue's parenthetical hint
"nearly-optimal Trotter error bounds (arXiv:1901.00564)" refers to a
*different* Childs & Su 2018 paper on nearly-optimal Trotter theory.
The paper actually reproduced here is the PNAS resource-estimation
paper, not the pure theory paper. This replication addresses the
PNAS paper.

## What the paper's headline actually is
The PNAS paper's headline is:
1. **Fault-tolerant T-count / qubit tables** for n = 50 and n = 100
   spin Heisenberg instances under three algorithms (PF, LCU, QSP).
2. A **quantum-speedup argument** vs the best classical simulation
   of the same Hamiltonian at those sizes.
3. A **cross-algorithm comparison** identifying which of PF / LCU / QSP
   wins at what parameter regime.

## What this replication actually did
The replication targets two *inputs* to the paper's argument, not its
outputs:
- (A) Fitted the empirical error-scaling exponents for PF1/PF2/PF4 on a
  small (n = 6) random-field Heisenberg instance and confirmed the
  textbook $O(r^{-p})$ result. Slopes -0.97 / -1.98 / -4.20 vs -1 / -2 / -4.
- (B) Compared the PF1 empirical error against the first-order
  commutator bound and observed a ~4x asymptotic overestimate.

## Honest gap summary (headline-exercised = NO)

### 1. Nearly-optimal Trotter bound was NOT independently reproduced
The paper derives tightened, model-specific commutator bounds that
underlie its resource estimates. This replication uses the standard
textbook first-order bound only, and does not attempt the paper's
derivation. No bespoke bound was implemented or verified.

### 2. Gate-count / error-vs-t not reproduced for the paper's specific
### Hamiltonian at paper's sizes vs quoted numbers
- The paper reports T-counts for n = 50 and n = 100 spins.
- This replication ran n = 6 only.
- No T-counts, no Clifford+T compilation, no comparison against the
  paper's numerical tables.

### 3. Comparison against standard Trotter-1/2/4 baseline: PARTIAL
- Scaling exponents were compared against theory (implicit baseline).
- But there is NO comparison at fixed error target between the paper's
  bespoke formula and standard Trotter-p on the paper's Hamiltonian
  at paper's sizes — because the bespoke formula was not implemented.

### 4. Asymptotic speedup NOT quantitatively verified at accessible sizes
- The speedup argument depends on Hamiltonian norm scaling and T-count
  scaling with n and t at n ~ 50.
- This replication measures at n = 6 with t = 1; the speedup claim
  cannot be extrapolated from these numbers.

### 5. LCU / Taylor and QSP algorithms: not implemented
- Cross-algorithm comparison — a central paper contribution —
  is entirely absent.

### 6. PF2 / PF4 bound-vs-empirical gap: not measured
- The paper highlights the empirical-vs-bound gap growing with p.
- Only PF1 was compared here; PF2 and PF4 comparisons are absent.

## Where the replication IS honest and complete
- Scaling exponents (Claim A) reproduced quantitatively.
- PF1 bound-vs-empirical gap (Claim B, limited form) reproduced.
- Fully deterministic, seed-fixed, laptop-runnable.
- Independent Argo judge invoked (PARTIALLY_REPRODUCED, 6/10 coverage).

## Verdict framing
Under a strict reading (headline exercised must equal replicated verdict):
this is **PARTIAL**, not REPLICATED, because the fault-tolerant
resource tables, the speedup claim, and the LCU/QSP comparisons — all
of which are the paper's marquee contributions — were not reproduced.

The queue verdict was recorded as REPLICATED. This backfill preserves
that verdict per the "trust on-disk REPORT.md" instruction, but flags
the substance mismatch honestly here. The self-assessed score
(Coverage 7/10, Agreement 9/10) and the independent Argo score
(Coverage 6/10, Agreement 8/10, PARTIALLY_REPRODUCED) both indicate
the coverage gap.

## Recommendation for a future stricter pass
- Implement standard PF-Trotter at n in {8, 10, 12} and record
  T-counts via a free Clifford+T toolchain (e.g., `staq`, `PyZX`).
- Implement Taylor-series LCU at the same sizes.
- Compare bound-vs-empirical for PF2 and PF4 in addition to PF1.
- Explicitly compute the paper's specific tightened commutator bound
  for at least one small instance and check against the numerical
  ratio observed here.
