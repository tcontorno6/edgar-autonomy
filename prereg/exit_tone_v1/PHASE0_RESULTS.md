# Phase 0 results: counts only (committed before any Phase 1 rule)

Protocol: `PHASE0.md` (commit 57b2ae6). Views: **GM's view** = robotaxi-service group, all
sections except `risk_factors` and `fls_legend` (the view behind Finding 05); **all-autonomy** =
both M2 groups, same exclusions. Cells are filings with at least one passage / passages / scored
words. Q0 = calendar quarter of the announcement (by filing date).

## Uber (ATG sale announced 2020-12-07, Q0 = 2020Q4); counted before `PHASE0.md` was committed

- GM's view: 7 passages in Q-8..Q+4. Q-6..Q-3 (2019Q2-2020Q1): 1/1/70, 1/1/70, 1/1/65, 1/2/117;
  Q+1: 1/1/89; Q+3: 1/1/34; every other quarter 0. The passages contain no LM negative or
  positive words, so tone is undefined.
- All-autonomy: Q-8..Q-7 (2018Q4-2019Q1) none (pre-IPO); Q-6..Q-1: 2/5/192, 3/14/460, 2/9/259,
  2/18/786, 4/8/239, 2/6/234; Q0..Q+4: 3/16/386, 3/22/722, 2/11/301, 3/16/462, 1/13/373.

## Lyft (Level 5 sale announced 2021-04-26, Q0 = 2021Q2); counted before `PHASE0.md` was committed

- GM's view: 7 passages in Q-8..Q+4, in 4 quarters with one filing each; no LM negative or
  positive words, so tone is undefined.
- All-autonomy: Q-8..Q-1 (2019Q2-2021Q1): 1/3/60, 1/3/59, 1/3/62, 1/14/497, 1/4/118, 1/5/146,
  1/5/128, 1/9/271; Q0..Q+4: 3/26/1021, 1/11/441, 2/16/473, 2/19/768, 1/8/261.

## Ford (Argo AI wind-down announced 2022-10-26, Q0 = 2022Q4); governed by `PHASE0.md`

105 filings, 176 documents fetched (filed 2020-10-01 to 2023-12-31); 175 cleaned, 1 skipped by the
cleaner's MIN_CHARS rule. No LM step was run for Ford. Last number in each cell: baseline words
(non-autonomy words, same sections, same filings).

| Quarter | Rel. | GM's view | All-autonomy |
|---|---|---|---|
| 2020Q4 | -8 | 0 | 6 / 15 / 578 / 32,594 |
| 2021Q1 | -7 | 0 | 6 / 23 / 965 / 74,897 |
| 2021Q2 | -6 | 0 | 8 / 13 / 532 / 31,994 |
| 2021Q3 | -5 | 1 / 1 / 34 / 4,489 | 6 / 15 / 450 / 32,280 |
| 2021Q4 | -4 | 0 | 8 / 16 / 487 / 39,053 |
| 2022Q1 | -3 | 0 | 7 / 22 / 652 / 78,289 |
| 2022Q2 | -2 | 0 | 5 / 9 / 230 / 28,603 |
| 2022Q3 | -1 | 0 | 6 / 10 / 244 / 30,779 |
| 2022Q4, Oct 1-25 | 0 | 0 | 0 |
| 2022Q4, Oct 26-Dec 31 | 0 | 0 | 2 / 12 / 708 / 27,742 |
| 2023Q1 | +1 | 0 | 3 / 16 / 706 / 73,587 |
| 2023Q2 | +2 | 0 | 3 / 5 / 166 / 23,805 |
| 2023Q3 | +3 | 0 | 4 / 6 / 185 / 29,054 |
| 2023Q4 | +4 | 0 | 2 / 5 / 183 / 28,252 |

## Exiting-unit coverage of the M2 lexicon (Q-8..Q+4, outside risk factors and legends)

| Company | Names searched | Sentences | In no autonomy passage | In M2 lexicon |
|---|---|---|---|---|
| Uber | ATG, Advanced Technologies Group, Apparate | 565 | 418 (74%) | ATG, Advanced Technologies Group yes; Apparate no |
| Lyft | Level 5 | 60 | 16 (27%) | yes |
| Ford | Argo | 192 | 102 (53%) | no |

Uber's ATG is an entity term: in financial or transaction sentences without autonomy wording M2
classes it "corporate", so those sentences never become passages.

## Against the yardstick in `PHASE0.md`

- **GM's view:** 7 (Uber), 7 (Lyft) and 1 (Ford) passages in the 13 quarters around each exit.
  Every comparison window has fewer than 5 filings. The view Finding 05 rests on cannot be scored
  for any of the three exits.
- **All-autonomy view (not GM's method):** with "4 quarters before vs the prior 8", Uber has 10 vs
  5 filings and Lyft 4 vs 4 (both prior windows cut short by the 2019 IPOs). Ford has 26 vs 26
  filings with 1,613 vs 2,525 words, about a fifth of GM's ~9,500 words per side, almost all in
  M2's technology group.
