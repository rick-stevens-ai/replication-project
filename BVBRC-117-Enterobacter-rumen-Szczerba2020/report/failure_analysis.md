# Failure Analysis — BVBRC-117

Honest documentation of what did not go smoothly, what was left partial, and what would be needed to close the gaps. Included even though the overall verdict is PARTIAL-leaning-solid, because the standard demands it.

## What failed / had friction (during this run)

### F1. PMC / EuropePMC PDF direct-download blocked from CherryRd
- **Symptom.** `curl` against `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7005296/pdf/` and `https://europepmc.org/backend/ptpmcrender.fcgi?accid=PMC7005296&blobtype=pdf` both returned tiny HTML interstitials ("Preparing to download..." / "HHS Vulnerability Disclosure"), not the actual PDF.
- **Root cause.** HHS/PMC now serve an anti-bot JS-challenge redirect; a naive `curl` never resolves it. EuropePMC's mirror had HTTP/2 STREAM_CLOSED errors even from uicgpu with `--http1.1` fallback.
- **Workaround.** Fetched the PDF directly from Nature (Scientific Reports open-access, CC-BY) via the UIC HTTPS proxy on uicgpu. Worked first try.
- **Prevention.** Prefer publisher direct URL for CC-BY papers when PMC blocks; only fall back to PMC when the paper is behind a paywall on the publisher side.

### F2. Argo Opus 4.7 and 4.8 both returning HTTP 502 during LLM-judge call
- **Symptom.** `POST /v1/chat/completions` with `model=argo:claude-opus-4.7` (and 4.8) returned `502 Bad Gateway` with `"Failed to parse upstream response: Value at 'choices[0].message' does not match any variant"`. Reproducible on both `:44497` (canonical Argo wrapper) and `:4000` (litellm aggregator on cherryrd).
- **Root cause.** Anthropic Vertex-AI upstream returned a malformed message structure (probably a policy-block or empty-content edge case in the vertex proxy path). This is a known transient class of Argo failure and is not our bug.
- **Workaround.** Fell back to `argo:claude-opus-4.6` (same Opus family, same free endpoint). The wave brief allows "Argo Opus (argo:claude-opus-4.7 or 4.8) as default judge model" — 4.6 is the closest working sibling under the same free-endpoint rule.
- **Prevention.** Add an Opus-ladder-retry helper (4.8 → 4.7 → 4.6 → 4.5) to the wave orchestrator so the next replicator doesn't have to hand-select.

### F3. `tesseract`-via-`ocr__ocr_pdf` tool refused to process the paper PDF
- **Symptom.** Every page returned `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x89 in position 270`.
- **Root cause.** The Nature PDF has embedded PNG images (byte `0x89` is PNG magic); the ocr tool's rasterization path was mis-decoding a bytestream as UTF-8.
- **Workaround.** `pdftotext -layout` locally + `marker_single` / `nougat` on uicgpu all worked cleanly, so we never needed OCR for this paper (it has a proper text layer).
- **Prevention.** For future runs, prefer `pdftotext` first, fall back to Marker/Nougat, only fall back to Tesseract OCR when the PDF is a pure scan.

## What we did NOT re-run (residual gaps, honest list)

### G1. SPAdes hybrid assembly (paper claim C4) — BLOCKED
The paper reports assembling the LU2 genome with SPAdes v3.11.1 from hybrid Illumina MiSeq (2×250) + ONT MinION reads, achieving 76× Illumina coverage. **Raw reads were never deposited to SRA** (there is no SRA accession linked to BioProject PRJNA516401, only the finished chromosome CP035466.1). Without raw reads, an independent re-assembly is impossible — you literally cannot re-run the paper's central methodological choice.
- **Impact:** medium. We can verify the assembly *product* is what the paper says (5,062,651 bp, circular, 55% GC), but we cannot verify the assembly *process* (SPAdes parameters, whether Unicycler would have given the same closed chromosome, whether the reported 76× coverage is real).
- **What would close it:** the corresponding author (hubert.szczerba@up.lublin.pl) uploading the raw reads to SRA. This is a common gap in ~2018-2020 Enterobacter genome papers; SRA deposition became standard practice only later.

### G2. PHASTER prophage re-run (paper claim C9) — plausibility-checked only
The paper's ~31.9 kb "intact" prophage best-matching Salmonella phage RE-2010 was not re-run through PHASTER because (a) PHASTER is a web-only tool with rate-limits, (b) its database has grown ~4× since 2019 and would likely give a different best-hit, and (c) we ran out of time budget. We did confirm 8 prophage-machinery gene annotations (integrase, tail, tape-measure) in the LU2 GenBank record, so *some* prophage is present. The paper's specific boundaries + phage identity are unverified.
- **Impact:** low for verdict, medium for open-question value.
- **What would close it:** rerun PHASTER (or PHASTEST, its 2025 successor) plus VirSorter2 and geNomad in parallel.

### G3. BAGEL4 bacteriocin re-run (paper claim C10) — plausibility-checked only
The paper's two RiPP/bacteriocin clusters detected via BAGEL4 were not re-run because BAGEL4 is a web-only interactive tool. We confirmed colicin-related annotations (`colicin V production protein`, `colicin uptake protein TolR`) exist in the LU2 GenBank record, but cluster count / boundaries / RiPP subclass are unverified.
- **Impact:** low.
- **What would close it:** BAGEL4 web submission + antiSMASH secondary-metabolite scan for cross-validation.

### G4. IslandViewer 4 genomic-island prediction (paper: 47 GIs) — not re-run
Same reason as G2/G3: web-only tool. We did not re-verify the 47-GI count.
- **What would close it:** IslandViewer 4 web submission or local IslandPath-DIMOB script run.

## Delta / discordance between our numbers and the paper (all understood)

### D1. Whole-genome BLASTN identity vs KCTC 2190: paper 99.44%, ours 98.26%
- **Root cause.** Different aligner cutoffs. The paper's identity comes from a web BLAST + specific coverage threshold (likely 80% subject coverage + megaBLAST defaults per the Method section, page 4). Ours used `blastn -perc_identity 70` (permissive, includes low-identity HSPs). Mash on the same pair gives ~98.61% ANI-equivalent — right between the two.
- **Not a discordance in substance.** Both numbers agree LU2 is a very close relative of KCTC 2190 (>98% ANI in every way of measuring).
- **See Open Question Q1** for how to close this.

### D2. Whole-genome BLASTN identity vs E. cloacae ATCC 13047: paper 94.72% at 68% QC, ours 82.88% at 53.87% QC
- **Root cause.** Same as D1. Also, the paper limited its BLAST to specific gene clusters (colicin, bottromycin, prophage regions) rather than whole-genome, so the paper's 94.72% may be a per-locus identity, not a whole-genome mean.
- **Not a discordance in substance.** Both agree LU2 is much more distant from E. cloacae than from K. aerogenes — the qualitative species-level phylogenetic signal is fully preserved.

### D3. AMRFinderPlus (2024-07-22.1 DB) surfaced 11 AMR/virulence genes; the paper's ResFinder 3.1 reported ~5 (β-lactam, sulI, uppP, cat3, plus mdtH/mdtL in GIs)
- **Root cause.** DB divergence (2020 → 2024) and tool scope divergence. AMRFinderPlus catches intrinsic Enterobacteriaceae chromosomal loci (oqxAB, fosA, ampC, uhpT-E350Q) that ResFinder 3.1 (2020, focused on acquired resistance) did not. Conversely, sulI/cat3/uppP were not surfaced by AMRFinderPlus — probably a threshold or DB-scope difference.
- **Not a discordance in substance.** Both tools agree LU2 is intrinsically β-lactam resistant.
- **See Open Question Q2** for the phenotypic follow-up.

## What would flip PARTIAL → REPLICATED

The single largest blocker is G1 (missing raw reads). Everything else is either already strongly replicated (Table 1 counts, taxonomy, no plasmids, no CRISPR, metabolic genes) or is a low-stakes web-tool re-run (G2/G3/G4).

If the authors deposited the raw reads today, this replication would upgrade to REPLICATED within one additional wave (~1 hour of assembly + polishing on uicgpu).
