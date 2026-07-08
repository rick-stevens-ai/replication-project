"""
Train GCN-DQN or MLP-DQN on the 8500-bus restoration env.
Implements:
  - Replay buffer (uniform)
  - Double DQN target
  - Action masking (mask invalid switches with -inf logits)
  - Epsilon-greedy exploration
  - Periodic evaluation (greedy) on held-out seeds
  - Saves checkpoint + history JSON
"""
import os, sys, json, time, argparse, random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from env_8500 import Env8500
from models_8500 import GCNDQN, MLPDQN, normalize_adj


def set_seed(s):
    random.seed(s); np.random.seed(s); torch.manual_seed(s); torch.cuda.manual_seed_all(s)


class ReplayBuffer:
    def __init__(self, cap, n_cells, feat_dim, n_actions):
        self.cap = cap; self.idx = 0; self.size = 0
        self.s  = np.zeros((cap, n_cells, feat_dim), dtype=np.float32)
        self.a  = np.zeros((cap,), dtype=np.int64)
        self.r  = np.zeros((cap,), dtype=np.float32)
        self.s2 = np.zeros((cap, n_cells, feat_dim), dtype=np.float32)
        self.d  = np.zeros((cap,), dtype=np.float32)
        self.m2 = np.zeros((cap, n_actions), dtype=np.float32)  # next-state action mask

    def push(self, s, a, r, s2, d, m2):
        i = self.idx
        self.s[i] = s; self.a[i] = a; self.r[i] = r; self.s2[i] = s2; self.d[i] = d; self.m2[i] = m2
        self.idx = (i + 1) % self.cap; self.size = min(self.size + 1, self.cap)

    def sample(self, n):
        idx = np.random.randint(0, self.size, size=n)
        return (self.s[idx], self.a[idx], self.r[idx], self.s2[idx], self.d[idx], self.m2[idx])


def build_action_mask(env_state, env, n_actions):
    """Return mask (n_actions,): 1.0 means VALID.
    Mask only the trivially invalid (already-closed or faulted) switches — the
    agent must learn the rest (loops, non-frontier)."""
    sw = env_state["switch_mask"]  # (S,) 1 if open & not faulted
    mask = np.zeros(n_actions, dtype=np.float32)
    mask[:env.n_switches] = sw
    mask[-1] = 1.0  # NoOp always valid
    return mask


def select_action(q, mask, epsilon):
    """q: (n_actions,) numpy; mask: (n_actions,) 1=valid; epsilon: float."""
    valid = np.where(mask > 0)[0]
    if len(valid) == 0:
        return q.shape[0] - 1  # NoOp
    if np.random.rand() < epsilon:
        return int(np.random.choice(valid))
    masked_q = np.where(mask > 0, q, -1e9)
    return int(np.argmax(masked_q))


def evaluate(net, env_seeds, env_eval, device, A_norm, model_name="gcn"):
    """Greedy evaluation on a set of seeds; return mean restored frac and mean steps."""
    fracs, steps_list, times = [], [], []
    env = env_eval
    for s_ in env_seeds:
        env.rng = np.random.RandomState(s_)
        st = env.reset()
        t0 = time.time()
        for t in range(env.max_steps):
            x = torch.as_tensor(st["node_features"], device=device).unsqueeze(0)
            with torch.no_grad():
                q = net(x, A_norm).cpu().numpy()[0]
            mask = build_action_mask(st, env, env.n_switches + 1)
            a = select_action(q, mask, epsilon=0.0)
            st, r, d, info = env.step(int(a))
            if d: break
        times.append(time.time() - t0)
        fracs.append(env.restored_frac)
        steps_list.append(env.step_count)
    return float(np.mean(fracs)), float(np.mean(steps_list)), float(np.mean(times))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", choices=["gcn", "mlp"], required=True)
    ap.add_argument("--episodes", type=int, default=1000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--gamma", type=float, default=0.96)
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--buffer-size", type=int, default=200_000)
    ap.add_argument("--eps-start", type=float, default=0.95)
    ap.add_argument("--eps-end", type=float, default=0.05)
    ap.add_argument("--eps-decay", type=float, default=0.995)
    ap.add_argument("--target-update", type=int, default=200)   # steps
    ap.add_argument("--learn-start", type=int, default=2000)
    ap.add_argument("--max-steps", type=int, default=600)
    ap.add_argument("--gpu", type=int, default=1)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--data", type=str, default="/gpustor/stevens/projects-active/replicate-1868518/data")
    ap.add_argument("--out", type=str, default="/gpustor/stevens/projects-active/replicate-1868518/results")
    ap.add_argument("--tag", type=str, default=None)
    args = ap.parse_args()

    set_seed(args.seed)
    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    print(f"[train] model={args.model} device={device} episodes={args.episodes}")

    # Build env (template)
    env = Env8500(args.data, max_steps=args.max_steps, seed=args.seed, fault_frac=0.03)
    s = env.reset()
    n_cells = env.n_cells; n_sw = env.n_switches; n_act = n_sw + 1
    feat_dim = env.feat_dim

    # Adjacency (constant) on device
    A = torch.as_tensor(env.cell_adj, device=device)
    A_norm = normalize_adj(A)

    # Networks
    if args.model == "gcn":
        net  = GCNDQN(n_cells, n_sw, env.switch_edges, feat_dim=feat_dim).to(device)
        tgt  = GCNDQN(n_cells, n_sw, env.switch_edges, feat_dim=feat_dim).to(device)
    else:
        net  = MLPDQN(n_cells, n_sw, feat_dim=feat_dim).to(device)
        tgt  = MLPDQN(n_cells, n_sw, feat_dim=feat_dim).to(device)
    tgt.load_state_dict(net.state_dict())
    for p in tgt.parameters(): p.requires_grad = False
    opt  = torch.optim.Adam(net.parameters(), lr=args.lr)

    n_params = sum(p.numel() for p in net.parameters())
    print(f"[train] params={n_params:,}")

    rb = ReplayBuffer(args.buffer_size, n_cells, feat_dim, n_act)
    eps = args.eps_start
    best_eval = -1.0
    history = {"episode": [], "ep_return": [], "ep_restored": [], "ep_steps": [],
               "eval_episode": [], "eval_restored": [], "eval_steps": [], "eval_time": [],
               "loss": [], "wall_seconds": [], "args": vars(args)}
    eval_seeds = list(range(10_000, 10_010))  # held-out
    total_steps = 0
    t_start = time.time()
    for ep in range(1, args.episodes + 1):
        env.rng = np.random.RandomState(args.seed * 1000 + ep)
        st = env.reset()
        ep_R = 0.0
        for t in range(args.max_steps):
            x = torch.as_tensor(st["node_features"], device=device).unsqueeze(0)
            with torch.no_grad():
                q = net(x, A_norm).cpu().numpy()[0]
            mask = build_action_mask(st, env, n_act)
            a = select_action(q, mask, epsilon=eps)
            s_prev = st["node_features"].copy()
            st, r, d, info = env.step(int(a))
            mask2 = build_action_mask(st, env, n_act)
            rb.push(s_prev, a, r, st["node_features"], 1.0 if d else 0.0, mask2)
            ep_R += r
            total_steps += 1

            # Learn
            if rb.size >= args.learn_start:
                bs, ba, br, bs2, bd, bm2 = rb.sample(args.batch_size)
                bs   = torch.as_tensor(bs,  device=device)
                bs2  = torch.as_tensor(bs2, device=device)
                ba   = torch.as_tensor(ba,  device=device).long()
                br   = torch.as_tensor(br,  device=device)
                bd   = torch.as_tensor(bd,  device=device)
                bm2  = torch.as_tensor(bm2, device=device)

                q_pred = net(bs, A_norm).gather(1, ba.unsqueeze(1)).squeeze(1)
                with torch.no_grad():
                    q_next_online = net(bs2, A_norm)
                    q_next_online = q_next_online + (bm2 - 1.0) * 1e9
                    a_next = q_next_online.argmax(1, keepdim=True)
                    q_next = tgt(bs2, A_norm).gather(1, a_next).squeeze(1)
                    target = br + args.gamma * (1 - bd) * q_next
                loss = F.smooth_l1_loss(q_pred, target)
                opt.zero_grad(); loss.backward()
                torch.nn.utils.clip_grad_norm_(net.parameters(), 5.0)
                opt.step()
                history["loss"].append(float(loss.item()))

                if total_steps % args.target_update == 0:
                    tgt.load_state_dict(net.state_dict())

            if d: break

        eps = max(args.eps_end, eps * args.eps_decay)
        history["episode"].append(ep)
        history["ep_return"].append(float(ep_R))
        history["ep_restored"].append(float(env.restored_frac))
        history["ep_steps"].append(int(env.step_count))
        history["wall_seconds"].append(time.time() - t_start)

        if ep % 25 == 0 or ep == 1:
            eval_frac, eval_steps, eval_time = evaluate(net, eval_seeds[:5], env, device, A_norm, args.model)
            history["eval_episode"].append(ep)
            history["eval_restored"].append(eval_frac)
            history["eval_steps"].append(eval_steps)
            history["eval_time"].append(eval_time)
            recent = np.mean(history["ep_restored"][-25:])
            tag = args.tag or args.model
            os.makedirs(args.out, exist_ok=True)
            best_path = os.path.join(args.out, f"{tag}_8500_best.pt")
            last_path = os.path.join(args.out, f"{tag}_8500_ckpt.pt")
            hist_path = os.path.join(args.out, f"{tag}_8500_history.json")
            saved_best = False
            if eval_frac > best_eval:
                best_eval = eval_frac
                torch.save({"state_dict": net.state_dict(), "args": vars(args),
                            "episode": ep, "eval": eval_frac}, best_path)
                saved_best = True
            torch.save({"state_dict": net.state_dict(), "args": vars(args), "episode": ep}, last_path)
            with open(hist_path, "w") as f:
                json.dump(history, f)
            print(f"  [{args.model} ep {ep:4d}] eps={eps:.3f} train_recent={recent*100:.1f}% "
                  f"eval={eval_frac*100:.1f}% best={best_eval*100:.1f}%{'*' if saved_best else ''} "
                  f"steps={eval_steps:.1f} t={eval_time:.2f}s buf={rb.size}", flush=True)

    print(f"[train] DONE. ckpt={ckpt_path} history={hist_path}")


if __name__ == "__main__":
    main()
