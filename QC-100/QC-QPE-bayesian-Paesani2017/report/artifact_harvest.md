# Artifact Harvest

| Artifact | Source | Type | Size / checksum |
|----------|--------|------|-----------------|
| Paesani et al. 2017 full text | https://ar5iv.org/abs/1703.05169 | HTML (ar5iv) | 663,656 B; md5 52cfe59251fb2b452c0fb33a8c3b9ba0 |
| Wiebe & Granade 2016 (RFPE method) | https://ar5iv.org/abs/1508.00869 | HTML (ar5iv) | 709,406 B; md5 5e4a13699a4eb735b596931bacef08f7 |
| Paesani plain text | derived (tag-strip) | txt | work/paesani_text.txt |
| Wiebe plain text | derived (tag-strip) | txt | work/wiebe_text.txt |
| H2/STO-3G FCI PES reference values | O'Malley et al. 2016 (PRX 6, 031007) standard STO-3G energies, hardcoded | data | 16 (R, E_FCI) pairs in qpe_replicate.py |

Tools: Python 3, NumPy 2.4.3, Matplotlib 3.10.8. LLM judge: Argo gpt-5.2 (free, localhost:44497).
No paid `pdf` tool used; arXiv/ar5iv fetched via curl. No hardware; no paid inference.
