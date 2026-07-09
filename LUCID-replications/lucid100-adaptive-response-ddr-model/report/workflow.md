# Workflow

## Paper
Piotrowski Ł., Krasowska J., Fornalski K.W. (2023).
*Mechanistic Modelling of DNA Damage Repair by the Radiation Adaptive Response
Mechanism and Its Significance.* BioMedInformatics 3(1), 150–163.
DOI: [10.3390/biomedinformatics3010011](https://doi.org/10.3390/biomedinformatics3010011).
License: CC BY 4.0.

## Slot
LUCID-100 #57, Wave 6, B-tier, simulation/model replication.
Audit: 2026-06-22 (Ollie subagent). Backfill: 2026-07-06.

## Workflow (chronological)
1. **PDF acquisition.** Direct fetch from `pub.mdpi-res.com` CDN
   (MDPI's `www.mdpi.com` front door is Akamai-gated and 403s to non-browser `curl`).
   `artifacts/paper.pdf` (9,170,352 B, sha16 `008cb5c8…`, CC BY 4.0).
2. **Figures.** 12 JPGs (550-px wide, largest CDN variant available) →
   `artifacts/figures/fig{001..012}.jpg`.
3. **Text extraction.** `pdftotext -layout artifacts/paper.pdf` →
   1,095-line layout text used for exhaustive claim extraction.
4. **Analytical replica (Eqs 1–4, Figs 1 + 12 theoretical curve).**
   `scripts/smoke_adaptive_response.py` — NumPy, `N₀ = 493,000`, `T₀ = 120 h`,
   paper-exact constants, vectorised recursion for f(D).
5. **Extended claim audit (Eq 5, unit consistency, P_hit point checks, PAR peak,
   §3.4 inconsistency).** `scripts/extended_claim_audit.py`.
6. **Attempted MC layer.** Blocked: parent MC tree (Fornalski 2022 *Dose-Response*)
   not released as code; not fully specified in present paper.
7. **Visual pixel-diff.** Deferred — vision endpoints unavailable during audit
   (Anthropic credits depleted; Gemini-Flash model id rejected by gateway).
   Substituted with numeric-band claim C5 verification.
8. **Report + verdict.** Full analytical-vs-MC layer separation, one paper-internal
   MISMATCH flagged (C4c), verdict PARTIAL (analytical 6/10, agreement 8/10).
9. **2026-07-06 backfill.** Added `report/REPORT.tex`,
   `report/open_questions.json`, `report/open_questions_section.tex`,
   `report/workflow.md`, `report/artifacts_summary.md`,
   `report/failure_analysis.md`, `extraction/nougat.mmd` (stub).

## Tools / versions
| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13 (system) | Analytical replica |
| NumPy | 2.x | Eq 1–5 evaluation |
| Matplotlib | 3.x | Fig 1, Fig 12, PAR peak heatmap, P_C table |
| pdftotext (poppler) | 25.x | PDF → layout text for claim extraction |
| curl | system | CDN PDF/figure fetch |
| Endpoint (backfill) | Argo `argo:claude-opus-4.7` @ `localhost:44497`, key `stevens` | LaTeX + JSON drafting |

Host: CherryRd (macOS, x64). CPU-only. No GPU, no HPC, no external network beyond
the (already cached) PDF and figures.

## Work estimate
- **Analytical layer (this replication):** ~2 h to extract, code, verify.
- **MC layer (not done, would be required for full REPLICATED verdict):**
  3–5 days if Fornalski 2022 parent paper is well specified, 1–2 weeks otherwise,
  plus 0.5–1 day to reconcile the §3.4 P_C label swap with the authors.
- **This backfill (7 artifacts):** ~30 min.

## Reproducer
```bash
# From repo root
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-adaptive-response-ddr-model/

# (a) Analytical layer + Fig 1 + Fig 12 theoretical curve
python3 scripts/smoke_adaptive_response.py

# (b) Extended claim audit (Eq 5, unit consistency, §3.4 MISMATCH check)
python3 scripts/extended_claim_audit.py

# (c) Text extraction for exhaustive claim list
pdftotext -layout artifacts/paper.pdf /tmp/lucid100_paper.txt

# Outputs land in outputs/ and can be regenerated deterministically.
```
Runtime: <1 s per script. RAM <200 MB. No external network required.

## Provenance
- Paper + figures: MDPI CC BY 4.0.
- Constants (α₀=22.9, α₁=79.4 mGy⁻¹, α₂=0.0832 h⁻¹; μ₀/μ₁ HBRA and in-vitro
  sets; a=1.3 Gy⁻¹; a₂=2.4 Gy⁻¹; N₀=493,000; T₀=120 h): from paper §2–3.
- Underlying calibration data (behind α_i, μ_i): Polish B.Sc./M.Sc. theses on
  ResearchGate (refs [21,22,25]); not re-fitted here.
- Parent MC tree: Fornalski et al. 2022 (*Dose-Response*, DOI 10.1177/15593258221103459),
  CC BY, no public code.
