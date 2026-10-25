# Stance validation samples (M4)

`stance_validation_v1.csv` and `stance_validation_v2.csv` (v2 is the published 80%) each hold
45 passages: the 15 scored most positive, the 15 most negative and the 15 most hedged. They are
constructed samples of extremes, not random draws.

The `human_label` column name is historical. The repository record shows unblinded self-rating
with no second rater: the only statements of who rated name Claude, the AI assistant that built
the scorer, and each row shows `model_label` (and a sample ID that names it). The labeling script
is not in the repository and has not been reviewed. `analysis/stance_kappa.py` computes Cohen's kappa
from these files (v2: 0.73, bootstrap 95% CI 0.57 to 0.87). That kappa is between `model_label`
and the scorer-builder's own unblinded read, so it is not an inter-rater measure; it is no longer
reported as validation. Provenance audit: `PROVENANCE.md`.
