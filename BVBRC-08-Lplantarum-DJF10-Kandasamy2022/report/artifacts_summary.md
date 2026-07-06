# Artifacts Summary — Kandasamy 2022 *L. plantarum* DJF10 Replication

**Paper:** Int. J. Mol. Sci. 2022, 23, 14494 · DOI 10.3390/ijms232214494 · PMID 36430971
**Verdict:** PARTIAL (Coverage 8 / Agreement 8; 17 VERIFIED · 11 PARTIAL · 0 CONTRADICTED · 0 NOT_TESTED across 28 claims)

---

## Top-Level Reports

| Path | Contents |
|---|---|
| `report/REPORT.md` | Canonical pass-2 report (17 VERIFIED, 11 PARTIAL, 0 CONTRADICTED, 0 NOT_TESTED) |
| `report/REPORT.pass1.md` | Pass-1 verbatim (16 VERIFIED, 6 PARTIAL, 6 NOT_TESTED, 0 CONTRADICTED) |
| `report/REPORT.tex` | LaTeX rendering of pass-2 report + dedicated GENUINE CRITIQUE section |
| `report/open_questions.json` | 5 truly open scientific questions grounded in the paper's domain |
| `report/workflow.md` | Pass-1 and pass-2 pipeline diagrams and command-level walkthrough |
| `report/failure_analysis.md` | Named blockers for every PARTIAL, plus tractable retries |
| `PARSER_PROVENANCE.md` (project root) | `pdftotext -layout` audit trail for every quoted claim |

---

## Pass-1 Artifacts (`results/pass1/`)

- Draft assembly (SPAdes, 33 contigs / 27 filtered; 3,382,068 bp; 44.29% GC).
- Prokka v1.14.6 annotation (3,169 CDS; 51 tRNA; 2–3 rRNA; 1 tmRNA).
- SwissProt blastp table (961 EC-annotated CDS).
- ANI matrix vs *L. plantarum* type strains (`pyani` / `fastANI`, 98.3–99.1%).
- Safety-screen JSONs:
  - RGI / CARD, AMRFinderPlus, ResFinder → 0 AMR hits.
  - VFDB / PATRIC-VF / Victors → 0 virulence hits.
  - PlasmidFinder / Platon / MOB-suite → 0 plasmid replicons.
- Targeted probiotic-gene BLAST tables: `tlyA` (41.8% ident), `cspA ×5`, chaperone set (groES/EL, clpB/C/E/L/P, hslO/V, dnaK/J), `cbh` (99.7% ident), 10 Na+/H+ antiporters incl. NhaC, sortase A.

---

## Pass-2 Artifacts (`results/repass/`)

### Prophages — `results/repass/prophage/`
- `SUMMARY.md` — narrative of 6 candidate regions, 2 INTACT-LIKE.
- `integrase_neighborhoods.json` — every integrase + ±30-ORF neighborhood.
- `custom_prophages.json` — final scored regions.
- `phispy_v4/` — raw phispy output (0 regions from RF classifier).
- `/tmp/phage_hits.tbl` (or `results/repass/prophage/phage_hits.tbl`) — HMMscan raw hits.
- **Key finding:** paper R1 integrase matched at 34 bp offset; R2 at 98 bp offset; R3 assembly-contig ambiguous.

### SEED subsystems — `results/repass/subsystems/`
- `SUMMARY.md` — 25-category breakdown.
- `seed_subsystem_counts.json` — machine-readable counts.
- `SUBSYSTEM_OUTPUT.txt` — flat per-CDS assignment.
- **Key finding:** 481/3,169 CDS (15.2%) vs paper 1,119/3,168 (~35%); 18/25 categories within ±4%; all 25 present.

### KEGG BRITE — `results/repass/kegg/`
- `SUMMARY.md` — per-category paper-vs-ours narrative.
- `kegg_brite_counts.json` — EC-driven pathway counts.
- **Key finding:** Carbohydrate metabolism 240 vs paper 226 (within 6%); other categories over-call due to EC-to-pathway fan-out; KofamScan retry tractable.

### CAZymes — `results/repass/cazy/`
- `SUMMARY.md` — class-by-class comparison table.
- `DJF10_cazy.tbl` — hmmscan tabular output.
- `DJF10_cazy.domtbl` — hmmscan per-domain output.
- **Key finding:** total 101 vs paper 98 (+3.1%); GH 58/54, GT 35/32, CE 5/5 exact, AA 3/3 exact; CBM 0 strict / 14 relaxed (brackets paper's 4).

### Genomic islands — `results/repass/islands/`
- `SUMMARY.md`
- `custom_islands_v2.json` — 10 islands, 28–100 kb.
- `DJF10_GIs_v3.gff` — DIMOB output (empty).
- `islandpath_v3.log` — DIMOB run log incl. `Bio/Perl.pm` shim.
- **Key finding:** existence + length scale replicate; count differs because IslandViewer 4 fuses DIMOB + SIGI-HMM + IslandPick.

### Bacteriocin clusters — `results/repass/bacteriocin/`
- `bagel_summary.md`
- `bagel_tblastn.tsv` — 16-protein UniProt plnC11 tblastn hits.
- **Key finding:** full plantaricin cluster on NODE_10 at 51.5–58.7 kb (plnF/J/N at 100% ident; plnA at 85%; plnG ABC transporter); sactipeptide cluster undetected without BAGEL4 RiPP HMMs.

### HMM databases — `results/repass/databases/`
- dbCAN-HMMdb V13 (826 HMMs, 120 MB).
- 25 phage Pfam HMMs (PF00589, PF02899, PF13495, 6× Terminase, Holin, Phage_lysozyme, CHAP, baseplate, capsid, portal, tail).
- PF04055 (Radical_SAM).

---

## Code (`code/`)

### `code/pass1/` (implicit)
Pass-1 drivers for SPAdes / Prokka / blast / ANI / safety-screen orchestration.

### `code/repass/`
- `seed_subsystem_count.py` — SEED bucketing regex, 25 categories.
- `kegg_brite_map.py` — EC → KEGG pathway → BRITE hierarchy walker.
- `find_prophages.py` — integrase-neighborhood scorer.
- `find_islands*.py` — hypothetical-density windowed-scan (moved from `/tmp`).
- `phage_neighbors.py` — helper for prophage windowing (moved from `/tmp`).

---

## Data Provenance

- SRR14598288 raw reads (Illumina NovaSeq 6000, 14.8M PE).
- BioProject PRJNA731289 · BioSample SAMN19277818.
- UniProt L. plantarum C11 plantaricin cluster proteins (16 references).
- KEGG REST API (`/link/pathway/ec`, `/get/br:ko00001`) accessed 2026-06-23.
- dbCAN-HMMdb V13 downloaded 2026-06-23 from pro.unl.edu/dbCAN2/download/Databases/V13/.
- Phage Pfam HMMs fetched 2026-06-23 from InterPro / EBI.

---

## Score Rollup

| Bucket | Pass 1 | Pass 2 | Δ |
|---|---|---|---|
| VERIFIED | 16 | 17 | +1 (prophages, integrase coord match) |
| PARTIAL | 6 | 11 | +5 (new pass-2 partials) |
| CONTRADICTED | 0 | 0 | 0 |
| NOT_TESTED | 6 | 0 | −6 (all attacked) |
| **Coverage** | 22/28 = 79% | **28/28 = 100%** | +21% |
| **Agreement (strong)** | 16/28 = 57% | **17/28 = 61%** | +4% |
| **No-contradiction agreement** | 22/28 = 79% | **28/28 = 100%** | +21% |

Compliance: free/Argo-only; no BV-BRC submissions; no paid services; every PARTIAL carries a named blocker; every claim traced to a Prokka/hmmscan/blast/JSON artifact; pass-1 report preserved verbatim.
