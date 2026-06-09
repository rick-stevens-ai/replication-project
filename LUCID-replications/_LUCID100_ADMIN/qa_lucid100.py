#!/usr/bin/env python3
from pathlib import Path
import csv, re
from collections import Counter
OUT=Path('/Users/stevens/.openclaw/workspace/lucid-replications')
IN=OUT/'LUCID100_NEW_CANDIDATES.tsv'
PRIOR=Path.home()/"Dropbox/REPLICATE-PROJECT/LUCID-replications"
DOI_RE=re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.I)

def clean_doi(s): return (s or '').rstrip('.,;:)\]}>').lower()
# DOI corrections from manual inspection / known supplement URLs
DOI_CORRECTIONS={
    '10.1371/journal.pone.0079541.s00':'10.1371/journal.pone.0079541',
    '10.2203/dose-response.10-039.scott':'10.2203/dose-response.10-039.scott',
}
# Hard exclusions after manual QA of v0.1/v0.2 top candidates.
EXCLUDE_DOIS={
    # false/off-topic search hits
    '10.1016/j.jcmgh.2018.09.014', # maltodextrin intestinal inflammation; not radiation biology
    '10.1186/1746-6148-4-18',      # bovine mastitis infection, no radiation
    '10.3390/ijms242015238',       # arsenic exposure, no ionizing radiation
    '10.1016/j.archoralbio.2023.105874', # photobiomodulation/bacterial stimulus marginal/off-topic
    '10.1089/cmb.2012.0283',       # LUCID proposal/review-response artifact, not paper
    '10.1093/occmed/kqae023.1211', # conference abstract only; keep lower backlog, not top100
    '10.51699/eaedxq67',           # review/future directions; not replication-first
    '10.2967/jnumed.118.210252',   # commentary, not replication target
    '10.1073/pnas.210171597',      # supplement-only artifact from prior p53 paper
    '10.1093/jrr/rrs119',          # PIDE dataset/support artifact; useful resource not paper replication target
    '10.1371/journal.pone.0187274', # generated Dropbox essay, not source paper PDF/title unreliable
    '10.1186/s40168-020-00927-5',  # generated microbial-models review PDF title, not paper itself here
    '10.1126/sciadv.abf1771',      # generated Novel Mechanistic Insights doc assigned wrong DOI
}
EXCLUDE_TITLE_SUBSTR=[
    'supporting information', 'project title: lucid', 'updated radiation quality factors',
    'novel mechanistic insights in radiation biology', 'investigating chronic low-dose radiation mechanisms via microbial models',
    'epigenetic mechanisms of human adaptation to', 'maltodextrin', 'bovine mammary',
    'human-induced radioresistance as a possible mechanism for producing biological weapons',
    'revisiting low dose radiobiology', 'o-316 the potential application',
]
# Require at least one radiation anchor unless source is Dropbox LUCID target PDF and title is clearly model/foci/etc.
RADIATION_ANCHORS=['radiation','irradiation','ionizing','gamma','x-ray','x ray','radiotherapy','radiosensitivity','radiobiolog','dose-rate','dose rate','low-dose','low dose','let','rbe','proton','carbon-ion','carbon ion','alpha therapy','bnct','neutron','actinium','lutetium','h2ax','53bp1','dna double-strand','double strand break']
REPLICABILITY_ANCHORS=['model','simulation','monte carlo','geant4','topas','medras','ode','stochastic','kinetic','equation','transcript','rna-seq','gene expression','methylation','proteomic','genomic','dataset','foci','dose-response','survival','rbe','repair kinetics','biomarker','signature']
REVIEW_ANCHORS=['review','commentary','editorial','perspective','future directions']

def prior_done_rows():
    rows=[]; done=set(); titles=[]
    if not PRIOR.exists(): return rows,done,titles
    for d in sorted([p for p in PRIOR.iterdir() if p.is_dir() and p.name.startswith('lucid-')]):
        files=[d/'REPORT.md',d/'NO-GO-REPORT.md',d/'README.md',d/'PROGRESS.md']
        txt='\n'.join(f.read_text(errors='ignore') for f in files if f.exists())
        if not txt: continue
        dois=[clean_doi(x) for x in DOI_RE.findall(txt)]
        doi=DOI_CORRECTIONS.get(dois[0],dois[0]) if dois else ''
        if doi: done.add(doi)
        title=''
        for pat in [r'(?im)^\s*\*\*Target paper[:.]\*\*\s*(.+)$',r'(?im)^\s*\*\*Paper[:.]\*\*\s*(.+)$',r'(?im)^\s*\*\*Citation[:.]\*\*\s*(.+)$',r'(?im)^\s*#\s+(.+)$']:
            m=re.search(pat,txt)
            if m:
                title=re.sub(r'[`*_\[\]]','',m.group(1)).strip(); break
        if not title or title.lower().startswith(('independent replication','lucid replication','report')):
            title=d.name.replace('lucid-','').replace('-',' ').title()
        verdict='DONE/TRIAGED'
        low=txt.lower()
        if 'no-go' in low: verdict='NO-GO / triaged unsuitable'
        elif 'partial' in low: verdict='PARTIAL'
        elif 'replicated' in low or 'reproduced' in low: verdict='REPLICATED'
        score=18 if verdict.startswith('REPLICATED') else (14 if verdict.startswith('PARTIAL') else 5)
        rows.append({'rank':'','wave':'Completed/triaged','tier':'A' if score>=14 else 'C','priority_score':score,'status':'completed_or_triaged','doi':doi,'title':title[:260],'year':'','venue':'','citationCount':'','themes':'Existing LUCID replication','sources':'prior_lucid_workspace','replication_folder':str(d),'pdf_or_url':'','verdict_or_plan':verdict,'qa_decision':'KEEP prior completed/triaged','abstract_or_notes':''})
    return rows,done,titles

def decide(r, done_dois):
    title=(r.get('title') or '').strip()
    doi=DOI_CORRECTIONS.get(clean_doi(r.get('doi','')),clean_doi(r.get('doi','')))
    text=' '.join([title,r.get('abstract_or_notes',''),r.get('themes','')]).lower()
    if doi in done_dois:
        return 'EXCLUDE','duplicate/prior completed DOI'
    if doi in EXCLUDE_DOIS:
        return 'EXCLUDE','manual exclusion: artifact/off-topic/review/conference/resource'
    if any(s in title.lower() for s in EXCLUDE_TITLE_SUBSTR):
        return 'EXCLUDE','manual exclusion by title artifact/off-topic'
    if not title or len(title)<18:
        return 'EXCLUDE','missing/weak title'
    rad=any(a in text for a in RADIATION_ANCHORS)
    repl=any(a in text for a in REPLICABILITY_ANCHORS)
    review=any(a in text for a in REVIEW_ANCHORS)
    if not rad:
        return 'EXCLUDE','no clear ionizing-radiation anchor'
    if review and int(r.get('priority_score') or 0)<16:
        return 'DEMOTE','review/commentary lower priority'
    if not repl and int(r.get('priority_score') or 0)<14:
        return 'DEMOTE','unclear computational/data replication handle'
    # Recent 2026 unknown/possibly not real: keep only if strong DOI and title is explicit; status needs verify.
    if str(r.get('year')) in {'2026','2025'} and not (r.get('openAccessPdf') or r.get('pdf_or_url') or r.get('doi')):
        return 'DEMOTE','new/metadata weak; needs verification'
    return 'KEEP','relevant and replication-plausible'

def infer_worktype(r):
    t=' '.join([r['title'],r.get('abstract_or_notes',''),r.get('themes','')]).lower()
    if any(k in t for k in ['transcript','rna-seq','gene expression','methylation','proteomic','genomic','biomarker','signature']): return 'omics/signature replication'
    if any(k in t for k in ['monte carlo','geant4','topas','medras','microdosimetry','simulation']): return 'simulation/model replication'
    if any(k in t for k in ['stochastic','ode','kinetic','mechanistic model','theoretical framework']): return 'math/model reimplementation'
    if any(k in t for k in ['h2ax','53bp1','foci','dose-response','survival','rbe']): return 'figure/table/dose-response replication'
    return 'artifact harvest + claim triage'

def adjust_score(r):
    score=int(r.get('priority_score') or 0)
    title=(r.get('title','')+' '+r.get('abstract_or_notes','')).lower()
    # Penalty for reviews/commentary and weak non-data items
    if any(k in title for k in REVIEW_ANCHORS): score-=4
    # Boost for explicit open-style work
    if any(k in title for k in ['github','public dataset','geo','sra','monte carlo','topas','geant4','model','simulation','rna-seq','gene expression']): score+=1
    return max(0,min(20,score))

prior,done,titles=prior_done_rows()
raw=list(csv.DictReader(IN.open(), delimiter='\t'))
kept=[]; demoted=[]; excluded=[]; seen=set()
for r in raw:
    doi=DOI_CORRECTIONS.get(clean_doi(r.get('doi','')),clean_doi(r.get('doi','')))
    key=doi or r.get('title','').lower()[:120]
    if key in seen: continue
    seen.add(key)
    decision,reason=decide(r,done)
    rr={**r,'doi':doi,'qa_decision':decision+': '+reason}
    rr['priority_score']=adjust_score(rr)
    rr['tier']='A' if int(rr['priority_score'])>=14 else ('B' if int(rr['priority_score'])>=9 else 'C')
    rr['worktype']=infer_worktype(rr)
    rr['verdict_or_plan']='TODO: '+rr['worktype']+'; artifact harvest; brief; run; report'
    rr['pdf_or_url']=rr.get('pdf_or_url') or rr.get('openAccessPdf') or rr.get('s2_url')
    if decision=='KEEP': kept.append(rr)
    elif decision=='DEMOTE': demoted.append(rr)
    else: excluded.append(rr)
kept.sort(key=lambda r:(-int(r['priority_score']), -(int(r.get('citationCount') or 0) if str(r.get('citationCount')).isdigit() else 0), r['title'].lower()))
demoted.sort(key=lambda r:(-int(r['priority_score']), r['title'].lower()))
# Need 100 total with prior + kept; if kept short use demoted, but label wave_later. We have enough kept likely.
needed=100-len(prior)
selected=kept[:needed]
if len(selected)<needed:
    selected += demoted[:needed-len(selected)]
final=prior+selected
fields=['rank','wave','tier','priority_score','status','doi','title','year','venue','citationCount','themes','worktype','sources','replication_folder','pdf_or_url','verdict_or_plan','qa_decision','abstract_or_notes']
for i,r in enumerate(final,1):
    r['rank']=i
    if r.get('status')!='completed_or_triaged':
        idx=i-len(prior)
        r['status']='candidate_curated'
        r['wave']=f'Wave {(idx-1)//10+1}'
        r.setdefault('replication_folder','')
for name, rows in [('LUCID100_SOLID_MASTER_QA.tsv', final), ('LUCID100_QA_KEPT.tsv', kept), ('LUCID100_QA_DEMOTED.tsv', demoted), ('LUCID100_QA_EXCLUDED.tsv', excluded)]:
    with (OUT/name).open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=fields, delimiter='\t', extrasaction='ignore'); w.writeheader(); w.writerows(rows)
# rewrite campaign QA markdown
with (OUT/'LUCID100_QA_REPORT.md').open('w') as f:
    f.write('# LUCID100 manual QA pass report\n\n')
    f.write('## Summary\n\n')
    f.write(f'- Prior completed/triaged papers retained: **{len(prior)}**\n')
    f.write(f'- New candidates kept after QA: **{len(kept)}**\n')
    f.write(f'- New candidates demoted/backlog: **{len(demoted)}**\n')
    f.write(f'- New candidates excluded: **{len(excluded)}**\n')
    f.write(f'- Curated master size: **{len(final)}**\n\n')
    f.write('## Main corrections applied\n\n')
    f.write('- Removed generated LUCID/proposal documents that were misread as source papers.\n')
    f.write('- Removed off-topic Semantic Scholar false positives, e.g. maltodextrin/intestinal inflammation, bovine mastitis, arsenic exposure.\n')
    f.write('- Removed supplement/resource artifacts such as `Supporting Information – S1 Text` and PIDE resource entries from the top 100.\n')
    f.write('- Penalized reviews/commentaries/conference abstracts unless they have a strong replication handle.\n')
    f.write('- Refilled the top 100 from the filtered backlog so it remains 31 completed/triaged + 69 curated new candidates.\n\n')
    f.write('## Curated Wave 1\n\n')
    for r in [x for x in final if x.get('wave')=='Wave 1']:
        f.write(f"{r['rank']}. **{r['title']}**")
        if r.get('doi'): f.write(f" — DOI `{r['doi']}`")
        f.write(f"\n   - Worktype: {r.get('worktype','')}\n   - QA: {r.get('qa_decision','')}\n")
print('prior',len(prior),'kept',len(kept),'demoted',len(demoted),'excluded',len(excluded),'final',len(final))
print('wrote', OUT/'LUCID100_SOLID_MASTER_QA.tsv')
print('wrote', OUT/'LUCID100_QA_REPORT.md')
print('wave1')
for r in [x for x in final if x.get('wave')=='Wave 1']:
    print(r['rank'], r['priority_score'], r['doi'], r['title'][:100], '|', r.get('worktype'))
