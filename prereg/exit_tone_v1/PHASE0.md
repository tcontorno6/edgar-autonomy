# Out-of-sample test of the GM tone signal on three AV exits: Phase 0 (feasibility, counts only)

Question: does GM's baseline-adjusted robotaxi tone drop (around 2023Q4, about a year before the
December 2024 Cruise decision) also appear before three other AV exits? Phase 0 only counts how
much text there is. No tone is computed in Phase 0. The decision rule (Phase 1) is committed
separately before any scoring.

## State of things when this file was committed

- **Announcement dates, verified from filings** (documents fetched in `prereg/winddown_v3` Phase A):
  - Uber, sale of ATG to Aurora: 8-K filed 2020-12-07. Q0 = 2020Q4.
  - Lyft, sale of Level 5 to Woven Planet: 8-K and EX-99.1 filed 2021-04-26. Q0 = 2021Q2.
  - Ford, Argo AI wind-down: 8-K EX-99 (Q3 earnings release) filed 2022-10-26; Ford's 10-Q filed
    2022-10-27 says "on October 26, 2022, we announced that Argo AI plans to wind down
    operations." Q0 = 2022Q4.
- **Uber and Lyft counts were pulled before this file existed**, from the existing corpus
  (`data\m4\passages.csv`, `baselines.csv` on the Desktop). That run also printed per-quarter
  Loughran-McDonald negative and positive word counts for Uber and Lyft, which are inputs to the
  outcome. They are not in this repository and are not used below, but the Desktop session that
  ran it has seen them. Separately, Uber's and Lyft's quarterly baseline-adjusted tone on the
  all-autonomy view is already published in `data/stance_vs_baseline.csv` (M4). Uber and Lyft are
  therefore not blind on either view. Ford is not in the corpus and has not been scored.
- **Uber and Lyft counts in GM's view** (robotaxi-service group, all sections except
  `risk_factors` and `fls_legend`), Q-8 to Q+4: Uber 7 passages in 13 quarters, never more than one
  filing per quarter; Lyft 7 passages over 4 quarters, one filing each. On the all-autonomy view
  (both M2 groups, same exclusions), "4 quarters before vs the prior 8" gives Uber 10 filings /
  1,518 words vs 5 / 652, and Lyft 4 / 663 vs 4 / 678; both prior windows are cut short by the 2019
  IPOs.

## Ford (governed by this file)

1. **Fetch.** CIK 0000037996. Forms 10-K, 10-Q and 8-K (main document plus every EX-99.x),
   amendments excluded, filed 2020-10-01 to 2023-12-31 (Q-8 = 2020Q4 to Q+4 = 2023Q4). Same fetch
   and cleaning rules as M1, same SEC User-Agent, polite rate limit. Write only under
   `Desktop\edgar-autonomy\data\exit_tone_v1\`. Never write into the existing corpus or edit an
   existing file. No push.
2. **Process with the existing code, unchanged:** the corpus cleaner (`scripts/clean_index.py`
   `clean_doc`), the sentence splitter and section tagger (`scripts/tone.py`), and the M2 autonomy
   lexicon and groups as they are. No term is added for Argo AI or any other unit.
3. **No scoring.** Do not run the Loughran-McDonald step. Do not compute, print or save any LM
   category count (negative, positive, uncertainty, constraining, hedge) for Ford. Word counts use
   the same tokenizer that `tone.py` uses for its `words` column.
4. **Report, per filing quarter Q-8 to Q+4, with Q0 split at the announcement date:** filings with
   at least one passage / passages / words, for (a) GM's view and (b) the all-autonomy view; and,
   for each view, the non-autonomy words in the same sections of the same filings (the baseline).
5. **Lexicon coverage, counts only, all three companies, Q-8 to Q+4:** sentences outside
   `risk_factors` and `fls_legend` that name the exiting unit (Uber: ATG, Advanced Technologies
   Group, Apparate; Lyft: Level 5; Ford: Argo), how many of them fall in no autonomy passage, and
   whether the M2 lexicon contains each name.
6. **Stop and report.** Phase 1 is written by a session that has not seen the Uber and Lyft LM
   counts.

## Yardstick, stated before the Ford counts exist

GM's 2023Q4 comparison rests on 33 vs 25 filings and about 9,500 scored words per side; GM's year
rows with fewer than 5 filings are flagged unreliable. A comparison window with fewer than 5
filings carrying passages in GM's view is reported as too thin for a filing-resampled interval.
