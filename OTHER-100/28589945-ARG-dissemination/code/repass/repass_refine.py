#!/usr/bin/env python3
"""Refinement pass: fix C8 with real actinobacterial cmx homologs, retry C5 with better strain search."""
import json, time, urllib.parse, urllib.request, subprocess, shutil, tempfile, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / 'results' / 'repass'
EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'
SLEEP = 1.0

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

def esearch(db, term, retmax=20):
    j = get(f'{EUTILS}/esearch.fcgi?db={db}&term={urllib.parse.quote(term)}&retmode=json&retmax={retmax}')
    if not j: return [], 0
    try:
        d = json.loads(j)
        return d['esearchresult'].get('idlist', []), int(d['esearchresult'].get('count', 0))
    except Exception:
        return [], 0

def efetch_fasta(uid):
    return get(f'{EUTILS}/efetch.fcgi?db=protein&id={uid}&rettype=fasta&retmode=text')

def cache_get(acc):
    d = RESULTS / 'seqs'; d.mkdir(exist_ok=True)
    fp = d / f'{acc}.fa'
    if fp.exists() and fp.stat().st_size > 0:
        return fp.read_text()
    ids, _ = esearch('protein', acc, retmax=1)
    if not ids: return None
    txt = efetch_fasta(ids[0])
    time.sleep(SLEEP)
    if txt and txt.startswith('>'):
        fp.write_text(txt); return txt
    return None

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

def write_json(name, obj):
    p = RESULTS / name
    p.write_text(json.dumps(obj, indent=2, default=str))
    log(f'[wrote] {p.relative_to(ROOT)}')

# ---------- C8 refined: real cmx homologs
def refine_C8():
    log('C8 refine: search "chloramphenicol exporter cmx" within Corynebacterium / Arthrobacter / Microbacterium')
    cmx_q = cache_get('WP_005297378.1')
    if not cmx_q:
        write_json('C8_cmx_99pct_actino.json', {'error': 'query_fetch_failed'})
        return
    actino_terms = [
        ('Corynebacterium', 'chloramphenicol exporter Corynebacterium NOT diphtheriae'),
        ('Arthrobacter',    'chloramphenicol exporter Arthrobacter'),
        ('Microbacterium',  'chloramphenicol exporter Microbacterium'),
        ('Paenarthrobacter','chloramphenicol exporter Paenarthrobacter'),
        ('Mycobacterium',   'chloramphenicol exporter Mycobacterium'),
    ]
    pairs = []
    for gen, term in actino_terms:
        ids, total = esearch('protein', term, retmax=5)
        time.sleep(SLEEP)
        log(f'  {gen}: {total} hits')
        best = None
        for uid in ids[:5]:
            fa = efetch_fasta(uid); time.sleep(SLEEP)
            if not fa or not fa.startswith('>'): continue
            defline = fa.splitlines()[0]
            if gen.lower() not in defline.lower(): continue
            b = blastp(cmx_q, fa)
            if b and (best is None or b['pident'] > best['blastp']['pident']):
                best = {'subject_uid': uid, 'subject_defline': defline, 'blastp': b}
        pairs.append({'genus': gen, 'best_hit': best})
    # Top identity
    any99 = False; top = None
    for p in pairs:
        if p.get('best_hit') and p['best_hit'].get('blastp'):
            pid = p['best_hit']['blastp']['pident']
            if pid >= 99.0: any99 = True
            if top is None or pid > top['blastp']['pident']:
                top = p['best_hit'] | {'genus': p['genus']}
    out = {
        'query_acc': 'WP_005297378.1 (proteobacterial Cmx)',
        'paper_claim': '>99% identity to non-Streptomyces actinobacterial cmx genes',
        'per_genus_top_hit': pairs,
        'top_overall': top,
        'any_subject_at_99pct': any99,
    }
    write_json('C8_cmx_99pct_actino.json', out)

# ---------- C5 refined: try more search variants
def refine_C5():
    log('C5 refine: Arthrobacter sp. 161MFSha2.1 + Corynebacterium glutamicum 1014 cmx')
    seqs = {}; log_entries = []
    # Strategy A: search assembly DB / nuccore for the strain and dig genes
    for tag, queries in [
        ('Arthrobacter_161MFSha21', [
            'Arthrobacter sp. 161MFSha2.1[ORGN]',
            'Arthrobacter 161MFSha2 chloramphenicol',
            '161MFSha2.1 cmx',
            '161MFSha2',
        ]),
        ('C_glutamicum_1014', [
            'Corynebacterium glutamicum 1014',
            'Corynebacterium glutamicum strain 1014',
            'Corynebacterium glutamicum 1014 cmx tnp45',
            'Corynebacterium glutamicum 1014 chloramphenicol exporter',
        ]),
    ]:
        chosen = None
        for q in queries:
            ids, total = esearch('protein', q, retmax=10); time.sleep(SLEEP)
            log_entries.append({'tag': tag, 'term': q, 'n_hits': total})
            log(f'  {tag}: {q!r} -> {total} hits')
            for uid in ids[:5]:
                fa = efetch_fasta(uid); time.sleep(SLEEP)
                if not fa: continue
                d = fa.splitlines()[0].lower()
                if ('chloramphenicol' in d or 'cmx' in d) and ('mfsha' in d or 'glutamicum' in d):
                    chosen = {'uid': uid, 'defline': fa.splitlines()[0], 'term': q}
                    seqs[tag] = fa
                    break
            if chosen: break
        if not chosen:
            # also try nuccore-based gene lookup
            ids, _ = esearch('nuccore', queries[0], retmax=5); time.sleep(SLEEP)
            log(f'  {tag}: nuccore fallback -> {len(ids)}')
            log_entries.append({'tag': tag, 'nuccore_fallback': ids})
    out = {
        'paper_claim': 'C. glutamicum 1014 cmx vs Arthrobacter sp. 161MFSha2.1 cmx = 93% identical',
        'search_log': log_entries,
        'seqs_found': list(seqs.keys()),
    }
    if len(seqs) == 2:
        b = blastp(seqs['C_glutamicum_1014'], seqs['Arthrobacter_161MFSha21'])
        out['blastp_result'] = b
        if b:
            out['delta_from_paper'] = b['pident'] - 93.0
            out['matches_paper'] = abs(b['pident'] - 93.0) <= 5.0
    else:
        out['blocker'] = (
            f'Could not find cmx protein record for strains: missing={set(["Arthrobacter_161MFSha21","C_glutamicum_1014"]) - set(seqs.keys())}. '
            'These specific strain-level cmx accessions appear not to be indexed under the strain '
            'designations used in the paper (the paper cites Supplementary Fig. 7, which would have '
            'the exact accessions used in the original alignment).'
        )
    write_json('C5_glutamicum_vs_arthrobacter.json', out)

if __name__ == '__main__':
    refine_C8()
    refine_C5()
