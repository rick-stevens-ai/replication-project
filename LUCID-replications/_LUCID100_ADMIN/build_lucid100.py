#!/usr/bin/env python3
"""Build a LUCID top-100 replication campaign seed from Dropbox corpus + Semantic Scholar search."""
from __future__ import annotations
from pathlib import Path
import csv, hashlib, json, os, re, subprocess, sys, time, urllib.parse, urllib.request
from collections import Counter, defaultdict
from zipfile import ZipFile
import xml.etree.ElementTree as ET

OUT = Path('/Users/stevens/.openclaw/workspace/lucid-replications')
DROP = Path.home()/'Dropbox'
XFER = DROP/'XFER/LUCID-replication-targets'
PRIOR = DROP/'REPLICATE-PROJECT/LUCID-replications'
OUT.mkdir(parents=True, exist_ok=True)
CACHE = OUT/'s2_cache'
CACHE.mkdir(exist_ok=True)

DOI_RE = re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.I)
URL_RE = re.compile(r'https?://\S+', re.I)

THEMES = {
    'DNA repair / DDR': ['dna repair','double-strand','dsb','nhej','homologous recombination','53bp1','gamma-h2ax','h2ax','atm','atr','dna-pk','p53','chromatin'],
    'dose-rate / low-dose response': ['low dose','low-dose','dose-rate','dose rate','chronic','ldr','hormesis','adaptive response','bystander'],
    'radiation quality / RBE': ['rbe','relative biological effectiveness','let','high-let','carbon ion','alpha','proton','neutron','actinium','lutetium','boron neutron'],
    'omics / biomarkers / signatures': ['rna-seq','transcript','gene expression','methylation','epigen','omics','biomarker','signature','mutational signature'],
    'immune / inflammation / senescence': ['immune','inflammation','sting','cgas','senescence','nf-kb','cox-2','immunogenic','microbiota'],
    'microbial / extremophile': ['microbial','bacteria','yeast','fungi','deinococcus','e. coli','escherichia','radiodurans','melanin'],
    'computational model / simulation': ['model','simulation','monte carlo','geant4','topas','ode','stochastic','agent-based','mechanistic','kinetic'],
}
REPL_WORDS = ['github','zenodo','figshare','supplement','data availability','code availability','model','equation','parameter','table','simulation','repository','source code']
NO_GO_WORDS = ['review','narrative review','perspective','editorial','commentary']

# Existing completed/triaged papers by DOI/file/title from current artifacts
completed_slugs=set()
completed_titles=[]
completed_dois=set()
if PRIOR.exists():
    for d in PRIOR.iterdir():
        if d.is_dir() and d.name.startswith('lucid-'):
            completed_slugs.add(d.name)
            for f in [d/'REPORT.md', d/'NO-GO-REPORT.md', d/'README.md']:
                if f.exists():
                    txt=f.read_text(errors='ignore')[:20000]
                    completed_titles.append((d.name, txt[:1000]))
                    completed_dois.update(x.rstrip('.,;)') for x in DOI_RE.findall(txt))


def clean_doi(s):
    return s.rstrip('.,;:)\]}>').lower()

def sha1_file(p: Path):
    h=hashlib.sha1()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1<<20), b''):
            h.update(b)
    return h.hexdigest()

def pdftotext(p: Path, timeout=25):
    try:
        r=subprocess.run(['pdftotext', str(p), '-'], capture_output=True, text=True, timeout=timeout)
        return r.stdout or ''
    except Exception:
        return ''

def docx_text(p: Path):
    try:
        with ZipFile(p) as z:
            names=[n for n in z.namelist() if n.startswith('word/') and n.endswith('.xml')]
            texts=[]
            for n in names:
                try:
                    root=ET.fromstring(z.read(n))
                    for el in root.iter():
                        if el.tag.endswith('}t') and el.text:
                            texts.append(el.text)
                except Exception: pass
            return ' '.join(texts)
    except Exception:
        return ''

def pptx_text(p: Path):
    try:
        with ZipFile(p) as z:
            names=[n for n in z.namelist() if n.startswith('ppt/slides/') and n.endswith('.xml')]
            texts=[]
            for n in names:
                try:
                    root=ET.fromstring(z.read(n))
                    for el in root.iter():
                        if el.tag.endswith('}t') and el.text:
                            texts.append(el.text)
                except Exception: pass
            return '\n'.join(texts)
    except Exception:
        return ''

def title_guess_from_text(txt):
    for line in txt.splitlines()[:80]:
        l=' '.join(line.strip().split())
        if len(l) < 18: continue
        low=l.lower()
        if any(x in low for x in ['downloaded from','copyright','bioone complete','for personal use only','www.','doi.org','citation:','received:','published:','open access']):
            continue
        return l[:260]
    return ''

def score_item(title, abstract, sample, has_pdf=False, source=''):
    text=' '.join([title or '', abstract or '', sample or '']).lower()
    score=0
    theme_hits=[]
    for theme, kws in THEMES.items():
        if any(k in text for k in kws):
            theme_hits.append(theme); score += 2
    if any(k in text for k in REPL_WORDS): score += 3
    if has_pdf: score += 2
    if source == 'dropbox_pdf': score += 3
    if source == 'lucid_reference': score += 1
    if any(k in text for k in NO_GO_WORDS): score -= 4
    # Low-dose biology campaign focus boost
    if any(k in text for k in ['low dose','low-dose','dose-rate','chronic low','low-let','ionizing radiation']): score += 3
    if any(k in text for k in ['dna repair','double-strand','dsb','gamma-h2ax','53bp1','p53']): score += 2
    if any(k in text for k in ['model','simulation','monte carlo','ode','stochastic','mechanistic']): score += 2
    score=max(0, min(20, score))
    tier='A' if score>=14 else ('B' if score>=9 else 'C')
    return score, tier, '; '.join(theme_hits[:4])

def s2_get(url, timeout=20):
    key=os.environ.get('S2_API_KEY')
    # also try macOS keychain once
    if not key:
        try:
            r=subprocess.run(['security','find-generic-password','-a','rick-stevens-ai','-s','semantic-scholar-api-key','-w'], capture_output=True, text=True, timeout=5)
            if r.returncode==0: key=r.stdout.strip()
        except Exception: pass
    req=urllib.request.Request(url, headers={'User-Agent':'Ollie-LUCID-replication-planner/1.0'})
    if key: req.add_header('x-api-key', key)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))

def s2_search(query, limit=10):
    fields='title,year,authors,venue,externalIds,url,abstract,citationCount,isOpenAccess,openAccessPdf,fieldsOfStudy,publicationTypes'
    q=urllib.parse.urlencode({'query':query, 'limit':limit, 'fields':fields})
    cache=CACHE/(hashlib.sha1((query+str(limit)).encode()).hexdigest()+'.json')
    if cache.exists():
        return json.loads(cache.read_text())
    url=f'https://api.semanticscholar.org/graph/v1/paper/search?{q}'
    try:
        data=s2_get(url)
        cache.write_text(json.dumps(data, indent=2))
        time.sleep(0.25)
        return data
    except Exception as e:
        return {'error':str(e), 'data':[]}

def s2_paper_by_doi(doi):
    fields='title,year,authors,venue,externalIds,url,abstract,citationCount,isOpenAccess,openAccessPdf,fieldsOfStudy,publicationTypes'
    did=doi.replace('/','_')
    cache=CACHE/(f'doi_{hashlib.sha1(doi.encode()).hexdigest()}.json')
    if cache.exists(): return json.loads(cache.read_text())
    url='https://api.semanticscholar.org/graph/v1/paper/DOI:'+urllib.parse.quote(doi, safe='')+'?fields='+urllib.parse.quote(fields)
    try:
        data=s2_get(url)
        cache.write_text(json.dumps(data, indent=2)); time.sleep(0.25); return data
    except Exception as e:
        return {'error':str(e)}

candidates={}
def add_candidate(key, **kw):
    if not key: return
    key=key.lower()
    cur=candidates.get(key, {})
    # merge preferentially non-empty/larger text
    for k,v in kw.items():
        if v in (None,'',[]): continue
        if k not in cur or not cur[k] or (isinstance(v,str) and len(v)>len(str(cur.get(k,'')))):
            cur[k]=v
    cur.setdefault('sources',[])
    if kw.get('source') and kw.get('source') not in cur['sources']:
        cur['sources'].append(kw.get('source'))
    candidates[key]=cur

# 1) Dropbox PDFs: XFER targets and LUCID/radiation PDFs.
pdfs=[]
if XFER.exists(): pdfs += list(XFER.glob('*.pdf'))
if PRIOR.exists(): pdfs += list(PRIOR.rglob('*.pdf'))
for p in DROP.glob('*.pdf'):
    n=p.name.lower()
    if any(k in n for k in ['lucid','radiation','dose','h2ax']): pdfs.append(p)
seen_hash=set()
for p in pdfs:
    try: sh=sha1_file(p)
    except Exception: continue
    if sh in seen_hash: continue
    seen_hash.add(sh)
    txt=pdftotext(p)
    dois=[clean_doi(x) for x in DOI_RE.findall(txt)]
    doi=dois[0] if dois else ''
    title=title_guess_from_text(txt)
    sample=' '.join(txt.split())[:1600]
    key='doi:'+doi if doi else 'file:'+sh
    add_candidate(key, doi=doi, title=title, sample=sample, pdf_path=str(p), sha1=sh, source='dropbox_pdf')

# 2) LUCID docs/docx/pptx/pdf references / URLs
lucid_docs=[]
for p in DROP.glob('*'):
    if p.is_file() and p.suffix.lower() in ['.pdf','.docx','.pptx','.rtf','.txt','.md']:
        n=p.name.lower()
        if any(k in n for k in ['lucid','low_dose','low-dose','radiation biology','radiation_mechanisms','chronic low']):
            lucid_docs.append(p)
if (DROP/'LUCID2').exists():
    lucid_docs += [p for p in (DROP/'LUCID2').rglob('*') if p.is_file() and p.suffix.lower() in ['.html','.txt','.docx','.pdf']]
for p in lucid_docs:
    suf=p.suffix.lower()
    if suf=='.pdf': txt=pdftotext(p)
    elif suf=='.docx': txt=docx_text(p)
    elif suf=='.pptx': txt=pptx_text(p)
    else:
        try: txt=p.read_text(errors='ignore')
        except Exception: txt=''
    for doi in DOI_RE.findall(txt):
        doi=clean_doi(doi)
        add_candidate('doi:'+doi, doi=doi, source='lucid_reference', sample='from '+str(p))
    # capture URL-title pairs from generated reference sections
    lines=[l.strip() for l in txt.splitlines() if l.strip()]
    for i,l in enumerate(lines):
        if l.startswith('http'):
            url=l.split()[0].rstrip('.,)')
            title=''
            # previous non-numeric line
            for j in range(i-1, max(-1,i-5), -1):
                if not lines[j].isdigit() and len(lines[j])>12 and not lines[j].startswith('http'):
                    title=lines[j]; break
            if title:
                key='url:'+url.lower()
                doi_match=DOI_RE.search(url)
                add_candidate(key, title=title[:260], url=url, doi=clean_doi(doi_match.group(0)) if doi_match else '', source='lucid_reference')

# 3) Semantic Scholar themed searches to fill/expand to >=100.
queries = [
    'low dose ionizing radiation biology DNA repair dose rate gene expression',
    'chronic low dose rate gamma irradiation gene expression DNA repair',
    'low dose radiation adaptive response hormesis DNA damage repair',
    'low dose ionizing radiation transcriptomic signature biomarker',
    'radiation induced DNA double strand break repair gamma H2AX low dose',
    '53BP1 repair kinetics radiation susceptibility low dose',
    'radiation dose rate relative biological effectiveness DNA repair model',
    'mechanistic model radiation induced DNA damage repair cell survival',
    'stochastic model DNA double strand break repair radiation',
    'Geant4-DNA TOPAS-nBio cell survival DNA damage repair model',
    'low LET high LET radiation RBE DNA repair p53 apoptosis',
    'cGAS STING ionizing radiation DNA damage response low dose',
    'radiation induced senescence DNA damage low dose',
    'microbial chronic low dose ionizing radiation gene expression Escherichia coli',
    'Deinococcus radiodurans chronic ionizing radiation DNA repair proteome',
    'yeast chronic low dose ionizing radiation adaptive evolution DNA repair',
    'radiation mutational signatures ionizing radiation low dose',
    'bystander effects low dose ionizing radiation DNA damage repair',
    'radiation epigenetic methylation low dose exposure DNA repair',
    'space radiation low dose rate biology DNA repair transcriptomics',
]
for q in queries:
    data=s2_search(q, limit=12)
    for item in data.get('data') or []:
        ext=item.get('externalIds') or {}
        doi=clean_doi(ext.get('DOI','')) if ext.get('DOI') else ''
        title=item.get('title') or ''
        if not title: continue
        key='doi:'+doi if doi else 's2:'+item.get('paperId','')
        add_candidate(key, doi=doi, title=title, year=item.get('year'), venue=item.get('venue'), abstract=item.get('abstract') or '',
                      citationCount=item.get('citationCount'), s2_url=item.get('url'), openAccessPdf=(item.get('openAccessPdf') or {}).get('url',''),
                      source='semantic_scholar')

# enrich DOI candidates with S2 metadata where missing; cap to avoid long runs.
for key, c in list(candidates.items()):
    doi=c.get('doi')
    if doi and not c.get('abstract') and len([x for x in candidates.values() if x.get('abstract')]) < 500:
        data=s2_paper_by_doi(doi)
        if data and not data.get('error'):
            c.update({k:v for k,v in {
                'title': data.get('title') or c.get('title'), 'year': data.get('year'), 'venue': data.get('venue'),
                'abstract': data.get('abstract'), 'citationCount': data.get('citationCount'), 's2_url': data.get('url'),
                'openAccessPdf': (data.get('openAccessPdf') or {}).get('url',''),
            }.items() if v})

# finalize rows
final=[]
for key,c in candidates.items():
    title=c.get('title') or c.get('title_guess') or ''
    abstract=c.get('abstract') or ''
    sample=c.get('sample') or ''
    srcs=c.get('sources') or []
    source='dropbox_pdf' if 'dropbox_pdf' in srcs else ('lucid_reference' if 'lucid_reference' in srcs else 'semantic_scholar')
    score,tier,themes=score_item(title, abstract, sample, has_pdf=bool(c.get('pdf_path')), source=source)
    doi=clean_doi(c.get('doi','')) if c.get('doi') else ''
    status='candidate'
    if doi and doi in completed_dois: status='already_done_or_triaged'
    # heuristic: prior workspace PDFs are likely evidence for already done if source path includes prior report dirs; don't mark all prior PDF by DOI because many source PDFs are done, ok actually prior source means done.
    if c.get('pdf_path') and 'REPLICATE-PROJECT/LUCID-replications/lucid-' in c.get('pdf_path',''):
        status='already_done_or_triaged'
    final.append({
        'key':key, 'doi':doi, 'title':title, 'year':c.get('year',''), 'venue':c.get('venue',''), 'citationCount':c.get('citationCount',''),
        'tier':tier, 'priority_score':score, 'themes':themes, 'status':status, 'sources':';'.join(srcs),
        'pdf_path':c.get('pdf_path',''), 'openAccessPdf':c.get('openAccessPdf',''), 's2_url':c.get('s2_url','') or c.get('url',''),
        'replication_notes': '', 'abstract': abstract[:1200] or sample[:1200]
    })
# sort: candidates first, high tier/score/citations, but keep completed in list lower
final.sort(key=lambda r: (r['status']!='candidate', -int(r['priority_score']), -(int(r['citationCount']) if str(r['citationCount']).isdigit() else 0), r['title'].lower()))
# assign rank; top 100 includes done/triaged for accounting, but top candidate launch list excludes status done
for i,r in enumerate(final,1): r['rank']=i

fields=['rank','tier','priority_score','status','doi','title','year','venue','citationCount','themes','sources','pdf_path','openAccessPdf','s2_url','replication_notes','abstract']
with (OUT/'LUCID_TOP100_MASTER.tsv').open('w', newline='') as f:
    w=csv.DictWriter(f, fieldnames=fields, delimiter='\t', extrasaction='ignore'); w.writeheader(); w.writerows(final[:100])
with (OUT/'LUCID_CANDIDATES_ALL.tsv').open('w', newline='') as f:
    w=csv.DictWriter(f, fieldnames=fields, delimiter='\t', extrasaction='ignore'); w.writeheader(); w.writerows(final)
# Campaign markdown
cand=[r for r in final if r['status']=='candidate']
with (OUT/'LUCID_100_REPLICATION_CAMPAIGN.md').open('w') as f:
    f.write('# LUCID 100-paper replication campaign\n\n')
    f.write('Built from Rick/Ollie Dropbox LUCID PDFs, prior LUCID replication workspace, extracted LUCID reference docs, and Semantic Scholar themed expansion.\n\n')
    f.write('## Corpus/accounting\n\n')
    f.write(f'- Total candidate records assembled: **{len(final)}**\n')
    f.write(f'- Master top-100 table: `LUCID_TOP100_MASTER.tsv`\n')
    f.write(f'- All candidates table: `LUCID_CANDIDATES_ALL.tsv`\n')
    f.write(f'- Existing completed/triaged LUCID replication dirs detected: **{len(completed_slugs)}**\n')
    f.write(f'- Launchable not-yet-done candidates in assembled pool: **{len(cand)}**\n\n')
    f.write('## Prioritization rubric\n\n')
    f.write('- Tier A: high mechanistic LDR relevance + feasible computational/data replication.\n')
    f.write('- Tier B: relevant and probably useful, but may need extraction, author data, or heavier setup.\n')
    f.write('- Tier C: background/review/low-artifact or less directly replicable.\n\n')
    f.write('Scoring favors low-dose/dose-rate biology, DNA repair/DDR, RBE/radiation quality, omics signatures, microbial chronic exposure models, explicit equations/code/data/supplements, and papers already present in the LUCID Dropbox corpus. Reviews/editorials are deprioritized or marked no-go candidates.\n\n')
    f.write('## First launch wave recommendation — new candidates only\n\n')
    for r in cand[:15]:
        f.write(f"{r['rank']}. **[{r['tier']}/{r['priority_score']}] {r['title']}**")
        if r['doi']: f.write(f" — DOI `{r['doi']}`")
        if r['year']: f.write(f" ({r['year']})")
        f.write(f"\n   - Themes: {r['themes'] or 'TBD'}\n")
        f.write(f"   - Source: {r['sources']}\n")
    f.write('\n## Operating protocol\n\n')
    f.write('For each paper: create a per-paper folder under `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/<slug>/`; write `README.md`, `PROGRESS.md`, `REPORT.md`; capture source PDF/text, code/data URLs, environment, scripts, logs, figures, and verdict. Use free endpoints only. No author contact unless Rick explicitly asks. Use LLM judges for final evaluative scoring, never regex-only final scoring.\n\n')
    f.write('## Wave structure\n\n')
    f.write('- Wave 1: 10 Tier-A/B not-yet-done papers, mostly open PDFs/code/supplementary data.\n')
    f.write('- Wave 2: 10 model/simulation papers needing heavier code extraction.\n')
    f.write('- Wave 3: 10 omics/signature papers needing GEO/SRA/supplement harvest.\n')
    f.write('- Wave 4+: continue in 10-paper chunks until 100 are accounted for.\n')
print(json.dumps({'total':len(final),'top100':min(100,len(final)),'launchable':len(cand),'out':str(OUT)}, indent=2))
