# edgar-autonomy

What six robotaxi and autonomy companies (Tesla, Alphabet/Waymo, Uber, Lyft, GM/Cruise, Amazon/Zoox) say about autonomy in their SEC filings, 2019 to 2026. The corpus is 762 filings (10-K, 10-Q, 8-K), 1,137 documents. It was built only from SEC EDGAR, with local models and no paid APIs.

- **Dashboard:** https://tcontorno6.github.io/edgar-autonomy/
- **Dataset:** https://huggingface.co/datasets/tcontorno/edgar-autonomy
- **Methodology and findings:** [WRITEUP.md](WRITEUP.md)
- **Data dictionary:** [data/README.md](data/README.md)

## Contents

| Path | What it is |
|---|---|
| `index.html` | Self-contained dashboard (served by GitHub Pages) |
| `WRITEUP.md` | Methodology, validation and findings |
| `data/*.csv` | Derived tidy tables: attention, quantification, stance vs baseline, GM wind-down |
| `data/validation/`, `analysis/stance_kappa.py` | The two 45-passage stance validation samples (v1, and the fresh v2 draw behind the published 80%) and the Cohen's kappa calculation |
| `prereg/winddown_v3/` | Pre-registered protocol, freeze record and frozen file for the out-of-sample GM wind-down test |

The pipeline code (EDGAR download, cleaning, keyword attention, number extraction, stance scoring) will be added in a follow-up commit. Raw filings, the model cache and the Loughran-McDonald lexicon are not redistributed.

## License

MIT
