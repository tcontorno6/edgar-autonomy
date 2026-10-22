"""Cohen's kappa for the M4 stance validation samples (model label vs rater label).

Usage: python analysis/stance_kappa.py data/validation/stance_validation_v2.csv

The samples are constructed (15 most positive, 15 most negative, 15 most hedged passages),
so kappa here describes agreement on extremes only and does not generalize to the corpus.
"""
import sys

import numpy as np
import pandas as pd

CATS = ["positive", "negative", "hedged", "off-target / other"]


def kappa(a, b):
    m = np.zeros((len(CATS), len(CATS)))
    for x, y in zip(a, b):
        m[CATS.index(x), CATS.index(y)] += 1
    n = m.sum()
    po = np.trace(m) / n
    pe = (m.sum(1) @ m.sum(0)) / n**2
    return (po - pe) / (1 - pe), po, m


def main(path):
    d = pd.read_csv(path)
    k, po, m = kappa(d.model_label, d.human_label)
    rng = np.random.default_rng(20261022)
    a, b = d.model_label.to_numpy(), d.human_label.to_numpy()
    boot = [kappa(a[i], b[i])[0] for i in (rng.integers(0, len(d), len(d)) for _ in range(20000))]
    lo, hi = np.percentile(boot, [2.5, 97.5])
    print(f"n={len(d)}  agreement={po:.3f}  kappa={k:.3f}  bootstrap 95% CI {lo:.2f}-{hi:.2f}")
    print(pd.DataFrame(m.astype(int), index=["model: " + c for c in CATS], columns=["rater: " + c for c in CATS]))


if __name__ == "__main__":
    main(sys.argv[1])
