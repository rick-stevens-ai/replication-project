# Artifact Harvest — OSTI 3367074

| Artifact | Source | Local path | Size | SHA-256 (prefix) |
|---|---|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/3367074 | `work/paper.pdf` | 1,562,174 B | `ce11f5d5…4182eff9` |
| AME2016 mass table | https://www-nds.iaea.org/amdc/ame2016/mass16.txt | `work/mass16.txt` | 418,937 B | `2167f57a…b4b9218a` |
| AME2020 mass table | https://www-nds.iaea.org/amdc/ame2020/mass_1.mas20.txt | `work/mass_1.mas20.txt` | 472,648 B | `e8599c6d…ed2a3307` |
| Parsed AME2016 (experimental) | derived | `work/ame2016_experimental.csv` | 79,668 B | — |
| Parsed AME2020 (experimental) | derived | `work/ame2020_experimental.csv` | 81,207 B | — |
| GP training subset used | derived | `report/evidence/train_used.csv` | 142,706 B | — |
| AME2020 new-nuclei test set (n=74) | derived | `report/evidence/test_ame2020_new.csv` | 7,154 B | — |
| Numeric replication results | derived | `report/evidence/results.json` | 2,105 B | — |
| Full run log | run output | `work/run.log` | 2,729 B | — |
| Replication code | authored | `work/replicate.py` | 13,928 B | — |

**Paper's own data-availability:** Science Data Bank record `10.57760/sciencedb.j00186.01007` (referenced in the paper) contains their per-model GP-refined predictions but requires manual harvest; we intentionally did NOT pull it so our replication is fully independent from their pre-computed numbers.

**Compute:** uicgpu (8×A100 host, but this run used CPU only — GP fits are ~55 s wall-time on ~1500 training points).
