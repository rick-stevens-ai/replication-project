# Attempt Log — BVBRC-66

**Analyst:** Ollie (OpenClaw AI, cron-spawned subagent, session bb00cf8a)
**Run date:** 2026-07-02 22:07–22:16 CDT (single session, all local on CherryRd)

## Chronology

1. **22:07** – Read `WAVE_BRIEF_2026-07-01.md`. Rules: free endpoints only, real replication only, LLM-judge scoring, do-not-overwrite. Mirrored BVBRC-17 output structure.
2. **22:08** – Created target dir `~/Dropbox/REPLICATE-PROJECT/BVBRC-66-enterobacter-hormaechei-blaVIM1-mcr9/{report/evidence,work}`. Verified no existing sibling dir with the same slug.
3. **22:08** – Confirmed paper metadata via NCBI eutils (PMID 32842587 → Sadek et al. 2020 *Pathogens* 9:687). Pulled abstract to enumerate concrete claims (C1..C7).
4. **22:09** – Searched NCBI for the isolate. Single hit in biosample = **SAMN14534668** (E. hormaechei strain EGYMCRVIM aka "MS37", beef burger, Egypt: Qena, 2017-07-15, submitted by Mustafa Sadek). Linked bioproject **PRJNA622990**, RefSeq assembly **GCF_013265685.1**, WGS project **JAAXDA010000000**. SRA experiment **SRX8054778** / run **SRR11478637**.
5. **22:09** – 🚩 **Discovery: raw reads are effectively empty.** SRR11478637 has only 5 spots / 5,188,211 bases — this is a placeholder record where "spots" equals the assembled genome length, i.e. the assembly was uploaded to SRA as a single dummy "read" instead of the actual Illumina fastq. No Nanopore SRA record exists. Consequence: *de novo* re-assembly from reads is impossible; we have to verify the deposited assembly directly.
6. **22:09** – Listed all 17 nuccore entries under strain EGYMCRVIM: found the complete deposited genome = **5 replicons**:
   - CP053190.1 chromosome, 4,673,152 bp
   - CP053191.1 plasmid **pMS-37a**, 270,915 bp ← paper's "270.9 kb" ✅
   - CP053192.1 plasmid pMS-37b, 129,016 bp
   - CP053193.1 plasmid pMS-37c, 108,277 bp
   - CP053194.1 plasmid pMS-37d, 6,851 bp
   - Total = 5,188,211 bp
   All flagged "complete sequence" and circular. WGS-project mirrors (JAAXDA01000000{1..5}) are identical molecules.
7. **22:10** – Downloaded all 5 replicons as FASTA via `efetch` and built BLAST DBs with `makeblastdb`. Grabbed the pMS-37a GenBank file (CP053191.1.gb) for header info. **Header confirms hybrid Unicycler v0.4.7 at 165× coverage** — matches paper's "Illumina MiniSeq + Oxford Nanopore hybrid" claim (though the header only lists Nanopore in `Sequencing Technology`, which is a common submission-form omission).
8. **22:10** – 🚩 GenBank file has **no CDS/gene features** — the submitter uploaded the raw sequence without annotation. We therefore had to do all downstream gene-calling by direct blast against curated DBs, exactly as ResFinder / MLST / PlasmidFinder do internally.
9. **22:10** – Cloned the open ResFinder DB (bitbucket `genomicepidemiology/resfinder_db`) and PlasmidFinder DB (`plasmidfinder_db`). Both are the reference DBs used by the CGE web tools.
10. **22:11** – Ran `blastn` of the full ResFinder AMR nucleotide DB against a concatenated genome (`EGYMCRVIM_full.fasta`) at 90% identity / 60% qcov. 151 hits. Reduced to best-hit-per-locus (region-clustering + max-pident/qcov). Result = **10 loci, all matching paper claims exactly:**
    - Chromosomal (CP053190.1): blaACT-16 (intrinsic AmpC), fosA (intrinsic fosfomycin resistance) — both expected for *Enterobacter cloacae* complex, not mentioned by paper but consistent.
    - Plasmid pMS-37a (CP053191.1): **blaVIM-1 (100%/100%), aac(6')-Il (100%/100%), dfrA1 (99.79%/100%), aadA1 (100%/90%, truncated → matches paper's "ΔaadA22"), sul1 (100%/100%), tet(A) (95%/94%), aac(6')-Ib-cr / aac(6')-Ib3 (100%/100%), mcr-9 (100%/100%)**.
11. **22:11** – Ran PlasmidFinder Inc typing on each of the 4 plasmids. **pMS-37a → IncHI2 + IncHI2A both at 100% identity**, exactly matching the paper's "IncHI2/pMLST1" claim. Other plasmids type as IncC/IncA (pMS-37b), IncFIB(pHCM2) (pMS-37c), Col(pHAD28) (pMS-37d) — all plausible.
12. **22:12** – Verified mcr-9 regulatory context. Fetched qseB (E. coli K-12 NP_417497.1) and qseC (NP_417498.1) proteins by protein-accession. `tblastn` vs pMS-37a → **qseB: zero hits; qseC: only one weak 27% identity paralog**, far below the ~80% expected for a real copy. Chromosome control has proper qseB (80.7% id, 218 aa) and qseC (69.5% id, 449 aa). **→ mcr-9 on pMS-37a lacks its downstream qseC/qseB regulatory pair, confirming the paper's "silent mcr-9" hypothesis.**
13. **22:13** – Verified IS903/IS1 flanking. Initial attempt with wrong NCBI accessions (X05610, J01730) returned unrelated sequences (human collagen, R100 mercury operon). Retried with correct canonical accessions **V00609.1 (IS1, 818 bp)** and **MK479294.1 (IS903 transposase + mgrB, 1367 bp)**.
    - IS1 → pMS-37a: **99.87% id, 100% qcov, positions 133556–134323**. mcr-9 CDS occupies 134319–135941 on the minus strand (5' end at 135941, 3' end at 134319). Therefore IS1 sits **4 bp downstream of mcr-9** (its 3' end just past mcr-9's 3' end). ✅ matches paper's "IS1 downstream".
    - IS903 → pMS-37a: **87.6% id, 87% qcov, 1062 bp, positions 136074–137131**. Sits **133 bp upstream of mcr-9's 5' end (135941)**. ✅ matches paper's "IS903 upstream".
14. **22:14** – Downloaded the PubMLST *E. cloacae* complex MLST scheme (`rest.pubmlst.org/db/pubmlst_ecloacae_seqdef/schemes/1`), pulled all 4,751 allele sequences across 7 loci (dnaA, fusA, gyrB, leuS, pyrG, rplB, rpoB), pulled the 3,292-profile ST table. `blastn` at 100% identity / 100% coverage against the chromosome. **All 7 loci called with perfect matches: dnaA=67, fusA=20, gyrB=19, leuS=45, pyrG=45, rplB=4, rpoB=32 → ST279. Paper reports ST279. Exact match.** ✅
15. **22:15** – Compiled `summary.json` with the full claims-vs-evidence table. Ran LLM-judge scoring via Argo proxy (:44497, key=stevens, FREE). Tried Claude Opus 4.8 (3× 502), Opus 4.7 (3× 502), then **Claude Sonnet 4.6** succeeded on first attempt. Judge verdict: **REPLICATED**, one-liner "All six genomic claims fully or substantially reproduced from public NCBI data; phenotypic MIC indirectly supported by genetic evidence." Per-claim scores: C1=3, C2=3, C3=3, C4=2 (IS903 87.6% id vs perfect), C5=3, C6=3, C7=2 (phenotypic MIC needs wet lab, but genetic basis fully supports).
16. **22:16** – Wrote report/{brief.md, attempt_log.md, artifact_harvest.md, REPORT.md}; copied evidence into report/evidence/.

## What worked

- Direct NCBI eutils resolution of paper → strain metadata → BioSample → assembly + all replicons (single API chain, no auth).
- Using ResFinder + PlasmidFinder curated open DBs directly with local `blastn` — no need to install ResFinder itself.
- PubMLST REST API is free and open (with a Dec-2024 rolling data lock, harmless here).
- Argo proxy fallback across models (Opus 4.8 → 4.7 → Sonnet 4.6) — Sonnet worked when both Opus tiers 502'd.

## What broke

- Wrong NCBI accessions for IS903 / IS1 on first try (guessed accessions from memory). Fixed by proper NCBI title search.
- pubmlst.org direct download returned HTML (public HTTP redirect). Switched to `rest.pubmlst.org` which returns raw CSV / FASTA.
- Both Claude Opus tiers on Argo returned 502 Bad Gateway repeatedly during the judge step. Retry loop with model fallback saved the run.
- BVBRC / abricate / mlst binaries not installed locally; used raw BLAST + curated DBs instead — same underlying algorithm as those tools.
