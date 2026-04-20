#!/usr/bin/env python3
"""
Convert molecule names/abbreviations to SMILES using PubChem + a manual lookup table.

Many perovskite passivation molecules use abbreviations (PEAI, BAI, etc.)
that PubChem doesn't recognize directly. This script handles both cases.
"""
import csv
import json
import time
import sys
import requests
from pathlib import Path

# ─── Manual lookup for common PSC passivation molecules ──────
# These are abbreviations commonly used in the perovskite literature
# that PubChem won't find by name
MANUAL_SMILES = {
    # Single letters / elements used as passivators
    "S": None,  # Sulfur treatment - not a discrete molecule
    "N": None,  # Nitrogen treatment
    "SN": None,  # Sulfur + Nitrogen

    # Polymers (excluded per paper: "Polymer passivators were excluded")
    "P3HT": None,
    "PTAA": None,
    "MEH-PPV": None,
    "Poly-TPD": None,
    "PBDTTT-CT": None,
    "PMMA": None,
    "PEIm": None,  # Polyethyleneimine
    "PEIE": None,  # Polyethyleneimine ethoxylated

    # Ammonium iodide salts (ionic - excluded per paper)
    "FABr": None,  # Formamidinium bromide (ionic)
    "FAI": None,
    "FACl": None,
    "MAI": None,  # Methylammonium iodide (ionic)
    "MABr": None,
    "MACl": None,
    "CsI": None,
    "CsBr": None,
    "GAI": None,  # Guanidinium iodide
    "GuaI": None,

    # Alkylammonium halides (ionic)
    "PEAI": "CCc1ccccc1CN",  # Phenethylammonium - base form (amine, not salt)
    "EAI": "CCN",  # Ethylamine
    "IAI": "CC(C)N",  # Isopropylamine
    "BAI": "CCCCN",  # Butylamine
    "HAI": "CCCCCCN",  # Hexylamine
    "OAI": "CCCCCCCCN",  # Octylamine
    "C4Br": "CCCCN",  # Butylammonium bromide → butylamine
    "C6Br": "CCCCCCN",  # Hexylammonium bromide → hexylamine
    "C8Br": "CCCCCCCCN",  # Octylammonium bromide → octylamine
    "FPEAI": "Fc1ccc(CCN)cc1",  # Fluorophenethylamine
    "FPMAI": "Fc1ccc(CN)cc1",  # Fluorophenylmethylamine
    "AVAI": "C=CCN",  # Allylammonium iodide → allylamine
    "HDADI": "NCCCCCCN",  # Hexanediammonium → hexanediamine

    # Common small molecules
    "tBP": "Cc1ccncc1",  # 4-tert-butylpyridine
    "2-MP": "Cc1ccccn1",  # 2-methylpyridine
    "Py": "c1ccncc1",  # Pyridine
    "PTT": "c1ccsc1",  # Thiophene (likely polythiophene-related)
    "MMI": "Cn1ccnc1",  # 1-Methylimidazole
    "Benzylamine": "NCc1ccccc1",
    "TP": "c1ccc2[nH]ccc2c1",  # Thieno[3,2-b]pyrrole or similar
    "ETP": "CCc1cc2ccccc2[nH]1",
    "BTP": "CCCCc1cc2ccccc2[nH]1",
    "MTP": "Cc1cc2ccccc2[nH]1",
    "HTP": "CCCCCCc1cc2ccccc2[nH]1",
    "DTP": "CCCCCCCCCCc1cc2ccccc2[nH]1",

    # TFDIB
    "TFDIB": "Fc1c(F)c(F)c(I)c(F)c1I",  # 1,4-diiodo-2,3,5,6-tetrafluorobenzene

    # Thiol molecules
    "HS-Ph-CN": "N#Cc1ccc(S)cc1",  # 4-cyanothiophenol
    "HS-Ph-NO2": "[O-][N+](=O)c1ccc(S)cc1",  # 4-nitrothiophenol
    "HS-Ph-F": "Fc1ccc(S)cc1",  # 4-fluorothiophenol
    "HS-Ph-Cl": "Clc1ccc(S)cc1",  # 4-chlorothiophenol
    "HS-Ph-Br": "Brc1ccc(S)cc1",  # 4-bromothiophenol
    "HS-Ph-OH": "Oc1ccc(S)cc1",  # 4-hydroxythiophenol
    "HS-Ph-NH2": "Nc1ccc(S)cc1",  # 4-aminothiophenol
    "HS-Ph-OMe": "COc1ccc(S)cc1",  # 4-methoxythiophenol
    "HS-Ph-CH3": "Cc1ccc(S)cc1",  # 4-methylthiophenol
    "HS-Ph-OCF3": "FC(F)(F)Oc1ccc(S)cc1",

    # Phosphonic acids
    "PPA": "O=P(O)(O)c1ccccc1",  # Phenylphosphonic acid
    "OPA": "O=P(O)(O)CCCCCCCC",  # Octylphosphonic acid

    # Common named molecules
    "Theophylline": "Cn1c(=O)c2[nH]cnc2n(C)c1=O",
    "Caffeine": "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
    "Urea": "NC(N)=O",

    # Lewis bases
    "DMSO": "CS(C)=O",
    "DMF": "CN(C)C=O",
    "NMP": "CN1CCCC1=O",

    # CAS-identifiable from Table S3
    "DL-Mandelic Acid": "OC(=O)C(O)c1ccccc1",
    "4-Maleimidobutyric Acid": "O=C(O)CCCN1C(=O)C=CC1=O",
    "Maleic Acid Monoamide": "NC(=O)/C=C\\C(=O)O",

    # Additional passivation molecules from literature
    "EPC": "CCOC(=O)c1ccccc1",  # Ethyl phenyl carbamate or ethyl benzoate
    "DPPS": "O=S(c1ccccc1)c1ccccc1",  # Diphenyl sulfoxide
    "BnOH": "OCc1ccccc1",  # Benzyl alcohol
    "BA": "CCCCN",  # Butylamine
    "PA": "CCCN",  # Propylamine
    "PEA": "NCCc1ccccc1",  # Phenethylamine
    "BPA": "O=P(O)(O)CCCC",  # Butylphosphonic acid
    "EDTA": "OC(=O)CN(CCN(CC(O)=O)CC(O)=O)CC(O)=O",  # EDTA
    "PZDI": "c1cnc[nH]1",  # Pyrazole or pyrazine derivative
    "PDAI": "c1cc2ccccc2cc1N",  # 2-Naphthylamine

    # Additional ionic compounds (to exclude)
    "HBAI.FAI": None,
    "HBAI.FABr": None,
    "HBAI.FACl": None,

    # More ionic salts
    "CHAI": None,  # Cyclohexylammonium iodide
    "CHMAI": None,  # Cyclohexylmethylammonium iodide
    "(HAD)I2": None,  # Hexanediammonium diiodide
    "(EDBE)I2": None,  # Ethylene diamine bis ethanol diiodide
    "CTABr": None,  # Cetyltrimethylammonium bromide (ionic surfactant)
    "TCPBr": None,  # Tricyclohexylphosphonium bromide
    "TCPI": None,
    "TAI": None,  # Trimethylammonium iodide
    "ImI": None,  # Imidazolium iodide
    "PEACl": None,  # Phenethylammonium chloride
    "OABr": None,  # Octylammonium bromide
    "OACl": None,  # Octylammonium chloride
    "[EMIM]Br": None,  # Ionic liquid
    "DMEDAI2": None,
    "FEAI": None,  # Fluoroethylammonium iodide
    "2-TEAI": None,  # 2-Thienylethylammonium iodide
    "ODAI2": None,  # Octanediammonium diiodide
    "ADAHCl": None,  # Adamantylamine HCl
    "ClTPPPF6": None,  # Ionic TPP complex
    "BrTPPPF6": None,  # Ionic TPP complex
    "DMIMPF6": None,  # Ionic liquid
    "BMIMBF4": None,  # Ionic liquid
    "PyNa+": None,  # Ionic
    "CBAH": None,  # Ionic

    # More polymers
    "Polystyrene": None,
    "Poly TPD": None,
    "PVP": None,  # Polyvinylpyrrolidone

    # Additional named molecules
    "Tetracene": "c1ccc2cc3cc4ccccc4cc3cc2c1",
    "PABA": "Nc1ccc(C(=O)O)cc1",  # 4-Aminobenzoic acid
    "CDCA": "OC(=O)CC1CCC2C3CC=C4CC(O)CCC4(C)C3CCC12C",  # Chenodeoxycholic acid
    "C8-BTBT": "CCCCCCCCc1cc2ccc3cc(CCCCCCCC)sc3c2s1",  # C8-BTBT
    "MTDAA": None,  # Unknown
    "OLA": "CCCCCCCCC=CCCCCCCCCN",  # Oleylamine
    "SDBS": None,  # Sodium dodecylbenzenesulfonate (ionic)
    "POSS-NH2": None,  # POSS cage (polymer-like)
    "POSS-SH": None,  # POSS cage
    "B2Cat2": "B1(OC2=CC=CC=C2O1)B1OC2=CC=CC=C2O1",  # Bis(catecholato)diboron
    "ADA": "C1C2CC3CC1CC(C2)C3N",  # Adamantylamine
    "AD": "C1C2CC3CC1CC(C2)C3",  # Adamantane
    "BEDCE": None,  # Unknown
    "QA": None,  # Quaternary ammonium (generic)
    "PTPD": None,  # Unknown
    "PHI": None,  # Unknown abbreviation
    "TFMBA": "FC(F)(F)c1ccc(C(=O)O)cc1",  # 4-(Trifluoromethyl)benzoic acid
    "TPPO": "O=P(c1ccccc1)(c1ccccc1)c1ccccc1",  # Triphenylphosphine oxide
    "TMPP": "COc1ccc(P(c2ccc(OC)cc2)c2ccc(OC)cc2)cc1",  # Tris(4-methoxyphenyl)phosphine
    "TPFP": None,  # Unknown
    "TBPO": "CCCCP(=O)(CCCC)CCCC",  # Tributylphosphine oxide
}

# Parse errors in extraction (not real molecules)
MANUAL_SMILES["0.972:3"] = None
MANUAL_SMILES[""] = None


def pubchem_name_to_smiles(name: str) -> str | None:
    """Look up SMILES from PubChem by molecule name."""
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{requests.utils.quote(name)}/property/CanonicalSMILES/JSON"
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            props = data.get("PropertyTable", {}).get("Properties", [])
            if props:
                return props[0].get("CanonicalSMILES") or props[0].get("ConnectivitySMILES")
    except Exception:
        pass
    return None


def convert_names_to_smiles(input_csv: str, output_csv: str):
    """Convert molecule names to SMILES, filtering out polymers and ionic compounds."""
    with open(input_csv) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    results = []
    skipped_polymer = 0
    skipped_ionic = 0
    skipped_notfound = 0
    found_manual = 0
    found_pubchem = 0

    for row in rows:
        name = row["name"].strip()

        # Check manual lookup first
        if name in MANUAL_SMILES:
            smi = MANUAL_SMILES[name]
            if smi is None:
                # Explicitly excluded (polymer, ionic, or non-molecule)
                skipped_polymer += 1
                continue
            found_manual += 1
            row["smiles"] = smi
            row["source"] = "manual"
            results.append(row)
            continue

        # Try PubChem
        smi = pubchem_name_to_smiles(name)
        if smi:
            found_pubchem += 1
            row["smiles"] = smi
            row["source"] = "pubchem"
            results.append(row)
            time.sleep(0.3)  # Rate limit
            continue

        # Try common variations
        for variant in [f"{name} iodide", f"{name} acid", name.replace("-", " ")]:
            smi = pubchem_name_to_smiles(variant)
            if smi:
                found_pubchem += 1
                row["smiles"] = smi
                row["source"] = "pubchem"
                results.append(row)
                break
            time.sleep(0.3)
        else:
            skipped_notfound += 1
            print(f"  NOT FOUND: {name}")

    # Write output
    fieldnames = ["id", "name", "smiles", "pce_initial", "pce_final", "delta_pce_norm", "source"]
    with open(output_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in results:
            w.writerow({k: row.get(k, "") for k in fieldnames})

    print(f"\nSummary:")
    print(f"  Total input:        {len(rows)}")
    print(f"  Found (manual):     {found_manual}")
    print(f"  Found (PubChem):    {found_pubchem}")
    print(f"  Skipped (excluded): {skipped_polymer}")
    print(f"  Not found:          {skipped_notfound}")
    print(f"  Output:             {len(results)} molecules with SMILES")
    print(f"  Saved to:           {output_csv}")


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent.parent / "data" / "liu_2022_molecules.csv")
    output_file = sys.argv[2] if len(sys.argv) > 2 else str(Path(__file__).parent.parent / "data" / "liu_2022_with_smiles.csv")
    convert_names_to_smiles(input_file, output_file)
