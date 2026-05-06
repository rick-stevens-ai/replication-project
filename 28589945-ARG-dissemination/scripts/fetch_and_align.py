#!/usr/bin/env python3
"""
Comprehensive replication of Jiang et al. 2017 - ARG dissemination
Fetches all 56 unique actinobacterial ARG proteins and their proteobacterial homologs,
runs pairwise needle alignments, and compares to paper's reported identities.
"""

import requests
import json
import os
import sys
import time
import subprocess
import re
from pathlib import Path

BASE_DIR = Path(os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/28589945-ARG-dissemination"))
SEQ_DIR = BASE_DIR / "sequences_v2"
ALIGN_DIR = BASE_DIR / "alignments_v2"
DATA_DIR = BASE_DIR / "data_v2"

for d in [SEQ_DIR, ALIGN_DIR, DATA_DIR]:
    d.mkdir(exist_ok=True)

# All 56 unique ARGs from Supplementary Data 1
# Format: (actino_accession, gene_type, paper_identity, proteo_accession, resistance, host)
ARGS = [
    ("AIA08936.1", "rph", 0.68, "WP_014395981.1", "rifamycin", "S. sp. WAC4747"),
    ("CAA42550", "lmra", 0.50, "WP_038989331.1", "lincomycin", "S. lincolnensis"),
    ("P31141", "cml_e5", 0.63, "WP_005297378.1", "chloramphenicol", "S. lividans"),
    ("CAA54186", "pur8", 0.48, "WP_043284319.1", "puromycin", "S. anulatus"),
    ("YP_002181880", "tcma", 0.35, "WP_046972988.1", "tetracenomycin_c", "S. sp. Mg1"),
    ("AAC32027", "cara", 0.35, "WP_020733565.1", "lincosamide/macrolide/streptogramin_b", "S. thermotolerans"),
    ("CAJ88549", "tet", 0.48, "WP_046110059.1", "tetracycline", "S. ambofaciens"),
    ("P20074", "cata5", 0.56, "WP_053238935.1", "chloramphenicol", "S. acrimycini"),
    ("Q55002", "otra", 0.49, "KQW79161.1", "tetracycline", "S. rimosus"),
    ("Q02652", "tet", 0.47, "KQW79161.1", "tetracycline", "S. lividans"),
    ("NP_625085", "tet", 0.46, "WP_046110059.1", "tetracycline", "S. coelicolor"),
    ("P25256", "tlrc", 0.35, "WP_015405003.1", "lincosamide/macrolide/streptogramin_b", "S. fradiae"),
    ("AAA26700", "aph33ia", 0.51, "WP_037160408.1", "streptomycin", "S. griseus"),
    ("P14559", "bl2a_exo", 0.48, "WP_042579266.1", "penicillin", "S. albus G"),
    ("AAB36568", "cml_e6", 0.45, "KRB39835.1", "chloramphenicol", "S. venezuelae"),
    ("1411197A", "bl2d_moxa", 0.47, "WP_038707481.1", "penicillin", "S. cacaoi"),
    ("BAC73509", "tcma", 0.37, "WP_045552340.1", "tetracenomycin_c", "S. avermitilis"),
    ("NP_733568", "tcma", 0.35, "WP_045552340.1", "tetracenomycin_c", "S. coelicolor"),
    ("P13249", "pac", 0.47, "WP_046974149.1", "puromycin", "S. alboniger"),
    ("Q06650", "bl2a_kcc", 0.47, "WP_012078434.1", "penicillin", "S. cellulosae"),
    ("P30180", "aac3vii", 0.49, "WP_014398725.1", "paromomycin", "S. rimosus"),
    ("BAD95833", "aac3viii", 0.48, "WP_014398725.1", "aminoglycoside", "S. fradiae"),
    ("CAG34024", "aac3viii", 0.46, "WP_014398725.1", "aminoglycoside", "S. ribosidificus"),
    ("P39886", "tcma", 0.35, "EFG83002.1", "tetracenomycin_c", "S. glaucescens"),
    ("AAA26815", "aph33ia", 0.51, "WP_031942890.1", "streptomycin", "S. griseus"),
    ("AAC15775", "otrb", 0.39, "WP_048022769.1", "tetracycline", "S. rimosus"),
    ("BAA07390", "tcr3", 0.38, "WP_032690226.1", "tetracycline", "S. aureofaciens"),
    ("YP_002188856", "tcma", 0.34, "WP_047570953.1", "tetracenomycin_c", "S. sp. SPB74"),
    ("BAG21957", "tcma", 0.32, "WP_047570953.1", "tetracenomycin_c", "S. griseus"),
    ("AAA88552", "aac3vii", 0.48, "KRA44973.1", "paromomycin", "S. rimosus"),
    ("BAA78619", "aac3x", 0.48, "WP_052513754.1", "aminoglycoside", "S. griseus"),
    ("AAA67509", "tcma", 0.34, "WP_019142923.1", "tetracenomycin_c", "S. glaucescens"),
    ("CAA66307", "ermn", 0.31, "WP_038013444.1", "lincosamide/macrolide/streptogramin_b", "S. fradiae"),
    ("AFK80333.1", "facT", 0.43, "WP_045683650.1", "factumycin", "S. sp. WAC5292"),
    ("CAG34043", "aph3vb", 0.41, "KPG77859.1", "aminoglycoside", "S. ribosidificus"),
    ("P00555", "aph3va", 0.40, "KPG77859.1", "aminoglycoside", "S. fradiae"),
    ("BAD95814", "aph3va", 0.40, "KPG77859.1", "aminoglycoside", "S. fradiae"),
    ("P08457", "sta", 0.39, "WP_015478479.1", "streptothricin", "S. lavendulae"),
    ("CAM96590", "srmb", 0.35, "WP_021475597.1", "lincosamide/macrolide/streptogramin_b", "S. ambofaciens"),
    ("CAA45050", "srmb", 0.35, "WP_021475597.1", "lincosamide/macrolide/streptogramin_b", "S. ambofaciens"),
    ("P18622", "aph6ib", 0.41, "WP_055679482.1", "streptomycin", "S. glaucescens"),
    ("CAH94334", "aph6ia", 0.39, "WP_055679482.1", "streptomycin", "S. griseus"),
    ("AAB17875", "tsnr", 0.39, "WP_054126540.1", "thiostrepton", "S. actuosus"),
    ("P18644", "tsnr", 0.35, "WP_054126540.1", "thiostrepton", "S. cyaneus"),
    ("P13079", "ermh", 0.34, "WP_004512062.1", "lincosamide/macrolide/streptogramin_b", "S. thermotolerans"),
    ("P45439", "erms", 0.34, "WP_004512062.1", "lincosamide/macrolide/streptogramin_b", "S. fradiae"),
    ("CAA55770", "ermu", 0.32, "KPK86540.1", "lincosamide/macrolide/streptogramin_b", "S. lincolnensis"),
    ("AAA50325", "oleb", 0.34, "WP_025803209.1", "lincosamide/macrolide/streptogramin_b", "S. antibioticus"),
    ("AAB51440", "ermv", 0.32, "WP_058025010.1", "lincosamide/macrolide/streptogramin_b", "S. viridochromogenes"),
    ("P52393", "tsnr", 0.37, "WP_053237320.1", "thiostrepton", "S. laurentii"),
    ("P18623", "vph", 0.33, "WP_043623898.1", "viomycin", "S. vinaceus"),
    ("NP_630216", "fush", 0.29, "WP_007869405.1", "fusidic_acid", "S. coelicolor"),
    ("1815179A", "ermo", 0.27, "WP_007145487.1", "lincosamide/macrolide/streptogramin_b", "S. lividans"),
    ("CAF31839", "aph4ib", 0.28, "WP_049767974.1", "hygromycin_b", "S. hygroscopicus"),
    ("CAA11706", "ermo", 0.23, "WP_039110121.1", "lincosamide/macrolide/streptogramin_b", "S. ambofaciens"),
    ("AFN41071.1", "sul1", 0.95, "ALJ92876.1", "sulfonamide", "Streptomyces sp. 1AL4"),
]

def fetch_ncbi_protein(accession, retries=3):
    """Fetch protein sequence from NCBI E-utilities."""
    # Clean up accession
    acc = accession.strip().split()[0]  # Handle "P00555 AAA26699.1" -> "P00555"
    
    # Handle old-style accessions
    if acc == "1411197A":
        # PDB-style, try alternative
        acc = "P35790"  # beta-lactamase from S. cacaoi - UniProt for MOXA
    elif acc == "1815179A":
        # Old PDB-style
        acc = "P21691"  # ErmO from S. lividans
    
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "protein",
        "id": acc,
        "rettype": "fasta",
        "retmode": "text"
    }
    
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=30)
            if r.status_code == 200 and r.text.strip().startswith(">"):
                return r.text.strip()
            elif r.status_code == 429:
                time.sleep(2 * (attempt + 1))
                continue
            else:
                # Try UniProt if NCBI fails
                if acc.startswith("P") or acc.startswith("Q"):
                    return fetch_uniprot(acc)
                time.sleep(1)
        except Exception as e:
            print(f"  Error fetching {acc}: {e}", file=sys.stderr)
            time.sleep(2)
    
    return None

def fetch_uniprot(acc):
    """Fetch from UniProt as fallback."""
    url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200 and r.text.strip().startswith(">"):
            return r.text.strip()
    except:
        pass
    return None

def run_needle(seq1_file, seq2_file, output_file):
    """Run EMBOSS needle alignment."""
    cmd = [
        "needle",
        "-asequence", str(seq1_file),
        "-bsequence", str(seq2_file),
        "-gapopen", "10",
        "-gapextend", "0.5",
        "-outfile", str(output_file),
        "-auto"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0
    except Exception as e:
        print(f"  Needle error: {e}", file=sys.stderr)
        return False

def parse_needle_identity(output_file):
    """Parse identity from needle output."""
    try:
        with open(output_file) as f:
            for line in f:
                if "Identity:" in line:
                    # Format: # Identity:     145/300 (48.3%)
                    match = re.search(r'\((\d+\.?\d*)%\)', line)
                    if match:
                        return float(match.group(1))
    except:
        pass
    return None

def main():
    results = []
    total = len(ARGS)
    
    # Status tracking
    fetched = 0
    aligned = 0
    failed = []
    
    for i, (actino_acc, gene, paper_id, proteo_acc, resistance, host) in enumerate(ARGS):
        idx = i + 1
        print(f"\n[{idx}/{total}] {gene} ({actino_acc} vs {proteo_acc})")
        
        # Clean accession for filename
        actino_clean = actino_acc.replace(" ", "_").replace("'", "").replace('"', '')
        proteo_clean = proteo_acc.replace(" ", "_").split("(")[0].strip()
        pair_name = f"{actino_clean}_vs_{proteo_clean}"
        
        actino_file = SEQ_DIR / f"{actino_clean}.fasta"
        proteo_file = SEQ_DIR / f"{proteo_clean}.fasta"
        needle_file = ALIGN_DIR / f"{pair_name}.needle"
        
        # Fetch actinobacterial sequence
        if not actino_file.exists() or actino_file.stat().st_size == 0:
            print(f"  Fetching actino: {actino_acc}")
            seq = fetch_ncbi_protein(actino_acc)
            if seq:
                with open(actino_file, 'w') as f:
                    f.write(seq + "\n")
                fetched += 1
            else:
                print(f"  FAILED to fetch actino: {actino_acc}")
                failed.append((actino_acc, "actino_fetch_failed"))
                results.append({
                    'idx': idx, 'actino_acc': actino_acc, 'gene': gene,
                    'paper_identity': paper_id * 100, 'proteo_acc': proteo_acc,
                    'replicated_identity': None, 'delta': None,
                    'verdict': 'FETCH_FAILED', 'resistance': resistance, 'host': host
                })
                time.sleep(0.5)
                continue
            time.sleep(0.4)  # Rate limit
        
        # Fetch proteobacterial sequence
        if not proteo_file.exists() or proteo_file.stat().st_size == 0:
            print(f"  Fetching proteo: {proteo_acc}")
            proteo_acc_clean = proteo_acc.split("(")[0].strip()
            seq = fetch_ncbi_protein(proteo_acc_clean)
            if seq:
                with open(proteo_file, 'w') as f:
                    f.write(seq + "\n")
                fetched += 1
            else:
                print(f"  FAILED to fetch proteo: {proteo_acc}")
                failed.append((proteo_acc, "proteo_fetch_failed"))
                results.append({
                    'idx': idx, 'actino_acc': actino_acc, 'gene': gene,
                    'paper_identity': paper_id * 100, 'proteo_acc': proteo_acc,
                    'replicated_identity': None, 'delta': None,
                    'verdict': 'FETCH_FAILED', 'resistance': resistance, 'host': host
                })
                time.sleep(0.5)
                continue
            time.sleep(0.4)
        
        # Run needle alignment
        if not needle_file.exists() or needle_file.stat().st_size == 0:
            print(f"  Running needle alignment...")
            success = run_needle(actino_file, proteo_file, needle_file)
            if not success:
                print(f"  NEEDLE FAILED for {pair_name}")
                failed.append((pair_name, "needle_failed"))
                results.append({
                    'idx': idx, 'actino_acc': actino_acc, 'gene': gene,
                    'paper_identity': paper_id * 100, 'proteo_acc': proteo_acc,
                    'replicated_identity': None, 'delta': None,
                    'verdict': 'ALIGN_FAILED', 'resistance': resistance, 'host': host
                })
                continue
            aligned += 1
        
        # Parse identity
        replicated = parse_needle_identity(needle_file)
        if replicated is not None:
            paper_pct = paper_id * 100
            delta = replicated - paper_pct
            
            # Determine verdict
            if abs(delta) <= 5:
                verdict = "MATCH"
            elif abs(delta) <= 10:
                verdict = "CLOSE"
            else:
                verdict = "MISMATCH"
            
            print(f"  Paper: {paper_pct:.1f}% | Replicated: {replicated:.1f}% | Δ={delta:+.1f}% | {verdict}")
            
            results.append({
                'idx': idx, 'actino_acc': actino_acc, 'gene': gene,
                'paper_identity': paper_pct, 'proteo_acc': proteo_acc,
                'replicated_identity': replicated, 'delta': delta,
                'verdict': verdict, 'resistance': resistance, 'host': host
            })
        else:
            print(f"  Could not parse identity from needle output")
            results.append({
                'idx': idx, 'actino_acc': actino_acc, 'gene': gene,
                'paper_identity': paper_id * 100, 'proteo_acc': proteo_acc,
                'replicated_identity': None, 'delta': None,
                'verdict': 'PARSE_FAILED', 'resistance': resistance, 'host': host
            })
    
    # Save results
    with open(DATA_DIR / "replication_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    successful = [r for r in results if r['replicated_identity'] is not None]
    matches = [r for r in successful if r['verdict'] in ('MATCH', 'CLOSE')]
    mismatches = [r for r in successful if r['verdict'] == 'MISMATCH']
    failed_list = [r for r in results if r['verdict'] in ('FETCH_FAILED', 'ALIGN_FAILED', 'PARSE_FAILED')]
    
    print(f"Total ARGs: {total}")
    print(f"Successfully aligned: {len(successful)}")
    print(f"  MATCH (±5%): {len([r for r in successful if r['verdict'] == 'MATCH'])}")
    print(f"  CLOSE (±10%): {len([r for r in successful if r['verdict'] == 'CLOSE'])}")
    print(f"  MISMATCH (>10%): {len(mismatches)}")
    print(f"Failed: {len(failed_list)}")
    
    if mismatches:
        print("\nMISMATCHES:")
        for r in mismatches:
            print(f"  {r['gene']} ({r['actino_acc']}): paper={r['paper_identity']:.1f}%, ours={r['replicated_identity']:.1f}%, Δ={r['delta']:+.1f}%")
    
    if failed_list:
        print("\nFAILED:")
        for r in failed_list:
            print(f"  {r['gene']} ({r['actino_acc']}): {r['verdict']}")
    
    # Print master table (TSV)
    table_file = DATA_DIR / "master_table.tsv"
    with open(table_file, 'w') as f:
        f.write("ARG\tGene\tResistance\tHost\tActino_Acc\tProteo_Acc\tPaper_Identity\tReplicated_Identity\tDelta\tVerdict\n")
        for r in results:
            rep = f"{r['replicated_identity']:.1f}" if r['replicated_identity'] is not None else "N/A"
            delta = f"{r['delta']:+.1f}" if r['delta'] is not None else "N/A"
            f.write(f"{r['idx']}\t{r['gene']}\t{r['resistance']}\t{r['host']}\t{r['actino_acc']}\t{r['proteo_acc']}\t{r['paper_identity']:.1f}\t{rep}\t{delta}\t{r['verdict']}\n")
    
    print(f"\nResults saved to {table_file}")

if __name__ == "__main__":
    main()
