#!/bin/bash
cd ~/Dropbox/REPLICATE-PROJECT/29769716-Mutant-phenotypes-bacterial-genes

BASE_URL="https://genomics.lbl.gov/supplemental/bigfit/html"

ORGS=(
  acidovorax_3H11 ANA3 azobra BFirm Cola Cup4G11 Dino Dyella79
  HerbieS Kang Korea Koxy Marino Miya Phaeo PS
  pseudo13_GW456_L13 pseudo1_N1B4 pseudo3_N2E3 pseudo5_N2C3_1
  pseudo6_N2E2 Pedo557 Ponti PV4 SB2B SynE WCS417
)

DATAFILES=(fit_genes.tab fit_logratios_good.tab fit_t.tab fit_quality.tab specific_phenotypes)

for org in "${ORGS[@]}"; do
    mkdir -p "data/${org}"
    for f in "${DATAFILES[@]}"; do
        dest="data/${org}/${f}"
        if [ -s "$dest" ]; then
            continue
        fi
        url="${BASE_URL}/${org}/${f}"
        wget -q -O "$dest" "$url" 2>/dev/null
        if [ $? -ne 0 ] || [ ! -s "$dest" ]; then
            curl -sS -f -L -o "$dest" "$url" 2>/dev/null
            if [ $? -ne 0 ] || [ ! -s "$dest" ]; then
                echo "FAILED: ${org}/${f}"
                rm -f "$dest"
            fi
        fi
    done
    fcount=$(ls "data/${org}/" 2>/dev/null | wc -l | tr -d ' ')
    fsize=$(du -sh "data/${org}/" 2>/dev/null | cut -f1)
    echo "DONE: ${org} (${fcount} files, ${fsize})"
done
