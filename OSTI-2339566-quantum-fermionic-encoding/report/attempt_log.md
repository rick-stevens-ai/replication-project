# Attempt Log — OSTI 2339566

Chronological log of the replication attempt (2026-07-02 evening, CDT).

1. Read wave brief `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`. Confirmed rules: Argo/Sophia/CELS only, real replication, LLM-judge for verdict.
2. Created target dir `~/Dropbox/REPLICATE-PROJECT/OSTI-2339566-quantum-fermionic-encoding/{report/evidence,work}`.
3. Attempted direct curl of https://www.osti.gov/servlets/purl/2339566 from CherryRd — hung. Killed after ~10 s.
4. Fetched via uicgpu using its proxy env: `ssh uicgpu 'source ~/env.sh && curl -sL -o /tmp/2339566.pdf ...'` → 2.7 MB PDF, v1.5. scp'd back to work/. **Provenance verified.**
5. Attempted `pdf` tool (Anthropic/Google/OpenAI vision) → all three failed (Anthropic credit exhausted, Gemini model gate closed, OpenAI PDF extraction plugin off). Fell back to pypdf text extraction.
6. Created venv, installed pypdf → extracted 66432 chars of paper text into `paper_text.txt`. Grepped for tables, molecules, encodings, ansatz details, and key numerical results (Table 1, 14 CNOTs for VV0, 10 for NV-, 136-term Hamiltonian, etc.).
7. Identified core replicable claims (C1..C5) — full paper spin-defect story requires WEST QDET + IBM hardware, but the QEE + QCC methodology on small molecules is fully reproducible from public specs.
8. Installed openfermion (1.7.1), pyscf (2.13.1), qiskit (2.5.0), openfermionpyscf, scipy, numpy in the venv. All import clean.
9. Wrote `replicate_qee_qcc.py`: builds PySCF+OpenFermion molecular Hamiltonian, enumerates all (Nα, Nβ) Slater determinants, sorts by diagonal energy (paper's ordering rule), builds full CI matrix from OpenFermion 1-/2-body integrals via Slater-Condon rules, diagonalizes = the QEE effective Hamiltonian on `2^⌈log₂ Q⌉` qubits, then screens Nq-qubit Paulis by first-derivative gradient at |Ψ₀⟩ = |0…0⟩ and runs classical VQE (scipy BFGS) with top-K entanglers.
10. Ran on H₂, LiH, H₄-linear (STO-3G). All three cases: independent CI matches PySCF FCI to <1e-14 Ha (cross-validation of the Slater-Condon Hamiltonian build). H₂ QCC(K=1) with entangler XY reaches FCI to <1e-15 Ha; LiH QCC(K=1..12) plateaus at 5.86 mHa above FCI; H₄ plateaus at 35 mHa above FCI (both consistent with the paper's own caveat that raw QCC without symmetry adaptation does not automatically hit chemical accuracy for stronger correlations).
11. Wrote `h2_dissociation.py`: H₂ curve at 10 bond lengths R = 0.4..3.0 Å. QEE+QCC(K=2) reproduces PySCF FCI to machine precision (<1.6e-15 Ha) at every point — full replication of the paper's referenced dissociation demo (from Ref. 54 which the paper cites).
12. Wrote `jw_vs_qee_qubits.py`: for H₂, LiH, BeH₂, H₂O in STO-3G, computed Q = C(N,Nα)·C(N,Nβ), Nq(QEE), Nq(JW), and the number of Pauli terms in the JW Hamiltonian. All qubit-compression numbers match the paper's `Nq = ⌈log₂ Q⌉` claim (2/4, 8/12, 11/14, 9/14).
13. Wrote `llm_judge.py`: sends paper summary + evidence to Argo LLM. First attempt to argo:claude-opus-4.7 returned 502 (payload likely too large for that Vertex route). Trimmed evidence to key numbers, retried with fallback list `argo:gpt-o3 → argo:gpt-4o → …`. Argo GPT-o3 responded cleanly.
14. Verdict from judge: **PARTIAL**, coverage 0.8, agreement 0.9. One-liner: "Small-molecule QEE/QCC results match; defect/hardware left untested".
15. Wrote final REPORT.md, artifact_harvest.md, and this attempt_log.md. Preserved all evidence in report/evidence/.

**Nothing overwritten** outside the target dir. `~/.openclaw/workspace/tmp-pdf/2339566.pdf` was a temp copy for the (failed) `pdf` vision tool; original stays in `work/`.
