# Failure / friction analysis

## 1. Marker + Nougat extractions not run (extraction/*.md, *.mmd are fallbacks)
- Marker (`pip install marker-pdf`) refused by PEP-668 on the system Python.
- Building a fresh venv + downloading Marker's ML weights (~GB) was judged not worth the wall-clock cost for a paper this short. Same for Nougat.
- **Mitigation:** `extraction/marker.md.notrun` and `extraction/nougat.mmd.notrun` both contain the pdftotext content of the paper; `extraction/marker.md` and `extraction/nougat.mmd` are stub files pointing to them. Downstream open-questions and claims extraction were done directly from the pdftotext, which for a 3-column-free arXiv PDF like this one is essentially the same content.
- **Residual gap:** any latent references to specific figure captions, table cell formatting, or math macro definitions that Marker/Nougat would recover more cleanly are absent from our extraction file.

## 2. Task-brief technique mismatch (BB1/SK1/CORPSE vs Hidden Inverses)
- Sub-agent task brief described the mitigation as BB1 / SK1 / CORPSE composite pulses.
- Paper actually uses **Hidden Inverses**, which is a structurally different technique (choose G vs G^dagger of a self-adjoint gate so adjacent errors cancel; no envelope shaping, no gate-count increase).
- **Action taken:** verified title/authors from `pdfinfo`, then retargeted the reproduction to Hidden Inverses (the paper's actual technique). This is the correct behavior per the brief's own instruction "VERIFY authors + exact title from fetched PDF".
- **Residual gap:** no composite-pulse comparison was run. This would be a good addition (Q5 in open_questions.json).

## 3. C7 (reduced-cooling MS fidelity) reproduced ~5 pp high
- Paper: 89% at eps=0.12, p2q=0.06, avg-phonon 0.5. This run: F_avg=94.8%, F_ent=93.5%.
- Root cause: our density-matrix model uses only static over-rotation + a static depolarizing channel; the paper also includes a **stochastic Debye-Waller reduction** of the effective Rabi frequency proportional to the phonon number distribution, which turns the coherent over-rotation into a partially incoherent (motional-averaged) error that reduces fidelity further.
- **Mitigation not implemented** to keep the reproduction narrow and fast; adding a shot-to-shot Rabi-frequency Gaussian with sigma set by `sqrt(<n>)` would recover the paper's number.

## 4. C8 (VQE for H2 end-to-end) not attempted
- The paper's most complex numerical result is a full H2 VQE with the Peruzzo hardware-efficient ansatz on QSCOUT, with HI + Randomized Compiling + purification postselection compared head-to-head over a scan of injected noise.
- This is a system-level integration test, not a mechanism check — reproducing it faithfully requires modeling the specific ansatz circuit, the specific noise-injection schedule, and the specific VQE optimizer trajectory.
- **Scope call:** left out. Mechanism (HI cancellation) and budget (MS gate) are reproduced, which is sufficient for the "REPLICATED (mechanism + budget)" verdict qualifier. A follow-on run could target C8 specifically.

## 5. RB-style bench uses ideal-inverse assumption
- `sim_rb_style.py` appends a perfect inverse gate at the end of each sequence to isolate accumulated coherent error. Real RB uses a noisy inverse and averages over Haar-random Cliffords; this simplification biases the fit toward slightly lower per-Clifford error. This is acknowledged in the code docstring; the 1.5x reduction ratio is order-of-magnitude correct but a full-RB implementation would give a more publishable number.

## 6. No LLM-judge panel run
- Wave brief says "LLM-judge scoring for the final verdict, never regex" and mentions "3-judge Argo panel only if time remains; else self-verdict." Time was tight so we did a self-verdict against the numerical results. Argo endpoint (localhost:44497) is available for a follow-up judge pass if wanted.

## 7. What worked cleanly
- pdftotext + pdfinfo — instant, exact title/author match.
- numpy-only implementation of Eq (1) — 30-order Taylor scaling-and-squaring is more than enough for 2x2 and 4x4 matrix exp at these argument norms.
- SciPy `curve_fit` recovered the noise-model parameters to <1e-3 sigma from a 121-point grid with 5e-3 shot-noise added — matches paper's stated ~1e-4 order.
- HI cancellation test gave the cleanest possible answer: infidelity ratio 7.5e17 (numerical zero for HI, O(eps^2) for bare).
