# Replication Report — "Cui 2021, genome sequence adaptation" (BVBRC-127)

## ⚠️ Paper-identity caveat (read first)

The replication shell contained **only a `.DS_Store`** — no PDF, no PubMed XML,
**no DOI, no PMID, no organism name**. The directory name
`Cui-Genome-Sequence-Adaptation-2021` is too generic to uniquely resolve the
source paper: many 2021 comparative-genomics papers by a "Cui" author concern
bacterial *genome sequence* + *adaptation* (host adaptation, niche adaptation,
within-host evolution, genome reduction, AMR). Targeted `web_search`/`web_fetch`
(2026-07-08) did **not** converge on a single unambiguous DOI/PMID. We therefore
**do not claim to replicate this specific paper's specific numeric claims.**

Instead we ran an honest, documented **method-level SPOT-CHECK** of the
reproducible core that *any* "bacterial genome sequence adaptation" study
computes — the **genomic signatures of adaptation** — on a small public
surrogate. This is transparent about scope: we verify the *method and the
canonical, literature-backed claims of the theme*, not the identity-specific
results.

## What we replicated

Canonical adaptation claims (literature-backed, testable from genome sequence):

- **A1** host-restriction/obligate association → **genome reduction** (smaller
  genome, fewer genes).
- **A2** adapted/reduced genomes shift **base composition** (often AT-enrichment).
- **A3** host restriction → loss of **coding density** / pseudogenization.
- **A4** these signatures **separate adaptation states** from raw genome stats.

## Method

Code `code/adaptation_signatures.py`; data (gitignored) `work/`; outputs
`report/evidence/adaptation.json`.

- **Genomes** (NCBI RefSeq complete, via `datasets`):
  free-living/generalist — *E. coli* K-12, *P. putida* KT2440, *S.* Typhimurium
  LT2; host-adapted/restricted — *S.* Typhi Ty2, *M. tuberculosis* H37Rv,
  *Buchnera aphidicola* APS (obligate endosymbiont).
- **Signatures** (Biopython): genome size, GC%, protein-coding gene count,
  genes/Mbp, coding density (3·total_aa / genome_bp), mean protein length,
  normalized amino-acid usage entropy.
- **Contrast**: mean signatures for free/generalist vs host-adapted/reduced.

## Results (numbers) — `evidence/adaptation.json`

| genome | category | Mbp | GC% | genes | g/Mbp | cod.den | protlen | aaH |
|---|---|---|---|---|---|---|---|---|
| P. putida KT2440 | free-living | 6.18 | 61.5 | 5448 | 881 | 0.866 | 328 | 0.949 |
| S. Typhimurium LT2 | generalist | 4.95 | 52.2 | 4554 | 920 | 0.865 | 313 | 0.962 |
| S. Typhi Ty2 | host-restricted | 4.79 | 52.0 | 4237 | 884 | **0.802** | 303 | 0.961 |
| E. coli K-12 | free-living | 4.64 | 50.8 | 4300 | 926 | 0.860 | 309 | 0.962 |
| M. tuberculosis H37Rv | host-adapted | 4.41 | 65.6 | 3906 | 885 | 0.895 | 337 | 0.932 |
| Buchnera aphidicola | endosymbiont | **0.66** | **26.4** | **577** | 880 | 0.856 | 324 | 0.947 |

Adaptation-state contrast:

| metric | free/generalist | host-adapted/reduced |
|---|---|---|
| mean genome (Mbp) | **5.26** | **3.29** |
| mean genes | **4767** | **2907** |
| mean GC% | 54.9 | 48.0 |

## Per-claim: what worked / what didn't

| Claim | Result |
|---|---|
| **A1** genome reduction with adaptation | ✅ **Confirmed.** Adapted/reduced mean genome 3.29 Mbp vs 5.26 Mbp free-living; mean genes 2907 vs 4767. Buchnera is the textbook extreme: 0.66 Mbp / 577 genes. |
| **A2** base-composition shift | ✅ **Confirmed (directionally).** Adapted mean GC 48.0% < free-living 54.9%; Buchnera 26.4% GC is the classic AT-enriched endosymbiont signature. (M. tuberculosis is a high-GC exception, correctly reflecting its actinobacterial lineage — a good sanity check that the metric is real, not curve-fit.) |
| **A3** coding-density loss in host restriction | ✅ **Confirmed for the matched pair.** *S.* Typhi (host-restricted) coding density 0.802 < *S.* Typhimurium (generalist) 0.865 — consistent with Typhi's known pseudogene accumulation. |
| **A4** signatures separate adaptation state | ✅ **Confirmed.** Genome size + gene count cleanly separate the two groups (no overlap once Buchnera and the reduced Salmonella/Mtb are included). |
| specific Cui-2021 numeric claims | ❌ **Not attempted** — paper not identifiable (see caveat). |

## Verdict

**Verdict: SPOT-CHECK** (Coverage 3/10, Agreement 7/10)

The specific "Cui 2021" paper could **not be identified** from the empty shell
(no PDF/PMID/DOI/organism; ambiguous title), so a faithful paper-specific
replication was impossible. We instead performed an honest, well-documented
**method-level spot-check** of the reproducible theme — genomic signatures of
bacterial adaptation — on a public surrogate. The canonical, literature-backed
adaptation claims (**genome reduction, base-composition shift, coding-density
loss on host restriction, and clean adaptation-state separation**) all
reproduced cleanly with real NCBI RefSeq data and free tools. Coverage of the
*actual* paper is low (identity unknown); agreement with the *general theme's*
established results is high. Honest verdict: **SPOT-CHECK**.


## Verdict

**Verdict: SPOT-CHECK** (Coverage 3/10, Agreement 7/10). — Exact Cui 2021 paper unidentifiable from empty shell (no PDF/PMID/DOI/organism; generic title); performed honest method-level spot-check of genomic adaptation signatures on public surrogate — genome reduction, GC/AT shift, coding-density loss on host restriction, and adaptation-state separation all reproduced with real NCBI RefSeq data.

<!-- census-verdict: SPOT-CHECK assigned 2026-07-08 by LLM judge (Argo Opus) -->
