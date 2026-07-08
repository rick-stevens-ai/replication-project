#!/usr/bin/env python3
"""
PASS-2 re-pass replication: PMID 26392213
"The outer mucus layer hosts a distinct intestinal microbial niche" — Li et al. 2015

Goal: lift COVERAGE from 6 -> >=8 by adding claims that pass-1 missed.

What pass-1 covered (kept as evidence):
  C1 — PERMANOVA on Bray-Curtis: SPF compartment effect (p=0.001, R^2=3.0%)
  C2 — PERMANOVA on Bray-Curtis: sDMDMm2 compartment effect (p=0.003, R^2=6.8%)
  C3 — Per-location PERMANOVA (Colon/Cecum/Ileum) for both datasets
  C4 — ANOSIM
  C5 — Alpha diversity Shannon mucus vs content (both datasets)
  C6 — PCoA visualization

What this script ADDS (target: ≥+2 additional reproduced claims):
  C7 — PAPER'S PRIMARY METRIC: Weighted UniFrac PERMANOVA (with de-novo tree
        on 97% vsearch OTU representatives).
  C8 — Number of bacterial species/OTUs detected in sDMDMm2 == 12 (the
        Oligo-Mouse-Microbiota size quoted in Methods).
  C9 — "All 12 sDMDMm2 constituents present at some level in BOTH compartments"
        — verified by per-OTU prevalence in mucus and content subsets.
  C10 — SPF colonic-LUMINAL Shannon = 8.22 ± 0.88, n=28 (Methods quote).
        Repro at 97% OTU clustering with proper rarefaction, colon-content only.
  C11 — sDMDMm2 colonic-LUMINAL Shannon = 1.98 ± 0.38, n=11.
  C12 — Compartment-vs-location variance partition (compare R^2): paper says
        compartment is real but "no significant longitudinal differences" in
        SPF; we test PERMANOVA(Compartment) AND PERMANOVA(Location|stratified).

Pipeline:
  Step 1. Re-demultiplex (chip-aware) — reuse pass-1 mapping logic.
  Step 2. Dereplicate -> cluster at 97% with vsearch (REAL OTUs, not truncation).
  Step 3. Build OTU representative MSA (MAFFT --auto) and tree (FastTree -nt).
  Step 4. Build OTU x sample count table.
  Step 5. Rarefy to 1000 reads/sample (per Methods: min 500 reads, paper
          standard for Ion Torrent V5-V6 is rarefaction).
  Step 6. Compute Shannon alpha, weighted UniFrac beta.
  Step 7. PERMANOVA (compartment, location), ANOSIM.
  Step 8. For sDMDMm2: count OTUs, check per-compartment presence.
  Step 9. Write JSON + figures + CLAIM TABLE to results/repass/.

This script is intentionally self-contained and deterministic
(numpy/skbio seed = 26392213).
"""

from __future__ import annotations

import gzip
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import skbio
from skbio import DistanceMatrix, TreeNode
from skbio.diversity import alpha_diversity, beta_diversity
from skbio.stats.distance import anosim, permanova
from skbio.stats.ordination import pcoa

SEED = 26392213
np.random.seed(SEED)

BASE_DIR = Path(os.path.expanduser(
    "~/Dropbox/REPLICATE-PROJECT/26392213-Outer-mucus-niche"))
DATA_DIR = BASE_DIR / "data" / "raw"
OUT_DIR = BASE_DIR / "results" / "repass"
WORK = OUT_DIR / "work"
OUT_DIR.mkdir(parents=True, exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)

MIN_READS = 500              # paper's QC threshold
RAREFY_DEPTH = 1000          # conservative rarefaction
OTU_IDENT = 0.97             # paper's UCLUST identity
TRUNC_LEN = 220              # V5-V6 expected ~250bp after barcode trim
PRE_SUBSAMPLE = 5000         # cap per-sample reads before clustering (speed)

VSEARCH = "/usr/local/bin/vsearch"
MAFFT = "/usr/local/Cellar/mafft/7.526/bin/mafft"
MAFFT_BINARIES = "/usr/local/Cellar/mafft/7.526/libexec/mafft"
FASTTREE = "/usr/local/bin/fasttree"


# ---------- demultiplex (reuse pass-1 logic) ----------

def parse_mapping_file(map_path):
    out = {}
    # also build sample_id -> description for canonical metadata
    sample_desc = {}
    with open(map_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t')
            sample_id = parts[0]
            barcode = parts[1].strip()
            descr = parts[3].strip() if len(parts) > 3 else ''
            out[barcode] = {'sample_id': sample_id, 'description': descr}
            sample_desc[sample_id] = descr
    return out, sample_desc


def demultiplex(fastq_path, barcode_map, trunc_len=TRUNC_LEN):
    demuxed = defaultdict(list)
    bc_lens = sorted({len(b) for b in barcode_map})
    opener = gzip.open if str(fastq_path).endswith('.gz') else open
    total = assigned = 0
    with opener(fastq_path, 'rt') as f:
        while True:
            h = f.readline().strip()
            if not h:
                break
            seq = f.readline().strip()
            f.readline()
            f.readline()
            total += 1
            for L in bc_lens:
                bc = seq[:L]
                if bc in barcode_map:
                    trimmed = seq[L:L + trunc_len]
                    if len(trimmed) >= 150:  # min length
                        demuxed[barcode_map[bc]['sample_id']].append(trimmed)
                        assigned += 1
                    break
    pct = 100 * assigned / max(1, total)
    print(f"  {fastq_path.name}: {total:,} reads, {assigned:,} assigned ({pct:.1f}%)")
    return demuxed, total, assigned


def meta_from_description(sample_id, description, dataset):
    """Canonical: use Description column from QIIME mapping file.
    SPF descriptions: IleumC, IleumM, ColonC, ColonM, CecumC, CecumM
    sDMDMm2: IleumContent, IleumMucus, ColonContent, ColonMucus, CecumContent, CecumMucus
    """
    d = (description or '').strip()
    if d.startswith('Ileum'):
        loc = 'Ileum'
    elif d.startswith('Colon'):
        loc = 'Colon'
    elif d.startswith('Cecum') or d.startswith('Caecum'):
        loc = 'Cecum'
    else:
        loc = 'Unknown'
    if 'Mucus' in d or d.endswith('M'):
        comp = 'Outer Mucus'
    elif 'Content' in d or d.endswith('C'):
        comp = 'Luminal Content'
    else:
        comp = 'Unknown'
    # Mouse id: last token after final '.'
    parts = sample_id.split('.')
    mouse = parts[-1] if parts else 'Unknown'
    if dataset == 'sDMDMm2' and len(parts) >= 2:
        # IDs like DM1.3.C.M1 or DM.028.A.M1 — mouse = parts[0..1]
        mouse = '.'.join(parts[:2])
    return comp, loc, mouse



def build_tree(centroids_fa, aln_fa, tree_nwk):
    print(f"  MAFFT alignment -> {aln_fa.name}")
    env = os.environ.copy()
    env['MAFFT_BINARIES'] = MAFFT_BINARIES
    with open(aln_fa, 'w') as f:
        subprocess.run([MAFFT, "--auto", "--thread", "4", str(centroids_fa)],
                       stdout=f, stderr=subprocess.DEVNULL, check=True, env=env)
    print(f"  FastTree -> {tree_nwk.name}")
    raw_tree = tree_nwk.with_suffix('.raw.nwk')
    with open(raw_tree, 'w') as f:
        subprocess.run([FASTTREE, "-nt", "-gtr", "-quiet", str(aln_fa)],
                       stdout=f, stderr=subprocess.DEVNULL, check=True)
    # FastTree converts underscore in leaf names to space — reverse that
    with open(raw_tree) as fin, open(tree_nwk, 'w') as fout:
        text = fin.read()
        # Only replace within leaf-name tokens: simple newick name char rules.
        # Safe approach: replace 'OTU '  followed by digits with 'OTU_'+digits
        import re
        fixed = re.sub(r'OTU (\d{5})', r'OTU_\1', text)
        fout.write(fixed)


def process_dataset(name, fastq_map_pairs):
    """fastq_map_pairs = list of (fastq_path, map_path)"""
    print(f"\n========== {name} ==========")
    samples_seqs = defaultdict(list)  # sample_id -> list of trimmed seqs
    total_reads = 0
    assigned_reads = 0

    sample_desc_all = {}
    for fq, mp in fastq_map_pairs:
        bc, sd = parse_mapping_file(mp)
        sample_desc_all.update(sd)
        d, t, a = demultiplex(fq, bc)
        total_reads += t
        assigned_reads += a
        for sid, seqs in d.items():
            samples_seqs[sid].extend(seqs)

    # Keep samples passing MIN_READS
    samples_seqs = {k: v for k, v in samples_seqs.items()
                    if len(v) >= MIN_READS}
    print(f"  {len(samples_seqs)} samples ≥{MIN_READS} reads after QC")

    # Cap reads per sample for tractable clustering (deterministic)
    rng = np.random.default_rng(SEED)
    capped = {}
    for sid, seqs in samples_seqs.items():
        if len(seqs) > PRE_SUBSAMPLE:
            idx = rng.choice(len(seqs), PRE_SUBSAMPLE, replace=False)
            capped[sid] = [seqs[i] for i in idx]
        else:
            capped[sid] = seqs
    samples_seqs = capped
    total_reads_capped = sum(len(v) for v in samples_seqs.values())
    print(f"  After per-sample cap @ {PRE_SUBSAMPLE}: {total_reads_capped:,} reads")

    # Write all seqs to single FASTA with USEARCH-style sample tag for vsearch's
    # --cluster_size --otutabout. Header format: 'SAMPLE_i;sample=SAMPLE'
    all_fa = WORK / f"{name}_all.fa"
    print(f"  writing {all_fa.name}")
    with open(all_fa, 'w') as f:
        for sid, seqs in samples_seqs.items():
            # vsearch parses ;sample= from header; use safe sample id
            safe_sid = sid.replace(';', '_').replace(' ', '_')
            for i, s in enumerate(seqs):
                f.write(f">{safe_sid}_{i};sample={safe_sid}\n{s}\n")

    # Dereplicate first (faster downstream)
    derep_fa = WORK / f"{name}_all.derep.fa"
    print(f"  dereplicating -> {derep_fa.name}")
    subprocess.run([VSEARCH, "--derep_fulllength", str(all_fa),
                    "--output", str(derep_fa),
                    "--sizein", "--sizeout",
                    "--minuniquesize", "2",
                    "--quiet"], check=True)

    centroids = WORK / f"{name}_otus.fa"
    otutab = WORK / f"{name}_otutab.tsv"
    print(f"  clustering + OTU table at {OTU_IDENT*100:.0f}% -> {otutab.name}")
    # cluster derep file, then map ORIGINAL reads to centroids via --usearch_global
    # with --otutabout for a direct OTU table.
    subprocess.run([VSEARCH, "--cluster_size", str(derep_fa),
                    "--id", str(OTU_IDENT),
                    "--centroids", str(centroids),
                    "--sizein", "--sizeout",
                    "--threads", "4",
                    "--quiet"], check=True)
    # Rename centroids to OTU_NNNN for cleaner downstream
    centroids_named = WORK / f"{name}_otus.named.fa"
    with open(centroids) as fin, open(centroids_named, 'w') as fout:
        idx = 0
        for line in fin:
            if line.startswith('>'):
                fout.write(f">OTU_{idx:05d}\n")
                idx += 1
            else:
                fout.write(line)
    centroids = centroids_named

    # Map ALL reads to centroids — use --otutabout for direct table.
    # Use a fast approximation: --usearch_global with --top_hits_only and id 0.97
    print(f"  mapping all reads -> centroids (otutabout)")
    subprocess.run([VSEARCH, "--usearch_global", str(all_fa),
                    "--db", str(centroids),
                    "--id", str(OTU_IDENT),
                    "--strand", "both",
                    "--otutabout", str(otutab),
                    "--threads", "4",
                    "--maxaccepts", "1", "--maxrejects", "8",
                    "--top_hits_only",
                    "--quiet"], check=True)

    # Read OTU table: rows = OTUs, columns = samples; transpose to samples x OTUs
    otu_df_t = pd.read_csv(otutab, sep='\t', index_col=0)
    otu_df = otu_df_t.T  # samples x OTUs
    otu_df = otu_df.fillna(0).astype(np.int64)
    # Drop samples that lost all reads after mapping
    otu_df = otu_df.loc[otu_df.sum(axis=1) > 0]
    all_samples = otu_df.index.tolist()
    print(f"  OTU table: {otu_df.shape[0]} samples × {otu_df.shape[1]} OTUs")

    # Build metadata from canonical Description column
    meta = []
    for sid in all_samples:
        desc = sample_desc_all.get(sid, '')
        comp, loc, mouse = meta_from_description(sid, desc, name)
        meta.append({'SampleID': sid, 'Compartment': comp,
                     'Location': loc, 'Mouse': mouse,
                     'Description': desc,
                     'TotalAssigned': int(otu_df.loc[sid].sum())})
    meta_df = pd.DataFrame(meta).set_index('SampleID')

    # Rarefy
    rarefied, rare_samples = rarefy(otu_df, RAREFY_DEPTH)
    meta_df_rare = meta_df.loc[rare_samples]
    print(f"  Rarefied to {RAREFY_DEPTH}: {len(rare_samples)} samples kept")

    # Build tree
    aln = WORK / f"{name}_otus.aln.fa"
    tree_nwk = WORK / f"{name}_otus.nwk"
    build_tree(centroids, aln, tree_nwk)
    tree = TreeNode.read(str(tree_nwk), convert_underscores=False)
    # Filter tree to OTUs in rarefied table
    rare_otus = [o for o in rarefied.columns if rarefied[o].sum() > 0]
    rarefied = rarefied[rare_otus]
    print(f"  After rarefy + prune: {rarefied.shape}")

    return otu_df, rarefied, meta_df_rare, tree, samples_seqs, {
        'total_reads': total_reads,
        'assigned_reads': assigned_reads,
        'n_samples_qc': len(samples_seqs),
        'n_samples_rare': len(rare_samples),
        'n_otus_97': otu_df.shape[1],
        'n_otus_rare': rarefied.shape[1],
    }


def rarefy(df, depth):
    """Subsample each row to `depth` reads, drop samples below threshold."""
    rng = np.random.default_rng(SEED)
    keep_rows = []
    keep_samples = []
    for s in df.index:
        row = df.loc[s].values.astype(np.int64)
        tot = row.sum()
        if tot < depth:
            continue
        # multinomial subsample of `depth` from row
        probs = row / tot
        sub = rng.multinomial(depth, probs)
        keep_rows.append(sub)
        keep_samples.append(s)
    if not keep_rows:
        return df.iloc[:0], []
    rare = pd.DataFrame(keep_rows, index=keep_samples, columns=df.columns)
    return rare, keep_samples


def weighted_unifrac(rare_df, tree):
    """Compute weighted UniFrac distance matrix via scikit-bio."""
    # Force python str for all IDs (avoid numpy dtype mismatch with tree keys)
    ids = [str(s) for s in rare_df.index]
    otu_ids = [str(o) for o in rare_df.columns]
    data = rare_df.values
    # Filter OTUs to those present in tree
    tree_taxa = {n.name for n in tree.tips() if n.name}
    keep_idx = [i for i, o in enumerate(otu_ids) if o in tree_taxa]
    if len(keep_idx) < len(otu_ids):
        print(f"  pruning {len(otu_ids)-len(keep_idx)} OTUs not in tree")
    data = data[:, keep_idx]
    otu_ids = [otu_ids[i] for i in keep_idx]
    # Drop samples that lose everything
    row_sums = data.sum(axis=1)
    nz = row_sums > 0
    data = data[nz]
    ids = [ids[i] for i, keep in enumerate(nz) if keep]
    print(f"  Computing weighted UniFrac on ({len(ids)}, {len(otu_ids)})")
    try:
        dm = beta_diversity('weighted_unifrac', data, ids=ids,
                            taxa=otu_ids, tree=tree, validate=False)
    except TypeError:
        dm = beta_diversity('weighted_unifrac', data, ids=ids,
                            otu_ids=otu_ids, tree=tree, validate=False)
    return dm


def run_stats(dm, meta, factor):
    """Run PERMANOVA and ANOSIM on dm grouped by meta[factor]."""
    # restrict to samples present in both
    common = [s for s in dm.ids if s in meta.index]
    if len(common) < 5:
        return None
    sub = dm.filter(common)
    grouping = meta.loc[common, factor]
    try:
        perm = permanova(sub, grouping, permutations=999)
    except Exception as e:
        perm = None
        print(f"  PERMANOVA failed: {e}")
    try:
        anos = anosim(sub, grouping, permutations=999)
    except Exception as e:
        anos = None
    out = {}
    if perm is not None:
        # variance explained: F * (n_groups-1) / (F*(n_groups-1) + n-n_groups)
        n = len(common)
        k = grouping.nunique()
        F = float(perm['test statistic'])
        r2 = (F * (k - 1)) / (F * (k - 1) + (n - k)) if k > 1 and n > k else float('nan')
        out['permanova'] = {'F': F, 'p': float(perm['p-value']),
                            'n': n, 'k_groups': int(k), 'R2': r2}
    if anos is not None:
        out['anosim'] = {'R': float(anos['test statistic']),
                         'p': float(anos['p-value'])}
    return out


def shannon_alpha(rare_df):
    return alpha_diversity('shannon', rare_df.values, ids=list(rare_df.index))


def main():
    results = {}

    # ---- SPF ----
    pairs = [(DATA_DIR / "SPF_chip_1.fastq.gz", DATA_DIR / "SPF_map1.txt"),
             (DATA_DIR / "SPF_chip_2.fastq.gz", DATA_DIR / "SPF_map2.txt")]
    spf_raw, spf_rare, spf_meta, spf_tree, _, spf_stats = process_dataset('SPF', pairs)
    spf_meta.to_csv(OUT_DIR / "SPF_meta_repass.csv")
    spf_rare.to_csv(OUT_DIR / "SPF_otu_rarefied.csv.gz", compression='gzip')

    # Shannon alpha at rarefied depth
    spf_shannon = shannon_alpha(spf_rare)
    spf_meta_sh = spf_meta.copy()
    spf_meta_sh['shannon'] = spf_shannon
    spf_meta_sh.to_csv(OUT_DIR / "SPF_alpha_repass.csv")

    # Colon-Content Shannon (paper quote: 8.22 ± 0.88 n=28)
    cc = spf_meta_sh[(spf_meta_sh.Compartment == 'Luminal Content') &
                     (spf_meta_sh.Location == 'Colon')]
    spf_cc_shannon = {'n': int(len(cc)),
                      'mean': float(cc.shannon.mean()) if len(cc) else None,
                      'sd': float(cc.shannon.std(ddof=1)) if len(cc) > 1 else None,
                      'paper_quote': '8.22 ± 0.88 (n=28)'}

    # Weighted UniFrac + stats
    spf_wuf = weighted_unifrac(spf_rare, spf_tree)
    spf_wuf_compartment = run_stats(spf_wuf, spf_meta, 'Compartment')
    spf_wuf_location = run_stats(spf_wuf, spf_meta, 'Location')

    # per-location compartment effect
    spf_per_loc = {}
    for loc in ['Colon', 'Cecum', 'Ileum']:
        sub_meta = spf_meta[spf_meta.Location == loc]
        if len(sub_meta) < 5:
            continue
        sub_ids = [s for s in spf_wuf.ids if s in sub_meta.index]
        if len(sub_ids) < 5:
            continue
        sub_dm = spf_wuf.filter(sub_ids)
        try:
            p = permanova(sub_dm, sub_meta.loc[sub_ids, 'Compartment'],
                          permutations=999)
            spf_per_loc[loc] = {'F': float(p['test statistic']),
                                'p': float(p['p-value']),
                                'n': len(sub_ids)}
        except Exception as e:
            spf_per_loc[loc] = {'error': str(e)}

    results['SPF'] = {
        'demux': spf_stats,
        'weighted_unifrac_compartment': spf_wuf_compartment,
        'weighted_unifrac_location': spf_wuf_location,
        'weighted_unifrac_per_location_compartment': spf_per_loc,
        'colon_content_shannon': spf_cc_shannon,
        'n_otus_97pct': spf_stats['n_otus_97'],
    }

    # ---- sDMDMm2 ----
    pairs = [(DATA_DIR / "sDMDMm2.fastq.gz", DATA_DIR / "sDMDMm2_map.txt")]
    sd_raw, sd_rare, sd_meta, sd_tree, _, sd_stats = process_dataset('sDMDMm2', pairs)
    sd_meta.to_csv(OUT_DIR / "sDMDMm2_meta_repass.csv")
    sd_rare.to_csv(OUT_DIR / "sDMDMm2_otu_rarefied.csv.gz", compression='gzip')

    sd_shannon = shannon_alpha(sd_rare)
    sd_meta_sh = sd_meta.copy()
    sd_meta_sh['shannon'] = sd_shannon
    sd_meta_sh.to_csv(OUT_DIR / "sDMDMm2_alpha_repass.csv")

    cc = sd_meta_sh[(sd_meta_sh.Compartment == 'Luminal Content') &
                    (sd_meta_sh.Location == 'Colon')]
    sd_cc_shannon = {'n': int(len(cc)),
                     'mean': float(cc.shannon.mean()) if len(cc) else None,
                     'sd': float(cc.shannon.std(ddof=1)) if len(cc) > 1 else None,
                     'paper_quote': '1.98 ± 0.38 (n=11)'}

    sd_wuf = weighted_unifrac(sd_rare, sd_tree)
    sd_wuf_compartment = run_stats(sd_wuf, sd_meta, 'Compartment')
    sd_wuf_location = run_stats(sd_wuf, sd_meta, 'Location')

    sd_per_loc = {}
    for loc in ['Colon', 'Cecum', 'Ileum']:
        sub_meta = sd_meta[sd_meta.Location == loc]
        sub_ids = [s for s in sd_wuf.ids if s in sub_meta.index]
        if len(sub_ids) < 5:
            continue
        sub_dm = sd_wuf.filter(sub_ids)
        try:
            p = permanova(sub_dm, sub_meta.loc[sub_ids, 'Compartment'],
                          permutations=999)
            sd_per_loc[loc] = {'F': float(p['test statistic']),
                               'p': float(p['p-value']),
                               'n': len(sub_ids)}
        except Exception as e:
            sd_per_loc[loc] = {'error': str(e)}

    # ----- C8/C9: number of OTUs detected in sDMDMm2 (paper: 12 species) -----
    # Use raw (unrarefied) counts; threshold: present if ≥ 0.1% relative abundance
    # in at least one sample, AND ≥ 5 reads total. This filters chimeras / noise.
    raw = sd_raw.copy()
    rel = raw.div(raw.sum(axis=1), axis=0).fillna(0)
    otu_present = (rel.max(axis=0) >= 0.001) & (raw.sum(axis=0) >= 5)
    n_real_otus = int(otu_present.sum())
    real_otus = raw.columns[otu_present].tolist()

    # C9: of the real OTUs, how many appear in BOTH mucus AND content samples?
    mucus_samples = sd_meta[sd_meta.Compartment == 'Outer Mucus'].index.tolist()
    content_samples = sd_meta[sd_meta.Compartment == 'Luminal Content'].index.tolist()
    mucus_samples = [s for s in mucus_samples if s in raw.index]
    content_samples = [s for s in content_samples if s in raw.index]
    in_mucus = set()
    in_content = set()
    for o in real_otus:
        if raw.loc[mucus_samples, o].sum() >= 1:
            in_mucus.add(o)
        if raw.loc[content_samples, o].sum() >= 1:
            in_content.add(o)
    shared = in_mucus & in_content

    species_facts = {
        'n_otus_total': int(sd_raw.shape[1]),
        'n_otus_real_filtered': n_real_otus,
        'n_otus_in_mucus': len(in_mucus),
        'n_otus_in_content': len(in_content),
        'n_otus_in_both': len(shared),
        'frac_in_both_of_real': len(shared) / max(1, n_real_otus),
        'paper_quote_n_species': 12,
        'paper_quote_all_constituents_in_both': True,
    }

    results['sDMDMm2'] = {
        'demux': sd_stats,
        'weighted_unifrac_compartment': sd_wuf_compartment,
        'weighted_unifrac_location': sd_wuf_location,
        'weighted_unifrac_per_location_compartment': sd_per_loc,
        'colon_content_shannon': sd_cc_shannon,
        'species_facts': species_facts,
        'n_otus_97pct': sd_stats['n_otus_97'],
    }

    # Save summary JSON
    with open(OUT_DIR / "repass_summary.json", 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nWrote {OUT_DIR/'repass_summary.json'}")

    # Print summary
    print("\n=== SUMMARY ===")
    print(json.dumps(results, indent=2, default=str))


if __name__ == '__main__':
    main()
