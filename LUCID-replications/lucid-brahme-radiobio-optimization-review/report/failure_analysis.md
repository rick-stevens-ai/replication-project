# Failure analysis + honest critique — Brahme (2024) LUCID slot

**Purpose.** Not a whitewash. Rick's 2026-07-05 rule: call out weak
evidence, shortcuts, tolerance hand-waving, missing controls, tooling
friction, and residual uncertainty. This slot has plenty of all of the
above because the target paper is a single-author review with no
primary artifact and it should never have been promoted to a full audit.

## 1. Root-cause failure at the pipeline level

The most consequential failure is upstream of any smoke:

- The paper was ingested as `candidate_curated` (tier B, score 13,
  master-TSV rank 91) despite being (i) a single-author review /
  opinion, (ii) in *Annals of Case Reports* (Gavin Publishers), a venue
  widely flagged as predatory, (iii) containing zero primary artifact,
  and (iv) making almost every quantitative claim by reference to the
  author's own earlier papers.
- A reasonable pre-audit venue+content gate (Cabells/DOAJ-removal check
  + count of Methods pages + presence of Data Availability + presence
  of any parameter table with > 5 rows) would have caught this before
  a single subagent-minute was spent. See Q5 in `open_questions.json`.
- Instead, the slot was audited (2026-06-09, 2026-06-22), tagged
  SPOT-CHECK, then retiered manually to NO-GO on 2026-06-25. That is a
  human-in-the-loop rescue, not a pipeline success.

Cost of this failure: two full audit passes + one manual retiering +
one backfill (this file). Estimated ~90 min of agent time and 0
scientific value produced. Multiply across a 100-slot corpus and this
category needs a hard gate.

## 2. What the audit was actually able to do

Genuinely accomplished (kept):
1. Deterministic re-implementation of Eq.(1) on a canonical
   Källman/Brahme Poisson sigmoid. Numerical headline reproducible in
   < 2 s on any laptop with numpy.
2. Independent 6-limit algebraic harness on 20,000 random (P_B, P_I)
   draws. 19/19 PASS, max|err| = 1.1 × 10⁻¹⁶ — a genuine well-formedness
   check on the equation, not a claim about clinical validity.
3. Qualitative direction check on the paper's two main verbal claims
   (C3: role of δ; C4: role of γ_C). Directions match.

## 3. What the audit hedged on or skipped (genuine gaps)

### 3.1 Eq.(1) tests are near-tautologies
The L1–L6 limits are consequences of the equation's algebraic form.
Any well-formed convex-combination-style objective on
$(P_B, P_I, \delta)\in[0,1]^3$ would pass most of them. Reporting 19/19
PASS as strong evidence would be misleading. The 2026-06-22 REPORT.md
correctly framed this as "formalism only" (Agreement 7/10), which is
the honest number. The audit did not, however, benchmark Eq.(1) against
any alternative objective (e.g. $P^{+}=P_B(1-P_I)$ hard-independent
baseline, or a Boolean AND) to show that Eq.(1) actually improves fit
on any deposited outcome. It couldn't: no outcomes released.

### 3.2 Choice of $(D_{50}, \gamma)$ is unaudited
The audit used $D_{50,T}=60$ Gy, $\gamma_C=3.0$ (low LET) and 1.8
(high LET), $D_{50,N}=70$ Gy, $\gamma_N=4.0$ — canonical Källman/Brahme
literature values, not derived from the paper (which never publishes
its own). Reasonable alternatives (e.g. $D_{50,T}=50$–$70$,
$\gamma_C=2.5$–$3.5$) would shift $P^{+}_{\max}$ by several percentage
points and $D^{*}$ by 2–5 Gy without changing the qualitative story.
No sensitivity analysis was run. This is a real gap: any claim of
numerical agreement is contingent on a set of parameters the paper
doesn't fix.

### 3.3 High-LET penalty is an arbitrary halving of $\gamma_C$
Reducing $\gamma_C$ from 3.0 to 1.8 to mimic the LET-driven penalty is
illustrative. The paper's actual claim (Fig.\,15 insert) is
$\gamma_C\approx 4$ for n/C vs.\ 5–6 for photons/Li. Our smoke uses
neither pair of values. This is not a refit of the paper's Fig.\,15
table; it is a direction-preserving toy.

### 3.4 RHR / RCR are completely untested
The paper's headline mechanistic novelty is the RHR survival model.
No parameters are given here, and the audit did not go to refs
[1–3, 23, 34, 45] to pull them. The audit's coverage of the paper's
mechanistic content is zero.

### 3.5 Figure-embedded numerics missed
The Fig.\,15 tabular insert (γ_C, σ_D/D̄, RBE per modality) is rendered
text inside a bitmap-ish figure and `pdftotext -layout` does not
recover it. A GPU Marker/Nougat pass would probably fix this. Not done
in either audit pass or in the backfill.

### 3.6 No cross-check of cited primary refs
Almost every quantitative claim in the paper points to Brahme's own
earlier work (refs [1–3, 23, 34, 45]). The audit did not fetch any of
those refs, did not check that the numbers cited are actually in the
refs, and did not check whether those refs are themselves reproducible.
That's the correct scope decision for a single-slot audit — but it
means "REPLICATED (formalism only)" is a narrower claim than the tag
suggests.

## 4. Toolchain friction

- **Internal `pdf` extraction tool unusable on 2026-06-09.** Anthropic
  credit balance depleted for the model on record, Gemini model-name
  mismatch, OpenAI extract plugin errored. Fell back to `pdftotext`.
  This is a generalizable weakness — the LUCID pipeline should not
  depend on a single commercial-LLM extractor.
- **GPU parse unavailable for this backfill.** Nougat requires GPU;
  no GPU allocation was arranged for the backfill run. Left
  `extraction/nougat.mmd` as a stub with the paper.pdf SHA-256 pointer
  so a later corpus sweep can fill it.

## 5. Residual uncertainty (what would need to be done to close it)

1. **Verify Fig.\,15 numerics.** Re-parse with GPU Marker/Nougat; if
   the insert becomes machine-readable, quote the values exactly and
   run a first-principles microdosimetric prediction against them
   (see Q3).
2. **Deposit RHR parameters.** Requires reading Brahme refs
   [1–3, 23, 34, 45] and extracting the parameter table. Then Q2 is
   actionable.
3. **Deposit an outcome cohort.** Requires an external effort — no
   public deposit is currently reachable at scale. Q1 depends on this.
4. **BIOART on an open PET-CT dataset.** Q4 is actionable now on TCIA
   HN-PET or NSCLC-Radiogenomics if we're willing to implement the
   uptake-to-$D_{0,\text{eff}}$ mapping from scratch.
5. **Add the venue+content pre-audit gate** to LUCID so this failure
   mode is caught upstream (Q5).

## 6. Overall honest assessment

- The audit did what could be done and correctly reported small
  Coverage (4/10) and moderate Agreement (7/10). It did not
  over-claim. The 2026-06-25 retier to NO-GO for LUCID-100 promotion
  is correct.
- Nothing in the paper other than Eq.(1) is meaningfully testable
  from the paper alone. Anyone using this REPLICATED tag downstream
  should read the retier banner, not the tag.
- The audit is easy to defend in a peer setting: it does not claim to
  reproduce the paper's clinical or mechanistic content, it says
  clearly why it cannot, and it lists 9 of 13 claims as untested with
  reasons.
- The audit is easy to attack on the narrow point: the tests it did
  run are near-tautologies of Eq.(1)'s algebraic structure and are
  therefore weak evidence in isolation.
- The real defensible value of this slot is negative: it demonstrates
  a concrete failure mode of the LUCID intake filter (predatory-venue
  reviews slip through). That's actionable (see Q5) and worth
  preserving.

**Verdict preserved:** REPLICATED (formalism only) — with the NO-GO
retiering banner in REPORT.md kept intact. Any downstream corpus use
should honor the retiering.
