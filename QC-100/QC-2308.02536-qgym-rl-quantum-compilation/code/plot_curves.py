#!/usr/bin/env python3
"""Plot training curves from scheduling_results.json to mirror paper Fig. 4."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "report" / "evidence"
d = json.loads((OUT / "scheduling_results.json").read_text())

len_curve = d["training_curve_episode_length_deciles"]
rew_curve = d["training_curve_episode_reward_deciles"]

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
xs = [10 * (i + 1) for i in range(len(len_curve))]  # % of training
ax[0].plot(xs, len_curve, "o-", color="tab:blue")
ax[0].set_xlabel("Training progress (% of 100k steps)")
ax[0].set_ylabel("Mean episode length")
ax[0].set_title("(A) Mean episode length ↓")
ax[0].grid(alpha=0.3)

ax[1].plot(xs, rew_curve, "s-", color="tab:orange")
ax[1].set_xlabel("Training progress (% of 100k steps)")
ax[1].set_ylabel("Mean episode reward")
ax[1].set_title("(B) Mean episode reward ↑")
ax[1].grid(alpha=0.3)

plt.suptitle("Replication of arXiv:2308.02536 Fig. 4 (qgym Scheduling PPO)")
plt.tight_layout()
out_png = OUT / "training_curves.png"
plt.savefig(out_png, dpi=120)
print(f"wrote {out_png}")
