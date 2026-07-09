#!/bin/bash
eval "$(/home/stevens/bin/micromamba shell hook -s bash)"
cd /data/stevens/bvbrc93-kpneu-st1588-independent
micromamba activate amr

# From AMRFinder: blaNDM-1 is at 308200-309009 on NZ_JAMJQY010000002.1 (+ strand)
# From AMRFinder: ble (bleMBL) is at 309016-309378 immediately downstream (+ strand)
# Get the region from ~305000 to ~315000 and around

python3 << 'PY'
seqs={}; name=None; buf=[]
for l in open('UCO361_all_contigs.fasta'):
    if l.startswith('>'):
        if name: seqs[name]=''.join(buf)
        name=l[1:].split()[0]; buf=[]
    else: buf.append(l.strip())
if name: seqs[name]=''.join(buf)
plasmid = seqs['NZ_JAMJQY010000002.1']
print(f"pNDM1_UCO361 length: {len(plasmid)} bp")
# Extract a 10kb window around blaNDM-1 (308200-309009)
w_start = max(0, 308200 - 5000)
w_end = min(len(plasmid), 309378 + 5000)
window = plasmid[w_start:w_end]
open('blaNDM_env_window.fasta','w').write(f">pNDM1_UCO361_blaNDM_env_{w_start}-{w_end}\n{window}\n")
print(f"Window: {w_start}-{w_end}  ({len(window)} bp)")
PY

# Extract every feature/CDS annotation in the plasmid GB file within the region 300000..315000
python3 << 'PY'
import re
gb = open('pNDM1_UCO361.gb').read()
# Parse features
# Simple regex approach for CDS/gene features
pattern = re.compile(r'^     (CDS|gene|misc_feature|mobile_element)\s+(complement\()?(?:<)?(\d+)\.\.(?:>)?(\d+)\)?', re.M)
records = []
for m in pattern.finditer(gb):
    feat = m.group(1); comp = bool(m.group(2)); s=int(m.group(3)); e=int(m.group(4))
    # grab the block starting at match till next feature (or ORIGIN)
    end_pos = gb.find('\n     ', m.end())
    while end_pos > 0:
        nxt_line = gb[end_pos+6:end_pos+30]
        # is this a new top-level feature? (starts with alpha, not with slash)
        stripped = nxt_line.lstrip()
        if stripped and stripped[0].isalpha() and gb[end_pos+6] != ' ':
            break
        end_pos = gb.find('\n     ', end_pos+1)
    block = gb[m.start():end_pos] if end_pos>0 else gb[m.start():m.start()+2000]
    prod = re.search(r'/product="([^"]+)"', block)
    gene = re.search(r'/gene="([^"]+)"', block)
    note = re.search(r'/note="([^"]+)"', block)
    mob = re.search(r'/mobile_element_type="([^"]+)"', block)
    records.append((s,e,comp,feat, (prod.group(1).replace('\n                     ',' ') if prod else ''),
                                    gene.group(1) if gene else '',
                                    note.group(1).replace('\n                     ',' ') if note else '',
                                    mob.group(1) if mob else ''))
# Filter to 300000..315000
records.sort()
print(f"\nFeatures within 300000..315000 on pNDM1_UCO361:\n")
print(f"{'start':>8} {'end':>8} {'str':>3} {'type':<15} {'gene':<10} {'product/note'}")
for s,e,c,ft,pr,g,n,mob in records:
    if s>=300000 and e<=315000:
        strand='-' if c else '+'
        info = pr or n or mob
        print(f"{s:>8} {e:>8} {strand:>3} {ft:<15} {g:<10} {info[:100]}")
PY
