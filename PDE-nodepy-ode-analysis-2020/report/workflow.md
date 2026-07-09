# Workflow — NodePy replication

## Pipeline

```
[JOSS PDF] --pdftotext--> [paper_raw.txt] --hand-cleanup--> [extraction/marker.md]
                                                                       |
                                                                       v
                     [claims C1..C9 mapped to nodepy API calls]  in  work/replicate.py
                                                                       |
                                                                       v
                                    python work/replicate.py --> [report/evidence/*.json, *.png]
                                                                       |
                                                                       v
                                    Argo /v1/chat/completions --> [report/evidence/llm_judge.json]
                                                                       |
                                                                       v
                                                              [report/REPORT.md + REPORT.tex]
```

## Tools

| Tool | Version | Role |
|---|---|---|
| Python | 3.14.6 | Interpreter (macOS 25.3.0, Darwin, x86_64) |
| nodepy | 1.0.1 | Package under test (from PyPI) |
| numpy | 2.5.1 | Numeric arrays / poly1d |
| sympy | 1.14.0 | Exact arithmetic |
| matplotlib | 3.10.7 | Figure output |
| scipy | 1.16.3 | (transitive; not directly used) |
| pdftotext | poppler | PDF text extraction |
| curl / urllib | — | HTTP to Argo `localhost:44497/v1` |
| Argo GPT-5.2 (`argo:gpt-5.2`) | 2025-12-11 build | LLM judge (FREE endpoint) |
| Argo Claude Opus 4.8 (`argo:claude-opus-4.8`) | — | First-choice judge; hit 502 upstream schema error, fell back to GPT-5.2 |

## Effort estimate

- Environment setup + install: ~2 minutes.
- PDF fetch + text extraction + claim extraction: ~5 minutes.
- Writing `replicate.py`: ~10 minutes.
- Debugging the SymPy-in-poly1d stability_function hang: ~15 minutes (two killed runs before diagnosis).
- Successful full run: ~1 minute wall-clock (~90 s CPU dominated by rooted-tree enumeration at n=6..7).
- LLM judge (2 attempts due to Opus 502): ~4 minutes.
- Report writing: ~15 minutes.
- **Total: ~50 minutes** for a solid REPLICATED verdict on 9 capability claims.

## Compute usage

- All work local on `CherryRd` (macOS). No uicgpu / GPU / HPC needed — this is a pure-Python analysis package with symbolic RK-order-condition checks, cheap on CPU.
- Peak memory ~600 MB (dominated by SymPy expression trees during the failed symbolic-polyval hangs; ~100 MB in the successful run).
- No external network beyond JOSS PDF download, PyPI install, and Argo `localhost:44497` LLM judge.
