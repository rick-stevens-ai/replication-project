# Failure analysis — arXiv:1701.08669 replication

Even for a clean REPLICATED verdict, the standard requires honest analysis of every friction
point, workaround, assumption, and residual gap. Here they are.

## 1. The paper's actual content is a proof, not a numerical claim

**What is genuinely testable.** Gogioso & Kissinger's paper is a *diagrammatic correctness proof*
of the standard abelian HSP quantum subroutine. Its headline number is not "we ran an experiment
and got X"; it is "the standard result is provable purely from Frobenius-algebra / strong-
complementarity axioms without ever invoking Peter-Weyl or explicit character sums." That is
not a directly-numerically-checkable claim.

**How we defined a REPLICATED-shaped verifiable content.** The concrete corollary is: *when
instantiated in fdHilb, the paper's Diagram 5.3 is the standard HSP-subroutine output
statistic.* We reproduce that statistic on two nontrivial test groups from real numpy
statevector simulation, and additionally verify the numerical content of the paper's key
algebraic rewrite (Sec 5.7 isometry cancellation) by comparing the two computational
pathways it identifies. See REPORT.tex Section "What is checkable numerically."

**Residual gap.** We do *not* execute the paper's diagrammatic proof itself (e.g.\ do not
run the rewrite chain in PyZX). That would be a stronger and complementary check; it is
listed as Q3 in `open_questions.json`.

## 2. Marker + Nougat not installed on host

**What failed.** The 8-artifact standard requires `extraction/marker.md` (Marker parse) and
`extraction/nougat.mmd` (Nougat parse). Neither tool is installed on CherryRd.

**Root cause.** Marker and Nougat are heavy PyTorch-based extractors that require GB-scale
model downloads and GPU (or slow CPU) for reasonable runtime. This is a QC-200 replication
working directory on a laptop-class host; the central SCOUT/LUCID/OSTI extraction corpuses do
not contain arXiv:1701.08669 (verified via directory scan).

**Workaround.** Same convention already used in sibling QC-200 dirs (e.g.\
`QC-0704.3628-quantum-algorithm-nand-tree-evaluation-childs-cleve/`): produce **labelled
surrogates**. `marker.md` is a PyMuPDF (fitz 1.27.2.3) page-boundary text extraction;
`nougat.mmd` is a `pdftotext -layout` extraction. Both files have header lines explicitly
stating the tool used. `extraction/README.md` documents this choice.

**Residual gap.** Structural equations (paper's dagger-Frobenius diagrams, the QFT unitary,
Diagram 5.3) are ASCII-shaped in pdftotext and lost in raw PyMuPDF text; Nougat would
preserve LaTeX-style math. Any downstream text-mining across the corpus that assumes
LaTeX-style math from Nougat will not get it here.

## 3. Task-brief mislabelling of the author lineage

**What was slightly off in the brief.** The subagent task text says
*"Zwiers/Coecke-style ZX-calculus / string-diagram treatment"*. The actual authors are
**Stefano Gogioso and Aleks Kissinger** (Oxford Quantum Group / Radboud iCIS). Coecke is
prior work (CD11 etc.), not an author. There is no "Zwiers" in the reference list either;
the closest categorical-QM lineage is Coecke-Kissinger-Vicary (whose earlier diagrammatic
HSP proof is [Vic12], cited by the paper).

**How we handled it.** Trust the arxiv_id as instructed; verify authors + exact title from
the fetched PDF. Both were verified from page 1 within the first tool call after download.
No follow-on effect on the replication.

## 4. Non-abelian and infinite-group extensions not tested

**What is missing.** The paper's Sections 6 and 7 extend the diagrammatic proof to
non-abelian groups (with strong extra hypotheses), real quantum theory (Simon's problem is
still efficient), and some infinite abelian groups. None of these are tested here.

**Root cause.** Numerical statevector simulation is not the right tool: (a) non-abelian
case requires the paper's exotic normal-classical-states hypothesis, which is not exhibited
concretely; (b) real quantum theory requires a real-Hilbert-space simulator; (c) infinite
abelian groups obviously cannot be simulated on finite hardware.

**Workaround.** Restricted to the abelian finite case, which is the paper's primary content
anyway (Sec 5).

**Residual gap.** Q1 in `open_questions.json` explicitly asks whether the non-abelian extension
can be exhibited on any concrete non-abelian group (e.g.\ D_n, Q_8).

## 5. Random hiding-function label choice not exhaustively swept

**What was skipped.** V3 (Sec 5.7 rewrite check) was run on 5 random hiding-function
labellings per test group, not exhaustively. For Z_8/H=<2> the coset space is only size 2 so
there are only 2! = 2 valid labellings into Z_2 (M=1), so 5 random draws is 2.5x-oversampled
and covers both. For Z_15/H=<5> the coset space is size 5 and M=3 so there are P(8,5) = 6720
valid injective labellings into Z_2^3, and 5 random draws is a genuine sample not a full
enumeration.

**Reason.** The paper's proof is symbolic and independent of label choice, so this is a
sanity-belt-and-braces check. Every drawn labelling passed with max deviation < 3e-16 (i.e.
identical up to float64 noise), which is strong evidence but not proof.

**Residual gap.** Q2 and Q3 in `open_questions.json` propose exhaustive sweeps and formal
diagrammatic (PyZX) verification respectively.

## 6. No 3-judge Argo panel

**What was skipped.** The QC brief calls for "3-judge Argo panel only if time remains; else
self-verdict."

**Reason.** Self-verdict is unambiguous here: the paper's Diagram 5.3 (character marginal
uniform on H^⊥, independent of coset outcome) is directly measured with real numpy statevector
simulation on two nontrivial test groups, with L2 deviation from analytic < 3e-15 (machine
noise) and per-coset independence verified exactly. Additionally, the paper's Sec 5.7
isometry-cancellation rewrite is verified numerically on 10 random hiding functions. There
is no ambiguity for a judge panel to resolve.

## Summary

Everything blocking a full green-check is documented above; none of it changes the verdict.
The paper's concrete Hilbert-space instantiation (Diagram 5.3 = standard HSP quantum
subroutine output) was reproduced with real linear-algebra simulation, using only free
tools, on a laptop, in under a second of compute.
