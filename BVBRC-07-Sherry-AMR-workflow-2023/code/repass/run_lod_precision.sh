#!/usr/bin/env bash
# Re-pass 2026-06-23: Compute computational LOD (C15) and precision (C16)
# for the Sherry et al. 2023 AMR workflow paper.
#
# Pipeline per (genome, coverage [, seed]):
#   1) wgsim simulate paired-end 150bp reads at target coverage (no extra mutations)
#   2) spades.py --only-assembler --isolate (miniforge 'assembly' env, v4.0.0)
#   3) amrfinder -n -O <organism>  on resulting contigs.fasta
#   4) compare AMR (Type=AMR) gene set to pass-1 reference-with-organism call set
#
# Truth = AMRFinder 4.2.7 / DB 2026-03-24.1 on ORIGINAL reference assembly with -O.
# This isolates the LOD signal: same tool, same DB, same flags; only difference is
# read simulation + assembly upstream.
#
# All paths relative to repo root. Free compute only (CherryRd).

set -euo pipefail

REPO="/Users/stevens/Dropbox/REPLICATE-PROJECT/BVBRC-07-Sherry-AMR-workflow-2023"
cd "$REPO"

OUTDIR="$REPO/results/repass"
WORKDIR="$REPO/results/repass/work"
LOGDIR="$REPO/results/repass/logs"
TRUTHDIR="$REPO/results/repass/truth_with_org"
mkdir -p "$OUTDIR" "$WORKDIR" "$LOGDIR" "$TRUTHDIR"

AMRFINDER="/usr/local/Caskroom/miniforge/base/envs/amrfinder/bin/amrfinder"
SPADES="/usr/local/Caskroom/miniforge/base/envs/assembly/bin/spades.py"
WGSIM=$(command -v wgsim)
[ ! -x "$AMRFINDER" ] && { echo "ERROR: amrfinder missing at $AMRFINDER"; exit 2; }
[ ! -x "$SPADES" ] && { echo "ERROR: SPAdes missing at $SPADES"; exit 2; }
[ -z "$WGSIM" ] && { echo "ERROR: wgsim missing"; exit 2; }

# Test genomes: (accession, organism flag)
# Both small (~3 MB), AMR-rich, with AMRFinder --organism support
GENOMES=(
  "GCA_000145595.1:Staphylococcus_aureus"   # S. aureus JKD6008, 22+ AMR genes, mecA-positive
  "GCA_003020685.1:Enterococcus_faecium"    # E. faecium, ~19 AMR genes, vanA/B candidates
)

# Coverages to sweep (matches paper LOD range)
COVERAGES=(40 80 120 150)
PRECISION_SEEDS=(2 3)   # seed=1 from LOD sweep doubles as the 1st replicate

READLEN=150
FRAGMEAN=500
FRAGSD=50

calc_pairs() {
  local gsize="$1"; local cov="$2"
  python3 -c "import math; print(math.ceil($cov * $gsize / (2 * $READLEN)))"
}

ensure_truth() {
  local acc="$1"; local org="$2"
  local truth="$TRUTHDIR/${acc}.tsv"
  if [ -f "$truth" ]; then return 0; fi
  echo "[truth] $acc with -O $org" >&2
  "$AMRFINDER" -n "$REPO/data/assemblies/${acc}.fna" \
    -o "$truth" -O "$org" --threads 4 \
    >> "$LOGDIR/truth_${acc}.log" 2>&1
}

run_one() {
  local acc="$1"; local org="$2"; local cov="$3"; local seed="$4"
  local tag="${acc}_cov${cov}_seed${seed}"
  local refasm="$REPO/data/assemblies/${acc}.fna"
  local work="$WORKDIR/${tag}"
  local log="$LOGDIR/${tag}.log"
  local final_tsv="$OUTDIR/amrfinder_${tag}.tsv"

  if [ -f "$final_tsv" ]; then
    echo "[$(date +%H:%M:%S)] SKIP $tag (already done)"
    return 0
  fi

  echo "[$(date +%H:%M:%S)] START $tag" | tee "$log"
  mkdir -p "$work"

  local gsize
  gsize=$(awk '/^>/{next} {n+=length($0)} END{print n}' "$refasm")
  local npairs
  npairs=$(calc_pairs "$gsize" "$cov")
  echo "  gsize=${gsize}bp  cov=${cov}X  pairs=${npairs}  organism=${org}" | tee -a "$log"

  # 1) Simulate reads (no extra mutations, only sequencing error)
  echo "  [wgsim] simulating..." | tee -a "$log"
  $WGSIM -1 $READLEN -2 $READLEN -d $FRAGMEAN -s $FRAGSD -N "$npairs" -S "$seed" \
    -e 0.005 -r 0.0 -R 0 -X 0 \
    "$refasm" "$work/r1.fq" "$work/r2.fq" >> "$log" 2>&1

  # 2) Assemble
  echo "  [spades] assembling..." | tee -a "$log"
  rm -rf "$work/spades"
  local t0=$(date +%s)
  if ! "$SPADES" --only-assembler --isolate -t 4 \
      -1 "$work/r1.fq" -2 "$work/r2.fq" \
      -o "$work/spades" >> "$log" 2>&1; then
    echo "  SPADES FAILED for $tag" | tee -a "$log"
    return 1
  fi
  echo "  spades took $(( $(date +%s) - t0 ))s" | tee -a "$log"

  local asm="$work/spades/contigs.fasta"
  [ ! -f "$asm" ] && { echo "  no contigs for $tag" | tee -a "$log"; return 1; }

  # 3) AMRFinder with organism
  echo "  [amrfinder] calling with -O ${org}..." | tee -a "$log"
  if ! "$AMRFINDER" -n "$asm" -o "$final_tsv" -O "$org" --threads 4 >> "$log" 2>&1; then
    echo "  AMRFINDER FAILED for $tag" | tee -a "$log"
    return 1
  fi

  # Cleanup heavy artifacts
  rm -rf "$work/spades" "$work/r1.fq" "$work/r2.fq"

  echo "[$(date +%H:%M:%S)] DONE  $tag  (hits=$(($(wc -l < $final_tsv) - 1)))" | tee -a "$log"
}

echo "=== Step 0: ensure truth-with-organism call sets ==="
for entry in "${GENOMES[@]}"; do
  acc="${entry%%:*}"; org="${entry##*:}"
  ensure_truth "$acc" "$org"
done

echo "=== Phase A: LOD sweep (40X, 80X, 120X, 150X) at seed=1 ==="
for entry in "${GENOMES[@]}"; do
  acc="${entry%%:*}"; org="${entry##*:}"
  for cov in "${COVERAGES[@]}"; do
    run_one "$acc" "$org" "$cov" 1 || echo "FAILED $acc cov=$cov seed=1"
  done
done

echo "=== Phase B: Precision replicates at 80X (seeds 2,3) ==="
for entry in "${GENOMES[@]}"; do
  acc="${entry%%:*}"; org="${entry##*:}"
  for seed in "${PRECISION_SEEDS[@]}"; do
    run_one "$acc" "$org" 80 "$seed" || echo "FAILED $acc cov=80 seed=$seed"
  done
done

echo "=== Phase C: Summarize ==="
python3 "$REPO/code/repass/summarize_repass.py"

echo "Re-pass complete."
