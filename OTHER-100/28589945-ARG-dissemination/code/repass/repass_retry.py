#!/usr/bin/env python3
"""Retry the rate-limited claim queries with longer sleeps + smarter terms."""
import json, time, urllib.parse, urllib.request, subprocess, shutil, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / 'results' / 'repass'
EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'
SLEEP = 1.2   # well under 3/sec; safer than 0.34

def log(m): print(f'[{time.strftime("%H:%M:%S")}] {m}', flush=True)

def get(url, timeout=30, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return r.read().decode()
        except Exception as e:
            log(f'  attempt {i+1}: {e}')
            time.sleep(SLEEP * (i+1) * 2)
    return None

def esearch(db, term, retmax=10):
    url = f'{EUTILS}/esearch.fcgi?db={db}&term={urllib.parse.quote(term)}&retmode=json&retmax={retmax}'
    j = get(url)
    if not j: return [], 0
    try:
        d = json.loads(j)
        return d['esearchresult'].get('idlist', []), int(d['esearchresult'].get('count', 0))
    except Exception:
        return [], 0

def esummary(db, uid):
    j = get(f'{EUTILS}/esummary.fcgi?db={db}&id={uid}&retmode=json')
    if not j: return None
    try:
        return json.loads(j)['result'][uid]
    except Exception:
        return None

def efetch_fasta(uid):
    return get(f'{EUTILS}/efetch.fcgi?db=protein&id={uid}&rettype=fasta&retmode=text')

def blastp(qfa, sfa):
    bp = shutil.which('blastp')
    if not bp: return None
    with tempfile.TemporaryDirectory() as td:
        q = Path(td) / 'q.fa'; q.write_text(qfa)
        s = Path(td) / 's.fa'; s.write_text(sfa)
        r = subprocess.run([bp,'-query',str(q),'-subject',str(s),
                            '-outfmt','6 pident qcovhsp evalue length nident'],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0 or not r.stdout.strip(): return None
        f = r.stdout.strip().splitlines()[0].split('\t')
        return {'pident': float(f[0]), 'qcovhsp': float(f[1]),
                'evalue': float(f[2]), 'length': int(f[3]), 'nident': int(f[4])}

def cache_get(acc):
    d = RESULTS / 'seqs'; d.mkdir(exist_ok=True)
    fp = d / f'{acc}.fa'
    if fp.exists() and fp.stat().st_size > 0:
        return fp.read_text()
    # search to get UID then efetch
    ids, _ = esearch('protein', acc, retmax=1)
    if not ids: return None
    txt = efetch_fasta(ids[0])
    time.sleep(SLEEP)
    if txt and txt.startswith('>'):
        fp.write_text(txt); return txt
    return None

def write_json(name, obj):
    p = RESULTS / name
    p.write_text(json.dumps(obj, indent=2, default=str))
    log(f'[wrote] {p.relative_to(ROOT)}')

# --------- C5 retry: C. glutamicum 1014 vs Arthrobacter 161MFSha2.1 cmx
def retry_C5():
    log('C5 retry: C. glutamicum 1014 cmx & Arthrobacter sp. 161MFSha2.1 cmx')
    candidates = [
        ('C_glutamicum_1014_cmx', [
            'Corynebacterium glutamicum 1014[ORGN] AND chloramphenicol',
            'Corynebacterium glutamicum AND cmx AND chloramphenicol exporter',
            'Corynebacterium glutamicum AND chloramphenicol resistance',
        ]),
        ('Arthrobacter_161MFSha21_cmx', [
            'Arthrobacter 161MFSha2 AND chloramphenicol',
            'Arthrobacter sp. 161MFSha2.1 AND chloramphenicol',
            'Arthrobacter AND cmx chloramphenicol exporter',
        ]),
    ]
    seqs = {}
    summary = {'paper_claim_identity_pct': 93, 'queries': []}
    for tag, terms in candidates:
        chosen_seq = None; chosen_meta = None
        for term in terms:
            ids, total = esearch('protein', term, retmax=10)
            time.sleep(SLEEP)
            log(f'  {tag}: term={term!r} -> {total} hits')
            # fetch deflines and pick best match
            for uid in ids[:5]:
                fa = efetch_fasta(uid)
                time.sleep(SLEEP)
                if not fa or not fa.startswith('>'): continue
                d = fa.splitlines()[0].lower()
                want = (tag.split('_')[0].lower() in d) or ('161mfsha' in d) or (tag.startswith('C_glut') and 'glutamicum' in d)
                if 'chloramphenicol' in d or 'cmx' in d:
                    chosen_seq = fa; chosen_meta = {'uid': uid, 'term': term, 'defline': fa.splitlines()[0]}
                    if want: break
            if chosen_seq and (chosen_meta.get('defline','').lower().find('161mfsha')>=0 or 'glutamicum' in chosen_meta.get('defline','').lower()):
                break
        summary['queries'].append({'tag': tag, 'chosen': chosen_meta})
        if chosen_seq: seqs[tag] = chosen_seq
    if len(seqs) == 2:
        b = blastp(seqs['C_glutamicum_1014_cmx'], seqs['Arthrobacter_161MFSha21_cmx'])
        summary['blastp_result'] = b
        if b:
            summary['delta_from_paper'] = b['pident'] - 93.0
            summary['matches_paper'] = abs(b['pident'] - 93.0) <= 5.0
    else:
        summary['blocker'] = 'could not retrieve cmx from one or both named strains'
    write_json('C5_glutamicum_vs_arthrobacter.json', summary)

# --------- C14 retry: cmx+tnp45 distribution
def retry_C14():
    log('C14 retry: cmx+tnp45 distribution')
    ids, total = esearch('nuccore', 'cmx+AND+tnp45', retmax=50)
    log(f'  total hits: {total}, sampled: {len(ids)}')
    ACTINO = {'streptomyces','corynebacterium','arthrobacter','mycobacterium','microbacterium',
              'rhodococcus','nocardia','actinomyces','paenarthrobacter','curtobacterium',
              'gordonia','tsukamurella','dietzia'}
    PROTEO = {'pseudomonas','escherichia','klebsiella','enterobacter','acinetobacter',
              'salmonella','vibrio','burkholderia','aeromonas','citrobacter','proteus','serratia',
              'shigella','providencia','morganella'}
    actino_gen=set(); proteo_gen=set(); other=set(); docs=[]
    for uid in ids[:40]:
        d = esummary('nuccore', uid)
        time.sleep(SLEEP)
        if not d: continue
        org = (d.get('organism') or '').lower()
        gen = org.split()[0] if org else ''
        docs.append({'uid': uid, 'organism': d.get('organism'), 'title': (d.get('title') or '')[:120]})
        if gen in ACTINO: actino_gen.add(gen)
        elif gen in PROTEO: proteo_gen.add(gen)
        elif gen: other.add(gen)
    out = {
        'paper_claim': 'intact cmx+tnp45 transposon found in both actinobacteria and proteobacteria',
        'total_nuccore_hits': total,
        'sampled_n': len(docs),
        'actino_genera_with_cmx_tnp45': sorted(actino_gen),
        'proteo_genera_with_cmx_tnp45': sorted(proteo_gen),
        'other_genera_with_cmx_tnp45': sorted(other),
        'both_phyla_present': bool(actino_gen) and bool(proteo_gen),
        'docs_sample': docs[:20],
    }
    write_json('C14_cmx_tnp45_distribution.json', out)

# --------- C12 retry: LmrA full sample
def retry_C12():
    log('C12 retry: LmrA WP_038989331.1 carrier')
    # Get protein UID, then elink to nuccore
    ids, _ = esearch('protein', 'WP_038989331.1', retmax=1)
    time.sleep(SLEEP)
    if not ids:
        write_json('C12_lmra_rsf1010.json', {'error': 'protein_uid_not_found'})
        return
    puid = ids[0]
    link = get(f'{EUTILS}/elink.fcgi?dbfrom=protein&db=nuccore&id={puid}&retmode=json')
    time.sleep(SLEEP)
    nucs = []
    if link:
        try:
            j = json.loads(link)
            for ls in j.get('linksets', []):
                for ldb in ls.get('linksetdbs', []):
                    if 'nuccore' in ldb.get('linkname',''):
                        nucs.extend(ldb.get('links', []))
        except Exception: pass
    nucs = list(dict.fromkeys(nucs))
    log(f'  linked nuccore: {len(nucs)}')
    sampled = []; plasmid_hits = 0; rsf_hits = 0
    for uid in nucs[:15]:
        d = esummary('nuccore', uid)
        time.sleep(SLEEP)
        if not d: continue
        title = d.get('title') or ''
        sampled.append({'uid': uid, 'title': title[:160], 'organism': d.get('organism')})
        tl = title.lower()
        if 'plasmid' in tl: plasmid_hits += 1
        if 'rsf1010' in tl or 'rsf 1010' in tl or 'incq' in tl: rsf_hits += 1
    out = {
        'paper_claim': 'WP_038989331.1 (LmrA) located on an RSF1010-like plasmid',
        'linked_nuccore_total': len(nucs),
        'sampled_meta': sampled,
        'sampled_n': len(sampled),
        'plasmid_titles_in_sample': plasmid_hits,
        'rsf1010_or_incq_titles_in_sample': rsf_hits,
        'plasmid_evidence': plasmid_hits > 0,
        'rsf1010_evidence_loose': rsf_hits > 0,
        'note': ('Titles rarely state "RSF1010" explicitly; many IncQ-family plasmids fit the '
                 '"RSF1010-like" description. We flag a hit if title contains rsf1010 or incq.'),
    }
    write_json('C12_lmra_rsf1010.json', out)

# --------- C9 retry: broader cmx+tnp45 colocation
def retry_C9():
    log('C9 retry: cmx+tnp45 colocation')
    # Try also 'tnp45 chloramphenicol' as fallback
    ids, total = esearch('nuccore', 'tnp45 AND chloramphenicol', retmax=20)
    log(f'  tnp45+chloramphenicol: {total} hits')
    if not ids:
        ids, total = esearch('nuccore', 'tnp45', retmax=20)
        log(f'  tnp45 alone: {total} hits')
    out = {
        'paper_claim': 'cmx is colocalized with actinobacterial transposase gene tnp45',
        'ncbi_nuccore_total_hits': total,
        'sampled_ids': ids[:10],
    }
    if ids:
        gb = get(f'{EUTILS}/efetch.fcgi?db=nuccore&id={ids[0]}&rettype=gb&retmode=text')
        time.sleep(SLEEP)
        if gb:
            (RESULTS / 'sample_cmx_tnp45.gb').write_text(gb)
            import re
            cmx_pos = []; tnp_pos = []
            lines = gb.splitlines()
            for i, l in enumerate(lines):
                low = l.lower()
                if 'cmx' in low or 'chloramphenicol' in low:
                    for j in range(i, max(0,i-10), -1):
                        ls = lines[j].lstrip()
                        if ls.startswith(('CDS ','gene ','mobile_element')):
                            mm = re.search(r'(\d+)\.\.(\d+)', lines[j])
                            if mm: cmx_pos.append((int(mm.group(1)), int(mm.group(2)))); break
                if 'tnp45' in low:
                    for j in range(i, max(0,i-10), -1):
                        ls = lines[j].lstrip()
                        if ls.startswith(('CDS ','gene ','mobile_element')):
                            mm = re.search(r'(\d+)\.\.(\d+)', lines[j])
                            if mm: tnp_pos.append((int(mm.group(1)), int(mm.group(2)))); break
            dist = None
            if cmx_pos and tnp_pos:
                dist = min(abs((c[0]+c[1])//2 - (t[0]+t[1])//2) for c in cmx_pos for t in tnp_pos)
            out['sample_locus'] = lines[0][:120] if lines else None
            out['cmx_features_found'] = len(cmx_pos)
            out['tnp45_features_found'] = len(tnp_pos)
            out['cmx_tnp45_min_distance_bp'] = dist
            out['colocated_within_5kb'] = bool(dist is not None and dist <= 5000)
    write_json('C9_cmx_tnp45_synteny.json', out)

if __name__ == '__main__':
    retry_C5()
    retry_C12()
    retry_C14()
    retry_C9()
