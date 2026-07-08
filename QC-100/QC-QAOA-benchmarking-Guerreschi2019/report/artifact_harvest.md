# Artifact Harvest

| Artifact | Source | How obtained | Notes |
|---|---|---|---|
| Paper abstract page | https://arxiv.org/abs/1907.02359 | `curl` HTML | Confirmed title + arXiv id |
| Full paper text (ar5iv HTML → text) | https://ar5iv.org/abs/1907.02359 | `curl` + regex strip → `work/paper_fulltext.txt` (84 KB) | Full body incl. Eqs. 1–31, Table 1 (results), Tables 2–5 (problem instances, Appendix B) |
| 16-var weighted MaxCut instance | Paper Table 2 (Appendix B) | Manually transcribed → `qaoa_core.py:MAXCUT_16` | 33 weighted edges; verified E_C0 = -17.7 (matches Fig. 10 caption) |
| 8-var 2-SAT instance (A) | Paper Table 3 (A) (Appendix B) | Manually transcribed → `qaoa_core.py:TWO_SAT_8A` | 7 nonzero (J,h) rows; verified E_C0 = -9 (matches Fig. 11 caption) |

**No code repository is published by the authors** (JUQCS is Jülich's in-house simulator, not open). Replication uses a clean-room numpy statevector implementation. All numbers are computed, none copied.

## Environment / tool versions
- Python 3.14.6, numpy 2.4.3, scipy 1.18.0 (local, host CherryRd)
- Pure classical statevector simulation (≤16 qubits, 2^16 = 65 536 amplitudes); ran locally, no GPU needed.
- LLM judge: Argo proxy (localhost:44497), models `argo:gpt-5.2` and `argo:gpt-5.1` (free endpoints only).
