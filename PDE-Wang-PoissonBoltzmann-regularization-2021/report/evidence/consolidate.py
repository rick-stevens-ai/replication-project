import json,os
# paper Table 1 values
paper_1q={11:-56.8468,21:-64.8951,31:-63.9885,41:-64.7367,51:-65.1096,101:-65.4422,201:-65.6210,401:-65.6644}
paper_2q={11:-271.3451,21:-310.5806,31:-300.3787,41:-303.0649,51:-305.7947,101:-305.1510,201:-304.1162,401:-303.7689}
def load(f):
    return {r['N']:r['E'] for r in json.load(open(f))} if os.path.exists(f) else {}
mine1=load('reg2_1charge_nondiv.json'); mine2=load('reg2_2charge_nondiv.json')
# merge uicgpu N=101/201 if present in extra files
for extra in ['reg2_1charge_nondiv_uic.json']:
    pass
def table(mine,paper,label):
    print(f"\n== {label} ==")
    print(f"{'N':>4} {'h':>7} {'mine':>12} {'paper':>12} {'absdiff':>9} {'%err':>7}")
    hs={11:2,21:1,31:0.6667,41:0.5,51:0.4,101:0.2,201:0.1,401:0.05}
    rows=[]
    for N in sorted(set(list(mine)+list(paper))):
        m=mine.get(N); p=paper.get(N)
        if m is None: 
            print(f"{N:>4} {hs.get(N,''):>7} {'--':>12} {p:>12.4f}"); continue
        d=abs(m-p); pe=100*d/abs(p)
        print(f"{N:>4} {hs[N]:>7} {m:>12.4f} {p:>12.4f} {d:>9.4f} {pe:>6.2f}%")
        rows.append(dict(N=N,h=hs[N],mine=m,paper=p,absdiff=round(d,4),pct=round(pe,2)))
    return rows
r1=table(mine1,paper_1q,"One-charge (Table 1, Regularization col)")
r2=table(mine2,paper_2q,"Two-charge (Table 1, Regularization col)")
json.dump({'one_charge':r1,'two_charge':r2},open('table1_comparison.json','w'),indent=2)
print("\nwrote table1_comparison.json")
