# Artifacts Summary — W1-vqe-photonic-peruzzo

## On-disk artifacts (as of 2026-07-06 backfill)

### Top level
- `REPORT.md` — canonical human-readable replication report (Ollie's audited version, 2026-06-26). **Preserved in place; not moved.**
- `REPORT.ollie-h2-inline.md.bak` — preserved provenance of the H2-hardcoded fallback attempt that briefly collided with the canonical PennyLane run.

### `report/` (added by this backfill)
- `REPORT.tex` — full LaTeX report with honest Critique section; `\input`s open-questions section.
- `open_questions.json` — 5 truly-open questions with `{q, basis, next_steps}` bodies, bare JSON list.
- `open_questions_section.tex` — LaTeX rendering of the 5 open questions.
- `workflow.md` — pipeline description (paper ingest → Hamiltonian → ansatz → optimize → audit).
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — honest critique + gap enumeration.

### Replication code + outputs (from original run)
- `replicate.py` — canonical PennyLane VQE implementation for HeH+ and H2.
- `logs/results.json` — per-bond-length dissociation-curve results.
- `logs/fine_eq.json` — 1-pm-resolution fine scan around HeH+ equilibrium.
- `logs/run.log` — runtime log.
- `figures/heh_dissociation.png` — HeH+ dissociation curve (VQE vs FCI overlay).
- `figures/h2_dissociation.png` — H2 dissociation curve (bonus).

### `extraction/`
- `nougat.mmd` — stub (paper text extraction; the original run relied on a `paper.md` at ingest time; this stub records that Supp. Table 2 tapered Hamiltonian is the known missing artifact).

## Headline exercised?

**YES.** The paper's headline is that VQE — a parameterized quantum state plus a classical optimizer with Hamiltonian averaging — recovers the ground-state energy of the HeH+ molecule. This replication independently reimplements the algorithm in PennyLane, runs it on the actual HeH+ molecule (STO-3G, Jordan–Wigner), reproduces the full dissociation curve to <2e-6 mHa vs FCI, recovers R_eq within ~6 pm of the paper's value, and cross-checks with the paper's own optimizer (Nelder–Mead). The algorithmic headline is fully exercised.

**What is not exercised:** the photonic-hardware demonstration itself (dual-rail encoding, photon loss, device noise) and the paper's specific absolute-energy convention (tapered 2-qubit Hamiltonian from Supp. Table 2, absent from parsed text).

## Verdict

**PARTIAL (strong; algorithm REPLICATED).** Coverage 6/10, Agreement 9/10.

Reasoning: on-disk REPORT.md verdict is preserved. The algorithm plus actual-molecule dissociation curve plus R_eq plus optimizer cross-check are fully reproduced (this is why "algorithm REPLICATED" appears in the verdict). Coverage is held at 6 because the photonic-hardware experiment and the tapered-Hamiltonian absolute-energy convention are unreproduced. Per the standing rule that the honest on-disk verdict wins over the queue label, and per substance-matching: the headline is algorithmically exercised but the hardware demonstration is not, so PARTIAL is the substance-honest verdict.
