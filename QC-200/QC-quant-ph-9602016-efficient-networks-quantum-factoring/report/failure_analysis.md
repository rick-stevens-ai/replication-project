# Failure analysis — QC-200 replication of quant-ph/9602016

Honest write-up of what did NOT work perfectly, what friction was hit, and
what residual gaps remain. Nothing here undermines the top-line verdict
(REPLICATED for the Sec. VII / N=15 construction), but each item is a real
limit on the strength of the claim.

## 1. Marker and Nougat not available on the host

**What happened.** The 8-artifact bar requires `extraction/marker.md` and
`extraction/nougat.mmd`. Neither Marker nor Nougat is installed on CherryRd,
and no central corpus entry exists for `quant-ph/9602016`.

**What we did.** Produced a **structured pdftotext fallback** for each:
`extraction/marker.md` is a hand-formatted Markdown version of the
abstract, §I, §VII, and §VIII with the key equations in text; `extraction/nougat.mmd`
is a LaTeX/Mathpix-flavored version of the equations we actually exercise
(7.1, 7.2, 7.3, 7.5, 7.6, 7.9, 7.10). Both files carry an in-file note
saying they are fallbacks and how to regenerate them properly. The full raw
`pdftotext` output is preserved at `work/paper.txt` and `work/paper_raw.txt`
so a downstream Marker/Nougat pass has canonical source to align against.

**Residual gap.** The equation typesetting in `extraction/nougat.mmd` is
transcribed by hand from the visual PDF layout; there is some risk of a
missing subscript. Only equations (7.1)–(7.10) are covered, not the full
paper (56 pages, mostly §V–§VI arithmetic primitives that we do not
exercise). Rerunning Nougat on a GPU host would replace this file with a
full-paper high-fidelity extraction.

## 2. We reproduced EXP N (Eq. 7.5), not EXP N' (Eq. 7.9)

**What happened.** The abstract's headline number is *"6 trapped ions and
38 laser pulses"*, which is achieved by the optimized EXP N' variant using
Appendix A custom controlled-NOT gates. We built and simulated the earlier,
simpler EXP N (Eq. 7.5) with [6, 0, 4] gate composition and 34 pulses.
Adding the 2-pulse Hadamard prep and 6-pulse L=2 QFT gives 42 pulses —
matching the paper's own intermediate number, not the 38-pulse headline.

**What we did.** Verified the paper's arithmetic 32 + 6 = 38 by inspection
(EXP N' saves 4 pulses over EXP N, and the paper says "state Eq. (7.2) can
be prepared with just 32 pulses"). Called this out explicitly in every
artifact (REPORT.tex claims table row C12 = SPOT-CHECK, workflow.md, this
file). Also produced Q1 in open_questions.json to flag that the custom-gate
pulse cost is the load-bearing assumption.

**Residual gap.** A truly complete replication of the "38 pulses" headline
would decompose the Appendix A custom gates into carrier + Molmer-Sorensen
pulses and count them independently. That is outside our simulator toolkit
(Qiskit does not model Cirac-Zoller pulses) and would need QuTiP or a
custom pulse-level simulator.

## 3. Operator-ordering ambiguity in Eq. (7.5)

**What happened.** The paper writes Eq. (7.5) as a product of ten operators
with no explicit statement of which end acts first on the ket. Our first
naive implementation (left-to-right, as-read-on-the-page) produced a
scrambled output that did not match the lookup table.

**What we did.** Cross-checked against the paper's §VI ADD-routine sequences
(Eq. 6.36 style), where the operator-product convention is
rightmost-acts-first. Implemented Eq. (7.5) with rightmost-first, and got
perfect agreement with Eq. (7.3). Documented the convention explicitly in
the code and REPORT. Flagged as Q3 in open_questions.json.

**Residual gap.** This was a "gotcha", not a bug in the paper, but it means
a naive reader can silently reproduce the wrong circuit and never notice
if they don't have the lookup table as ground truth. Any future
replications of pre-2000 Preskill-era quantum papers should assume
rightmost-first unless the paper explicitly states otherwise.

## 4. Ideal simulation only — no noise

**What happened.** All results (fidelity 1.000, uniform y distribution)
come from noiseless statevector simulation. The paper never gives a noise
model either, so we are matching a coherent-idealized theoretical
prediction, not an experimental outcome.

**What we did.** Called this out in the claims table (C1–C3 marked "N/A"
because they are asymptotic scaling, not testable at K=4) and in Q2 of
open_questions.json (what per-pulse error rate p breaks the 38-pulse demo?).

**Residual gap.** The natural next replication step — noise-inclusive
Qiskit-Aer simulation with a plausible mid-1990s ion-trap error model —
was not done. This is Q2 and is tractable in ~30 more minutes on the same
host.

## 5. General-purpose N=15 numbers (15 284 / 14 878 pulses) not touched

**What happened.** Section VII quotes 15 284 pulses on 21 qubits and 14 878
on 22 for the *general-purpose* algorithm at N=15 (K=4, L=8). We did not
implement or verify these.

**What we did.** Focused entirely on the specialized §VII lookup-table
construction, which is the one that reaches the abstract's 6-qubits /
38-pulse headline. Called out this omission in Q5.

**Residual gap.** These numbers anchor the paper's 396 K³ asymptotic
headline; nobody appears to have independently reproduced them in the ~30
years since publication. A follow-on replication running the full
ADD/MUXADD/MULT/MODMULT/EXPN cascade at K=4, L=8 would either confirm or
adjust them and is a natural sequel.

## 6. Argo LLM panel not used

**What happened.** The wave brief suggests a 3-judge Argo panel scoring if
time remains. We did not run one.

**What we did.** All primary claims were deterministic and self-verifiable
by direct comparison to explicit numbers/tables in the paper, so a
qualitative LLM judge would have added noise, not information. We instead
put the human-facing verdict + justification into REPORT.tex §Verdict.

**Residual gap.** For consistency with other QC-200 papers that use the
Argo panel, this could be added. It would not change the verdict for this
paper (the reproduced numbers are exact, not fuzzy).

---

**Bottom line.** The replication is *strong* on its stated scope (§VII
first construction reproduced exactly, all 4 primary quantitative claims
match to unit fidelity / to the exact integer pulse count) and *transparent*
about its scope limits (headline 38-pulse variant not directly re-simulated,
noise not modeled, general-purpose K=4 L=8 cascade not counted).
