"""Post-analysis: distribution stats + paired Wilcoxon + sampled MAX-CUT verification."""
import json, os, sys, numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qaoa_maxcut_fast import build_graph, make_maxcut_diag, qaoa_statevector, single_start, multistart

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "..", "report", "evidence")

d = json.load(open(os.path.join(EV, "qaoa_multistart_results.json")))
G = build_graph(d["graph"]["n_vertices"], d["graph"]["graph_seed"])
n = d["graph"]["n_vertices"]
cost_diag = make_maxcut_diag(G, n)
exact = d["graph"]["exact_maxcut"]

# -- distribution summary
lines = []
lines.append("Distribution of approximation ratios (n=20 seeds per condition):")
lines.append(f"{'cond':<28}{'min':>8}{'q25':>8}{'med':>8}{'mean':>8}{'q75':>8}{'max':>8}{'std':>8}")
summary = {}
for k, v in d["conditions"].items():
    r = np.array(v["approx_ratios"])
    row = dict(
        min=float(r.min()),
        q25=float(np.percentile(r, 25)),
        median=float(np.median(r)),
        mean=float(r.mean()),
        q75=float(np.percentile(r, 75)),
        max=float(r.max()),
        std=float(r.std()),
    )
    summary[k] = row
    lines.append(f"  {k:<26}{row['min']:>8.3f}{row['q25']:>8.3f}{row['median']:>8.3f}{row['mean']:>8.3f}{row['q75']:>8.3f}{row['max']:>8.3f}{row['std']:>8.3f}")

# -- paired Wilcoxon
wilcox = {}
lines.append("\nPaired Wilcoxon (one-sided, alt: MS > SS) per-seed:")
lines.append(f"{'condition':<24}{'mean(MS-SS)':>14}{'p-value':>10}{'wins':>6}{'ties':>6}{'loss':>6}")
for p in [1, 2, 4]:
    ss = np.array(d["conditions"][f"p={p}/single_start"]["approx_ratios"])
    for M in [5, 10, 20]:
        ms = np.array(d["conditions"][f"p={p}/multistart_M={M}"]["approx_ratios"])
        diffs = ms - ss
        if np.allclose(diffs, 0, atol=1e-9):
            row = dict(mean_diff=0.0, pvalue=None, wins=0, ties=int(len(diffs)), loss=0, note="all ties")
        else:
            try:
                st, pv = stats.wilcoxon(ms, ss, alternative="greater", zero_method="wilcox")
                row = dict(
                    mean_diff=float(diffs.mean()),
                    pvalue=float(pv),
                    wins=int(np.sum(diffs > 0)),
                    ties=int(np.sum(diffs == 0)),
                    loss=int(np.sum(diffs < 0)),
                )
            except Exception as e:
                row = dict(error=str(e))
        wilcox[f"p={p}/M={M}"] = row
        if "error" in row:
            lines.append(f"  p={p} M={M:<3}                   ERROR: {row['error']}")
        elif row.get("note") == "all ties":
            lines.append(f"  p={p} M={M:<3}                    all ties")
        else:
            lines.append(f"  p={p} M={M:<3}                {row['mean_diff']:>+14.4f}{row['pvalue']:>10.4f}{row['wins']:>6d}{row['ties']:>6d}{row['loss']:>6d}")

# -- sampled MAX-CUT from best QAOA state at p=2
lines.append("\nSampled MAX-CUT quality (best QAOA(p=2) state, seed=42 for sampling):")
lines.append(f"exact MAX-CUT = {exact}")
# rerun a single seed to recover params
for label, runner, kwargs in [
    ("single_start seed=0", single_start, dict(seed=0, budget=1000)),
    ("multistart M=10 seed=0", multistart, dict(seed=0, M=10, total_budget=1000)),
]:
    v, params, ne = runner(G, 2, cost_diag, n, **kwargs)
    if params is None:
        continue
    state = qaoa_statevector(G, params, 2, cost_diag, n)
    probs = (state.conj() * state).real
    probs = probs / probs.sum()
    rng = np.random.default_rng(42)
    samples = rng.choice(len(probs), size=100000, p=probs)
    cuts = cost_diag[samples]
    best_cut = int(cuts.max())
    mean_cut = float(cuts.mean())
    frac_optimal = float((cuts >= exact).mean())
    frac_9plus = float((cuts >= 9).mean())
    lines.append(
        f"  {label}: <H_C>={v:.3f}  best_bitstring_cut={best_cut}/{exact}  "
        f"mean_sampled_cut={mean_cut:.3f}  P(cut==optimum)={frac_optimal:.3f}  P(cut>=9)={frac_9plus:.3f}"
    )

report = "\n".join(lines)
print(report)
with open(os.path.join(EV, "analysis.txt"), "w") as f:
    f.write(report + "\n")

json.dump(
    dict(distribution_summary=summary, paired_wilcoxon=wilcox),
    open(os.path.join(EV, "stats.json"), "w"),
    indent=2,
)
print(f"\nSaved: {os.path.join(EV, 'analysis.txt')}")
print(f"Saved: {os.path.join(EV, 'stats.json')}")
