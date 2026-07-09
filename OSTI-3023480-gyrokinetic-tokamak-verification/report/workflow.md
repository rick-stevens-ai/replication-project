# Workflow — OSTI 3023480 replication

## Human effort estimate
- Setup + PDF fetch: 5 min
- Text extraction fallback debugging (pdf tool → pdftotext): 5 min
- Paper reading + claim extraction: 20 min
- Analytic reproduction (v1 → v2 → v3 diagnosis + fix): 25 min
- LLM-judge two-model cross-check: 10 min
- Report + open-questions authoring: 30 min
- **Total wall clock: ~95 min agent time.**

## Wall-clock compute estimate
- CPU: seconds (three python scripts run instantly).
- No GPU used. No storage beyond 3 MB workspace footprint.
- If we WERE to attempt a full GTC rerun: ~100k node-hours on OLCF (paper-scale), i.e. INCITE-tier. Firmly out of the wave-brief scope.

## Tools + code inventory
| Tool | Version | Role |
|------|---------|------|
| pdftotext | 22.05.0 | PDF → plain text extraction (marker fallback) |
| Python | 3.13 | analytic reproduction scripts |
| curl / ssh / scp | system | artifact fetch |
| Argo LiteLLM aggregator | http://<tailnet-aggregator>:4000/v1 (Bearer stevens) | LLM judge routing |
| Argo GPT-5.4 | latest | LLM judge #1 |
| Argo GPT-5.2 | latest | LLM judge #2 |

## Reproduction pipeline
```
   OSTI PDF          Paper §3 params            Reproduction script
   ────────    →    ─────────────────    →    ────────────────────
   3023480.pdf      R_0=0.5, a=0.2,           reproduce_baae_v3.py
                    B_a=1.72, n_ea=7.37e19,   (Turnbull BAE gap,
                    T_ea=4.18, q~1..14,        q sweep, ω_*i,
                    D main ion                 v_A, β, TAE gap)
                                                        │
                                                        ▼
                                              baae_reproduction_v3.json
                                                        │
                                                        ▼
                                               LLM judge (Argo GPT-5.4)
                                               LLM judge (Argo GPT-5.2)
                                                        │
                                                        ▼
                                                REPORT.md verdict
```

## What worked
- pdftotext -layout captured the whole paper cleanly, including the analytic formula reference and all on-axis numeric parameters.
- Recognising that BAAE lives in the *bottom of the BAE gap at q>1* — not on-axis at q=1 — cracked the 3× discrepancy in v1/v2.
- The Turnbull BAE-gap formula ω = c_s √(7/4 + T_e/T_i)/(qR₀) reproduces both the paper's 90 kHz (q=2.5) and NOVA's 68.8 kHz (q=3.0) using only ST40 parameters and paper's own T_i≈T_e assumption. Ion diamagnetic drift matches within 5%.
- Argo aggregator's Anthropic proxy failed but GPT-5.x variants worked — two independent judges gave the identical SPOT-CHECK verdict.

## What didn't work / what was out of scope
- `pdf` tool: Anthropic credit exhausted → fell back to pdftotext.
- No nougat parse in the central LUCID corpus for OSTI 3023480 (checked ~/Dropbox/LUCID-100). `extraction/nougat.mmd` is thus a placeholder pointer to `marker.md` — the paper is prose+equations, both extractions would look similar.
- No GTC / NOVA / ALCON source available or accessible on our infrastructure. TRANSP profile files not public. Full-rerun of the paper's simulations is not achievable in this wave without contacting the authors.

## Effort/impact ratio
Analytic + ω_*i + β reproduction touches 5 of the paper's 10 numbered claims. The 5 not touched are pure simulation diagnostics (growth rate, δf² phase-space maps, wave-particle energy exchange, E∥/E∥,es polarization, EP-inclusion scan). SPOT-CHECK is the honest verdict.
