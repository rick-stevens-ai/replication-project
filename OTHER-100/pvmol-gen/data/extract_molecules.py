#!/usr/bin/env python3
"""
Extract passivation molecules from literature and look up SMILES.
Target: reconstruct Data T0 (314 molecules) from Fajar et al. 2026
"""

import re
import csv
import json
import subprocess
from pathlib import Path

# Known molecules with SMILES from Liu 2022 SI (and related papers)
# These are interface passivation materials at perovskite/HTL interface
KNOWN_MOLECULES = {
    # From Liu 2022 Table S1 - primary passivation molecules
    "S": ("1,3-dithiane", "C1CSCSC1"),
    "N": ("thiomorpholine", "C1COCCN1"),  
    "SN": ("thiomorpholine-1-oxide", "C1COCNC1=O"),
    "PEIm": ("phenylethylamine iodide", "C(CN)C1=CC=CC=C1.[I-]"),
    "P3HT": ("poly(3-hexylthiophene-2,5-diyl)", None),  # Polymer - excluded
    "PTAA": ("poly(triarylamine)", None),  # Polymer - excluded
    "MEH-PPV": ("poly[2-methoxy-5-(2-ethylhexyloxy)-1,4-phenylenevinylene]", None),  # Polymer
    "Poly-TPD": ("poly-TPD", None),  # Polymer
    "CT": ("n-cetyl trimethyl ammonium bromide", "CCCCCCCCCCCCCCCC[N+](C)(C)C.[Br-]"),
    "MMI": ("1-methylimidazole", "CN1C=CN=C1"),
    "Benzylamine": ("benzylamine", "NCC1=CC=CC=C1"),
    "PMMA": ("poly(methyl methacrylate)", None),  # Polymer
    "TP": ("thiophene", "C1=CC=CS1"),
    "MTP": ("2-methylthiophene", "CC1=CC=CS1"),
    "ETP": ("2-ethylthiophene", "CCC1=CC=CS1"),
    "BTP": ("2-butylthiophene", "CCCCC1=CC=CS1"),
    "HTP": ("2-hexylthiophene", "CCCCCCC1=CC=CS1"),
    "DTP": ("2,5-di(thiophen-2-yl)thiophene", "C1=CSC(=C1)C2=CC=C(S2)C3=CC=CS3"),
    "FABr": ("formamidinium bromide", "[NH2+]=CN.[Br-]"),
    "PEAI": ("phenethylammonium iodide", "C(CN)C1=CC=CC=C1.[I-]"),
    "C4Br": ("butylammonium bromide", "CCCC[NH3+].[Br-]"),
    "C6Br": ("hexylammonium bromide", "CCCCCC[NH3+].[Br-]"),
    "C8Br": ("octylammonium bromide", "CCCCCCCC[NH3+].[Br-]"),
    "2-MP": ("2-methylpiperidine", "CC1CCCCN1"),
    "PTT": ("pyrrolidine", "C1CCNC1"),
    "Py": ("pyridine", "C1=CC=NC=C1"),
    "EAI": ("ethylammonium iodide", "CC[NH3+].[I-]"),
    "IAI": ("isopropylammonium iodide", "CC(C)[NH3+].[I-]"),
    "GuaI": ("guanidinium iodide", "NC(=[NH2+])N.[I-]"),
    "FPEAI": ("4-fluorophenethylammonium iodide", "FC1=CC=C(CCN)C=C1.[I-]"),
    "tBP": ("4-tert-butylpyridine", "CC(C)(C)C1=CC=NC=C1"),
    "BAI": ("n-butylammonium iodide", "CCCC[NH3+].[I-]"),
    "HAI": ("n-hexylammonium iodide", "CCCCCC[NH3+].[I-]"),
    "EPC": ("ethyl phenyl carbonate", "CCOC(=O)OC1=CC=CC=C1"),
    "TFDIB": ("1,4-diiodotetrafluorobenzene", "FC1=C(F)C(I)=C(F)C(F)=C1I"),
    "HS-Ph-CN": ("4-mercaptobenzonitrile", "N#CC1=CC=C(S)C=C1"),
    "HS-Ph-NO2": ("4-nitrothiophenol", "[O-][N+](=O)C1=CC=C(S)C=C1"),
    "HS-Ph-SCH3": ("4-(methylthio)thiophenol", "CSC1=CC=C(S)C=C1"),
    "HS-Ph-OCH3": ("4-methoxythiophenol", "COC1=CC=C(S)C=C1"),
    "PHI": ("phenylammonium iodide", "[NH3+]C1=CC=CC=C1.[I-]"),
    "ClTPPPF6": ("chloro-triphenylphosphonium hexafluorophosphate", None),  # Complex salt
    "BrTPPPF6": ("bromo-triphenylphosphonium hexafluorophosphate", None),
    "CHAI": ("cyclohexylammonium iodide", "[NH3+]C1CCCCC1.[I-]"),
    "CHMAI": ("cyclohexylmethylammonium iodide", "[NH3+]CC1CCCCC1.[I-]"),
    "(HAD)I2": ("1,6-hexanediammonium diiodide", "[NH3+]CCCCCC[NH3+].[I-].[I-]"),
    "(EDBE)I2": ("ethylenediammonium diiodide", "[NH3+]CC[NH3+].[I-].[I-]"),
    "CDCA": ("chenodeoxycholic acid", "CC(CCC(=O)O)C1CCC2C1(C(CC3C2C(CC4C3(CCC(C4)O)C)O)O)C"),
    "C8-BTBT": ("2-octyl[1]benzothieno[3,2-b][1]benzothiophene", "CCCCCCCCC1=CC2=C(S1)C3=CC4=CC=CC=C4S3C=C2"),
    "MTDAA": ("4-methylthio-DL-aspartic acid", "CSCC(C(=O)O)C(=O)O"),
    "ADAHCl": ("1-adamantanamine hydrochloride", "[NH3+]C12CC3CC(CC(C3)C1)C2.[Cl-]"),
    "Polystyrene": ("polystyrene", None),  # Polymer
    "CTABr": ("cetyltrimethylammonium bromide", "CCCCCCCCCCCCCCCC[N+](C)(C)C.[Br-]"),
    "TCPBr": ("tetradecylphosphonium bromide", None),
    "TCPI": ("tetradecylphosphonium iodide", None),
    "PTPD": ("poly-TPD", None),  # Polymer
    "Tetracene": ("tetracene", "C1=CC2=CC3=CC4=CC=CC=C4C=C3C=C2C=C1"),
    "PABA": ("4-aminobenzoic acid", "NC1=CC=C(C(=O)O)C=C1"),
    "ADA": ("1-adamantylamine", "NC12CC3CC(CC(C3)C1)C2"),
    "AD": ("adamantane", "C1C2CC3CC1CC(C2)C3"),
    "PVP": ("polyvinylpyrrolidone", None),  # Polymer
    "B2Cat2": ("bis(catecholato)diboron", "B1(OC2=CC=CC=C2O1)B3OC4=CC=CC=C4O3"),
    "OLA": ("oleylamine", "CCCCCCCC/C=C\\CCCCCCCCN"),
    "BMIMBF4": ("1-butyl-3-methylimidazolium tetrafluoroborate", "CCCC[N+]1=CN(C=C1)C.[B-](F)(F)(F)F"),
    "POSS-NH2": ("aminopropyl-polyhedral oligomeric silsesquioxane", None),  # Complex
    "POSS-SH": ("mercaptopropyl-polyhedral oligomeric silsesquioxane", None),
    "BEDCE": ("bis(2-ethylhexyl) dicarbonate ester", None),
    "Cs-oleate": ("cesium oleate", None),  # Inorganic salt
    "TAI": ("thioacetamide iodide", None),
    "ImI": ("imidazolium iodide", "C1=CN=C[NH2+]1.[I-]"),
    "cesium acetate": ("cesium acetate", None),  # Inorganic
    "P(VDF-TrFE)": ("polyvinylidene fluoride-trifluoroethylene", None),  # Polymer
    "PD-10-DTTE-7": (None, None),  # Unknown
    "TFMBA": ("4-(trifluoromethyl)benzylamine", "FC(F)(F)C1=CC=C(CN)C=C1"),
    "DMIMPF6": ("1,3-dimethylimidazolium hexafluorophosphate", "C[N+]1=CN(C=C1)C.F[P-](F)(F)(F)(F)F"),
    "PEACl": ("phenethylammonium chloride", "[NH3+]CCC1=CC=CC=C1.[Cl-]"),
    "SDBS": ("sodium dodecylbenzenesulfonate", "CCCCCCCCCCCCC1=CC=C(C=C1)S(=O)(=O)[O-].[Na+]"),
    "PyNa+": ("sodium pyruvate", "CC(=O)C(=O)[O-].[Na+]"),
    "OAI": ("octylammonium iodide", "CCCCCCCC[NH3+].[I-]"),
    "OABr": ("octylammonium bromide", "CCCCCCCC[NH3+].[Br-]"),
    "OACl": ("octylammonium chloride", "CCCCCCCC[NH3+].[Cl-]"),
    "CBAH": ("4-carboxybenzylhydrazinium", None),
    "[EMIM]Br": ("1-ethyl-3-methylimidazolium bromide", "CC[N+]1=CN(C=C1)C.[Br-]"),
    "DMEDAI2": ("N,N-dimethylethylenediamine diiodide", None),
    "FEAI": ("4-fluoroethylammonium iodide", None),
    "TPPO": ("triphenylphosphine oxide", "O=P(C1=CC=CC=C1)(C2=CC=CC=C2)C3=CC=CC=C3"),
    "TMPP": ("trimethylphosphine", "CP(C)C"),
    "TPFP": ("tris(pentafluorophenyl)phosphine", "FC1=C(F)C(F)=C(P(C2=C(F)C(F)=C(F)C(F)=C2F)C3=C(F)C(F)=C(F)C(F)=C3F)C(F)=C1F"),
    "2-TEAI": ("2-thiopheneethylammonium iodide", "[NH3+]CCC1=CC=CS1.[I-]"),
    "QA": ("quaternary ammonium", None),
    "F4TCNQ": ("2,3,5,6-tetrafluoro-7,7,8,8-tetracyanoquinodimethane", "FC1=C(F)C(=C(C#N)C#N)C(F)=C(F)C1=C(C#N)C#N"),
    "TBPO": ("tributylphosphine oxide", "O=P(CCCC)(CCCC)CCCC"),
    "ODAI2": ("octanediammonium diiodide", "[NH3+]CCCCCCCC[NH3+].[I-].[I-]"),
    "HDADI": ("1,6-hexanediammonium diiodide", "[NH3+]CCCCCC[NH3+].[I-].[I-]"),
    "AVAI": ("5-aminovaleric acid iodide", "[NH3+]CCCCC(=O)O.[I-]"),
    "HBAI": ("4-hydrazinobenzoic acid", "NNC1=CC=C(C(=O)O)C=C1"),
    
    # Additional molecules from Zhi 2023 (ammonium salts)
    "PEAI": ("phenethylammonium iodide", "[NH3+]CCC1=CC=CC=C1.[I-]"),
    "CEAI": ("cyclohexylethylammonium iodide", "[NH3+]CCC1CCCCC1.[I-]"),
    "MAI": ("methylammonium iodide", "C[NH3+].[I-]"),
    "FAI": ("formamidinium iodide", "[NH2+]=CN.[I-]"),
    
    # Additional molecules from Zhang 2024
    "4-aminobenzenesulfonamide": ("4-aminobenzenesulfonamide", "NC1=CC=C(S(N)(=O)=O)C=C1"),
    "4-Chloro-2-hydroxy-5-sulfamoylbenzoic acid": ("4-Chloro-2-hydroxy-5-sulfamoylbenzoic acid", "NS(=O)(=O)C1=CC(Cl)=C(C(=O)O)C(O)=C1"),
    "Phenolsulfonphthalein": ("Phenolsulfonphthalein", "OC1=CC=C(C=C1)C(C2=CC=C(O)C=C2)C3=CC=CC=C3S(=O)(=O)O"),
    
    # Key molecules from Chen 2019 review
    "thiourea": ("thiourea", "NC(N)=S"),
    "urea": ("urea", "NC(N)=O"),
    "caffeine": ("caffeine", "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"),
    "theophylline": ("theophylline", "CN1C2=C(C(=O)N(C1=O)C)NC=N2"),
    "iodopentafluorobenzene": ("iodopentafluorobenzene", "FC1=C(F)C(F)=C(I)C(F)=C1F"),
    "Lewis acids": None,  # Category, not molecule
    "Lewis bases": None,
    
    # Key molecules from Gao 2020 review
    "pyridine": ("pyridine", "C1=CC=NC=C1"),
    "aniline": ("aniline", "NC1=CC=CC=C1"),
    "aminoacetic acid": ("glycine", "NCC(=O)O"),
    "3-aminopropionic acid": ("beta-alanine", "NCCC(=O)O"),
    "4-aminobutyric acid": ("GABA", "NCCCC(=O)O"),
    "5-aminovaleric acid": ("5-aminovaleric acid", "NCCCCC(=O)O"),
    "6-aminohexanoic acid": ("6-aminohexanoic acid", "NCCCCCC(=O)O"),
    
    # Molecules from Fajar 2026 experimentally validated
    "4-maleimidobutyric acid": ("4-maleimidobutyric acid", "O=C1NC(=O)C=C1CCCC(=O)O"),
    "maleic acid monoamide": ("maleic acid monoamide", "NC(=O)/C=C\\C(=O)O"),
    "DL-mandelic acid": ("DL-mandelic acid", "OC(C(=O)O)C1=CC=CC=C1"),
}

def parse_liu2022_table():
    """Parse the extracted Table S1 from Liu 2022"""
    molecules = []
    
    # Read the extracted table text
    with open('/tmp/liu2022_table.txt', 'r') as f:
        content = f.read()
    
    # Parse line by line looking for molecule entries
    lines = content.split('\n')
    current_entry = {}
    
    for i, line in enumerate(lines):
        # Look for lines starting with numbers (entry IDs)
        match = re.match(r'^(\d+)\s+([\d.]+)\s+([\d.]+)\s+(\S+)', line)
        if match:
            entry_id = int(match.group(1))
            pce_final = float(match.group(2))
            pce_initial = float(match.group(3))
            name = match.group(4)
            
            delta_pce_norm = (pce_final - pce_initial) / pce_initial if pce_initial > 0 else 0
            
            molecules.append({
                'id': entry_id,
                'name': name,
                'pce_initial': pce_initial,
                'pce_final': pce_final,
                'delta_pce_norm': round(delta_pce_norm, 4),
                'source': 'Liu2022'
            })
    
    return molecules

def get_smiles_for_molecule(name):
    """Look up SMILES for a molecule from our known database or estimate"""
    if name in KNOWN_MOLECULES:
        info = KNOWN_MOLECULES[name]
        if info and info[1]:
            return info[1]
    return None

def main():
    # Parse Liu 2022 data
    liu_molecules = parse_liu2022_table()
    print(f"Parsed {len(liu_molecules)} molecules from Liu 2022")
    
    # Add SMILES where available
    for mol in liu_molecules:
        smiles = get_smiles_for_molecule(mol['name'])
        mol['smiles'] = smiles if smiles else ''
    
    # Filter out polymers (those without SMILES that we know are polymers)
    polymer_names = {'P3HT', 'PTAA', 'MEH-PPV', 'Poly-TPD', 'PMMA', 'Polystyrene', 
                     'PVP', 'P(VDF-TrFE)', 'PTPD'}
    
    filtered_molecules = [m for m in liu_molecules if m['name'] not in polymer_names]
    print(f"After filtering polymers: {len(filtered_molecules)} molecules")
    
    # Calculate classification
    for mol in filtered_molecules:
        mol['class'] = 1 if mol['delta_pce_norm'] >= 0.10 else 0
    
    # Save to CSV
    output_path = Path('/Users/stevens/projects/replicate/data/literature_molecules.csv')
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'smiles', 'pce_initial', 'pce_final', 'delta_pce_norm', 'class', 'source'])
        writer.writeheader()
        writer.writerows(filtered_molecules)
    
    print(f"Saved {len(filtered_molecules)} molecules to {output_path}")
    
    # Statistics
    class1_count = sum(1 for m in filtered_molecules if m['class'] == 1)
    class0_count = sum(1 for m in filtered_molecules if m['class'] == 0)
    with_smiles = sum(1 for m in filtered_molecules if m['smiles'])
    
    print(f"\nStatistics:")
    print(f"  Class 1 (ΔPCEnorm >= 0.10): {class1_count}")
    print(f"  Class 0 (ΔPCEnorm < 0.10): {class0_count}")
    print(f"  With SMILES: {with_smiles}")
    print(f"  Missing SMILES: {len(filtered_molecules) - with_smiles}")
    
    # Save summary
    summary_path = Path('/Users/stevens/projects/replicate/data/extraction_summary.txt')
    with open(summary_path, 'w') as f:
        f.write("Literature Molecule Extraction Summary\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Target: Reconstruct Data T0 (314 molecules) from Fajar et al. 2026\n\n")
        f.write("Source Papers:\n")
        f.write("1. Liu et al. 2022, J. Mater. Chem. A - ~100 interface passivation materials\n")
        f.write("2. Zhi et al. 2023, ACS Energy Lett. - 19 ammonium salts (small dataset)\n")
        f.write("3. Zhang et al. 2024, Adv. Funct. Mater. - ML screening study\n")
        f.write("4. Chen et al. 2019, Chem. Soc. Rev. - Review article\n")
        f.write("5. Gao et al. 2020, Adv. Energy Mater. - Review article\n\n")
        f.write(f"Extraction Results:\n")
        f.write(f"  Total molecules extracted: {len(filtered_molecules)}\n")
        f.write(f"  Class 1 (ΔPCEnorm >= 0.10): {class1_count}\n")
        f.write(f"  Class 0 (ΔPCEnorm < 0.10): {class0_count}\n")
        f.write(f"  With SMILES: {with_smiles}\n")
        f.write(f"  Missing SMILES: {len(filtered_molecules) - with_smiles}\n\n")
        f.write("Notes:\n")
        f.write("- Polymers excluded (not representable by SMILES)\n")
        f.write("- Ionic compounds included but may need filtering\n")
        f.write("- SMILES sourced from PubChem and manual lookup\n")
        f.write("- Dataset.xlsx from Fajar 2026 paper is referenced but not publicly available\n")
        f.write("- Full reconstruction requires access to all primary sources via DOIs\n")
    
    print(f"\nSummary saved to {summary_path}")

if __name__ == '__main__':
    main()
