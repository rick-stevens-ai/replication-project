# Failure Analysis — BVBRC-85 (S. aureus SO-1977, Sudan; Ali et al. 2019)

**Verdict:** PARTIAL REPLICATION
**Why not FULL:** one contradicted secondary claim (`norA` uniqueness), interpretive over-reach on Teicoplanin/Carbapenem/Cephamycin resistance-class inventory, one edge-truncated call requiring a caveat, and pipeline-dependent virulence-gene counts.
**Why not FAILED:** every numeric descriptor reproduces exactly, the central `tet(K)+tet(M)` uniqueness claim reproduces cleanly under an independent modern protocol, and the taxonomic + core resistance calls all reproduce at 100% identity.

---

## Failure Mode 1 — CONTRADICTED: `norA` uniqueness

**Paper claim:** `norA` (quinolone efflux) is unique to SO-1977 among the three compared strains (SO-1977 vs MRSA252 vs MSSA476).

**Replication finding:** `norA` is present in all three strains at near-identical identity (~99%) under CARD, NCBI AMRFinder, and ResFinder — this is a canonical core *S. aureus* chromosomal efflux gene.

**Root cause:** Comparator-annotation artifact of the original RSAT-based pipeline used in the paper. RSAT does not perform genome-wide AMR-gene detection with a curated modern database; the 2019 workflow appears to have relied on RAST-subsystem membership + selective RSAT queries, which can miss a gene in a comparator without flagging the miss. Any modern AMR-DB call (CARD/NCBI/ResFinder) on the same three FASTAs recovers `norA` universally.

**Severity:** Moderate. It is a secondary comparative claim, not the paper's central result. But it is unqualified in the paper's Table 4 and downstream readers might treat it as a distinctive biomarker of the Sudanese isolate. It is not.

**Consequence for verdict:** blocks a FULL verdict, drives PARTIAL classification. LLM-judge coverage bounded at 0.75–0.82 partly because of this.

**Reproducibility of the contradiction:** Independent second-agent rerun reproduces the same `norA` contradiction (present in all 3 strains). All 3 LLM-judge models (GPT-5.2, Claude-Sonnet-4.6, Gemini-2.5-Pro) independently flagged the contradiction.

---

## Failure Mode 2 — INTERPRETIVE OVER-REACH: Teicoplanin / Carbapenem / Cephamycin resistance claims

**Paper claim:** SO-1977 is predicted-resistant to Teicoplanin, Fluoroquinolones, Quinolone, Cephamycins, Tetracycline, Acriflavin, and Carbapenems (abstract-level resistance-class inventory).

**Replication finding:**
- Fluoroquinolone/Quinolone: efflux support (`norA`, `norC`, `LmrS`, `mepA/R`) is present but core to *S. aureus* — not distinctive.
- Tetracycline: strongly supported (`tet(K)`, `tet(M)`, `tet(38)`).
- Cephamycins: implied by `mecA` presence (methicillin/β-lactam), acceptable.
- **Teicoplanin: weakly supported.** Only `TcaA/B/R` present, which are membrane/regulator components without a validated MIC-level effect on teicoplanin susceptibility. The paper's assertion appears to derive from mapping the RAST subsystem *name* ("Teicoplanin resistance in Staphylococcus") to a resistance phenotype.
- **Carbapenems: not supported.** No carbapenemase detected by any of CARD/NCBI/ResFinder/ARGannot/MEGARes. The claim rests on interpretive RAST-subsystem membership, not validated resistance-gene detection.

**Root cause:** Reliance on RAST-subsystem name-based inference rather than validated resistance-gene detection with curated AMR databases. This was state-of-practice in 2019 but does not survive AMRFinder-style re-analysis today.

**Severity:** Moderate. These are abstract-level statements; the paper's phenotypic evidence is confined to oxacillin+cefoxitin disc-diffusion, which supports only the β-lactam/methicillin call.

**Consequence for verdict:** contributes to PARTIAL. Cannot be independently confirmed with modern curated AMR databases.

---

## Failure Mode 3 — EDGE-TRUNCATION CAVEAT: `mecR1` in SO-1977

**Paper claim:** `mecR1` is present in SO-1977 (paper Table 4).

**Replication finding:** abricate at default coverage cutoff (≥80% coverage) reports `mecR1` absent in SO-1977 because the CDS is broken at a contig boundary in the 151-contig draft. Manual tblastn cross-check using MRSA252 MecR1 protein (`WP_000952923.1`, 585 aa) against SO-1977 nucleotide DB returns 100.000% identity over 310 aa on contig `NFZY01000034.1`. The CDS is real but truncated at the contig break.

**Root cause:** 151-contig draft assembly fragments the SCCmec locus at the contig boundary. Not a paper error; a limitation of drafting to contig level rather than closed genome.

**Severity:** Low. Paper's Table 4 call is factually correct. Only affects tool-based automated calls at default thresholds.

**Consequence for verdict:** Handled with caveat in the results table; does not degrade verdict below PARTIAL. Both primary replication and independent second-agent rerun independently reproduce the truncation via tblastn.

---

## Failure Mode 4 — PIPELINE-DEPENDENT: virulence-gene count

**Paper claim:** 83 genes in the RAST "Virulence, Disease, Defense" subsystem.

**Replication finding:** 73 VFDB hits via abricate.

**Root cause:** Different curation depth. RAST/SEED subsystems and VFDB are different curation objects with different inclusion criteria — one counts subsystem members (some of which are metabolic or regulatory), the other counts curated virulence-factor gene hits. The qualitative story matches (capsule, adhesion, coagulase, hemolysins, Isd iron acquisition, T7SS, sortase).

**Severity:** Very low. Not a claim of biological uniqueness; it is a summary count.

**Consequence for verdict:** Flagged as "shape match" rather than exact match. Does not degrade verdict.

---

## Failure Mode 5 — GAPS the paper leaves open (not paper failures, but replication limitations)

- **No MLST** in the paper. This replication supplies **ST140** as novel evidence.
- **No SCCmec typing** in the paper. Not attempted in this replication; feasible with SCCmecFinder/staphopia-sccmec on the same assembly.
- **No plasmid enumeration** in the paper. This replication supplies 3 replicons (`repUS43`, `repUS70`, `rep5a`) as novel evidence via PlasmidFinder.
- **No explicit PVL/TSST-1/enterotoxin gene-level BLAST calls** — the VFDB hit-count sweep captures the shape, but a paper-standard analysis would explicitly report presence/absence of `lukSF-PV`, `tst`, and the `seA-seU` panel.
- **n=1.** Single-isolate first-report; Sudan-specific epidemiological generalizations must be drawn cautiously.
- **Phenotype coverage thin.** Only oxacillin+cefoxitin disc-diffusion reported; predicted resistance across 7 classes is not tested phenotypically.

---

## Tool-level failures encountered

| Tool | Failure | Resolution |
|---|---|---|
| Homebrew `mlst` | Perl-XS ABI mismatch (binary broken) | Manual pubMLST scheme BLAST against `mlst 2.19.0` shipped allele TFAs at `/usr/local/Cellar/mlst/2.19.0/libexec/db/pubmlst/saureus/`; profile lookup against `saureus.txt` → ST140 |
| abricate default coverage cutoff | Miscalls edge-truncated `mecR1` as absent | tblastn cross-check with MRSA252 MecR1 protein query → confirms 310 aa @ 100% ID on contig `NFZY01000034.1` |

---

## Summary

The replication does not fail — it succeeds with well-characterized caveats:

- **Central paper claim reproduces:** `tet(K)+tet(M)` unique to SO-1977 (doubly confirmed).
- **One secondary claim contradicts:** `norA` uniqueness (doubly confirmed as an artifact).
- **Numeric core reproduces exactly:** all 8 assembly stats match to the bit.
- **Data integrity confirmed:** MD5 match on downloaded FNA.
- **Novel additions supplied:** ST140 + 3 plasmid replicons.
- **3-model LLM-judge consensus:** PARTIAL, coverage 0.75–0.82.
- **Independent second-agent rerun:** 16/16 checked items reproduce byte-exactly.

The PARTIAL verdict is the correct call: the paper is scientifically solid at the numeric and central-comparative level, but carries one wrong secondary comparative claim and abstract-level over-interpretation on Teicoplanin/Carbapenem/Cephamycin resistance-class inference. A charitable summary is that the paper is right about what it measures directly, and imprecise about what it infers from RAST subsystem labels.
