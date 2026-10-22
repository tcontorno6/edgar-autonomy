# edgar-autonomy: Phase B (apply the frozen list) and Phase C (Finding 05 breakpoint)

Analysis plan written and committed before the Phase A freeze existed. It is sent to a separate
Desktop session after the freeze, together with the freeze commit SHA and the frozen file's
sha256. Same standing rules as Phase A: zero paid APIs, write only inside
`Desktop\edgar-autonomy\data\winddown_v3\results\` and `data\breakpoint_v1\`, no edits to existing
files or `data\dashboard\`, no push, UTF-8 with `\n` line endings, PowerShell.

## B0. Verify the freeze, then never touch the list

- Recompute the sha256 of the bytes from `git show <FREEZE_SHA>:data/winddown_v3/frozen_winddown_terms_v3.json`.
  Abort on mismatch. Write the freeze SHA and the hash into every output file.
- Import the matcher from `data\winddown_v3\scripts\common.py` as committed in the freeze, and
  compile the regex strings stored in the JSON. Never rebuild them, never add, drop, stem or
  inflect a term, and never compute any other variant of the list on GM.

## Shared definitions (B and C)

- **Periods use the `filed` date** (EDGAR filing date), never the fiscal period. Pre = filed
  on or before 2023-09-30; post = filed on or after 2023-10-01. Year and quarter are the calendar
  year and quarter of `filed`, compared as integers. The 2026 row is labeled
  "2026 (filed Jan 1 to Sep 30, partial year)" everywhere. 2023 also gets two sub-rows,
  pre-cut and post-cut. Before any analysis print min and max `filed`, the row count, and every
  row whose `quarter` column disagrees with the calendar quarter of `filed`.
- **GM robotaxi view** = the exact filter in the existing M4 code that produced
  `gm_winddown.csv` (cite file and function; reading that code is allowed now). Expected 565
  passages. If the count differs, stop and report before scoring.
- **Bootstrap**: unit = accession (an 8-K and its EX-99 exhibits are one unit). Resample
  accessions with replacement within each stratum (year for yearly tables; pre and post separately
  for the cut), keep all passages of each drawn accession, 10,000 reps, percentile 95% CI,
  `numpy.random.default_rng(20261022)`, accessions sorted ascending before drawing, a new
  generator per table, one set of draws shared by all statistics in a table. If the bootstrap
  distribution is degenerate (share 0 or 1, or one accession), print "degenerate" and use the
  Wilson interval at n = n_accessions for that cell. Flag cells with fewer than 5 accessions
  "few filings; interval unreliable". Empty cells print "—", never 0%.
- **Checks, not targets.** Every "expected" number below is computed once with these definitions.
  If it does not match, report both values with the counts behind them and continue with these
  definitions. Never change the view, cut, date column, columns, matcher or estimator to make a
  number match.

## Phase B. Apply the frozen list (Task 2, step 4)

- **B1 primary result (declared before scoring).** Frozen-list share of GM robotaxi passages
  (passages whose `text` matches at least one primary term) pre vs post 2023Q4, the post minus pre
  difference and its accession-clustered bootstrap 95% CI. The wind-down reading is described as
  supported out of sample only if that CI is entirely above 0. Shown next to the post-2023Q4 shares
  for Tesla, Alphabet and Amazon. If the list barely fires on GM, that is reported as the result.
- **B2 by year.** For GM: n_accessions, n_passages, hits, share, bootstrap CI, Wilson CI at
  n = n_passages (labeled "assumes independent passages"), form counts. Quarterly CSV with counts
  and shares only, no intervals.
- **B3 original post-hoc list, side by side.** Apply the original list with its original matching
  code (cite file and function) to the same view, by year and at the cut. Check it against the
  per-year shares behind the published chart. Label every column with its list and its matcher,
  with the note "Differences between columns reflect both the word list and the matching rule."
- **B4 per-term breakdown** of frozen-term hits on GM by year. No term is removed for any reason.
- **B5a placebo (never exited): Tesla, Alphabet, Amazon**, by year and pre/post, on two views:
  all autonomy passages outside `risk_factors`/`fls_legend`, and the same robotaxi-service filter
  used for GM.
- **B5b Uber and Lyft are training data, not a placebo.** Report them under the caption
  "In-sample. Terms were derived from these companies' exit filings and filtered on their pre-exit
  passages, so high post-exit and low pre-exit shares follow by construction." Also report how many
  of their `passages.csv` accessions appear in `exit_passages.csv`.
- **B6 secondary lists** (thresholds 0.02 and 0.10): GM by year and pre/post, labeled secondary.
- **B7 exploratory, exit passages only:** for each exit, the share of its passages matched by
  frozen terms that also match another exit's passages. Label "leave-one-exit-out, approximate: the
  extraction saw all three exits."
- **B8 sensitivity:** B1 and B2 recomputed keeping only the first-filed copy of each distinct
  whitespace-normalized `text`; report n_distinct_texts per year.

## Phase C. Finding 05 breakpoint (Task 1)

- **C0 estimator.** The page reports word-level pooled rates: sum of LM-negative (or positive)
  words over sum of scored words, times 1,000, using the scored-word and category-count columns of
  `passages.csv` (name them). This was chosen for consistency with every other per-1k figure on the
  page and in `stance_timeline.csv`. It was chosen after the word-level 2023Q4 counts
  (69/9,521 and 188/9,612, recomputed from `stance_timeline.csv`) had been seen, and before any
  per-passage 2023Q4 mean was computed. Per-passage means (passages with scored words above 0 only;
  log how many have 0) and Poisson intervals are secondary, reported in full even if they disagree,
  and the headline is not switched.
- **C1 check.** At the published 2025 cut (filed on or before 2024-12-31 vs on or after
  2025-01-01): per-passage negative mean (published 7.7 vs 16.8) and per-passage net tone
  (published −0.8 vs −14.7).
- **C2 the 2023Q4 cut.** Word-level negative rate (check 69/9,521 and 188/9,612), per-passage
  negative mean, word-level net tone and per-passage net tone, pre and post. Accession bootstrap
  CIs (pre and post strata) for each, plus CIs for post minus pre and post over pre from the same
  draws. Exact Poisson (Garwood) CIs for the word-level negative rate, labeled "assumes independent
  words; not adjusted for clustering", never the headline. Permutation test: T = post minus pre
  word-level negative rate; reassign pre/post labels at random among GM-view accessions holding the
  number per period fixed and keeping each accession's passages together; 20,000 permutations; two-
  sided p = (1 + #{|T*| ≥ |T_obs|}) / (1 + 20,000). Secondary: labels permuted within form type, and
  p-values for the other three statistics from the same permutations. The 2023Q4 cut was read off
  GM's quarterly tone series, so label the single-cut p "nominal (cut chosen after looking at the
  series)" and also report a max-statistic p: permute the time order of accessions, compute |T| at
  every quarterly cut from 2020Q1 to 2025Q4 with at least 4 accessions on each side, take the
  maximum, and compare the observed maximum with that distribution. Caption: "Tests a difference in
  level. It does not distinguish a break at 2023Q4 from a gradual trend."
- **C3 year-by-year table.** Year (with the 2023 sub-rows and the 2026 label), n_accessions,
  n_passages, scored words, negative words, word-level negative per 1k with bootstrap CI,
  per-passage negative mean with bootstrap CI, word-level net tone with bootstrap CI, form counts,
  flags.
- **C4 wind-down at the cut.** Frozen-list and original post-hoc shares pre and post 2023Q4, side
  by side, each with n_passages, n_accessions, bootstrap and Wilson CIs.
- **C5 sensitivity.** C2 recomputed on first-filed copies of each distinct text.

## Outputs and report

Scripts and CSVs in `data\winddown_v3\results\` and `data\breakpoint_v1\`, committed locally in a
commit after the freeze commit. Report compact tables in the thread (no attachments possible):
B1, B2 with B3 side by side, B4 top terms, B5a, C1, C2, C3, C4, and any check that did not match.
