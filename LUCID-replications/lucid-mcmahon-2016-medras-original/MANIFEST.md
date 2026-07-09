# Artifact Manifest — LUCID slot 62 (Wave 7)

McMahon SJ et al. 2016, *Sci. Rep.* **6**:33290.
DOI: 10.1038/srep33290 · License: CC BY 4.0.

All SHA-256 verified 2026-06-09.

## Upstream artifacts (as fetched)

| File | Bytes | SHA-256 | Source URL |
|---|---:|---|---|
| `artifacts/srep33290.pdf` | 1,335,397 | `f0133d37a7b67f64cd9be72361e530b222e50e0d7e427b277220e89cd9527080` | `https://www.nature.com/articles/srep33290.pdf` |
| `artifacts/supplementary_methods.pdf` | 768,472 | `74b53d56511e04fbea9507ddd85951213fc783d8131f25f0b09fb0c284337b7c` | `https://static-content.springer.com/esm/art%3A10.1038%2Fsrep33290/MediaObjects/41598_2016_BFsrep33290_MOESM1_ESM.pdf` |
| `artifacts/supplementary_code.zip` | 27,856 | `c342c2573c8af3ad29deccaf654c9659861cbc3497a0595892980fc8145c0efe` | `https://static-content.springer.com/esm/art%3A10.1038%2Fsrep33290/MediaObjects/41598_2016_BFsrep33290_MOESM2_ESM.zip` |

## Derived (subagent-produced) artifacts

| File | SHA-256 | Notes |
|---|---|---|
| `artifacts/srep33290.txt` | `6899a26e478bef0e78c53a682fb1a5b46a7afd38c61389adb306b441991c10f5` | `pdftotext -layout` extract |
| `code_py3/CharacteriseCell.py` | `7cb6d798b5e73624e01b7a74a323d62693a21f11a9c2fe69ed0dd63e895e2346` | Py3 port (xrange→range, print→print()) |
| `code_py3/CellDNAModel.py` | `d04e75f6f6eebf69051510ff7d74e3959441d40047b2f88df2539af149eb4dc8` | Py3 port |
| `code_py3/SurvivalModel.py` | `3ef5a673aaf5fae903c8873a273ee70188eeb91a633211ce123ae58b4119ec59` | Py3 port |
| `code_py3/DNAModelFit.py` | `fb8fae9218d3f2d349bc1a35061a240e49d264c34716bdcdd8737f3f865a67be` | Py3 port + `list(map(float, row))` |
| `code_py3/SurvivalFit.py` | `1e30abd2709d5ce2b50871ae6169c6fb07125fe882d231ecdb2f8d957ba251e9` | Py3 port |
| `code_py3/CellModelOutputs.py` | `d312399a3bcb38a3b9d42a1e85d7f2020e2c4ce4980337f3abcf1adcdb933b43` | Py3 port |
| `code_py3/Full DNA Data Sets.csv` | `a0c764370127a429c86963cc5ed658f6774ae92f100977446b2b6f7fabc134ae` | Unchanged copy of upstream CSV |
| `code_py3/Full Survival Data Sets.csv` | `1e01c94663fad64f542aba7843b9591a3fc86400837b33a74a5f913bc8f15f65` | Unchanged copy of upstream CSV |
| `scripts/plot_survival.py` | `20447100eff3f7ed91f001fdfc31706c957f4e5d57895895a06bd660e6e53595` | Local plotting helper |
| `results/Model Data - Survival.tsv` | `6a2c65aa54a69ddec9d0f3400af3fd5ab00348157a872919c36d24f6d1b28f10` | Fig. 5 model curves |
| `results/Model Data - Foci Yields.tsv` | `3995e82ea6d7cf7a744e8638ccee73540e414639ba480e24273e0dc84dddcce9` | Fig. 1 model curves |
| `results/Model Data - Misrepaired Breaks.tsv` | `a61ca5804add7d5538c29d56aca3885c071d11afd923e4152f64e428f03967c2` | Fig. 2 model curve |
| `results/Model Data - Aberration Yield.tsv` | `ad949484473b8c1186b3b1162405a3479a1bca5438abeb73fb129158109b89da` | Fig. 3a model curves |
| `results/Model Data - Aberration Kinetics.tsv` | `a192c5a3f2a246a3e942807168e1aabd981f1e4af13c52ef81b2ea6eacfabc77` | Fig. 3b model curves |
| `results/Model Data - Mutation Yield.tsv` | `43ee9a278ad4c26b53fdaee41614d48dce7b65f14fc6cc25112c23da9ce4e0c3` | Fig. 4 model curve |
| `figures/fig5_reproduction_survival.png` | `96d835c2e5f72bc8cce345194e6c59a44cde15127de63ffdd3571c1d63314ae1` | 4-panel survival plot |
| `logs/dna_fit.log` | — | Captured stdout of `DNAModelFit.py` |
| `logs/survival_fit.log` | — | Captured stdout of `SurvivalFit.py` |
| `logs/cell_model_outputs.log` | — | Captured stdout of `CellModelOutputs.py` |

## Minimal Py2 → Py3 patch list (applied to `code_py3/*.py`)

1. `s/\bxrange\b/range/g` — applied to all six modules.
2. Wrap bare `print …` lines as `print(…)` — applied to all six modules.
3. `DNAModelFit.py` line 58: `row=map(float,row)` → `row=list(map(float,row))`
   (Py3 `map` returns an iterator; downstream code slices `row[0:-2]`).

No algorithmic changes.
