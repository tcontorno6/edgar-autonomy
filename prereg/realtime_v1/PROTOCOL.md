# Real-time detection test of GM's robotaxi tone drop (pre-registration, v1)

Written and committed 2026-10-25, **before** any rule below has been computed on any company.
The owner's request (project thread, 2026-10-25 18:08 UTC): test whether the method behind
Finding 05 would have flagged GM in real time, using only filings filed on or before each quarter
end, with no constants tuned on GM, and report every pre-registered rule whatever it shows.

The published claim being tested: GM's baseline-adjusted robotaxi tone drops at 2023Q4, about a
year before GM ended Cruise robotaxi funding on 2024-12-10. 2023Q4 was read off the full series
through 2026. This test asks whether a rule fixed in advance, run forward quarter by quarter,
would have fired, when, and how often the same rule fires on the other five companies.

## 1. Input (fixed)

- Source: `stance_timeline.csv` (M4 v2 deliverable, project files), sha256
  `3005c7c9659c4433adaa30ff73e207ecff0893b575c0afb464f26f3a4274f8ca`.
- Slice committed here: `input_service_ex_boilerplate.csv`, rows with `group = service` and
  `section = ALL_ex_boilerplate`, all six companies, columns `ticker, quarter, passages,
  autonomy_words, baseline_words, net_tone_delta_vs_baseline`. 97 rows, sha256
  `249cedef8df5d17b6ae287c3727d132596b96e4db817c0cb518d95f3d882a800`.
- Series x_t = `net_tone_delta_vs_baseline` (LM positive minus negative per 1k words in robotaxi
  passages outside risk factors and forward-looking legends, minus the same rate in the
  non-autonomy text of the same sections in the same filings). This is the quarterly series plotted
  in Finding 05 (checked: GM's 31 values equal the page's `GM` array to 3 decimals). It is the
  view the published claim uses; no other view, group, section or measure is scored.
- `quarter` is the calendar quarter of the **filing date** (README of the dataset). Each x_t and
  its same-filing baseline use only filings filed in quarter t, so x_t is known at the end of t.
  2026Q3 runs to 2026-09-29, the last filing in the corpus, and is used as is.

## 2. Eligibility and warm-up (fixed on general grounds)

- A quarter is **eligible** if it has a row, `passages >= 3` and `autonomy_words > 0`. The 3-passage
  floor is the one M4 already used for its quarter-over-quarter flags (M4_NOTES §5); it was set in
  M4, not here. Ineligible quarters are skipped: they neither fire, nor break, nor count toward a
  run of consecutive quarters. "Previous quarter" below means previous eligible quarter.
- **Reference set** B for a quarter: all eligible quarters of the same company filed strictly
  before it (expanding window, never including the quarter tested or anything later). Mean and
  sample SD (ddof = 1) of x over B. A z-score needs |B| >= 8 (two years of quarters) and SD > 0;
  otherwise the quarter is not evaluated.
- Nothing is reset or re-estimated after a firing except the CUSUM statistic (rule R3).

## 3. Rules (all three are reported, whatever they show)

Constants are textbook defaults for control charts, chosen before computing anything and not
varied. No company-specific constant exists.

- **R1, 3-sigma (Shewhart).** At eligible T with |B_T| >= 8: z_T = (x_T − mean(B_T)) / sd(B_T).
  Fires if z_T < −3.
- **R2, 2-sigma for 2 consecutive quarters.** At eligible T with previous eligible quarter P,
  using the single reference set B = B_P (quarters before P, so neither tested quarter is in it),
  |B| >= 8: fires if (x_P − mean(B)) / sd(B) < −2 and (x_T − mean(B)) / sd(B) < −2.
- **R3, lower one-sided CUSUM, k = 0.5, h = 5** (Montgomery's standard choice; in-control
  average run length about 465). z_t = (x_t − mean(B_t)) / sd(B_t) for each evaluable t;
  C_t = max(0, C_prev − z_t − 0.5), C starts at 0 before the first evaluable quarter. Fires if
  C_t > 5; C is set to 0 after a firing. Non-evaluable quarters leave C unchanged.

Each rule is evaluated at every eligible quarter end T, from the first evaluable one, using only
rows with quarter <= T. The script enforces this by truncating the data at T before every
evaluation.

## 4. What is reported

**Episodes.** A firing episode is a run of firing quarters with no non-firing evaluated quarter
between them; its date is the end of its first quarter. For each rule and company: number of
evaluated quarters, every firing quarter, every episode.

**Phase 2, GM.** First firing quarter per rule (or "never"), and lead time = 2024-12-10 minus the
end date of that quarter, in days and quarters. Also stated for each rule: whether it fired
before 2023Q4, at 2023Q4, or later, and whether a known GM event (section 5) already happened in
or before the first firing quarter (in which case the firing is a reaction, not a forecast).

**Phase 3, other five.** The identical code over Tesla, Alphabet, Amazon, Uber and Lyft. Every
episode is listed. An episode is **followed** if an event from the frozen list in section 5 falls
in (episode date, episode date + 4 quarters]. Primary count: episodes not followed by a Tier 1
event (false positives). Secondary: not followed by Tier 1 or Tier 2. GM's episodes are scored the
same way. A company that never reaches 8 eligible reference quarters is reported as
**infeasible** for that rule; the view is not widened to rescue it.

Anything computed beyond this list is labelled exploratory and does not change the result.

## 5. Event list (frozen now, before any rule is run)

Compiled from public reporting and the companies' own announcements, from general knowledge, not
from the tone series. Dates are as best known now; after scoring, dates are checked against
8-Ks or press releases where possible. Any correction is logged in FREEZE_RECORD, with whether it
moved an event into or out of a window. Events found later are reported separately and do not
enter the primary count.

- **Tier 1:** the company exits, sells, shuts down, stops funding, or suspends driverless
  operations of its own robotaxi or AV program (or a line of it).
- **Tier 2:** regulator action against the company's own AV or driver-assist program (recall,
  permit suspension, formal investigation opened, penalty), a crash that leads to such action,
  layoffs or leadership exit at the AV unit.
- Partner programs (for example Motional for Lyft, Aurora for Uber) do not count.

| Company | Date | Tier | Event |
|---|---|---|---|
| GM | 2022-09-01 | 2 | Cruise software recall (80 vehicles) after June 2022 crash |
| GM | 2022-12-12 | 2 | NHTSA opens preliminary evaluation of Cruise hard braking |
| GM | 2023-10-02 | 2 | Cruise vehicle drags pedestrian in San Francisco |
| GM | 2023-10-24 | 2 | California DMV suspends Cruise driverless permits |
| GM | 2023-10-26 | 1 | Cruise pauses driverless operations nationwide |
| GM | 2023-11-08 | 2 | Cruise recall of 950 vehicles |
| GM | 2023-11-19 | 2 | Cruise CEO Kyle Vogt resigns |
| GM | 2023-12-14 | 2 | Cruise lays off about 24% of staff |
| GM | 2024-09-30 | 2 | NHTSA civil penalty against Cruise ($1.5M) |
| GM | 2024-11-14 | 2 | Cruise deferred prosecution agreement ($500k) |
| GM | 2024-12-10 | 1 | GM ends funding of Cruise robotaxi development (**the target**) |
| GM | 2025-02-04 | 1 | GM completes folding Cruise into GM, robotaxi work ended |
| UBER | 2020-12-07 | 1 | Sale of Uber ATG to Aurora announced |
| LYFT | 2021-04-26 | 1 | Sale of Level 5 to Toyota (Woven Planet) announced |
| TSLA | 2021-08-13 | 2 | NHTSA opens Autopilot investigation (PE21-020) |
| TSLA | 2022-06-09 | 2 | NHTSA upgrades Autopilot probe to engineering analysis |
| TSLA | 2023-02-16 | 2 | FSD Beta recall (about 363k vehicles) |
| TSLA | 2023-12-13 | 2 | Autopilot recall (about 2M vehicles) |
| TSLA | 2024-04-26 | 2 | NHTSA opens recall query on the Autopilot recall |
| TSLA | 2024-10-18 | 2 | NHTSA opens FSD investigation (reduced visibility) |
| TSLA | 2025-01-07 | 2 | NHTSA opens Actually Smart Summon investigation |
| TSLA | 2025-10-09 | 2 | NHTSA opens FSD traffic-violation investigation |
| GOOGL | 2023-01-25 | 2 | Waymo layoffs |
| GOOGL | 2023-07-26 | 1 | Waymo pauses Via autonomous trucking to focus on ride-hailing |
| GOOGL | 2024-02-13 | 2 | Waymo recall (444 vehicles) |
| GOOGL | 2024-05-13 | 2 | NHTSA opens Waymo investigation |
| GOOGL | 2024-06-12 | 2 | Waymo recall (672 vehicles) |
| GOOGL | 2025-05-14 | 2 | Waymo recall (1,212 vehicles) |
| GOOGL | 2025-10-20 | 2 | NHTSA opens Waymo school-bus investigation |
| AMZN | 2024-05-13 | 2 | NHTSA opens Zoox investigation |
| AMZN | 2025-03-25 | 2 | Zoox recall (258 vehicles) |
| AMZN | 2025-05-06 | 2 | Zoox recall (270 vehicles) after Las Vegas crash |

The machine-readable copy is `events.csv`; the script reads it.

## 6. What a result means (stated now)

- The published claim survives as a real-time claim only if at least one rule first fires on GM
  at or before 2024Q3 **and** the same rule's unfollowed episode count on the other five is small
  (here, on average at most one per feasible company over 2019 to 2026). If GM's first firing
  comes after a public Tier 1/2 GM event, that is a reaction to known news, and the page must say
  so rather than claim a lead.
- If no rule fires on GM before the decision, the result is "the method would not have caught
  this in real time" and is published as such.
- If rules fire on GM but fire as often on companies with no following event, the result is "not
  a signal", whatever the GM lead time.

## 7. Blindness and context (stated before running)

The rule author is **not blind to GM**. GM's quarterly series is public on the dashboard and this
session read it (and the M4 notes, the GM breakpoint check and the page) before writing these
rules, so the author can roughly anticipate where GM's z-scores fall. The constants above are
standard defaults rather than values picked to fit, but that knowledge cannot be undone and is
disclosed. The other five companies' quarterly values were not looked at before this commit (only
the row count of the slice and one header row of Amazon 2021Q1 were seen), though they too are
public in `data/stance_vs_baseline.csv`.

Other limits known now: the robotaxi lexicon (M2), the section tagger and the dictionary were all
built in 2026 with the whole corpus in view, so the *measurement* is not real-time, only the
rule is; per-quarter values rest on few passages for most companies.
