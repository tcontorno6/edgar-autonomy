# Stance validation samples (M4)

`stance_validation_v1.csv` and `stance_validation_v2.csv` (v2 is the published 80%) each hold
45 passages: the 15 scored most positive, the 15 most negative and the 15 most hedged. They are
constructed samples of extremes, not random draws.

The `human_label` column name is historical. The labels were set by Claude, the AI assistant that
built the scorer, not by a human, and the rater could see `model_label` (and the sample ID, which
names it) while labeling: unblinded self-rating. `analysis/stance_kappa.py` computes Cohen's kappa
from these files (v2: 0.73, bootstrap 95% CI 0.57 to 0.87).
