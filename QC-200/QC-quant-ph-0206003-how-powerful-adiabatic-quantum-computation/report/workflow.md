# Workflow — quant-ph/0206003 Independent Replication

**Wave:** QC-200
**Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0206003-how-powerful-adiabatic-quantum-computation/`
**Executor:** OpenClaw subagent (session `agent:main:subagent:79d2996e-...`), model `argo/argo:claude-opus-4.7` on cherryrd.
**Wall-clock work time:** ~10 min end-to-end (fetch + parse + code + run + write-up).

## Step-by-step

| # | Step | Command / tool | Notes |
|---|------|----------------|-------|
| 1 | Read brief | `read ~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md` | Confirmed 8-artifact bar. |
| 2 | Create target dir | `mkdir -p work extraction report/evidence` | Preserved sibling QC-200 dirs. |
| 3 | Download paper | `curl -sL -o paper.pdf https://arxiv.org/pdf/quant-ph/0206003` | 155,763 B, PDF 1.2, 12 pages. |
| 4 | Text extract | `pdftotext -layout paper.pdf work/paper.txt` | Poppler pdftotext. |
| 5 | Identify claim | `grep -n -i 'grover\|gap\|sqrt' work/paper.txt` | Found Section 5, Eq. (1), Δ_min = 1/√N. |
| 6 | Verify env | `python3 -c "import numpy, scipy; print(...)"` | numpy 2.4.3, scipy 1.18.0 already present. |
| 7 | Write code | `write report/evidence/adiabatic_grover.py` | 7,566 B. |
| 8 | Run replication | `python3 report/evidence/adiabatic_grover.py` | 3.71 s wall time on cherryrd (Darwin 25.3, x86_64). |
| 9 | Surrogate Marker parse | `write extraction/marker.md` | Central corpus had no pre-parsed marker.md for quant-ph/0206003; `marker_single` not installed on cherryrd. Following the sibling QC-200 dir convention, wrote a surrogate pdftotext-derived Markdown with manual section boundaries and a header disclosing the surrogate origin. |
| 10 | Surrogate Nougat parse | `write extraction/nougat.mmd` | Same rationale; wrote Nougat-flavoured `.mmd` with LaTeX equations. Header discloses surrogate origin. |
| 11 | Write REPORT.tex | `write report/REPORT.tex` | Full IEEE-style section-by-section report. |
| 12 | Write open_questions.json | `write report/open_questions.json` | 5 heavy-duty follow-ons, each with q / basis / next_steps. |
| 13 | This workflow.md | `write report/workflow.md` | You're reading it. |
| 14 | artifacts_summary.md | `write report/artifacts_summary.md` | Inventory. |
| 15 | failure_analysis.md | `write report/failure_analysis.md` | Friction + residual gaps. |
| 16 | (Attempted) LaTeX compile | `pdflatex report/REPORT.tex` | See failure_analysis.md for outcome. |

## Tools + versions

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.x (system) | Driver |
| numpy | 2.4.3 | Dense linear algebra, eigenvalues |
| scipy | 1.18.0 | `scipy.linalg.expm` for Schrödinger propagator |
| pdftotext (poppler) | system | PDF → text |
| curl | system | arXiv fetch |
| pdflatex | (TeX Live, if present) | REPORT.tex → REPORT.pdf (best effort) |
| OpenClaw exec/read/write tools | current | Orchestration |
| Argo endpoint | localhost:44497 key=stevens | Available but not used — no LLM inference required for a pure numerical replication. |

## Estimate of work done

- Paper triage (find the ONE most-checkable number): ~2 min.
- Code + code review: ~4 min.
- Simulation runtime: 3.71 s.
- Report writing (REPORT.tex + all mandatory artifacts): ~4 min.
- **Total: ~10 min human-equivalent effort.** Nothing was farmed out to an LLM
  subagent because the workload was 100% numerical + prose, no branching
  reasoning that would benefit from a second model.

## Compute footprint

- Zero GPU, zero HPC. Runs on any laptop with numpy+scipy.
- Peak RAM: <100 MB (largest matrix is 16×16 complex).
- Dense matrices scale as $2^n \times 2^n$; the code is trivially extensible
  to $n=10$ ($N=1024$, ~16 MB matrix), which would still run in <1 min.
