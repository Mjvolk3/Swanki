---
id: ni9j9eixdap9l8hiqk31m49
title: 134811 Outline
desc: ''
updated: 1773603474582
created: 1773603474582
---

# 12-Slide Lit Review Outline: Merzbacher et al. 2025 -- Flux Cone Learning

**Paper:** Accurate prediction of gene deletion phenotypes with Flux Cone Learning
**Authors:** Charlotte Merzbacher, Oisin Mac Aodha, Diego A. Oyarzun
**Journal:** Nature Communications (2025) 16:8492

---

## Slide 1: Title Slide

- Title, authors, affiliation (University of Edinburgh)
- Nature Communications, September 2025

## Slide 2: Motivation -- Why Predict Gene Deletion Phenotypes?

- Gene deletions impact cell function, proliferation, environment interaction
- Applications: cancer therapy targets, antimicrobial resistance, metabolic engineering
- Genome-wide deletion screens (CRISPR/RNAi) are costly and condition-specific
- Computational prediction fills gaps, extrapolates, prioritizes experiments

## Slide 3: The FBA Limitation

- Flux Balance Analysis (FBA) = gold standard for metabolic gene essentiality
- FBA assumes cells optimize an objective (e.g., growth)
- Works well in microbes, but optimality assumption breaks in higher organisms
- Need: objective-free prediction from the structure of metabolism itself

## Slide 4: Key Insight -- Learning from Flux Cone Geometry

- GEM defines feasible metabolic space (Sv=0, flux bounds)
- Gene deletion = zeroing reaction bounds = slicing the polytope
- FBA picks one optimal point; FCL samples the entire feasible region
- Learn correlations between cone shape changes and phenotype
- **Fig 1** (pipeline overview)

## Slide 5: FCL Pipeline End-to-End

- Step 1: Build deletion-specific GEMs via GPR rules
- Step 2: Monte Carlo sampling (OptGPSampler -- hit-and-run random walk)
- Step 3: Train supervised ML (random forest, HGB) on flux samples + fitness labels
- Step 4: Aggregate sample-level predictions to gene-level
- Feature matrix: X in R^(kq x n), k deletions, q samples, n reactions

## Slide 6: E. coli Essentiality Results

- FCL achieves ~95% accuracy on iML1515 (1202 deletions, 2712 reactions)
- Outperforms FBA in accuracy, precision, recall, F1
- Essential gene prediction: FCL 98% vs FBA 82%
- Shallow sampling sufficient: 10-100 samples/cone match or exceed FBA
- **Fig 2a,b**

## Slide 7: Interpretability and Feature Importance

- Sample-level prediction score distributions distinguish essential from non-essential
- Top predictive reactions: transport and exchange reactions dominate
- A few hundred reactions explain most predictive power
- Jensen-Shannon / Hellinger distance defines deletion-to-wildtype metric
- **Fig 2c,d**

## Slide 8: Learned Metabolic Representations (Fig S2)

- VAE trained on flux samples from 5 bacterial pathogens (shared reactions only)
- t-SNE of 8-dim embeddings shows species-specific clustering
- Flux cone geometry is learnable from Monte Carlo samples
- Path toward metabolic foundation models across species
- **Supplementary Fig S2** (VAE t-SNE)

## Slide 9: Higher-Order Organisms -- Yeast and CHO

- S. cerevisiae: FCL AUROC 0.78 vs FBA 0.69 (5-fold CV)
- CHO cells: FCL AUROC 0.72 vs FBA 0.62
- Performance gains more pronounced where optimality assumptions degrade
- Class imbalance challenge (most genes non-essential)
- **Fig 3a,b**

## Slide 10: Beyond Essentiality -- Predicting Small Molecule Production

- Betaxanthin production in S. cerevisiae deletion library (4223 deletions)
- 3-class prediction: low/medium/high producers
- Best model (HGB + rebalancing): 69.8% accuracy
- Does NOT require heterologous pathway in GEM
- First demonstration: small molecule production predictable from deletion screens
- **Fig 4a,b,c**

## Slide 11: Discussion and Limitations

- FCL requires labeled deletion screen data (not zero-shot like FBA)
- Sampling is computationally expensive (3-13 GB per organism)
- Predictive power depends on phenotype-metabolism coupling
- Deep learning (feedforward, CNN) did not improve over RF -- linear constraint structure
- PCA dimensionality reduction hurts: high-D boundary info needed

## Slide 12: Takeaways and Future Directions

- Paradigm shift: from "optimize assumed objective" to "learn from feasible space shape"
- FCL broadly applicable: any organism, any metabolic phenotype
- Foundation models: large-scale sampling across species and conditions
- Future: better samplers, multi-omics integration, GEM-aware architectures
- Strain engineering: identify knockouts for improved production
