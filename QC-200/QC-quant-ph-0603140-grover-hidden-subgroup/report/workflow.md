# Workflow — Replication of Lomonaco & Kauffman (arXiv:quant-ph/0603140)

## Narrative

1. **Read wave brief.** `~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`
   and the 8-artifact standard `REPLICATION_DIR_STANDARD_2026-07-05.md`.
2. **Fetch paper.** `curl -sL https://arxiv.org/pdf/quant-ph/0603140 -o work/0603140.pdf`.
   Author-verify from PDF: Samuel J. Lomonaco Jr. (UMBC) & Louis H. Kauffman (UIC),
   dated 2006-03-15 — matches arxiv metadata.
3. **Skim & extract claims.** `pdftotext work/0603140.pdf work/0603140.txt`; read all
   ~700 lines. Identify the paper is largely theoretical: the reproducible core is
   (i) standard Grover success probability, (ii) invariance under Stab_{j0},
   (iii) the coset structure of Prop.1, (iv) both parts of the Section-9 "However"
   argument, and (v) the pushed-oracle equivalence of Section 8. Section 9's central
   claim (standard QHS cannot solve this HSP) is confirmed structurally via
   Hallgren-Russell-Ta-Shma (cited, not re-derived).
4. **Set up environment.**
   `python3 -m venv ~/.qc_venv && . ~/.qc_venv/bin/activate && pip install qiskit qiskit-aer numpy sympy`
   → qiskit 2.5.0, numpy 2.5.1, sympy 1.14.0.
5. **Write single monolithic simulation script** `code/grover_hsp.py` covering:
   - A. Textbook Grover on N=4,8,16 via `qiskit.QuantumCircuit` + `Statevector`
   - B. Random-permutation invariance check
   - C. Exhaustive coset enumeration via sympy `PermutationGroup`
   - D. Normal-subgroup ∩ Stab_0 check + pairwise-conjugacy check
   - E. Induced-rep dimension report (structural, references HRT)
   - F. Pushed-oracle vs Grover-oracle equivalence
6. **Run.** `python code/grover_hsp.py` — wall clock ~2 s on M1 MacBook.
   Every check passes (see `report/evidence/results.json`).
7. **Marker/Nougat.** Not installed in this environment; write pdftotext-fallback
   `extraction/marker.md` and `extraction/nougat.mmd` per sibling convention
   (QC-quant-ph-0102014-nonabelian-hidden-subgroup).
8. **Write REPORT.tex** with claims table, per-part results, verdict.
9. **Write open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md.**
10. **Verify 8-artifact bar** with `~/Dropbox/REPLICATE-PROJECT/scripts/check_repl_dir_standard.py`.

## Tools and codes used (with versions)

| Tool                    | Version    | Purpose                                        |
|-------------------------|------------|------------------------------------------------|
| Python                  | 3.14       | runtime                                        |
| Qiskit                  | 2.5.0      | Grover circuit build + Statevector simulation  |
| numpy                   | 2.5.1      | permutation unitaries, fidelity                |
| sympy                   | 1.14.0     | `PermutationGroup`, `SymmetricGroup`, `AlternatingGroup`, exact coset arithmetic |
| Poppler `pdftotext`     | system     | PDF → text (both reading and marker/nougat fallback) |
| curl                    | system     | fetch PDF from arxiv                           |
| bash / zsh              | system     | glue                                           |

Custom code:
- `code/grover_hsp.py` (~450 LOC) — Parts A–F end-to-end.

## Effort estimate

| Category          | Amount                                             |
|-------------------|----------------------------------------------------|
| Compute wall-time | ~2 s (Grover N=16 statevector) + ~1 s (sympy S_5)  |
| Human/agent time  | ~15 min planning + reading + coding + review       |
| LOC written       | ~450 (grover_hsp.py) + ~250 (REPORT.tex) + ~100 (docs) |
| Runs executed     | 1 clean run of `grover_hsp.py` (all Parts passed on first go) |
| PDFs fetched      | 1 (0603140.pdf, 185 KB)                            |
| No LLM calls      | Zero paid endpoints; no Argo calls needed          |
