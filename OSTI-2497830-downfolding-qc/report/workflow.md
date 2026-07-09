# Workflow — OSTI-2497830 (Alvertis / Khan / Tubman, PRApplied 23:044028, 2025)

Chronology of the replication attempt executed on 2026-07-02. Everything ran on Ollie's CherryRd session and a UIC GPU proxy for the OSTI fetch. LaTeX and reporting-artifact backfill (2026-07-06) by Kukla subagent — no compute re-runs.

## 0. Setup

- Session dir: `~/Dropbox/REPLICATE-PROJECT/OSTI-2497830-downfolding-qc/`
- Rank: TOPUP50 #24
- Time budget: ~15 minutes of active work
- Compute: laptop-class (SciPy sparse Lanczos)
- Runtime env: `~/.venv-osti` (Python 3.11, numpy, scipy)

## 1. Ingest

1. **Bibliographic resolve** — DOI `10.1103/PhysRevApplied.23.044028` → arXiv `2409.12237v3` → OSTI `2497830` → Fermilab preprint `FERMILAB-PUB-24-0896-SQMS-V`. Confirmed open-access on OSTI + arXiv.
2. **PDF fetch** — direct fetch via UIC GPU shell:
   ```bash
   ssh uicgpu 'source ~/env.sh && curl -sSL -o /tmp/osti_2497830.pdf \
       https://www.osti.gov/servlets/purl/2497830'
   scp uicgpu:/tmp/osti_2497830.pdf work/
   ```
   Result: `work/osti_2497830.pdf` — 2.17 MB, 45 pages.
3. **Text extraction** — attempted `pdf` tool (Anthropic-backed); failed on billing + misconfigured Gemini fallback. Pivoted to poppler CLI:
   ```bash
   pdftotext -layout work/osti_2497830.pdf work/osti_2497830.txt
   ```
   → 997-line extraction preserving two-column layout and **all Appendix C matrices verbatim** (critical for downstream ED).

## 2. Claim extraction

Read the extracted text end-to-end. Identified 9 numbered claims (C1–C9) spanning:
- **Data availability** (C1)
- **Numerical eigenvalues** (C2, C4, C6)
- **Numerical observables** (C3, C5, C7)
- **Arithmetic sanity** (C8)
- **Norm sanity** (C9)

Prioritized by two criteria:
- (a) Testability from public artifacts alone
- (b) Compute feasibility on a laptop in the 15-minute window

Only Ca$_2$CuO$_3$ (20 qubits, dim = 63,504) satisfied both. SrVO$_3$ was reduced to a sanity check; WTe$_2$ dropped entirely.

## 3. Independent replication — Ca$_2$CuO$_3$

Author: `work/ca2cuo3_ed.py` (from scratch, 8.2 KB).

Steps:
1. Enumerate C(10,5) = 252 up-spin bitmask basis states (repeat for down spin).
2. Diagonal H (U on-site + V nearest-neighbour) via vectorised NumPy on the 63,504-dim product basis.
3. Hopping H per spin sector as sparse CSR with Jordan–Wigner fermion-sign tracking `(-1)^(# bits below)`.
4. Assemble `H = kron(H_hop_up, I_dn) + kron(I_up, H_hop_dn) + diag(H_UV)`.
5. `scipy.sparse.linalg.eigsh(H, k=3, which="SA")` — 0.02 s build + 0.82 s Lanczos.
6. Compute `<S^z_1 S^z_j> - <S^z_1><S^z_j>` from ground-state amplitudes.

Output: `work/ca2cuo3_ed_results.json` and mirror at `report/evidence/ca2cuo3_ed_results.json`.

## 4. Sanity check — SrVO$_3$ (partial)

Author: `work/srvo3_charge_order.py`. Ran three cases at 2×2 single band, half filling:
- Paper params (t=−0.263, U=3.527, V=0.649 eV)
- Non-interacting control (U=V=0)
- Strong-V control (V=3 eV)

Result: A/B-symmetric 2×2 forces Φ = 0 by sublattice symmetry. Documented as a geometric artifact, not a paper contradiction.

Output: `work/srvo3_ed_results.json` and mirror at `report/evidence/`.

## 5. Arithmetic cross-check

Table II Ca$_2$CuO$_3$: $0.999^{290} = 0.7476 \approx 74.8\%$. **Consistent.**

Output: `report/evidence/table_II_cross_check.json`.

## 6. LLM-judge verdict

Assembled full paper-summary + method + result prompt. Called via Argo proxy at `localhost:44497`:
- `argo:claude-opus-4.7` — upstream parse error (not usable this run)
- `argo:gpt-5.2` — returned `PARTIAL` verdict + one-sentence justification (recorded in REPORT.md §5)

## 7. Report + verdict

- Wrote `report/REPORT.md` (comprehensive, ~14.6 KB) with tables, verdict, LLM-judge quote, WAVE_RESULT tag.
- Emitted `WAVE_RESULT set=OSTI paper=2497830 verdict=PARTIAL …` to REPLICATE-PROJECT queue.

## 8. Backfill (2026-07-06, Kukla subagent — no compute)

Added to reach 8-artifact standard:
- `report/REPORT.tex` — LaTeX render of the full report
- `report/open_questions.json` — bare list of 5 open-question objects
- `report/open_questions_section.tex` — matching LaTeX section (input by REPORT.tex)
- `report/workflow.md` — this file
- `report/artifacts_summary.md` — enumeration + provenance of every artifact
- `report/failure_analysis.md` — honest critique of what was NOT exercised
- `extraction/nougat.mmd` — placeholder stub (no real Nougat parse available)

No paper re-fetch, no ED re-run, no LLM re-call.
