"""
Evaluate trained GCN-DQN and MLP-DQN on held-out scenarios.
Compute metrics comparable to the paper's Table V (8500-bus testing):
   - Average restored load (% of UB)
   - Average steps to restoration (proxy for time)
   - Wall-clock inference time per episode (s)
Also produce learning-curve plots (paper's Fig 10) and bar comparison.
"""
import os, sys, json, time, argparse
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from env_8500 import Env8500
from models_8500 import GCNDQN, MLPDQN, normalize_adj
from train_8500 import build_action_mask


def random_baseline(env, n_act, rng):
    """Random valid action."""
    s = env.reset()
    R = 0.0
    for t in range(env.max_steps):
        mask = np.zeros(n_act, dtype=np.float32)
        mask[:env.n_switches] = s["switch_mask"]
        mask[-1] = 1.0
        valid = np.where(mask > 0)[0]
        a = int(rng.choice(valid))
        s, r, d, info = env.step(a)
        R += r
        if d: break
    return env.restored_frac, env.step_count


def greedy_baseline(env, n_act, rng):
    """Heuristic: greedy frontier expansion biased toward high-load cells."""
    s = env.reset()
    R = 0.0
    for t in range(env.max_steps):
        en = s["energized"]; sw = s["switch_mask"]
        # Score each switch: load of the not-yet-energized endpoint, if it extends frontier
        best_a = env.n_switches  # NoOp
        best_score = -1e9
        for i in range(env.n_switches):
            if sw[i] == 0: continue
            u, v = env.switch_edges[i]
            if en[u] and not en[v]:    score = env.epi_load[v]
            elif en[v] and not en[u]:  score = env.epi_load[u]
            else: continue
            if score > best_score:
                best_score = score; best_a = i
        s, r, d, info = env.step(int(best_a))
        R += r
        if d: break
    return env.restored_frac, env.step_count


def policy_eval(net, env, A_norm, device, n_act):
    s = env.reset()
    t0 = time.time()
    for t in range(env.max_steps):
        x = torch.as_tensor(s["node_features"], device=device).unsqueeze(0)
        with torch.no_grad():
            q = net(x, A_norm).cpu().numpy()[0]
        mask = np.zeros(n_act, dtype=np.float32)
        mask[:env.n_switches] = s["switch_mask"]
        mask[-1] = 1.0
        masked_q = np.where(mask > 0, q, -1e9)
        a = int(np.argmax(masked_q))
        s, r, d, info = env.step(a)
        if d: break
    elapsed = time.time() - t0
    return env.restored_frac, env.step_count, elapsed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="/gpustor/stevens/projects-active/replicate-1868518/data")
    ap.add_argument("--results", default="/gpustor/stevens/projects-active/replicate-1868518/results")
    ap.add_argument("--figures", default="/gpustor/stevens/projects-active/replicate-1868518/figures")
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--n-eval", type=int, default=30)
    ap.add_argument("--max-steps", type=int, default=600)
    args = ap.parse_args()
    os.makedirs(args.figures, exist_ok=True)

    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    env_t = Env8500(args.data, max_steps=args.max_steps, seed=0, fault_frac=0.03)
    env_t.reset()
    A = torch.as_tensor(env_t.cell_adj, device=device)
    A_norm = normalize_adj(A)
    n_act = env_t.n_switches + 1
    feat_dim = env_t.feat_dim

    # Load checkpoints
    nets = {}
    for tag, cls in [("gcn", GCNDQN), ("mlp", MLPDQN)]:
        ckpt = os.path.join(args.results, f"{tag}_8500_best.pt")
        if not os.path.exists(ckpt):
            ckpt = os.path.join(args.results, f"{tag}_8500_ckpt.pt")
        if not os.path.exists(ckpt):
            print(f"[eval] missing {ckpt}, skipping {tag}")
            continue
        if cls is GCNDQN:
            net = cls(env_t.n_cells, env_t.n_switches, env_t.switch_edges, feat_dim=feat_dim).to(device)
        else:
            net = cls(env_t.n_cells, env_t.n_switches, feat_dim=feat_dim).to(device)
        sd = torch.load(ckpt, map_location=device)["state_dict"]
        net.load_state_dict(sd); net.eval()
        nets[tag] = net

    # Evaluate on N seeds
    seeds = list(range(20_000, 20_000 + args.n_eval))
    rng = np.random.RandomState(99)
    results = {"random": [], "greedy": [], **{k: [] for k in nets}}

    for s_ in seeds:
        env_t.rng = np.random.RandomState(s_)
        rf, sc = random_baseline(env_t, n_act, np.random.RandomState(s_))
        results["random"].append((rf, sc, 0.0))

        env_t.rng = np.random.RandomState(s_)
        rf, sc = greedy_baseline(env_t, n_act, np.random.RandomState(s_))
        results["greedy"].append((rf, sc, 0.0))

        for tag, net in nets.items():
            env_t.rng = np.random.RandomState(s_)
            rf, sc, el = policy_eval(net, env_t, A_norm, device, n_act)
            results[tag].append((rf, sc, el))

    summary = {}
    for tag, arr in results.items():
        arr = np.array(arr)
        summary[tag] = {
            "mean_restored_frac": float(arr[:, 0].mean()),
            "std_restored_frac":  float(arr[:, 0].std()),
            "mean_steps":         float(arr[:, 1].mean()),
            "mean_inference_s":   float(arr[:, 2].mean()),
        }

    print("\n=== 8500-bus restoration: methods comparison ===")
    print(f"{'method':<10s} {'restored%':>12s} {'steps':>8s} {'time(s)':>10s}")
    for k, v in summary.items():
        print(f"{k:<10s} {v['mean_restored_frac']*100:>10.2f}±{v['std_restored_frac']*100:.1f} "
              f"{v['mean_steps']:>8.1f} {v['mean_inference_s']:>10.4f}")

    with open(os.path.join(args.results, "eval_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    # Plot 1: Learning curves
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for tag, color in [("gcn", "C0"), ("mlp", "C1")]:
        hist_path = os.path.join(args.results, f"{tag}_8500_history.json")
        if not os.path.exists(hist_path): continue
        with open(hist_path) as f: h = json.load(f)
        ep = np.array(h["episode"]); rest = np.array(h["ep_restored"])
        # smooth
        w = 25
        if len(rest) >= w:
            kernel = np.ones(w) / w
            rest_smooth = np.convolve(rest, kernel, mode="valid")
            ep_smooth = ep[w-1:]
            axes[0].plot(ep_smooth, rest_smooth*100, label=f"{tag.upper()}-DQN", color=color)
        if h["eval_episode"]:
            axes[1].plot(h["eval_episode"], np.array(h["eval_restored"])*100,
                         "o-", label=f"{tag.upper()}-DQN", color=color)
    axes[0].set_xlabel("Training episode"); axes[0].set_ylabel("Train restored load (%)")
    axes[0].set_title("Learning curve (smoothed train)"); axes[0].legend(); axes[0].grid(alpha=0.3)
    axes[1].set_xlabel("Training episode"); axes[1].set_ylabel("Eval restored load (%)")
    axes[1].set_title("Held-out evaluation (greedy)"); axes[1].legend(); axes[1].grid(alpha=0.3)
    fig.suptitle("IEEE 8500-bus Distribution System Restoration (replication of Zhao&Wang 2022, Fig 10)")
    fig.tight_layout()
    p1 = os.path.join(args.figures, "8500_learning_curves.png")
    fig.savefig(p1, dpi=150); plt.close(fig)
    print("Saved", p1)

    # Plot 2: Bar comparison
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    tags = list(summary.keys())
    rests = [summary[t]["mean_restored_frac"]*100 for t in tags]
    sts   = [summary[t]["mean_steps"] for t in tags]
    bars1 = axes[0].bar(tags, rests, color=["#888","#aaa","C0","C1"][:len(tags)])
    axes[0].set_ylabel("Restored load (%)"); axes[0].set_title("Test scenarios (n=%d)"%args.n_eval)
    axes[0].axhline(100, ls="--", color="k", alpha=0.3, label="Paper G-RL: 100%")
    axes[0].legend()
    for b, v in zip(bars1, rests): axes[0].text(b.get_x()+b.get_width()/2, v+1, f"{v:.1f}", ha="center")
    bars2 = axes[1].bar(tags, sts, color=["#888","#aaa","C0","C1"][:len(tags)])
    axes[1].set_ylabel("Steps to terminate"); axes[1].set_title("Restoration steps")
    for b, v in zip(bars2, sts): axes[1].text(b.get_x()+b.get_width()/2, v+5, f"{v:.0f}", ha="center")
    fig.suptitle("8500-bus Comparison: GCN-DQN vs MLP-DQN vs Heuristics")
    fig.tight_layout()
    p2 = os.path.join(args.figures, "8500_comparison_bar.png")
    fig.savefig(p2, dpi=150); plt.close(fig)
    print("Saved", p2)


if __name__ == "__main__":
    main()
