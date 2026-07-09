#!/usr/bin/env python3
"""
SEED subsystem surrogate counter (RAST replication).

Maps Prokka product names + EC numbers to the SEED top-level subsystem buckets
the way RAST reports them (Table 2 in Kandasamy et al. 2022).

Method:
    1. Parse Prokka GBK + GFF for /product= and EC numbers.
    2. Apply hand-curated regex rules per SEED subsystem bucket.
       Rules built directly from the SEED hierarchy documented at
       https://pubseed.theseed.org/?page=SubsystemSelect (the SEED top-level
       categories used by RAST/RASTtk web service).
    3. Each CDS is assigned to AT MOST one subsystem (first match wins, in the
       order RAST scores them — Carbohydrates and Amino acids first because
       they are the largest buckets). This mirrors RAST's "subsystem coverage"
       behavior where one feature contributes to one subsystem.
    4. Output: per-subsystem CDS count + percent of CDSs-with-subsystem-call.

LIMITATIONS (declared up front):
    - RAST/RASTtk uses curated SEED FIGfam HMMs (not free / not downloadable as
      a standalone offline asset). We use product-name regex which under-counts
      CDSs whose Prokka product is "hypothetical protein" (~49% of all CDSs).
    - Therefore our subsystem coverage % will be LOWER than RAST's 24%.
    - The category PERCENT-of-total-subsystem-coverage should still be in the
      same ballpark per category if the regex rules track the SEED definitions.
"""
import re, sys, json
from collections import defaultdict, OrderedDict
from pathlib import Path

GBK = "results/repass/prokka_full/DJF10_clean.gbk"

# SEED top-level subsystems used in Table 2 of Kandasamy et al. 2022 (and the
# standard RAST/RASTtk SEED hierarchy in the same order):
# https://pubseed.theseed.org/SubsysEditor.cgi?page=BrowseSubsystem
# Order matters: a CDS is assigned to the FIRST matching subsystem.
SUBSYSTEMS = OrderedDict([
    ("Cofactors, Vitamins, Prosthetic Groups, Pigments", [
        r"\bbiotin\b", r"\bthiamin", r"\briboflavin", r"\bcobalamin",
        r"\bpyridoxal", r"\bpyridoxine", r"\bfolate\b", r"\bfolyl",
        r"\bpantothenate", r"\bvitamin\b",
        r"\b[Mm]olybdopterin\b", r"\bquinone\b", r"\bmenaquinone\b",
        r"\bporphyrin\b", r"\bheme\b", r"\bsiroheme\b", r"\bcoenzyme A\b",
        r"\bnicotinate\b", r"\bnicotinamide\b", r"\bNAD\b", r"\bNADP\b",
        r"\bdihydrofolate", r"\bcoenzyme F420\b",
        r"\bbioY\b", r"\bbio[A-Z]?\d?\b", r"\bthi[A-Z]\b", r"\bcob[A-Z]\b",
        r"\bfol[A-Z]\b", r"\brib[A-Z]\b",
    ]),
    ("Cell Wall and Capsule", [
        r"\bpeptidoglycan\b", r"\bteichoic\b", r"\bmurein\b",
        r"\bcell wall\b", r"\bcell-wall\b", r"\bcapsul",
        r"\bMurI?[A-Z]?\b", r"\bMur[A-Z]\b", r"\blipopolysaccharide\b",
        r"\bO-antigen\b", r"\bDltA\b", r"\bdltA\b", r"\bD-alanyl\b",
        r"\bLysM\b", r"\bSlap\b", r"\bsortase\b", r"\bdacA\b",
        r"\bUDP-N-acetylmuramoylalanine\b", r"\bD,D-transpeptidase\b",
        r"\bdacB\b", r"\bglmU\b", r"\bglmM\b", r"\bglmS\b",
    ]),
    ("Virulence, Disease and Defense", [
        r"\bdefense\b", r"\bantibiotic\b", r"\bresistance protein\b",
        r"\bmacrolide efflux\b", r"\btetracycline resistance\b",
        r"\bcamphor resistance\b", r"\bbeta-lactam\b", r"\bvancomycin\b",
        r"\b[Tt]ype II toxin\b", r"\b[Tt]ype III secret\b", r"\bvirulence\b",
        r"\bmultidrug resistance\b", r"\bMfd\b", r"\bClpL\b",
        r"\bCRISPR\b", r"\bCas[0-9]+\b",
        r"\bcatA\b", r"\btetM\b", r"\btetO\b", r"\bvanX\b", r"\bvanY\b",
        r"\bmef\b", r"\blincosamide\b", r"\bmacrolide\b",
    ]),
    ("Potassium metabolism", [
        r"\bpotassium\b", r"\bK\+ transport", r"\bkdpA\b", r"\bkdpB\b", r"\bkdpC\b",
        r"\bkdpD\b", r"\bkdpE\b", r"\btrkA\b", r"\btrkH\b", r"\bktrA\b", r"\bktrB\b",
    ]),
    ("Phages, Prophages, Transposable elements, Plasmids", [
        r"\bphage\b", r"\bprophage\b", r"\bbacteriophage\b",
        r"\binsertion sequence\b", r"\btransposase\b", r"\bIS[0-9]+", 
        r"\bintegrase\b", r"\binvertase\b", r"\btransposon\b",
        r"\bIS[A-Z]\w*\b", r"\bmobile element\b",
        r"\bplasmid replication\b", r"\bRepA\b", r"\bRepB\b", r"\bRepC\b",
    ]),
    ("Membrane Transport", [
        r"\b[Tt]ype I secret", r"\b[Ss]ecretion\b", r"\bSec translocase\b",
        r"\bSecA\b", r"\bSecE\b", r"\bSecG\b", r"\bSecY\b", r"\bTatA\b",
        r"\bSrp\b", r"\bSRP\b", r"\bFtsY\b", r"\bphosphotransferase system\b",
        r"\bPTS\b", r"\bABC transporter ATP-binding\b", r"\bABC transporter permease\b",
        r"\bABC superfamily\b", r"\bSugar phosphotransferase\b",
        r"\bPotE\b", r"\bSpermidine transport\b",
    ]),
    ("Iron acquisition and metabolism", [
        r"\bferric\b", r"\bferrous\b", r"\biron transport\b", r"\bsiderophore\b",
        r"\bferrichrome\b", r"\bFhuA\b", r"\bFhuB\b", r"\bFhuC\b", r"\bFhuD\b",
        r"\bfepA\b", r"\bfepB\b", r"\bfeoA\b", r"\bfeoB\b",
        r"\biron-sulfur\b", r"\b[Ff]erritin\b", r"\bdpsA\b",
    ]),
    ("RNA Metabolism", [
        r"\bRNA polymerase\b", r"\bRNAse\b", r"\bRNase\b",
        r"\btranscription\b", r"\brRNA\b", r"\btransfer RNA\b",
        r"\btmRNA\b", r"\bribonuclease\b", r"\bRho-\b", r"\brnj\b", r"\brnpA\b",
        r"\bRpoA\b", r"\bRpoB\b", r"\bRpoC\b", r"\bRpoD\b", r"\bRpoE\b",
        r"\bNusA\b", r"\bNusG\b", r"\bgreA\b", r"\bgreB\b", r"\bNTP pyrophosphohydrolase\b",
    ]),
    ("Nucleosides and Nucleotides", [
        r"\bpurine\b", r"\bpyrimidine\b", r"\bnucleoside\b", r"\bnucleotide\b",
        r"\bxanthine\b", r"\buridine\b", r"\bthymidine\b", r"\bcytidine\b",
        r"\badenosine\b", r"\bguanosine\b", r"\bdeoxyribose\b", r"\bribose-5\b",
        r"\bPurA\b", r"\bPurB\b", r"\bPurC\b", r"\bPurD\b", r"\bPurE\b", r"\bPurF\b",
        r"\bPyrA\b", r"\bPyrB\b", r"\bPyrC\b", r"\bPyrD\b", r"\bPyrE\b", r"\bPyrF\b",
        r"\bDut\b", r"\bUMP\b", r"\bCMP\b", r"\bAMP\b", r"\bdUTP\b",
        r"\binosine\b", r"\borotate\b", r"\b[Dd]eaminase\b", r"\bnudix\b",
    ]),
    ("Protein Metabolism", [
        r"\bribosomal protein\b", r"\baminoacyl-tRNA\b", r"\btRNA ligase\b",
        r"\btRNA synthetase\b", r"\b[Cc]haperone\b", r"\bGroEL\b", r"\bGroES\b",
        r"\bDnaK\b", r"\bDnaJ\b", r"\bHsp[0-9]+\b", r"\b[Cc]lp[A-Z]?\b",
        r"\b[Tt]ranslation factor\b", r"\b[Ee]longation factor\b",
        r"\b[Pp]eptidase\b", r"\b[Pp]rotease\b", r"\bsignal peptidase\b",
        r"\b30S\b", r"\b50S\b", r"\bribosome\b", r"\bRsmA\b",
        r"\b[Tt]ranslation initiation factor\b",
    ]),
    ("Cell Division and Cell Cycle", [
        r"\bcell division\b", r"\bFtsZ\b", r"\bFtsA\b", r"\bFtsK\b", r"\bFtsN\b",
        r"\bFtsW\b", r"\bMurZ\b", r"\bDivIB\b", r"\bMinC\b", r"\bMinD\b", r"\bMinE\b",
        r"\bMreB\b", r"\bMreC\b", r"\bMreD\b", r"\bGpsB\b",
        r"\bchromosome partition\b", r"\bSmc\b", r"\bParA\b", r"\bParB\b",
    ]),
    ("Regulation and Cell signaling", [
        r"\bhistidine kinase\b", r"\bresponse regulator\b", r"\btwo-component\b",
        r"\b[Tt]ranscriptional regulator\b", r"\b[Rr]epressor\b",
        r"\b[Aa]ctivator\b", r"\bHTH\b", r"\bMarR\b", r"\bGntR\b", r"\bLysR\b",
        r"\bcyclic-di-GMP\b", r"\bdiguanylate cyclase\b",
    ]),
    ("Secondary Metabolism", [
        r"\bsecondary metabolite\b", r"\bpolyketide\b", r"\bterpene\b",
        r"\b[Bb]acteriocin\b", r"\b[Pp]lantaricin\b", r"\b[Ll]antibiotic\b",
        r"\b[Ss]actipeptide\b", r"\bnonribosomal peptide synthet\b",
    ]),
    ("DNA Metabolism", [
        r"\bDNA polymerase\b", r"\bDNA helicase\b", r"\bDNA gyrase\b",
        r"\bDNA topoisomerase\b", r"\b[Rr]eplication\b", r"\bDNA repair\b",
        r"\b[Rr]ecombinase\b", r"\bRecA\b", r"\bRecB\b", r"\bRecF\b", r"\bRecN\b",
        r"\bRecJ\b", r"\bRecG\b", r"\bRecQ\b", r"\bRuvA\b", r"\bRuvB\b", r"\bRuvC\b",
        r"\bRadA\b", r"\bUvrA\b", r"\bUvrB\b", r"\bUvrC\b", r"\bUvrD\b",
        r"\bMutL\b", r"\bMutS\b", r"\bDinB\b", r"\bDam\b", r"\bDcm\b",
        r"\b[Mm]ethylase\b.*DNA", r"\brestriction\b", r"\b[Mm]odification\b.*DNA",
    ]),
    ("Fatty Acids, Lipids, and Isoprenoids", [
        r"\bfatty acid\b", r"\bacyl-CoA\b", r"\bphospholipid\b",
        r"\b[Ll]ipoyl\b", r"\b[Ll]ipid biosynthesis\b", r"\bisoprenoid\b",
        r"\bFabA\b", r"\bFabB\b", r"\bFabD\b", r"\bFabF\b", r"\bFabG\b",
        r"\bFabH\b", r"\bFabI\b", r"\bFabK\b", r"\bFabZ\b",
        r"\bcardiolipin\b", r"\b[Pp]hosphatidyl\b",
    ]),
    ("Nitrogen Metabolism", [
        r"\bnitrogen\b.*[Mm]etabolism", r"\bnitrate\b", r"\bnitrite\b",
        r"\bammonium\b", r"\bnirA\b", r"\bnasA\b", r"\bglnA\b", r"\bglnB\b",
    ]),
    ("Dormancy and Sporulation", [
        r"\b[Ss]pore\b", r"\bsporulation\b", r"\b[Ss]por[A-Z]\b",
        r"\b[Gg]erminat", r"\bSpoVG\b", r"\bGerA\b", r"\bGerB\b",
    ]),
    ("Respiration", [
        r"\b[Cc]ytochrome\b", r"\b[Qq]uinol\b", r"\b[Tt]erminal oxidase\b",
        r"\bATP synthase\b", r"\bNADH\b.*[Dd]ehydrogenase\b",
        r"\b[Uu]biquinone\b",
    ]),
    ("Stress Response", [
        r"\bstress\b", r"\bcold shock\b", r"\bheat shock\b", r"\bCspA\b",
        r"\bCspL\b", r"\bIbp[AB]\b", r"\bGrp[E]\b", r"\bunivers stress\b",
        r"\bUsp[A-Z]\b", r"\b[Ss]uperoxide dismut", r"\b[Cc]atalase\b",
        r"\bperoxidase\b", r"\bthioredoxin\b", r"\boxidative stress\b",
        r"\bHslU\b", r"\bHslV\b", r"\bHslO\b",
    ]),
    ("Metabolism of Aromatic Compounds", [
        r"\baromatic compound\b", r"\bphenol\b", r"\bbenzoate\b",
        r"\bphenylacetate\b", r"\baromatic amino acid\b",
        r"\bp-hydroxybenzoate\b", r"\bcatechol\b",
    ]),
    ("Amino Acids and Derivatives", [
        r"\bamino acid\b.*[Bb]iosynthesis", r"\bglutamate\b", r"\bglutamine\b",
        r"\baspartate\b", r"\basparagine\b", r"\bhistidine\b", r"\barginine\b",
        r"\bproline\b", r"\bornithine\b", r"\blysine\b", r"\bthreonine\b",
        r"\bserine\b", r"\bglycine\b", r"\bcysteine\b", r"\bmethionine\b",
        r"\bisoleucine\b", r"\bleucine\b", r"\bvaline\b", r"\bphenylalanine\b",
        r"\btyrosine\b", r"\btryptophan\b", r"\balanine\b",
        r"\b[Tt]ransaminase\b", r"\b[Dd]eaminase\b",
        r"\bArg[A-Z]\b", r"\bHis[A-Z]\b", r"\bLys[A-Z]\b", r"\bMet[A-Z]\b",
        r"\bIlv[A-Z]\b", r"\bLeu[A-Z]\b", r"\bTrp[A-Z]\b", r"\bTyr[A-Z]\b",
        r"\bPhe[A-Z]\b", r"\bSer[A-Z]\b", r"\bThr[A-Z]\b", r"\bAro[A-Z]\b",
    ]),
    ("Sulfur Metabolism", [
        r"\b[Ss]ulfur\b", r"\bsulfate\b", r"\bsulfide\b", r"\bsulfonate\b",
        r"\b[Cc]ystathion\b", r"\bcysB\b", r"\bcysC\b", r"\bcysD\b", r"\bcysE\b",
        r"\bcysH\b", r"\bcysI\b", r"\bcysJ\b", r"\bcysK\b", r"\bcysM\b",
    ]),
    ("Phosphorus Metabolism", [
        r"\bphosphate transport\b", r"\bphosphonate\b", r"\bphytase\b",
        r"\bPstA\b", r"\bPstB\b", r"\bPstC\b", r"\bPstS\b", r"\bphoB\b",
        r"\bphoR\b", r"\bphoU\b",
    ]),
    ("Carbohydrates", [
        r"\bglycoside hydrolase\b", r"\bglycosyltransferase\b",
        r"\b[Cc]arbohydrate\b", r"\b[Gg]lyco[gs]en\b",
        r"\bsugar transporter\b", r"\bsucrose\b", r"\bmaltose\b",
        r"\bglucose\b", r"\bfructose\b", r"\bgalactose\b", r"\blactose\b",
        r"\bcellobiose\b", r"\bxylose\b", r"\barabinose\b", r"\bmannose\b",
        r"\btrehalose\b", r"\bglycerol\b", r"\bstarch\b", r"\bpyruvate\b",
        r"\b[Pp]hosphoenolpyruvate\b", r"\bglycolysis\b",
        r"\b[Gg]lucon", r"\bxylulose\b", r"\bribulose-5\b",
        r"\bphosphogluconate\b", r"\bhexokinase\b", r"\bphosphoglycerate\b",
        r"\bpentose phosphate\b", r"\b[Ll]actate dehydrogenase\b",
        r"\bphosphoketolase\b", r"\bacetate kinase\b", r"\bglucose-6-phosphate\b",
        r"\b[Ee]nolase\b",
        r"\b[Aa]lpha-glucan\b", r"\b[Bb]eta-glucan\b",
    ]),
])

# Parse Prokka GBK and extract /product= per CDS
products = []
current = None
with open(GBK) as fh:
    for line in fh:
        m_cds = re.match(r"^     CDS\s+", line)
        if m_cds:
            if current:
                products.append(current)
            current = ""
            continue
        m_prod = re.match(r'\s+/product="(.+)"', line)
        if m_prod and current is not None:
            current = m_prod.group(1)
        elif current is not None and line.startswith("     ") and not line.startswith("     CDS "):
            # Continuation of /product if multi-line
            if current and line.strip().endswith('"'):
                pass
if current is not None:
    products.append(current)

print(f"Total CDS products parsed: {len(products)}")
hypothetical = sum(1 for p in products if 'hypothetical' in p.lower())
print(f"Hypothetical: {hypothetical}")
print(f"Annotated: {len(products) - hypothetical}")

# Apply rules
counts = OrderedDict((k, 0) for k in SUBSYSTEMS)
assigned = 0
unassigned_examples = []
for p in products:
    if not p or 'hypothetical' in p.lower():
        continue
    matched = False
    for cat, patterns in SUBSYSTEMS.items():
        for pat in patterns:
            if re.search(pat, p):
                counts[cat] += 1
                assigned += 1
                matched = True
                break
        if matched: break
    if not matched and len(unassigned_examples) < 30:
        unassigned_examples.append(p)

total = sum(counts.values())
print(f"\n=== SEED subsystem distribution (RAST surrogate) ===")
print(f"Total CDSs assigned to a subsystem: {total}")
print(f"\n{'Subsystem':<55} {'Count':>6} {'%':>7}")
print("-" * 70)
for cat, n in counts.items():
    pct = 100 * n / total if total else 0
    print(f"{cat:<55} {n:>6} {pct:>6.2f}%")

# Compare to paper Table 2
PAPER = OrderedDict([
    ("Cofactors, Vitamins, Prosthetic Groups, Pigments", (106, 9.5)),
    ("Cell Wall and Capsule", (52, 4.6)),
    ("Virulence, Disease and Defense", (41, 3.7)),
    ("Potassium metabolism", (6, 0.5)),
    ("Miscellaneous", (14, 1.3)),
    ("Phages, Prophages, Transposable elements, Plasmids", (9, 0.8)),
    ("Membrane Transport", (35, 3.1)),
    ("Iron acquisition and metabolism", (5, 0.4)),
    ("RNA Metabolism", (38, 3.4)),
    ("Nucleosides and Nucleotides", (91, 8.1)),
    ("Protein Metabolism", (127, 11.3)),
    ("Cell Division and Cell Cycle", (4, 0.4)),
    ("Regulation and Cell signaling", (16, 1.4)),
    ("Secondary Metabolism", (4, 0.4)),
    ("DNA Metabolism", (63, 5.6)),
    ("Fatty Acids, Lipids, and Isoprenoids", (34, 3.0)),
    ("Nitrogen Metabolism", (8, 0.7)),
    ("Dormancy and Sporulation", (6, 0.5)),
    ("Respiration", (16, 1.4)),
    ("Stress Response", (20, 1.8)),
    ("Metabolism of Aromatic Compounds", (8, 0.7)),
    ("Amino Acids and Derivatives", (175, 15.6)),
    ("Sulfur Metabolism", (4, 0.4)),
    ("Phosphorus Metabolism", (7, 0.6)),
    ("Carbohydrates", (230, 20.55)),
])
paper_total = sum(v[0] for v in PAPER.values())
print(f"\n=== Side-by-side vs Kandasamy 2022 Table 2 (paper total={paper_total}, ours total={total}) ===")
print(f"{'Subsystem':<55} {'Paper N':>8} {'Paper %':>8} {'Ours N':>7} {'Ours %':>8}")
print("-" * 100)
matches = 0
for cat in PAPER:
    pn, pp = PAPER[cat]
    on = counts.get(cat, 0)
    op = 100 * on / total if total else 0
    delta_p = op - pp
    sign = "✅" if abs(delta_p) < 4 else ("⚠️" if abs(delta_p) < 8 else "❌")
    if abs(delta_p) < 4: matches += 1
    print(f"{cat:<55} {pn:>8} {pp:>7.2f}% {on:>7} {op:>7.2f}% {sign}")

print(f"\nCategories matching within 4% absolute: {matches}/{len(PAPER)}")

# Output to JSON for later use
out = {"total_cds_with_subsystem": total, "paper_total": paper_total, "categories": {k:{"paper_n":PAPER.get(k,(None,))[0], "paper_pct":PAPER.get(k,(None,None))[1], "ours_n":v, "ours_pct": 100*v/total if total else 0} for k,v in counts.items()}}
Path("results/repass/subsystems").mkdir(parents=True, exist_ok=True)
with open("results/repass/subsystems/seed_subsystem_counts.json","w") as fh:
    json.dump(out, fh, indent=2)
print("\nWrote results/repass/subsystems/seed_subsystem_counts.json")

print(f"\n=== Sample unassigned annotated products (first 20) ===")
for p in unassigned_examples[:20]:
    print(f"  - {p}")
