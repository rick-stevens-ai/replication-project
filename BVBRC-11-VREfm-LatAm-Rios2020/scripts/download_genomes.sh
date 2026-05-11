#!/bin/bash
# Download all 55 ERV genomes from NCBI
# Uses WGS accessions to find assembly accessions, then downloads via datasets
set -e

DATADIR=~/Dropbox/REPLICATE-PROJECT/BVBRC-11-VREfm-LatAm-Rios2020/data/genomes
ACCFILE=~/Dropbox/REPLICATE-PROJECT/BVBRC-11-VREfm-LatAm-Rios2020/data/erv_accessions.tsv
LOGFILE=~/Dropbox/REPLICATE-PROJECT/BVBRC-11-VREfm-LatAm-Rios2020/data/download_log.tsv
mkdir -p "$DATADIR"

echo -e "Strain\tWGS_Accession\tAssembly_Accession\tStatus" > "$LOGFILE"

# Read accessions (skip header)
tail -n +2 "$ACCFILE" | while IFS=$'\t' read -r strain wgs country year source st subclade; do
    echo "Processing $strain ($wgs)..."
    
    # Check if already downloaded
    if ls "$DATADIR"/${strain}*.fna 2>/dev/null | head -1 | grep -q .; then
        echo "  Already downloaded, skipping"
        echo -e "${strain}\t${wgs}\tALREADY_EXISTS\tskipped" >> "$LOGFILE"
        continue
    fi
    
    # Look up assembly accession from WGS
    wgs_prefix=$(echo "$wgs" | sed 's/[0-9]*$//')
    assembly_ids=$(curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=assembly&term=${wgs}" | grep '<Id>' | sed 's/.*<Id>\([0-9]*\)<\/Id>.*/\1/' | head -1)
    
    if [ -z "$assembly_ids" ]; then
        echo "  WARNING: No assembly found for $wgs"
        echo -e "${strain}\t${wgs}\tNOT_FOUND\tfailed" >> "$LOGFILE"
        continue
    fi
    
    # Get assembly accession
    assembly_acc=$(curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=assembly&id=${assembly_ids}" | grep 'AssemblyAccession' | head -1 | sed 's/.*>\(GC[AF]_[0-9.]*\)<.*/\1/')
    
    if [ -z "$assembly_acc" ]; then
        echo "  WARNING: Could not extract assembly accession for $wgs"
        echo -e "${strain}\t${wgs}\tPARSE_ERROR\tfailed" >> "$LOGFILE"
        continue
    fi
    
    echo "  Found assembly: $assembly_acc"
    
    # Download using datasets
    cd /tmp
    datasets download genome accession "$assembly_acc" --include genome 2>/dev/null || {
        echo "  WARNING: datasets download failed for $assembly_acc, trying GCA variant"
        gca_acc=$(echo "$assembly_acc" | sed 's/GCF/GCA/')
        datasets download genome accession "$gca_acc" --include genome 2>/dev/null || {
            echo "  FAILED: Could not download $strain"
            echo -e "${strain}\t${wgs}\t${assembly_acc}\tfailed" >> "$LOGFILE"
            continue
        }
        assembly_acc="$gca_acc"
    }
    
    # Extract
    unzip -o ncbi_dataset.zip -d ncbi_dataset_tmp 2>/dev/null
    fna_file=$(find ncbi_dataset_tmp -name "*.fna" | head -1)
    if [ -n "$fna_file" ]; then
        cp "$fna_file" "$DATADIR/${strain}.fna"
        echo "  Downloaded: ${strain}.fna"
        echo -e "${strain}\t${wgs}\t${assembly_acc}\tsuccess" >> "$LOGFILE"
    else
        echo "  WARNING: No .fna file found in download"
        echo -e "${strain}\t${wgs}\t${assembly_acc}\tno_fna" >> "$LOGFILE"
    fi
    
    rm -rf ncbi_dataset.zip ncbi_dataset_tmp
    
    # Rate limit
    sleep 0.5
done

echo ""
echo "=== Download Summary ==="
echo "Total: $(tail -n +2 "$LOGFILE" | wc -l)"
echo "Success: $(grep -c 'success' "$LOGFILE" || echo 0)"
echo "Failed: $(grep -c 'failed' "$LOGFILE" || echo 0)"
