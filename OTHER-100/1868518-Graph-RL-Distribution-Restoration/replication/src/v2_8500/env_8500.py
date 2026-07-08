"""
8500-bus distribution restoration environment, cell-aggregated.
Sequential-MDP framing matching Zhao & Wang (2022): per step, agent picks
one switchable line to close; reward = incremental restored load fraction.

State representation:
  node_features (n_cells, F):
      [energized, load_pu, has_dg, dg_active, voltage_proxy, faulted, distance_to_root, ones]
  adjacency_open : (n_cells, n_cells)  binary, all switchable + already-closed
  adjacency_closed : (n_cells, n_cells) currently energized backbone
  switch_mask : (n_switches,) 1 if switch is currently OPEN and could be closed

Action space: discrete over n_switches+1 (NoOp last).

Reward per step:
    +1.0 * delta_energized_load / total_load
    -0.2 if action invalid (switch already closed / would create loop / no-op when work remains)
    +5.0 terminal bonus if 100% restoration.
"""
import os, json
import numpy as np


class Env8500:
    def __init__(self, data_path, n_dgs=20, max_steps=80, seed=0,
                 fault_frac=0.05, load_jitter=0.3):
        d = np.load(os.path.join(data_path, "cell_graph.npz"))
        self.cell_adj   = d["cell_adj"].astype(np.float32)         # (C,C) 0/1
        self.cell_load  = d["cell_load_kw"].astype(np.float32)
        self.cell_xy    = d["cell_xy"]
        self.cell_size  = d["cell_size"]
        self.n_cells    = self.cell_adj.shape[0]

        # Switch list = unique edges in cell_adj
        ii, jj = np.where(np.triu(self.cell_adj, k=1) > 0)
        self.switch_edges = np.stack([ii, jj], axis=1)             # (S,2)
        self.n_switches   = self.switch_edges.shape[0]

        # Static features
        self.root_cell = int(np.argmax(self.cell_size))            # substation cell = largest one (proxy)
        self.n_dgs     = n_dgs
        rng = np.random.RandomState(42)
        # Choose DG cells: largest-load cells excluding root
        order = np.argsort(-self.cell_load)
        self.dg_cells = np.array([c for c in order if c != self.root_cell][:n_dgs], dtype=np.int64)
        self.has_dg = np.zeros(self.n_cells, dtype=np.float32)
        self.has_dg[self.dg_cells] = 1.0

        self.max_steps   = max_steps
        self.fault_frac  = fault_frac
        self.load_jitter = load_jitter
        self.rng         = np.random.RandomState(seed)

        # Pre-compute neighbors of each cell
        self.cell_nbrs = [np.where(self.cell_adj[c] > 0)[0] for c in range(self.n_cells)]

        # Pre-compute non-bridge edges so we don't pick faulted_lines that disconnect the graph.
        import networkx as nx
        G = nx.from_numpy_matrix(self.cell_adj)
        bridges = set()
        for u, v in nx.bridges(G):
            a, b = (u, v) if u < v else (v, u)
            bridges.add((a, b))
        edge_to_idx = {(int(self.switch_edges[i,0]), int(self.switch_edges[i,1])): i
                       for i in range(self.n_switches)}
        self.non_bridge_idx = np.array(
            [i for (e, i) in edge_to_idx.items() if e not in bridges], dtype=np.int64)
        # Quiet logging by default.

        self.feat_dim = 8

    # --------------------------------------------------------------
    def _bfs_energized(self):
        """Return mask of cells reachable from root via currently CLOSED switches.
        Faulted cells can still conduct (pass-through) but their load isn't served."""
        mask = np.zeros(self.n_cells, dtype=bool)
        mask[self.root_cell] = True
        frontier = [self.root_cell]
        while frontier:
            nxt = []
            for u in frontier:
                for v in self.cell_nbrs[u]:
                    v = int(v)
                    if mask[v]: continue
                    eid = self._edge_id(u, v)
                    if self.switch_closed[eid]:
                        mask[v] = True
                        nxt.append(v)
            frontier = nxt
        return mask

    def _edge_id(self, u, v):
        # Look up index into self.switch_edges; small (~595) so OK.
        a, b = (u, v) if u < v else (v, u)
        return self._edge_lookup[(a, b)]

    def reset(self):
        # Initialize switch state up-front (used by helpers below).
        self.switch_closed = np.zeros(self.n_switches, dtype=bool)
        self._edge_lookup = {(int(self.switch_edges[i,0]), int(self.switch_edges[i,1])): i
                             for i in range(self.n_switches)}
        # Fault scenario: random LINES permanently faulted (cannot be closed by agent).
        # Cells remain energizable through alternative paths (paper's framing).
        self.faulted_cells = np.zeros(self.n_cells, dtype=bool)
        # Optionally drop a few cells (substation-isolated zones) — keep small.
        n_dead_cells = 0  # cells are always energizable; only line-faults block restoration
        if n_dead_cells > 0:
            cands = np.array([c for c in range(self.n_cells) if c != self.root_cell])
            flt = self.rng.choice(cands, size=n_dead_cells, replace=False)
            self.faulted_cells[flt] = True
        # Faulted lines: a few non-bridges + ensure decent reachability.
        # We re-roll until reachable upper-bound is at least min_ub of total cells.
        self.faulted_lines = np.zeros(self.n_switches, dtype=bool)
        n_line_faults = min(
            len(self.non_bridge_idx),
            max(1, int(self.fault_frac * self.n_switches)))
        min_ub = int(0.6 * self.n_cells)
        for attempt in range(20):
            cand = self.rng.choice(self.non_bridge_idx, size=n_line_faults, replace=False)
            self.faulted_lines[:] = False; self.faulted_lines[cand] = True
            self.switch_closed[:] = ~self.faulted_lines
            reach = int(self._bfs_energized().sum())
            if reach >= min_ub: break
            n_line_faults = max(1, n_line_faults - 1)  # back off
        self.switch_closed[:] = False

        # Load jitter
        self.epi_load = self.cell_load * self.rng.uniform(
            1 - self.load_jitter, 1 + self.load_jitter, size=self.n_cells).astype(np.float32)
        self.epi_load[self.faulted_cells] = 0.0

        self.dg_active = np.zeros(self.n_cells, dtype=np.float32)
        self.dg_active[self.dg_cells] = 1.0  # DGs always available (simplification)

        # Compute upper-bound restorable load (all non-faulted switches closed)
        self.switch_closed[:] = ~self.faulted_lines
        self.reachable_ub = self._bfs_energized()
        self.total_load = max(float(self.epi_load[self.reachable_ub].sum()), 1.0)
        # Reset switches to all-open for episode start
        self.switch_closed[:] = False

        self.step_count   = 0
        self.energized    = self._bfs_energized()
        self.restored     = float(self.epi_load[self.energized].sum())
        self.last_restored = self.restored
        self.invalid_count = 0

        return self._state()

    def _state(self):
        n = self.n_cells
        feats = np.zeros((n, self.feat_dim), dtype=np.float32)
        feats[:, 0] = self.energized.astype(np.float32)
        feats[:, 1] = self.epi_load / max(self.epi_load.max(), 1.0)
        feats[:, 2] = self.has_dg
        feats[:, 3] = self.dg_active
        feats[:, 4] = 1.0 - self.faulted_cells.astype(np.float32)
        feats[:, 5] = self.faulted_cells.astype(np.float32)
        # distance proxy: BFS depth from root (not recomputed each step — approximate by row of adjacency)
        feats[:, 6] = self.energized.astype(np.float32) * 1.0
        feats[:, 7] = 1.0
        # current adjacency among energized switches
        # available action mask: still OPEN and not faulted
        sw_mask = ((~self.switch_closed) & (~self.faulted_lines)).astype(np.float32)
        return {
            "node_features": feats,
            "adjacency": self.cell_adj.copy(),       # static cell graph
            "switch_mask": sw_mask,                  # (S,) — 1 = action available
            "switch_edges": self.switch_edges,       # (S,2)
            "energized": self.energized.copy(),
            "step": self.step_count,
        }

    def step(self, action):
        """action ∈ [0, n_switches] — n_switches = NoOp."""
        info = {"invalid": False, "loop": False}
        reward = 0.0

        if action == self.n_switches:  # NoOp
            reward -= 0.05
            info["invalid"] = False
        else:
            if action < 0 or action >= self.n_switches:
                reward -= 0.2
                info["invalid"] = True
            elif self.switch_closed[action] or self.faulted_lines[action]:
                reward -= 0.2
                info["invalid"] = True
            else:
                u, v = int(self.switch_edges[action, 0]), int(self.switch_edges[action, 1])
                # Loop check: both endpoints already energized -> loop
                if self.energized[u] and self.energized[v]:
                    reward -= 0.3
                    info["loop"] = True
                    self.invalid_count += 1
                else:
                    self.switch_closed[action] = True
                    self.energized = self._bfs_energized()
                    new_restored = float(self.epi_load[self.energized].sum())
                    delta = new_restored - self.last_restored
                    reward += delta / self.total_load
                    self.last_restored = new_restored
                    self.restored = new_restored

        self.step_count += 1
        done = (self.step_count >= self.max_steps) or \
               (self.last_restored / self.total_load > 0.995)
        if done and self.last_restored / self.total_load > 0.995:
            reward += 1.0  # bonus

        return self._state(), reward, done, info

    @property
    def restored_frac(self):
        return self.last_restored / self.total_load


if __name__ == "__main__":
    import sys
    env = Env8500("/gpustor/stevens/projects-active/replicate-1868518/data", seed=0)
    s = env.reset()
    print("cells:", env.n_cells, "switches:", env.n_switches, "DGs:", env.n_dgs,
          "total load (kW):", round(env.total_load, 1), "root:", env.root_cell)
    print("Random rollout sanity check:")
    rng = np.random.RandomState(1)
    total_r = 0.0
    for t in range(80):
        # pick a random open switch where one endpoint is energized
        avail = np.where((s["switch_mask"] > 0))[0]
        # filter to ones with at least one energized endpoint
        en = s["energized"]
        good = []
        for a in avail:
            u, v = env.switch_edges[a]
            if en[u] != en[v] and not (env.faulted_cells[u] or env.faulted_cells[v]):
                good.append(a)
        a = rng.choice(good) if good else env.n_switches
        s, r, d, info = env.step(int(a))
        total_r += r
        if d: break
    print(f"random greedy: steps={env.step_count} restored={env.restored_frac*100:.2f}% reward={total_r:.3f}")
