---
id: j79zfagjg81qayut4t0xtku
title: Thornburg Fish Speech Run
desc: 'Standalone run for thornburg after qpdf install'
updated: 1775577447647
created: 1775577447647
---

## Install qpdf

```bash
sudo dnf install -y qpdf
```

## Run thornburg standalone

```bash
conda activate swanki && script -qc "swanki \
  pdf_path=/scratch/projects/torchcell-scratch/Swanki_Data/thornburgBringingGeneticallyMinimal2026/thornburgBringingGeneticallyMinimal2026_clean.pdf \
  citation_key=thornburgBringingGeneticallyMinimal2026 \
  +output_dir=/scratch/projects/torchcell-scratch/Swanki_Data/thornburgBringingGeneticallyMinimal2026/thornburgBringingGeneticallyMinimal2026-fish \
  models=fish_speech \
  audio=all \
  zotero=sync \
  pipeline.processing.confirm_before_generation=false" /dev/null
```

## Batch 1 Status

| Paper | Pages | Status |
|-------|-------|--------|
| cardiffSystemsLevelModelingCRISPRBased2024 | 6 | COMPLETE |
| boobDesignDiverseFunctional2025 | 14 | COMPLETE |
| ryuDeepLearningMetabolic2023 | 9 | COMPLETE |
| avsecAdvancingRegulatoryVariant2026 | 26 | COMPLETE |
| tazzaMINNMetabolicinformedNeural2025 | 8 | COMPLETE |
| kimEnzymeFunctionalClassification2025 | 15 | COMPLETE |
| palssonApproachesAcceleratingMicrobial2026 | 7 | COMPLETE |
| cuiScGPTBuildingFoundation2024 | 18 | COMPLETE |
| merzbacherModelingHostPathway2025 | 9 | COMPLETE |
| dengPathwayEvolutionBottleneckingDebottlenecking2024 | 11 | COMPLETE |
| thornburgBringingGeneticallyMinimal2026 | 39 | FAILED (qpdf missing) |
