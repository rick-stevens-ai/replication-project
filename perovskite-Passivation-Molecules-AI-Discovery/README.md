# Generative AI-Driven Accelerated Discovery of Passivation Molecules for Perovskite Solar Cells

- **Authors:** Fajar, Lambard, Manopo, Guo, Septioga, Pari, Matsushima, Guo
- **Journal:** Advanced Science, 2026
- **DOI:** 10.1002/advs.202523042
- **Rank:** #11 (user-selected)
- **Code:** https://github.com/adroitfajar/pvmol-gen

## Why This Paper
AI-driven framework integrating discriminative (SMILES-X) and generative (GPT-2) language models to discover passivation molecules for perovskite solar cells. Fully computational pipeline producing 100,000+ novel molecules, filtered to ~8000 candidates. Experimentally validated with 19.3% -> 22.2% PCE improvement.

## Replication Plan
1. Reproduce SMILES-X classifier training on literature dataset (314 molecules)
2. Fine-tune GPT-2 on effective passivation molecules (Data T1)
3. Run iterative generation-screening pipeline (3 cycles)
4. Apply multi-criteria filtering and clustering
5. Validate predictions against reported results
6. DFT calculations for molecule-surface interaction

## Status
- [ ] Paper reviewed
- [ ] Code repo cloned and tested
- [ ] Data identified
- [ ] SMILES-X classifier reproduced
- [ ] GPT-2 generative model reproduced
- [ ] Filtering pipeline reproduced
- [ ] DFT calculations reproduced
- [ ] Results validated
