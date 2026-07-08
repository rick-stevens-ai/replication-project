"""Verify mesolve → steadystate agreement at long time for N=6."""
import json, time, numpy as np, qutip as qt
from pathlib import Path

sx, sz, sm = qt.sigmax(), qt.sigmaz(), qt.sigmam()
I2 = qt.qeye(2)
N = 6

def op_at(op, k, N=N):
    return qt.tensor([op if i == k else I2 for i in range(N)])

H = sum(-op_at(sx, k) * op_at(sx, k+1) for k in range(N-1)) + sum(-op_at(sz, k) for k in range(N))
c_ops = [np.sqrt(0.1) * op_at(sm, k) for k in range(N)]
psi0 = qt.tensor([qt.basis(2, 0)] * N)
e_ops = [op_at(sz, k) for k in range(N)] + [op_at(sx, 0) * op_at(sx, N-1)]

# Long time evolution: gamma=0.1, so ~1/gamma = 10 time units per relaxation, need >> that
tlist = np.array([0.0, 50.0, 100.0, 200.0, 400.0])
print(f"Running mesolve to tmax={tlist[-1]} ...", flush=True)
t0 = time.time()
me = qt.mesolve(H, psi0, tlist, c_ops=c_ops, e_ops=e_ops,
                options={"progress_bar": False, "nsteps": 200000})
print(f"mesolve wall: {time.time()-t0:.2f}s", flush=True)

rho_ss = qt.steadystate(H, c_ops)
ss_evals = np.array([qt.expect(op, rho_ss) for op in e_ops])
print("\n operator | t=50 | t=100 | t=200 | t=400 | steadystate | |t=400 - SS|")
op_labels = [f"<sz_{k}>" for k in range(N)] + [f"<sx_0 sx_{N-1}>"]
for i, lbl in enumerate(op_labels):
    row = [me.expect[i][j] for j in range(len(tlist))]
    diff = abs(row[-1] - ss_evals[i])
    print(f"  {lbl}  | {row[1]:+.4f} | {row[2]:+.4f} | {row[3]:+.4f} | {row[4]:+.4f} | {ss_evals[i]:+.4f} | {diff:.2e}")

out = {
    "tlist": tlist.tolist(),
    "mesolve_expect_by_op": {lbl: [float(me.expect[i][j]) for j in range(len(tlist))]
                              for i, lbl in enumerate(op_labels)},
    "steadystate_exact_by_op": {lbl: float(ss_evals[i]) for i, lbl in enumerate(op_labels)},
    "max_abs_final_vs_steadystate": float(max(abs(me.expect[i][-1] - ss_evals[i]) for i in range(len(op_labels)))),
}
outdir = Path(__file__).resolve().parent.parent / "report" / "evidence"
(outdir / "steadystate_verify_N6.json").write_text(json.dumps(out, indent=2))
print(f"\nmax_abs_final_vs_steadystate: {out['max_abs_final_vs_steadystate']:.4e}")
print(f"Wrote {outdir / 'steadystate_verify_N6.json'}")
