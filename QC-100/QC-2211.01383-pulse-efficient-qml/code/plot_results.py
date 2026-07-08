"""Plot CX-count and accuracy comparison from results.json."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

R = Path(__file__).resolve().parents[1] / "report" / "evidence" / "results.json"
data = json.loads(R.read_text())

experiments = [k for k in data.keys() if isinstance(data[k], dict) and "comparison" in data[k]]
labels, std_cx, pei_cx, std_acc, pei_acc = [], [], [], [], []
for k in experiments:
    v = data[k]
    labels.append(k)
    std_cx.append(v["standard_full_entanglement"]["circuit"]["cx"])
    pei_cx.append(v["pulse_inspired_linear"]["circuit"]["cx"])
    std_acc.append(v["standard_full_entanglement"]["metrics"]["test_acc"])
    pei_acc.append(v["pulse_inspired_linear"]["metrics"]["test_acc"])

x = np.arange(len(labels))
w = 0.35

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].bar(x - w/2, std_cx, w, label="Standard (full entanglement)", color="#c93b3b")
axes[0].bar(x + w/2, pei_cx, w, label="Pulse-inspired (linear entanglement)", color="#3b7cc9")
axes[0].set_ylabel("CX (CNOT) count after transpile")
axes[0].set_title("Circuit CX gate count\n(paper Fig.2c analog: PE circuits shorter)")
axes[0].set_xticks(x, labels, rotation=25, ha="right")
axes[0].legend()
axes[0].grid(True, axis="y", alpha=0.3)
for i, (s, p) in enumerate(zip(std_cx, pei_cx)):
    axes[0].text(i - w/2, s + 0.5, str(s), ha="center", fontsize=9)
    axes[0].text(i + w/2, p + 0.5, str(p), ha="center", fontsize=9)

axes[1].bar(x - w/2, std_acc, w, label="Standard (full entanglement)", color="#c93b3b")
axes[1].bar(x + w/2, pei_acc, w, label="Pulse-inspired (linear entanglement)", color="#3b7cc9")
axes[1].set_ylabel("Test-set classification accuracy")
axes[1].set_title("Classification accuracy\n(paper Fig.2b analog: accuracy retained/improved)")
axes[1].set_ylim(0, 1)
axes[1].set_xticks(x, labels, rotation=25, ha="right")
axes[1].legend()
axes[1].grid(True, axis="y", alpha=0.3)
axes[1].axhline(0.5, color="gray", linestyle="--", alpha=0.5, label="chance")
for i, (s, p) in enumerate(zip(std_acc, pei_acc)):
    axes[1].text(i - w/2, s + 0.01, f"{s:.2f}", ha="center", fontsize=9)
    axes[1].text(i + w/2, p + 0.01, f"{p:.2f}", ha="center", fontsize=9)

plt.tight_layout()
out = R.parent / "cx_and_accuracy.png"
plt.savefig(out, dpi=140)
print(f"Wrote {out}")
