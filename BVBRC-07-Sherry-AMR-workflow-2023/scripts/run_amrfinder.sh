#!/bin/bash
set -e
BASEDIR="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS_DIR="$BASEDIR/results/amrfinder"
mkdir -p "$RESULTS_DIR"

echo "Running AMRFinderPlus on GCA_900620215.1 (Staphylococcus aureus)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_900620215.1.fna" --organism Staphylococcus_aureus --plus --threads 4 --output "$RESULTS_DIR/GCA_900620215.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_900620215.1"

echo "Running AMRFinderPlus on GCA_000145595.1 (Staphylococcus aureus)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_000145595.1.fna" --organism Staphylococcus_aureus --plus --threads 4 --output "$RESULTS_DIR/GCA_000145595.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_000145595.1"

echo "Running AMRFinderPlus on GCA_001456055.3 (Klebsiella pneumoniae)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001456055.3.fna" --organism Klebsiella --plus --threads 4 --output "$RESULTS_DIR/GCA_001456055.3.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001456055.3"

echo "Running AMRFinderPlus on GCA_004006035.1 (Klebsiella pneumoniae)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_004006035.1.fna" --organism Klebsiella --plus --threads 4 --output "$RESULTS_DIR/GCA_004006035.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_004006035.1"

echo "Running AMRFinderPlus on GCA_003020705.1 (Enterococcus faecium)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_003020705.1.fna" --organism Enterococcus_faecium --plus --threads 4 --output "$RESULTS_DIR/GCA_003020705.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_003020705.1"

echo "Running AMRFinderPlus on GCA_003020685.1 (Enterococcus faecium)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_003020685.1.fna" --organism Enterococcus_faecium --plus --threads 4 --output "$RESULTS_DIR/GCA_003020685.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_003020685.1"

echo "Running AMRFinderPlus on GCA_002811555.3 (Escherichia coli)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_002811555.3.fna" --organism Escherichia --plus --threads 4 --output "$RESULTS_DIR/GCA_002811555.3.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_002811555.3"

echo "Running AMRFinderPlus on GCA_002202175.1 (Escherichia coli)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_002202175.1.fna" --organism Escherichia --plus --threads 4 --output "$RESULTS_DIR/GCA_002202175.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_002202175.1"

echo "Running AMRFinderPlus on GCA_001573125.1 (Acinetobacter baumannii)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001573125.1.fna" --organism Acinetobacter_baumannii --plus --threads 4 --output "$RESULTS_DIR/GCA_001573125.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001573125.1"

echo "Running AMRFinderPlus on GCA_005280375.1 (Acinetobacter baumannii)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_005280375.1.fna" --organism Acinetobacter_baumannii --plus --threads 4 --output "$RESULTS_DIR/GCA_005280375.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_005280375.1"

echo "Running AMRFinderPlus on GCA_001647755.1 (Salmonella enterica)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001647755.1.fna" --organism Salmonella --plus --threads 4 --output "$RESULTS_DIR/GCA_001647755.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001647755.1"

echo "Running AMRFinderPlus on GCA_005844025.1 (Salmonella enterica)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_005844025.1.fna" --organism Salmonella --plus --threads 4 --output "$RESULTS_DIR/GCA_005844025.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_005844025.1"

echo "Running AMRFinderPlus on GCA_001792835.1 (Pseudomonas aeruginosa)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001792835.1.fna" --organism Pseudomonas_aeruginosa --plus --threads 4 --output "$RESULTS_DIR/GCA_001792835.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001792835.1"

echo "Running AMRFinderPlus on GCA_001679685.1 (Pseudomonas aeruginosa)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001679685.1.fna" --organism Pseudomonas_aeruginosa --plus --threads 4 --output "$RESULTS_DIR/GCA_001679685.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001679685.1"

echo "Running AMRFinderPlus on GCA_001022215.1 (Serratia marcescens)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001022215.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_001022215.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001022215.1"

echo "Running AMRFinderPlus on GCA_001294565.1 (Serratia marcescens)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001294565.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_001294565.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001294565.1"

echo "Running AMRFinderPlus on GCA_000284595.1 (Stenotrophomonas maltophilia)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_000284595.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_000284595.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_000284595.1"

echo "Running AMRFinderPlus on GCA_002138415.1 (Stenotrophomonas maltophilia)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_002138415.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_002138415.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_002138415.1"

echo "Running AMRFinderPlus on GCA_000292915.1 (Burkholderia cepacia)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_000292915.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_000292915.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_000292915.1"

echo "Running AMRFinderPlus on GCA_002197405.1 (Proteus mirabilis)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_002197405.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_002197405.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_002197405.1"

echo "Running AMRFinderPlus on GCA_005960425.1 (Citrobacter freundii)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_005960425.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_005960425.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_005960425.1"

echo "Running AMRFinderPlus on GCA_003482165.1 (Clostridioides difficile)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_003482165.1.fna" --organism Clostridioides_difficile --plus --threads 4 --output "$RESULTS_DIR/GCA_003482165.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_003482165.1"

echo "Running AMRFinderPlus on GCA_002975475.1 (Mycobacterium tuberculosis)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_002975475.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_002975475.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_002975475.1"

echo "Running AMRFinderPlus on GCA_004151605.1 (Enterobacter cloacae)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_004151605.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_004151605.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_004151605.1"

echo "Running AMRFinderPlus on GCA_003812545.1 (Listeria monocytogenes)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_003812545.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_003812545.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_003812545.1"

echo "Running AMRFinderPlus on GCA_001717625.1 (Campylobacter jejuni)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001717625.1.fna" --organism Campylobacter --plus --threads 4 --output "$RESULTS_DIR/GCA_001717625.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001717625.1"

echo "Running AMRFinderPlus on GCA_003965345.2 (Enterobacter hormaechei)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_003965345.2.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_003965345.2.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_003965345.2"

echo "Running AMRFinderPlus on GCA_003719755.1 (Vibrio cholerae)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_003719755.1.fna" --organism Vibrio_cholerae --plus --threads 4 --output "$RESULTS_DIR/GCA_003719755.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_003719755.1"

echo "Running AMRFinderPlus on GCA_001580175.1 (Shigella flexneri)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001580175.1.fna" --organism Escherichia --plus --threads 4 --output "$RESULTS_DIR/GCA_001580175.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001580175.1"

echo "Running AMRFinderPlus on GCA_900087725.2 (Neisseria gonorrhoeae)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_900087725.2.fna" --organism Neisseria --plus --threads 4 --output "$RESULTS_DIR/GCA_900087725.2.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_900087725.2"

echo "Running AMRFinderPlus on GCA_001752965.1 (Legionella pneumophila)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001752965.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_001752965.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001752965.1"

echo "Running AMRFinderPlus on GCA_001558495.2 (Vibrio parahaemolyticus)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001558495.2.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_001558495.2.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001558495.2"

echo "Running AMRFinderPlus on GCA_001870185.1 (Klebsiella oxytoca)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001870185.1.fna" --organism Klebsiella --plus --threads 4 --output "$RESULTS_DIR/GCA_001870185.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001870185.1"

echo "Running AMRFinderPlus on GCA_003204135.1 (Providencia rettgeri)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_003204135.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_003204135.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_003204135.1"

echo "Running AMRFinderPlus on GCA_003265245.1 (Shigella sonnei)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_003265245.1.fna" --organism Escherichia --plus --threads 4 --output "$RESULTS_DIR/GCA_003265245.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_003265245.1"

echo "Running AMRFinderPlus on GCA_000626595.1 (Neisseria meningitidis)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_000626595.1.fna" --organism Neisseria --plus --threads 4 --output "$RESULTS_DIR/GCA_000626595.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_000626595.1"

echo "Running AMRFinderPlus on GCA_007035805.1 (Enterobacter asburiae)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_007035805.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_007035805.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_007035805.1"

echo "Running AMRFinderPlus on GCA_001558855.2 (Providencia stuartii)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001558855.2.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_001558855.2.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001558855.2"

echo "Running AMRFinderPlus on GCA_001577285.1 (Acinetobacter pittii)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001577285.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_001577285.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001577285.1"

echo "Running AMRFinderPlus on GCA_002949815.1 (Shigella dysenteriae)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_002949815.1.fna" --organism Escherichia --plus --threads 4 --output "$RESULTS_DIR/GCA_002949815.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_002949815.1"

echo "Running AMRFinderPlus on GCA_003047125.1 (Vibrio vulnificus)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_003047125.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_003047125.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_003047125.1"

echo "Running AMRFinderPlus on GCA_007632255.1 (Klebsiella aerogenes)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_007632255.1.fna" --organism Klebsiella --plus --threads 4 --output "$RESULTS_DIR/GCA_007632255.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_007632255.1"

echo "Running AMRFinderPlus on GCA_003955965.1 (Morganella morganii)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_003955965.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_003955965.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_003955965.1"

echo "Running AMRFinderPlus on GCA_000814165.3 (Acinetobacter nosocomialis)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_000814165.3.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_000814165.3.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_000814165.3"

echo "Running AMRFinderPlus on GCA_000975245.1 (Serratia liquefaciens)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_000975245.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_000975245.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_000975245.1"

echo "Running AMRFinderPlus on GCA_001514455.1 (Serratia fonticola)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001514455.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_001514455.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001514455.1"

echo "Running AMRFinderPlus on GCA_001679745.1 (Vibrio alginolyticus)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_001679745.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_001679745.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_001679745.1"

echo "Running AMRFinderPlus on GCA_002208845.2 (Citrobacter braakii)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_002208845.2.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_002208845.2.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_002208845.2"

echo "Running AMRFinderPlus on GCA_002216835.1 (Klebsiella michiganensis)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_002216835.1.fna" --organism Klebsiella --plus --threads 4 --output "$RESULTS_DIR/GCA_002216835.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_002216835.1"

echo "Running AMRFinderPlus on GCA_002249995.1 (Citrobacter farmeri)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_002249995.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_002249995.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_002249995.1"

echo "Running AMRFinderPlus on GCA_002843985.1 (Campylobacter coli)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_002843985.1.fna" --organism Campylobacter --plus --threads 4 --output "$RESULTS_DIR/GCA_002843985.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_002843985.1"

echo "Running AMRFinderPlus on GCA_002872455.1 (Escherichia albertii)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_002872455.1.fna" --organism Escherichia --plus --threads 4 --output "$RESULTS_DIR/GCA_002872455.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_002872455.1"

echo "Running AMRFinderPlus on GCA_003798165.1 (Raoultella ornithinolytica)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_003798165.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_003798165.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_003798165.1"

echo "Running AMRFinderPlus on GCA_003955925.1 (Cronobacter sakazakii)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_003955925.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_003955925.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_003955925.1"

echo "Running AMRFinderPlus on GCA_003990375.1 (Klebsiella quasipneumoniae)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_003990375.1.fna" --organism Klebsiella --plus --threads 4 --output "$RESULTS_DIR/GCA_003990375.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_003990375.1"

echo "Running AMRFinderPlus on GCA_006965505.1 (Citrobacter amalonaticus)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_006965505.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_006965505.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_006965505.1"

echo "Running AMRFinderPlus on GCA_900520355.1 (Acinetobacter calcoaceticus)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_900520355.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_900520355.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_900520355.1"

echo "Running AMRFinderPlus on GCA_900635475.1 (Kluyvera intermedia)"
conda run -n amrfinder amrfinder --nucleotide "$BASEDIR/data/assemblies/GCA_900635475.1.fna"  --plus --threads 4 --output "$RESULTS_DIR/GCA_900635475.1.tsv" 2>> "$RESULTS_DIR/amrfinder.log" || echo "FAILED: GCA_900635475.1"

echo "AMRFinderPlus completed for all genomes"
