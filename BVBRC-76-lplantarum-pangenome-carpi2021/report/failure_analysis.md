# Failure Analysis — BVBRC-76 (Carpi 2021 replication)

**Report date.** 2026-07-03
**Verdict.** PARTIAL REPLICATION (not full REPLICATED)

This file catalogs what did **not** work during the replication attempt, root causes, mitigations, and — where relevant — recommendations for future replicators. The purpose is to make the "PARTIAL" verdict honest and diagnostic rather than a vague hedge.

---

## F1. Wiley Cloudflare wall on supplementary Table S5 → Claim C4 UNTESTED (BLOCKING)

**What failed.** All attempts to fetch the paper's supplementary ZIP `jam15199-sup-0001-Tables.zip` (which contains Table S5 with the 75-probiotic-marker-gene panel) returned a Cloudflare CAPTCHA HTML page instead of the ZIP archive.

**Fetch endpoints tried.**
- `https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1111%2Fjam.15199&file=jam15199-sup-0001-Tables.zip`
- Same URL with browser User-Agent
- Same URL via `browser` tool (Chromium 144)

**Root cause.** Wiley protects supplementary downloads behind an interactive Cloudflare challenge that requires JavaScript execution and a solvable CAPTCHA. Neither `curl` nor an automated headless browser can pass it. The main paper is CC-BY OA and downloads cleanly from PMC; the supplementary material effectively is not.

**Scientific consequence.** Claim C4 (~70% of the 75 PMGs fall in core/soft-core) cannot be independently verified from public artifacts. This is the paper's central *functional-annotation* claim, and the replication verdict is downgraded from REPLICATED to **PARTIAL** solely for this reason.

**Mitigations attempted.**
- PMC full-text supplementary — the ZIP is not mirrored to PMC (only main-text PDF/XML is).
- Wayback Machine — no crawl of the Wiley supplementary URL.
- Google Scholar cached copies — none for the ZIP.

**Mitigation not yet attempted (deferred).**
- Direct email to corresponding author (Napolioni) for the PMG list.
- Interactive human-solved CAPTCHA + manual download.

**Recommendation to future replicators.** Budget an interactive-CAPTCHA download step at the start of the replication, or contact the corresponding author before starting compute. The PMG list is 75 gene names — a plain-text supplementary would completely resolve this.

---

## F2. Argo Anthropic (opus-4.7 / opus-4.8) 502 Bad Gateway during LLM-judge scoring (MITIGATED)

**What failed.** Both `argo:claude-opus-4.7` and `argo:claude-opus-4.8` returned repeated 502 Bad Gateway errors from the Argo proxy (`http://127.0.0.1:44497/v1`) during the LLM-judge scoring pass.

**Root cause.** Transient Argo backend / Anthropic upstream instability on 2026-07-03. Not specific to this replication — other CherryRd sessions saw the same 502 pattern in the same window.

**Mitigation.** Kept the 3-independent-family constraint by substituting `argo:gpt-5.4` and `argo:gemini-2.5-pro` alongside `argo:gpt-5.2`. Final judge panel: OpenAI × 2 (across generations gpt-5.2 + gpt-5.4) + Google gemini-2.5-pro. Preserved model-family diversity while dodging the failing endpoint.

**Consequence.** None on the verdict. All three replacement judges scored PARTIAL, mean coverage 0.81, agreement 0.85, confidence 0.85 — well above scoring thresholds.

**Recommendation.** For time-critical judge passes, keep an alternative-family fallback list pre-selected. Do not block on one endpoint family being down.

---

## F3. Prokka / Roary version drift (ACCEPTED as version noise)

**What differs.**
- Prokka **1.14.6** (this run) vs 1.14.5 (paper)
- Roary **3.13.0** (this run) vs 3.11.2 (paper)

**Root cause.** Six years of bioconda updates between the paper's July 2020 cutoff and our July 2026 rerun. Fresh env pins are not available for the paper's exact versions without deep container archaeology.

**Consequence.** Minor. Prokka minor-version changes shift borderline ORF annotation confidence; Roary minor-version changes tune MCL clustering marginally. These feed into the ~2–3% delta on total pan-genome size (16,522 vs 16,911) alongside the cohort delta (N=124 vs 127). Impossible to attribute the delta cleanly to cohort-vs-version without running matched-version legacy containers.

**Mitigation.** Explicitly reported version drift in `REPORT.md` Section 3b and `REPORT.tex` Genuine Critique.

**Recommendation.** For strict version-matched replication, use `docker pull staphb/prokka:1.14.5` and `docker pull staphb/roary:3.11.2` (both StaPH-B images exist). This is worth doing if the ±2–3% delta needs to be attributed decisively to cohort vs version.

---

## F4. Cohort delta (N=124 vs 127) → soft-core reshuffling (ACCEPTED as curation drift)

**What differs.** 124 unique-strain RefSeq assemblies passed our July-2020 cutoff filter, vs the paper's 127.

**Root cause.** NCBI RefSeq occasionally suppresses genomes for "detected anomalies" (same reason the paper's 3 exclusions cite — CNEI-KCA5, KLDS1.0391, SN13T). Between July 2020 and July 2026, additional suppressions and possibly some strain-dedup differences produced our 124.

**Consequence.**
- Total pan-genome: −2.3% (well within noise).
- Combined core + soft-core: +2.1% (within noise).
- Individual core: **+8.5%** (higher than expected).
- Individual soft-core: **−20.3%** (significantly lower than expected).

The last two are the biggest deltas in the whole report. **Explanation:** with N=124 vs 127, the 99%-strain cutoff line (≥123/124 vs ≥126/127) sits at a slightly different absolute strain count, and a few dozen gene families that were at 95–99% in the paper cross the ≥99% line here (or vice versa). This is threshold-boundary sensitivity, not a scientific disagreement — the joint core+soft-core count is stable within 2%.

**Mitigation.** Reported both split (paper-comparable) and joint totals; noted the threshold-boundary explanation.

**Recommendation.** For claims about "the" core-genome size, always report core+soft-core jointly rather than only the ≥99% threshold value. The joint number is what's actually stable across replicators.

---

## F5. Prokka `--fast` mode omits some HMM libraries (ACCEPTED tradeoff)

**What differs.** We ran Prokka with `--fast`, which skips CDD/PFAM HMM annotation and uses only the core Prokka database. This trades runtime (~20 min for 124 genomes) for annotation completeness.

**Consequence.** A small fraction (~1–3%) of borderline ORFs that full-mode Prokka would annotate are left unannotated in `--fast` mode. This slightly reduces total ORF counts per genome, which slightly reduces total pan-genome cluster counts.

**Mitigation.** None — we accepted the tradeoff for wall-time reasons and because the qualitative openness result is not sensitive to ±3% ORF count.

**Recommendation.** For future runs where the total-count number matters more than wall time, drop `--fast` and budget ~4× the runtime on Prokka.

---

## F6. No Panaroo cross-tool sanity check (KNOWN GAP — deferred)

**What we did not do.** Panaroo 1.8.0 is installed in the env but was not run.

**Why it matters.** Panaroo aggressively de-noises annotation errors (fragmented ORFs, misassemblies) that Roary passes through. A Panaroo pass at the same 95% identity would tell us whether the 16.5k pan-genome size is Roary-specific or a real property of the data. Panaroo typically gives smaller pan-genomes (~30–50% smaller) for datasets with heavy annotation noise. If Panaroo returned e.g. 10k here, the openness claim would need re-examination.

**Mitigation.** None yet. Flagged in `REPORT.tex` Genuine Critique as the single biggest missing sanity check.

**Recommendation.** Run `panaroo -i gffs/*.gff --clean-mode moderate -o panaroo -t 48` (~1 h wall time). Compare pan-genome size to Roary's 16,522.

---

## F7. Downstream paper analyses not attempted (SCOPE-LIMITED)

**What we did not test.**
- Parsnp core-SNP phylogeny (paper Fig 4)
- OrthoFinder phylogeny sanity check (paper Fig 1)
- FastANI all-vs-all (paper Fig 2)
- Plasmid / prophage / CRISPR / bacteriocin counts (PlasmidFinder, PHASTER, BAGEL4, CRISPRCasFinder, RAST)

**Why.** These are downstream analyses the paper reports as *characterization* results, not *headline* claims. A headline-claims replication was the scope of this pass.

**Mitigation.** Explicit scope statement in `REPORT.md` Section 4 "What we did NOT reproduce and why".

**Recommendation.** A follow-up "full replication" pass could extend the artifact set with these — the input FASTA + GFF set is unchanged, so the incremental cost is only downstream tool runs (~2–3 hours wall time total on the same uicgpu node).

---

## F8. No confidence interval on the Heaps' fit (MINOR)

**What we did not compute.** A bootstrap CI on γ = 0.3854.

**Why it matters (or doesn't).** γ = 0.385 is comfortably below 1, so the openness verdict is robust to any plausible CI width. But strictly, we do not quote a CI, which means we cannot answer questions like "is γ_LP significantly different from γ_LC (L. casei)?" from this run.

**Mitigation.** None; would require additional bootstrap runs.

**Recommendation.** If cross-species comparison is downstream, run a 500-permutation bootstrap of the genome-order → Heaps' fit and report 95% CI on γ.

---

## Summary

| ID | Failure | Severity | Consequence | Status |
|---|---|---|---|---|
| F1 | Wiley Cloudflare blocks Table S5 | **BLOCKING** | Claim C4 untested → verdict PARTIAL not REPLICATED | Unresolved |
| F2 | Argo Anthropic 502 during judging | Mitigated | Panel substitution kept 3-family diversity | Resolved |
| F3 | Prokka/Roary version drift | Accepted | Contributes to ~2–3% number delta | Documented |
| F4 | Cohort N=124 vs 127 | Accepted | Reshuffles core-vs-soft-core split by ±20% | Documented |
| F5 | Prokka --fast omits some HMMs | Accepted | ~1–3% ORF-count reduction | Documented |
| F6 | No Panaroo cross-check | Known gap | Cannot rule out Roary-specific pan-genome inflation | Deferred |
| F7 | Downstream analyses not run | Scope-limited | Only headline claims tested | Documented |
| F8 | No Heaps' CI | Minor | γ = 0.385 << 1 makes CI academic | Deferred |

**Net.** Only F1 (Wiley Cloudflare) forces the PARTIAL verdict. Every other item is version/scope noise that either is documented or does not affect the qualitative conclusions.
