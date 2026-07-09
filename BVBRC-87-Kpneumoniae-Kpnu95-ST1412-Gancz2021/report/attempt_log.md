# Attempt Log — BVBRC-87

**Analyst:** Ollie (OpenClaw subagent, argo/argo:claude-opus-4.7)  
**Session:** agent:main:subagent:e2eef5e8-f7ed-411f-9b31-8ab62982c00f (BVBRC-87)  
**Date:** 2026-07-03 CDT

## Timeline

1. **12:20 CDT** — Read wave brief; task = BVBRC-87 (Gancz 2021, Kpnu95 ST1412), PMID 34068663.
2. **12:20** — Inspected exemplar `BVBRC-17-Ecoli-B2-IBD-metabolic-2018` for output-structure template.
3. **12:21** — Created target dir `~/Dropbox/REPLICATE-PROJECT/BVBRC-87-Kpneumoniae-Kpnu95-ST1412-Gancz2021/{report,work,report/evidence}`.
4. **12:21** — Pulled paper metadata via NCBI eutils esummary:
   - Title, journal (Microorganisms), DOI 10.3390/microorganisms9051022, epub 2021-05-10.
   - PMC ID: 8151138.
5. **12:22** — PDF fetch attempts:
   - MDPI direct `/pdf` → Akamai edge "Access Denied" (typical MDPI anti-bot).
   - PMC direct PDF URL → HHS Vulnerability Disclosure landing page (JS-required).
   - `europepmc.org/backend/ptpmcrender.fcgi` → same generic HTML.
   - `oa.fcgi?id=PMC8151138` returned an `ftp://` package URL; ftp is disabled on this host and the equivalent `https://` path returned 404 (NCBI moved this file path recently).
6. **12:23** — Fell back to **NCBI eutils `efetch db=pmc rettype=xml`**, which returned the **full-text JATS XML (169 KB)** including every section, table, ref, and figure caption. This provided all the specific numeric claims for the replication.
7. **12:23** — Full-text parse yielded:
   - Strain isolated 2016, healthy woman UTI (Israel).
   - BioProject `PRJNA494961`, plasmid GenBank `MK552109`.
   - Chromosome 5,055,295 bp, 5087 ORFs, 57.76% GC.
   - Plasmid pKpnU95 180,286 bp, 243 ORFs, 50.21% GC, IncFIB(K), 10 ARGs.
   - Section-3.4 says "K109 capsular type"; Section-3.5 comparison table says 4/5 ST1412 (incl. Kpnu95) = KL107.
8. **12:23** — Resolved BioProject → assembly `GCA_015714665.1 / ASM1571466v1` (Scaffold, strain KpnU95).
9. **12:23** — Downloaded assembly via `datasets/v2alpha/genome/accession/.../download` (2.9 MB zip) with genome FASTA, protein FASTA, GFF.
   - Assembly stats: 61 contigs, 5,223,689 bp, 57.51% GC, 5063 CDS in GFF, 4952 protein FASTA entries.
   - 16 contigs labelled "plasmid pU95" (Illumina-only scaffolded plasmid; sums to ~168 kb — expected under-recovery vs. the 180.3 kb hybrid closure because IS26-flanked repeats collapse in short-read data).
10. **12:23** — Downloaded plasmid MK552109 as FASTA + GenBank (`efetch db=nuccore`). Confirmed length 180,286 bp exactly, GC 50.23%, 243 CDS.
11. **12:23-27** — Tool availability check:
    - Local `mlst` (Homebrew) — Perl `XS.c` mismatched-key error, hung on run; killed.
    - Local `blastn` (mbedtls version mismatch) — broken, unusable.
    - Local `abricate` present but not needed after Kleborate ran cleanly.
    - **uicgpu** (via ssh, source `~/env.sh`) — `amr` env has mlst 2.35.0 + amrfinder 3.12.8 + blastn; separate env at `/data/stevens/envs/kleborate` has **Kleborate 3.2.4** + Kaptive.
12. **12:31** — scp'd assembly + plasmid to `uicgpu:/data/stevens/BVBRC-87-work/`.
13. **12:31** — `mlst --scheme klebsiella kpnu95.fna` → **ST1412 with all 7 loci exact-matched**: gapA(2), infB(5), mdh(1), pgi(1), phoE(4), rpoB(1), tonB(18). **C2 REPLICATED.**
14. **12:32** — `kleborate -a kpnu95.fna -p kpsc` (Kleborate 3.2.4, DB shipped 2024) →
    - ST: **1412** ✅
    - K_locus: **KL107** (K_type "unknown (KL107)") — resolves the K109/KL107 tension in favor of KL107 (matches paper's own comparison in Sec 3.5, contradicts paper's own Sec 3.4 mention of K109 — internal paper inconsistency).
    - O_locus: OL2α.2 → O2β.
    - **10 acquired resistance genes** across 6 classes:
      - Bla_ESBL_acquired: **CTX-M-15** ✅
      - Bla_chr: SHV-1 (chromosomal β-lactamase, consistent with C6)
      - Flq_acquired: **qnrS1** ✅
      - AGly_acquired: strA*, strB*, aadA2
      - MLS_acquired: Mrx, mphA
      - Sul_acquired: sul1, sul2
      - Tmt_acquired: dfrA12
    - Ciprofloxacin MIC pred: 1 mg/L [1-2] (nonwildtype R) — consistent with paper's Cipro MIC on plasmid-carrying strain.
    - virulence_score 0 (no aerobactin/salmochelin/yersiniabactin/colibactin acquired) — consistent with paper's description that classical yersiniabactin/colibactin were **not** acquired, only the *fecABCDIR* iron-citrate uptake system (which is plasmid-encoded and not scored by Kleborate's virulence rubric).
15. **12:32** — Attempted AMRFinderPlus (`amrfinder -n kpnu95.fna --organism Klebsiella_pneumoniae --plus`) — segfaulted (`Aborted (core dumped)`) on uicgpu. Kleborate results are sufficient for the AMR claim; skipped.
16. **12:32-33** — PlasmidFinder replicon typing:
    - Downloaded PlasmidFinder DB (`enterobacteriales.fsa`, 159 replicon sequences) from bitbucket.
    - Built blastdb from pKpnU95, queried the PlasmidFinder set against it.
    - Result: **`IncFIB(K)(pCAV1099-114)_1__CP011596` hits at 100.000% identity across the full 560-bp probe.** This matches the paper's exact statement ("100% identity to *K. oxytoca* pCAV1099-114 replicon locus, accession CP011596"). Also hits: `IncFIB(K)_1__JN233704` at 91.4% and `repB_KLEB_VIR_AP006726` at 99.8%. Also confirmed on the WGS assembly contig `VYKM01000035.1` (one of the "plasmid pU95" contigs). **C4 REPLICATED.**
17. **12:33** — GenBank annotation audit of MK552109.1 (243 CDS): confirmed presence of every paper-claimed gene/operon:
    - Resistance: blaCTX-M-15, qnrS1, sul1, sul2, dfrA12, aadA2, strA', strB', mph(A), chrA (×2) → **10 ARGs, exact match**.
    - Persistence: full **pcoBSRE** copper-silver, **silPE**, **arsHRB**, **chrA** chromate, **umuCD** UV.
    - Iron uptake: full **fecIRABCDE** operon.
    - Replicon/partition: repB, parA, parB.
    - Conjugation: single **traI** (pseudogene per paper) and nothing else from *tra* — matches paper's finding "conjugation unsuccessful, absence of conjugation genes except pseudogene *traI*".
    - Integron: qacE_D1 present.
18. **12:37** — LLM-judge verdict via Argo (free endpoint, argo:gpt-5, temp=1 required by the model):
    - Per-claim: C2/C4/C5/C7/C8 REPLICATED; C3/C6 PARTIAL; C1/C9 UNTESTED; C10 (K109 vs KL107) CONTRADICTED in favor of KL107.
    - **Overall verdict: PARTIAL**.
    - One-line: "Core genomic and plasmid features incl. 10 ARGs are confirmed; capsule is KL107 (not K109); source and meta-analysis untested."

## Failures / limitations

- MDPI + PMC PDF fetches all bot-blocked; had to use the JATS XML full-text route (which turned out to be strictly better because it's structured).
- Local `mlst` and `blastn` on cherryrd have Perl/mbedtls library breakage; all compute moved to uicgpu — a good reminder to always test tools on a small case before assuming a Mac Homebrew stack will run.
- AMRFinderPlus segfaulted on uicgpu; Kleborate covered the same ground.
- Wet-lab claims (*C. elegans* killing, plasmid-curing MIC changes, artificial-urine fitness, copper-tolerance kinetics) are inherently non-replicable from public data. Noted, not attempted.
- The paper's own text has a K109 vs KL107 inconsistency between Sections 3.4 and 3.5; independent Kleborate call resolves it as KL107 (which also matches the paper's comparison table).

## Endpoints used

- **Argo proxy** localhost:44497 for LLM judge (free per project rule; argo:gpt-5 model; temp=1).
- No Anthropic/OpenAI/OpenRouter direct calls.
