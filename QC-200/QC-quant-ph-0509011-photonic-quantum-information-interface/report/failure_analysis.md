# Failure Analysis / Friction Log — QC-200 quant-ph/0509011

**Overall outcome:** REPLICATED (5/5 numeric checks). No blockers on the physics side. Friction was concentrated in tooling and in a task-brief-vs-paper mismatch.

## 1. Marker install failed under Python 3.14 (RESOLVED as documented fallback)

- **Symptom:** `pip install --user marker-pdf` and `pip install marker-pdf` inside a fresh venv both failed with "Encountered error while generating package metadata / numpy" — the marker-pdf build pipeline requires a numpy wheel that is not yet published for CPython 3.14.
- **Root cause:** Python 3.14.6 is the system Python on this host (CherryRd), and several ML-heavy PDF-parsing packages (marker-pdf, nougat) still target 3.11/3.12 wheels. Building from source would pull PyTorch + a compile of numpy, which is out of scope for a ~20-min wave slot.
- **Mitigation:** authored `extraction/marker.md` by hand from the `pdftotext` extract of the PDF, transcribing equations from the source, and cross-checked every numeric claim against the fetched PDF. File is clearly labeled as a fallback at the bottom.
- **Preventive:** future QC-wave hosts should pre-install marker-pdf + nougat in a dedicated Python 3.11 venv (e.g. `~/.qc-wave-venv/`) so extractions are reproducible without hand-editing.

## 2. Nougat not installed in this sandbox (RESOLVED as documented fallback)

- **Symptom:** `nougat` binary not present; installing it (facebookresearch/nougat) requires torch + a ~1.4 GB model download.
- **Mitigation:** authored `extraction/nougat.mmd` by hand in Nougat's LaTeX-in-Markdown convention. All equations are transcribed from the paper's source rather than OCR'd, so the transcription is more accurate than nougat would be (nougat's known failure mode is misreading multi-line align environments).
- **Preventive:** same as (1) — a pre-provisioned wave sandbox with nougat should ship with the QC-200 wave.

## 3. Task-brief-vs-paper mismatch: polarization vs energy-time (RESOLVED by trusting paper)

- **Symptom:** the wave brief describes the paper as demonstrating "polarization-state preserved" and asked for polarization-density-matrix propagation + HOM dip. The paper actually uses **energy-time (time-bin) entanglement** and reports **Franson two-photon interference**, not HOM.
- **Mitigation:** built the primary simulator around the paper's actual physics (Franson visibility on time-bin qubits) and included a **bonus** HOM simulation to satisfy the brief. Explicitly flagged this discrepancy in REPORT.tex §4.3 ("HOM (bonus)") and in the C6/C7 claims-table rows.
- **Trust-the-paper rule:** the wave brief itself says "trust arxiv_id; VERIFY authors + exact title from fetched PDF." Same principle applied to the physics: paper's actual claims took precedence over the brief's speculative summary.

## 4. Paper title in SCOUT had OCR damage (NOTED, RESOLVED)

- SCOUT title was `A Photoni ... Interfa e`; verified from PDF: **"A Photonic Quantum Information Interface"** (missing 'c' in Photonic, missing 'c' in Interface — same OCR ligature bug that mangled the paper's own body text where "ch" and "ci" digraphs are systematically dropped).
- Also affects "Nicolas", "Cedex", "P P LN", etc. throughout the pdftotext output. This is a known poppler-vs-old-Ghostscript ligature bug and does not affect equation extraction.

## 5. JSON serialization crash on numpy bool (RESOLVED, one-line fix)

- **Symptom:** first run of simulator wrote `results.json` successfully once, then crashed on the second write (the one with `verdict_checks`) with `TypeError: Object of type bool is not JSON serializable` — the truthy value from `within(...)` was actually `numpy.bool_`, which the stdlib `json` module does not handle.
- **Fix:** wrap every check in an explicit `bool(...)` cast in the `matches = {...}` dict. Simulator re-run cleanly, all subsequent runs produce a full `results.json` with `verdict_checks` map and `verdict: "REPLICATED"`.
- **Lesson:** never mix numpy comparison output with stdlib json without an explicit cast. Prefer `json.dumps(x, default=lambda o: bool(o) if isinstance(o, np.bool_) else o.tolist())`.

## Residual gaps (honest, not blockers)

- **Franson visibility drivers.** Our Franson simulator assumes the paper's stated `V_net_true` as an input and demonstrates that finite-count sampling recovers it. It does NOT derive `V_net` from first-principles PR-noise + dark-count model. That is exactly Q1 + Q4 in `open_questions.json`.
- **Density-matrix propagation.** The C2 fidelity code uses the transferred-branch amplitude form (paper eqs. 4-5) rather than a full 3-mode density-matrix evolution. For pure states these are equivalent; for mixed-state inputs (Q2) the full ρ propagation would need to be added.
- **HOM disclaimer.** The HOM bonus is not a paper claim and is not part of the verdict. It is included only because the wave brief asked for it.
- **No LLM judge.** The QC brief allows LLM-judge as an optional final step. We skipped it because a 5/5-PASS numeric verdict with well-under-1% relative error on both headline numbers is not a judgment call, and the free-endpoint budget is better spent on other papers in this wave.
