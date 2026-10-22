# Dashboard data (tidy CSVs)

Built by `python scripts\export_dashboard.py`. One row per observation. Quarters are
**calendar quarters of the filing date** (`quarter` = `2025Q3`; `quarter_start` = ISO date).
Booleans are `True`/`False`. Empty cells mean "not defined" (e.g. no words that
quarter), never zero.

Coverage: 6 companies, 762 filings (10-K, 10-Q, 8-K; 19 amendments excluded), 1,137
documents (primary documents + 375 8-K EX-99 exhibits), filed 2019-01-02 to 2026-09-29.
`2026Q3` is partial (corpus fetched 2026-09-30) and flagged `partial_quarter`.

## 1. `attention.csv`: ATTENTION over time (M2)

372 rows = 6 companies × 31 quarters × 2 groups.

| Column | Meaning |
|---|---|
| ticker, company | TSLA, GOOGL, UBER, LYFT, GM, AMZN; display name |
| quarter, quarter_start | filing quarter |
| group | `robotaxi_service` (robotaxi / driverless-service / deployment terms) or `autonomy_tech` (broader autonomy / ADAS / self-driving tech) |
| mentions | counted keyword hits (prose only; tables and corporate/finance-only mentions excluded) |
| words | words in all documents filed that quarter |
| mention_rate_per_1k_words | mentions / words × 1000 |
| filings, filings_mentioning, share_of_filings_mentioning | filings that quarter, how many have ≥1 mention, ratio |
| top_doc_share | share of the quarter's mentions from its single densest document |
| spike_driven_by_one_doc | rate > 2× trailing 4-quarter median **and** one document holds ≥50% of the mentions |
| risk_factor_share_of_mentions | share of mentions inside Item 1A |
| boilerplate_share_of_mentions | share of mentions whose sentence repeats in 3+ filings |
| no_filings, pre_ipo, partial_quarter | gap flags (Uber and Lyft 2019Q1 have no filings: pre-IPO) |
| gap_flags | full flag string, including `no_10K_expected_2019` and `amendments_excluded=N` |

## 2a. `quantification_summary.csv`: QUANTIFICATION GAP (M3)

6 rows, one per company.

| Column | Meaning |
|---|---|
| distinct_numbers_in_text | distinct operational autonomy numbers found in filing **text** (first disclosures only) |
| company_reported_numbers | of which reported by the company |
| third_party_benchmark_numbers | of which third-party benchmarks the company quotes (Tesla: 2 U.S./NHTSA crash averages) |
| subjects | what the company-reported numbers are about, with counts (e.g. "GM Super Cruise, driver-assist (not Cruise): 7") |
| metrics | counts by metric type (miles_driven, rides, riders, cities, fleet_size, safety_rate, road_coverage_miles) |
| first_number_filed, last_number_filed | date range of the numbers |
| notably_never_quantified | what a reader would expect but the filings never put a number on |
| autonomy_mentions_2019_2026 | counted M2 mentions, both groups, whole period |
| company_numbers_per_100_mentions | company_reported_numbers / mentions × 100: the "talk vs action" ratio |

## 2b. `quantification_numbers.csv`: the 29 numbers behind 2a (M3)

| Column | Meaning |
|---|---|
| filed, quarter, subject, metric | when, about what |
| value, value_text, unit | parsed number; the exact text in the filing; unit |
| bound | exact / approx / lower_bound / upper_bound |
| period_basis | cumulative / per_week / per_month / per_quarter / increment / point_in_time / rate |
| supervision | driverless / safety_driver / driver_supervised_adas / not_applicable / unspecified |
| commercial, status, reporter | paid/testing/…; actual / target_or_plan / commitment; company / third_party_benchmark |
| confidence, review | high / medium / low; `keep` if a low row was human-reviewed |
| source_sentence, source_url | the verified sentence and the SEC document URL |

## 3. `stance_vs_baseline.csv`: STANCE vs baseline (M4)

712 rows, one per company × quarter × section with ≥1 autonomy passage.

| Column | Meaning |
|---|---|
| section | risk_factors, fls_legend, mdna, business, financial_statements, earnings_exhibit, 8k_body, legal, other, or `ALL_ex_boilerplate` (everything except risk_factors and fls_legend) |
| is_boilerplate_section | risk_factors or fls_legend |
| is_headline_view | `True` for `ALL_ex_boilerplate`, the recommended default view |
| passages, autonomy_words, low_n | passages scored; scored words; `low_n` = fewer than 3 passages |
| net_tone_per_1k | (LM positive − LM negative) per 1k words of the autonomy sentences |
| baseline_net_tone_per_1k | same measure on the **non-autonomy text of the same section in the same filings** |
| net_tone_vs_baseline | autonomy − baseline: **the controlled stance** (>0 = more positive about autonomy than the surrounding text) |
| negative_, positive_, uncertainty_, constraining_, hedge_, forward_looking_vs_baseline | per-category deltas, per 1k words |
| qoq_shift_flag | quarter-over-quarter change > 2 SD of the company's history (headline view only) |

## 4. `gm_winddown.csv`: GM WIND-DOWN (M4)

31 rows, one per quarter. GM passages containing a robotaxi-group term (Cruise,
robotaxi, driverless…), outside risk factors and legends.

| Column | Meaning |
|---|---|
| robotaxi_passages, low_n | passage count; fewer than 3 |
| robotaxi_net_tone_per_1k | net tone of those passages |
| robotaxi_net_tone_vs_baseline | minus the same filings' same-section non-autonomy baseline |
| negative_per_1k, constraining_per_1k, positive_per_1k | LM category rates |
| winddown_vocab_pct | **Original list, written after reading GM's filings (post-hoc; not independent evidence).** % of passages with wind down / no longer fund / pause / suspend / restructur- / refocus / discontinue / cease / exit |
| expansion_vocab_pct | Also post-hoc. % of passages with launch / expand / scale / commercialize / growth / new cities or markets |

The out-of-sample replacement for `winddown_vocab_pct` is in section 5.

## 5. GM breakpoint and out-of-sample wind-down list (Finding 05 revision)

Same GM robotaxi view as section 4 (565 passages, 58 filings). Rows are calendar years of the
filing date; 2023 also has a pre-cut row (filed Jan 1 to Sep 30) and a post-cut row (filed
Oct 1 to Dec 31); 2026 is a partial year (filed Jan 1 to Sep 30). Intervals are percentile 95%
intervals from 10,000 bootstrap draws that resample whole filings (an 8-K and its exhibits are
one filing) within each row. Plan and frozen list: `prereg/winddown_v3/`.

### 5a. `gm_breakpoint_by_year.csv`

| Column | Meaning |
|---|---|
| year | row label (see above) |
| n_accessions, n_passages | filings and passages in the row |
| scored_words, negative_words | summed over the row's passages (`passages.csv` columns `words`, `negative`) |
| neg_per_1k, neg_per_1k_boot_lo/hi | **word-level** negative rate, negative_words / scored_words × 1000: the estimator used on the page |
| neg_mean, neg_mean_boot_lo/hi | per-passage mean of the negative rate (passages with scored words only): secondary, not used on the page |
| net_per_1k, net_per_1k_boot_lo/hi | word-level (positive − negative) / scored words × 1000 |
| forms_accessions | filings by form |
| flags | `few filings; interval unreliable` when fewer than 5 filings |

### 5b. `gm_winddown_v3_by_year.csv`

Two lists side by side. **frozen_\*** = list v3: 41 terms derived only from the Uber/ATG,
Lyft/Level 5 and Ford/Argo exit filings, frozen and hashed before GM was scored, matched with
the regexes stored in `prereg/winddown_v3/frozen_winddown_terms_v3.json`. **original_\*** = the
post-hoc list of section 4, matched with its original code. Differences between the columns
reflect both the word list and the matching rule. The last two rows are the declared test:
filed on or before 2023-09-30 vs on or after 2023-10-01.

| Column | Meaning |
|---|---|
| row, n_accessions, n_passages, forms_accessions | as in 5a |
| *_hits, *_share | passages matching at least one term; hits / n_passages |
| *_boot_lo/hi | filing-resampled interval; for a `degenerate` cell (share 0 or 1 in every draw) it is the Wilson interval at n = filings |
| *_wilson_passages_lo/hi | Wilson interval at n = passages (assumes independent passages; narrower than it should be) |
| *_flags | `degenerate`, `few filings; interval unreliable` |

### 5c. `gm_winddown_v3_quarterly.csv`

One row per filing quarter (2019Q1 to 2026Q3): n_accessions, n_passages, and hits and share for
each list. Counts only, no intervals; this is the series behind the vocabulary chart.

