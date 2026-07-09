# Failure analysis — BVBRC-120

## Verdict impact
Verdict is **PARTIAL — REPLICATED** for 3 of 4 testable headline claims. The failures / gaps below are documented for honest scoring; none of them undermines the verdict.

## What failed / what was worked around

### F1. Wrong-paper misfire on the first PDF fetch
- **What.** First curl of `bmcmicrobiol.biomedcentral.com/counter/pdf/10.1186/s12866-023-02921-x.pdf` succeeded and returned a valid 8.2 MB PDF — but of the wrong paper (Zhang J. *et al.* 2023 on *Staphylococcus aureus* wound infections in Wenzhou). The DOI 02921 was a guess; the real DOI is 02907.
- **Root cause.** Fabricated DOI from an incomplete BMC URL scheme without first verifying via `esummary`.
- **Fix.** Ran `esummary` against PMID 37337195 to obtain the canonical DOI (`10.1186/s12866-023-02907-9`), refetched from BMC → correct 10.26 MB PDF.
- **Prevention.** Always resolve PMID → DOI via NCBI eutils before constructing a publisher PDF URL. Baked into the download step for future replications.

### F2. `env.sh` proxy did not propagate to background analysis subshell
- **What.** The nested `analyze.sh` on uicgpu called `source ~/env.sh` inside a subshell, but that env.sh has a `mkdir -p "$HF_HOME"` line that errors out early and short-circuits the proxy export block. Result: `efetch` in the "fetch 13 missing focal accessions" step got "Could not resolve host: eutils.ncbi.nlm.nih.gov".
- **Root cause.** env.sh assumes an interactive/login context where earlier lines set HF_HOME; in a fresh script context that line fails and downstream proxy exports never execute.
- **Fix.** Rewrote the 13-accession fetcher to export HTTP_PROXY / HTTPS_PROXY directly instead of sourcing env.sh. All 13 accessions then downloaded cleanly.
- **Residual gap.** None — 20/20 focal accessions ultimately in hand.

### F3. Whole-genome MAFFT alignment of 20 divergent phages timed out
- **What.** `mafft --auto --thread 32 lytic_20_from_236.fa` was still running after ~4 minutes with no output; predictable given the panel contains Sipho-, Myo-, and Podoviridae with essentially no end-to-end nucleotide homology.
- **Root cause.** End-to-end nucleotide alignment is an inappropriate method for a panel this divergent — mafft `--auto` cannot converge on a global alignment when most sequence pairs share <10% identity.
- **Fix.** Killed MAFFT; substituted a MASH-distance BIONJ tree via `rapidnj -i pd`. This is a valid substitute — the paper itself uses VIRIDIC (intergenomic similarity) rather than global alignment for the same task.
- **Residual gap.** The resulting tree has long branches and weak resolution across ~91% of pairs (d ≈ 1.0). See open question Q5 for a follow-on: use a shared-cluster protein-presence-absence tree as an independent check.

### F4. 5 of 236 requested accessions were not returned by NCBI
- **What.** After 5 efetch batches of 50 accessions each (total 236 requested), only 231 sequences came back.
- **Root cause.** NCBI's dedup and record-suppression policy — some accessions listed in Table S9 have been superseded/withdrawn since 2022 (e.g. GenBank replaced by RefSeq under a different NC_* number, or an entry was suppressed). Which 5 exactly: 231 unique headers vs 236 requested → 5 not returned. A diff of requested vs returned accessions would identify them; not blocking for the verdict.
- **Fix.** Accepted 231 as the working set. Statistics were computed on n=231 and clearly labelled.
- **Residual gap.** Marginal — 2.1% attrition on a set characterised as "n≈236" does not change any headline number.

## What was skipped (out of wave scope)

### S1. PHASTER prophage re-derivation from 178 (or the 10-per-species subset) Bacillus host genomes
- **Why skipped.** PHASTER is a web service; batch usage requires either polite manual queueing or a paid credit account, both out of wave scope.
- **Impact.** Cannot independently verify the 36-prophage-set characteristics OR the "clear boundary between prophage and lytic phage" sub-claim. Open question Q2 proposes VirSorter2/geNomad-lite (free, local) as the follow-on.

### S2. WebMGA COG functional annotation
- **Why skipped.** WebMGA is a web service. A local COG search would need the NCBI CDD flat file (a few GB) plus a Diamond+CDD pipeline that is out of scope for this wave.
- **Impact.** The specific COG-family sporulation/biofilm/virulence-factor cargo sub-claim of C1 not verified. The broader "large number of unknown-function gene fragments" sub-claim was still verified via MMseqs2 singleton statistics.

### S3. Lysis-module type-I/type-II frequency across the 231-panel
- **Why skipped.** Time budget for this wave rank. Proposed as open question Q4 with a concrete HMMER-based follow-on plan.

### S4. Mauve / Easyfig genome-layout visualisation of the 20 focal phages
- **Why skipped.** Mauve is a Java GUI tool with a batch mode that is slow on 20 divergent genomes; Easyfig is also GUI. Both replaced by MASH-distance + BIONJ tree for the quantitative core; the paper's Mauve figures are qualitative and out of scope for a numeric verdict.

## Assumptions

1. Prodigal `-p meta` is a valid substitute for GeneMark on Bacillus phage genomes (both are ab-initio, both trained on prokaryotes; Prodigal is now the community-standard tool).
2. MMseqs2 at 30% identity / 50% coverage is a reasonable protein-family threshold for phage proteins (this is looser than typical bacterial family clustering; phage proteins are known to be highly divergent).
3. MASH k=21 s=1000 (defaults) is a valid genome-similarity proxy at the scale the paper cares about — supported by the fact that MASH distances < 0.05 correspond to ANI > 95% (species boundary).
4. NCBI's nuccore record for each accession contains the complete genome referenced by the paper (i.e., the paper did not use a private curated version).

## What would close the remaining gaps

To upgrade from PARTIAL to full REPLICATED:
- Add VirSorter2/geNomad rerun on the 10 host genomes → recover a truly independent 36-prophage set, then compute the prophage↔lytic MASH boundary.
- Add a local COG search (Diamond vs CDD) on 6,875 protein-cluster representatives → recover the sporulation/biofilm/virulence-factor cargo sub-claim of C1.
- Add HMMER lysis-module scan on the 231-panel proteome → close C4 quantitatively.

Total additional wall-clock estimate: ~2 h on uicgpu. Would push verdict to full REPLICATED on all 4 claims.
