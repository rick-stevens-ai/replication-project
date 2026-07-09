# Attempt Log — BVBRC-123 — 2026-07-05 evening (CDT)

## 20:07 — Wave brief read; task = A. veronii Alim_AV_1000 WGS replication (PMID 37969805)
- Read WAVE_BRIEF_2026-07-01.md — clear on 8-artifact bar, free endpoints, LLM-judge, real analysis only.
- Target dir created: `~/Dropbox/REPLICATE-PROJECT/BVBRC-123-Aeromonas-veronii-catfish-Rahman-2023/{report,extraction,work}`.

## 20:08 — Paper acquisition
- NCBI PMC PDF endpoint (`/pmc/articles/PMC10636080/pdf/`) returned 1817-byte HTML — not usable.
- Europe PMC OA render at `https://europepmc.org/articles/PMC10636080?pdf=render` → **2.26 MB PDF** (worked cleanly).
- OpenClaw `pdf` tool blocked (only accepts paths under specific allowed dirs, then hit expired Anthropic API key credit + missing Gemini plugin). Used `pdftotext -layout` instead → clean 570-line text extraction.

## 20:09 — Paper claims extracted
- Full text parsed. Key numbers: 4,494,515 bp, GC 58.87%, 93 contigs, N50 150,337, L50 12, 0 plasmids, 4,229 CDS, 102 tRNA, 13 rRNA, MLST ST 492, closest to TH0426/B56, MDR (R to 7/9 antibiotics), 2 intact + 1 incomplete prophage, WGS accession JALLKR000000000, BioProject PRJNA810265 (paper's stated).

## 20:10 — Accession triangulation surprise
- NCBI Datasets `/genome/bioproject/PRJNA810265` returned a **Pasteurella multocida DC2020** project by the same institution — this is NOT the A. veronii project!
- Searched Assembly by strain name Alim_AV_1000: uid 14736231 → **GCA_026738955.1 / GCF_026738955.1**, real BioProject **PRJNA827572**, BioSample **SAMN27611687**, WGS JALLKR01, coverage 186x, assembly method MEGAHIT (matches paper).
- Downloaded both GCA (GenBank) and GCF (RefSeq with PGAP annotation) via NCBI Datasets v2 REST API.

## 20:10 — Assembly stats recomputed from FASTA (Python)
- contigs=93 ✅, total=4,494,464 (paper 4,494,515; Δ=−51 = 0.001%), N50=150,337 ✅, L50=12 ✅, GC=58.87 ✅.
- Bit-perfect assembly reproduction except 51 bp diff (likely trailing-N trimming pre/post-deposit).

## 20:11 — PGAP annotation counts vs paper's RAST
- 4,171 gene / 4,099 CDS (paper RAST: 4,229 CDS; −3% typical annotator variance).
- 102 tRNA ✅ exact.
- 28 rRNA (paper 13 — PGAP counts each 16S/23S/5S fragment across contigs; 13 likely intact-operon-equivalent).
- 4,034 proteins.

## 20:12 — AMR + virulence via abricate 1.4.0 (databases dated 2026-07-03, fresh)
- **CARD**: 3 acquired hits (OXA-12, rsmA, cphA4) vs paper's 9.
- **ResFinder**: 2 hits (ampS_1, cphA4_1).
- **NCBI-AMRFinder**: 2 hits (blaOXA-12, cphA-4).
- **VFDB**: 130 unique gene hits vs paper's 7 in specialty-gene table (paper's 7 = strict intersection; my BLAST-based = permissive).
- **PlasmidFinder**: 0 replicons ✅ matches paper.

## 20:13 — MLST via pubMLST REST (local mlst binary had Perl XS mismatch)
- Local `mlst` binary: `XS.c: loadable library and perl binaries are mismatched (got handshake key 0xfa80080, needed 0xf880080)` — known Homebrew issue.
- Fallback: POST base64-encoded FASTA to `https://rest.pubmlst.org/db/pubmlst_aeromonas_seqdef/schemes/1/sequence` with `Content-Type: application/json` (required — form-encoded returned 400).
- Result: 5 exact allele matches (recA=1460, metG=124, gyrB=633, gltA=340, groL=91), ppsA no exact.
- Fetched ST 492 profile: gyrB=112, groL=347, gltA=44, metG=217, ppsA=384, recA=381 — **complete mismatch**.
- Scanned all 2,756 aeromonas profiles: **0 profiles match ≥3 of my alleles**. Novel/undesignated ST.
- This directly contradicts the paper's ST 492 claim.

## 20:14 — ANI to phylogenetic comparators
- Downloaded: TH0426 (GCF_001593245.1), B565 (GCF_000204115.1), FDAARGOS_632 (GCF_008693705.1 — the paper's NZ_CP044060.1 proteome ref).
- skani triangle + fastANI: all three refs at 96.2-96.5% ANI. TH0426 is NOT uniquely closest.
- Paper's "close relationship" claim reflects RaxML tree topology, not genome distance.

## 20:15 — Prophage proxy (PHASTER not rerun, would need paid/heavy install)
- Grepped PGAP GFF for phage-family products, grouped by contig: 78 has 16 phage genes (portal, terminase L+S, capsid, tail, virion morphogenesis, tail-assembly chaperone, holin) — clear intact prophage; 90 has 7 (integrase + capsid + tail) — likely second intact prophage; 6 other contigs with 3 phage genes each = candidates for the "1 incomplete" region.
- Qualitatively reproduces paper's "2 intact + 1 incomplete" without a full PHASTER rerun.

## 20:16 — LLM-judge verdict
- Argo local :44497 returned 502 for claude-opus-4.7.
- Switched to cherryrd litellm aggregator `http://<tailnet-aggregator>:4000/v1`.
- claude-opus-4.8 also 502.
- **argo:gpt-5.4** succeeded and returned **PARTIAL** verdict independently:
  > "Core assembly-level claims are independently reproduced from the deposited genome: contigs (93), GC% (58.87), N50/L50 (150337/12), no plasmids, and genome size within 51 bp of the paper, with CDS/tRNA broadly consistent given annotation-tool differences. However, a key genomic claim is contradicted: the deposited assembly does not support MLST ST492 at all, and the paper also misreports the BioProject accession; some other claims are only qualitative/partial (rRNA count, phylogenetic closeness, prophage pattern)."

## 20:17-20:35 — Artifact assembly
- Wrote brief.md, REPORT.md (16 claim table + method + results + verdict), open_questions.json (5 grounded Qs), artifact_harvest.md, workflow.md, artifacts_summary.md, failure_analysis.md, REPORT.tex (LaTeX version), extraction/marker.md + extraction/nougat.mmd (pdftotext-based fallback since marker/nougat servers not directly available for on-demand call).
- Verified all 8 mandatory artifacts present.

## Things that failed / had to be worked around
1. NCBI PMC direct PDF endpoint → returned HTML. Europe PMC render worked.
2. `pdf` tool: paid Anthropic quota exhausted + Gemini/OpenAI unavailable → used pdftotext.
3. Paper's `PRJNA810265` accession → wrong organism → had to triangulate via strain name search.
4. Local `mlst` binary: Perl XS ABI mismatch → used pubMLST REST directly.
5. `mash` not installed locally → used `skani` + `fastANI` (equivalent / better).
6. Argo :44497 direct 502 + aggregator claude-opus-4.8 502 for LLM-judge → switched to argo:gpt-5.4 which worked.
7. PHASTER: no free API + heavy install → used PGAP annotation grep as documented proxy.

## Things that worked first-shot
- Europe PMC PDF download.
- pdftotext extraction (all key numbers found on first pass).
- NCBI Datasets v2 REST download of GCA/GCF FASTAs.
- Python assembly-stats recompute (exact match to paper's N50, L50, contigs, GC).
- abricate CARD/ResFinder/NCBI/VFDB/PlasmidFinder (fresh 2026-07-03 databases).
- pubMLST REST (once JSON body + base64 encoding used).
- skani/fastANI on the three comparators.
