# Talk vs. action in the robotaxi race: what six companies' SEC filings actually say

*edgar-autonomy, a primary-source study built only from SEC filings. Tyler Contorno, 2026.*

## The question

Robotaxis and self-driving are among the most hyped topics in large-cap tech and autos.
Press releases and earnings calls are full of them. But what do these companies put **in
their SEC filings**, the documents that carry legal liability?

For six companies we measure, over time:

1. **Attention:** how much each company talks about autonomy;
2. **Quantification:** which hard operational numbers (miles, rides, cities, fleet,
   safety) it actually discloses;
3. **Stance:** whether the language is confident or hedged, positive or negative, once
   the boilerplate in risk factors is controlled for.

Every data point traces back to the exact sentence and SEC document it came from.

## Data

| | |
|---|---|
| Companies (CIK verified against EDGAR) | Tesla (1318605), Alphabet/Waymo (1652044), Uber (1543151), Lyft (1759509), GM/Cruise (1467858), Amazon/Zoox (1018724) |
| Forms | 10-K, 10-Q, 8-K (with EX-99 press-release exhibits); amendments excluded |
| Period | filed 2019-01-02 to 2026-09-29: fiscal periods through Q2 2026; filing-quarter 2026Q3 is partial |
| Corpus | **762 filings, 1,137 documents** (762 primary documents + 375 EX-99 exhibits), 9.27M words |
| Source | EDGAR only (free; descriptive User-Agent, ≤5 requests/s). Earnings-call transcripts are out of scope (no clean free source) |
| Gaps (flagged, never silent) | Uber and Lyft IPO'd in 2019, so there are no 2019Q1 filings and no 2019 10-K; 19 amendments excluded; 2026Q3 partial |

Waymo, Cruise and Zoox are not SEC registrants. Everything about them comes from their
parents' filings, which is part of the story.

## Methods by phase

**M1 – Corpus.** The EDGAR client (`edgar_min`) and HTML cleaner (`clean.py`) are reused
unchanged from edgar-tok. Each CIK was verified by name and ticker before fetching. For
8-Ks, EX-99 exhibits are included, because the cover document usually carries no content.
Zero fetch or clean errors.

**M2 – Attention.** A curated keyword set is split into two tracked groups:
*robotaxi-service* (robotaxi, driverless, rider-only, teleoperation, Waymo, Cruise, Zoox, …)
and *autonomy-tech* (autonomous vehicle, self-driving, ADAS, Autopilot, FSD, Super Cruise, …).
- **Matching:** word boundaries everywhere; case-sensitive matching for product names and
  acronyms that double as common words (Cruise, Aurora, AV, FSD); exclusions for "Super
  Cruise", "cruise control" and Amazon's Aurora database.
- **What counts:** hits in table rows, and hits that only name an AV unit in a financing or
  corporate-transaction sentence, are kept but **not counted**.
- **Metrics:** mention rate per 1,000 words and share of filings mentioning, per company
  per quarter, with a breakout by form and a flag for spikes driven by one dense document.

**M3 – Quantification.** Regex finds numbers attached to metric units, with about 15
documented rejection rules (currency, speeds, ranges, "vehicle" as a modifier, product
names, slide page numbers, chart-axis ticks…).
- **Local model:** a cross-encoder (`BAAI/bge-reranker-v2-m3`, fp32, offline on the local
  GPU) acts as a relevance gate. It never sets a value.
- **Citation check (the edgar-verify method):** the stored sentence must match the cleaned
  filing at its offsets, the value text must match the sentence at its span, and
  re-parsing must give the stored number. **0 rows failed.**
- **Qualifiers** are stored as fields: bound, cumulative vs per-period, driverless vs
  safety driver vs driver-assist, paid vs testing, actual vs target vs commitment, entity,
  and company vs third-party.

**M4 – Stance.** Loughran-McDonald (2018) Negative, Positive, Uncertainty, Litigious and
Constraining lists, plus a hedging measure (LM weak modals + *believe*) and a separate
forward-looking measure (*intend, expect, plan, anticipate*).
- **What is scored:** only the autonomy sentence itself, or ±25 words around the term when
  the sentence is over 60 words.
- **Section control, both ways:** (a) every passage is tagged by filing section and every
  metric is reported by section; (b) every rate is also reported **relative to the
  non-autonomy text of the same section in the same filings**.

All analysis is local and free: no paid API was used at any step.

## Findings

### 1. Attention: GM talks about robotaxis most; the actual operators barely appear

Robotaxi-service mentions per 1,000 words, pooled 2019–2026:
- **GM 1.04** (48% of filings mention it)
- Uber 0.11, Tesla 0.09, Lyft 0.06
- **Alphabet 0.02, Amazon 0.03**

Waymo and Zoox, the two companies actually running driverless services, are nearly
invisible in their parents' filings.

**Tesla's robotaxi language is near zero through 2023**, then rises to 0.08 (2024),
0.23 (2025) and 0.72 per 1k (2026 YTD) around the June 2025 Robotaxi launch. Four of those
quarters are flagged as spikes driven by a single document.

*Validation (fresh random sample, rules frozen before drawing; 15 hits per company):*
- **Wrong-sense false positives: 1/90 = 1.1%** (95% CI 0.2–6.0%).
- **Strict precision** (sentence genuinely about autonomy): **84.4%** (75.6–90.5%).

### 2. The quantification gap: 29 numbers in 1,137 documents

Across the **text** of 1,137 documents, the six companies disclosed **29 distinct
operational autonomy numbers**: 27 their own, plus 2 U.S.-average crash benchmarks quoted
by Tesla.

| Company | Numbers | What they are about | Notably never quantified |
|---|---|---|---|
| Tesla | 13 (11 + 2 benchmarks) | FSD (Supervised) 5, Autopilot 3, Robotaxi 3, all mileage driver-supervised | Robotaxi miles, rides or fleet (chart images only) |
| GM | 7 | **all Super Cruise** | **Cruise: 0 numbers in 7 years** |
| Amazon | 4 | Zoox: ~2M miles, 350k+ riders, 6th and 8th test cities | anything before 2025 |
| Lyft | 2 | 100k+ partner rides (Aptiv; Motional, paid), both with safety drivers | anything after 2021 |
| Uber | 2 | 100k autonomous freight miles; commitment to buy 20k+ Nuro/Lucid vehicles | its own AV-partner rides or miles |
| Alphabet | 1 | Waymo: 500k+ fully autonomous rides a week (Q1 2026) | Waymo miles, cities, fleet, safety |

**The only driverless operating number in seven years of filings is Waymo's weekly ride
count.**

*Validation (seeded 20-row sample of the frozen v1 extractions):*
- Number correct **20/20 = 100%** (CI 84–100%).
- Number plus what it measures correct **19/20 = 95%** (76–99%).
- Every qualifier also correct **16/20 = 80%** (58–92%).

A full check of all 37 v1 rows found no wrong number, 2 wrong claims and 7 wrong
qualifiers. All were fixed in v2 and the final 35 rows re-checked clean. That re-check
uses the same rows, so the v1 sample is the independent estimate.

### 3. Talk vs. action runs in reverse

Company-reported numbers per 100 counted autonomy mentions:

| | Uber | Lyft | GM | Tesla | Alphabet | Amazon |
|---|---|---|---|---|---|---|
| Mentions | 2,012 | 1,798 | 2,000 | 1,308 | 36 | 64 |
| Numbers | 2 | 2 | 7 | 11 | 1 | 4 |
| **Numbers per 100 mentions** | **0.10** | **0.11** | **0.35** | **0.84** | **2.8** | **6.3** |

The companies that talk most about autonomy (Uber, Lyft and GM, largely in risk factors)
back it with the fewest numbers. The companies that own operating robotaxi services
(Alphabet, Amazon) mention it least but almost only to report something. The small-count
ratios (Alphabet 1, Amazon 4) are descriptive, not estimates.

### 4. Stance: the "negative about autonomy" picture is a risk-factor artifact

40% of autonomy passages sit in risk factors. Read without a control, every company looks
negative: net tone (positive − negative per 1k words) is −20.8 for Lyft, −7.7 Uber,
−6.6 GM, −5.9 Tesla. Two controls change the picture.

- **(a) By section:** inside risk factors, autonomy language is **less** negative than the
  risk factors around it, for every company with risk-factor passages (Tesla +9.4, GM
  +9.9, Lyft +13.6, Uber +23.5 vs the same section).
- **(b) Outside boilerplate, relative to baseline** (95% bootstrap CI over passages):

| Company | Net tone vs same-section baseline |
|---|---|
| Alphabet | **+36.4** (26.0 to 48.0) |
| Amazon | **+32.2** (26.8 to 37.0) |
| Uber | **+20.4** (17.4 to 23.5) |
| GM | **+9.6** (6.4 to 12.9) |
| Tesla | **+6.2** (1.9 to 10.3) |
| Lyft | **+0.5** (−4.0 to 4.8): no different from baseline |

Five of six companies write about autonomy measurably more positively than about the rest
of the same sections; Lyft is indistinguishable. Autonomy passages are also less uncertain
than baseline for all six (−3 to −10 per 1k).

*Validation (15 most positive + 15 most negative + 15 most hedged passages):*
- **v2 (final): 36/45 = 80%** (CI 66–89%): negative 13/15, hedged 13/15, positive 10/15.
  **Cohen's kappa 0.73** (bootstrap 95% CI 0.57–0.87), over four categories (positive,
  negative, hedged, off-target).
- v1 (scoring a ±1-sentence window): 34/45 = 75.6% (61–86%), with negative only 8/15;
  kappa 0.67 (0.52–0.81).
- The v2 sample is a fresh draw with no overlap with v1.
- **This is an upper bound, not an accuracy estimate.** The 45 passages are a stratified
  sample of extremes, the 15 highest-scoring passages in each class, not a random sample.
  Extremes are easier to classify than the ambiguous middle of the distribution.
- **Who rated, and blinding.** The rater was Claude, the AI assistant that built the scorer,
  not a human. It saw the model's label before deciding (each sample ID names the label, e.g.
  `most_positive-14`). This was **unblinded self-rating**. All 9 disagreements are passages
  the rater judged off-target; it never assigned the opposite stance.
- Kappa is computed on this constructed sample, whose 15/15/15 label mix was fixed by design.
  It does not generalize to the full corpus.

### 5. GM: the robotaxi language is a wind-down, and it turns in late 2023

GM's robotaxi passages, outside risk factors and legends:
- **Tone vs baseline:** about **+20 per 1k** through 2021, **+5 to +10** in 2022–23, and
  **negative from 2023Q4** (−3 to −10 in most quarters since).
- **Wind-down vocabulary** (wind down, no longer fund, pause, restructur-…): **0%** of
  passages 2019–22, **30%** in 2024, **79%** in 2026.
- **Expansion vocabulary:** from ~30% to 7%.

2025+ vs 2019–2024 (permutation test, 20,000 shuffles):
- net tone **−0.8 → −14.7** per 1k (p < 0.001)
- negative **7.7 → 16.8** (p < 0.001)
- wind-down vocabulary **7% → 66%** (p < 0.001)
- constraining language **falls** (4.3 → 1.2, p = 0.04)

The negativity is financial (restructuring, losses, termination, impairment), not
regulatory. The turn begins at the October 2023 pedestrian accident and pause, a year
before the December 2024 decision to stop funding Cruise's robotaxi work. GM's high M2
attention in 2024–25 is mostly the language of shutting Cruise down.

## Limitations

- **Lexicon positive class.** Loughran-McDonald counts *gain*, *benefit* and *collaborat-*
  whatever the subject. With sentence-only scoring, short accounting sentences ("gain from
  the sale of … Yandex Self Driving", GM's "benefit from reduced expenses at Cruise") top
  the positive ranking; 10/15 positive extremes matched the rater's read. The same-section
  baseline absorbs much of this, because the surrounding text uses the same accounting
  words, but positive-tone levels should be read with care.
- **Wording vs events.** A lexicon measures language, not facts. GM's December 2024 release
  frames the Cruise wind-down positively. Wind-down and expansion vocabulary are reported
  next to tone for that reason.
- **Chart-only figures were deliberately not extracted.** Tesla's paid Robotaxi miles and
  FSD-miles-by-version appear only as chart images. In filing text they are axis ticks,
  which the extractor rejects rather than guessing. The quantification count is a count
  of numbers stated **in text**.
- **Risk-factor control.** Absolute tone is dominated by risk factors (40% of passages)
  and forward-looking legends. Every stance number in the findings is section-tagged and
  baseline-relative; absolute rows are kept only to show the trap. The section tagger was
  spot-checked at 29/30.
- **Validation accuracies by phase:**

| Phase | What was checked | Result |
|---|---|---|
| M1 | CIKs vs EDGAR; fetch and clean | 6/6 verified; 0 errors |
| M2 | fresh 90-hit sample, frozen rules | 1.1% wrong-sense (0.2–6.0); 84.4% strict precision (75.6–90.5) |
| M3 | seeded 20-row sample, frozen v1 | values 100% (84–100); value + claim 95% (76–99); all qualifiers 80% (58–92); citation check 0 failures |
| M4 | 45 extremes (15 per class, not random), fresh v2 draw, unblinded self-rating by Claude | 80% match (66–89), an upper bound; kappa 0.73 (0.57–0.87); v1 was 75.6% |

- **One coder.** All labels were set by one reviewer (Claude, with Tyler approving each
  rule change). There is no inter-rater agreement measure. For M4 the rater also saw the
  model's label before deciding; the kappa above is model-vs-rater agreement, not
  inter-rater agreement.
- **Bootstrap CIs on stance** resample passages independently. Boilerplate repeats across
  filings make passages correlated, so the intervals are somewhat narrow.
- **Small samples.** Alphabet (22 non-boilerplate passages, 1 number) and Amazon (36, 4)
  are too small for quarterly trends; read them pooled.
- **Coverage.** Earnings-call transcripts, where most operational numbers are spoken, are
  out of scope (no clean free source). The study measures what reaches the legal record.

## Reproducibility

Windows / PowerShell, from the repo root. Re-activate the venv in every new window.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
python -m pip install -r requirements.txt

$env:EDGAR_USER_AGENT = "Tyler Contorno tyler.contorno1234@gmail.com"   # optional; this is the default
python scripts\fetch_corpus.py --verify-only
python scripts\fetch_corpus.py           # resumable, <=5 req/s
python scripts\clean_index.py            # M1
python scripts\count_mentions.py match   # M2
python scripts\count_mentions.py aggregate
python scripts\extract_metrics.py        # M3 (needs the bge-reranker-v2-m3 weights in .hf_cache\)
python scripts\m3_summary.py
python scripts\tone.py passages          # M4
python scripts\tone.py aggregate
python scripts\export_dashboard.py       # M5 tidy CSVs -> data\dashboard\
```

Validation scripts (re-print the accuracy tables from the stored labels):
- `scripts\label_round3.py` (M2)
- `scripts\label_m3.py`, `scripts\label_m3_v2.py` (M3)
- `scripts\label_m4.py` (M4)

Seeds are fixed in each script. Phase notes with every rule and decision:
`docs/M2_NOTES.md`, `docs/M3_NOTES.md`, `docs/M4_NOTES.md`.
