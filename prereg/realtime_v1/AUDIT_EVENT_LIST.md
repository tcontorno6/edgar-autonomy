# Audit: event list used for scoring vs. the one post-hoc candidate (2026-10-25)

Requested by the owner before merging PR #3. Audit only: rules, code and event list unchanged.

## 1. The event in question

- **What:** the Cruise robotaxi crash in San Francisco on **2022-06-03** (a left-turn collision
  with injuries; it led to the 2022-09-01 software recall of 80 vehicles, which *is* in the frozen
  list).
- **Why it came up:** while writing RESULTS.md after scoring, I noticed the frozen list carries
  this crash only through its recall date. PROTOCOL §5 Tier 2 includes "a crash that leads to such
  action", so the crash arguably belonged in the list under its own date.
- **Status:** it was **never added**. `events.csv` at HEAD is byte-identical to d1234dc
  (sha256 `1b69a26b…a16d`), and every published count already uses the frozen list. The
  FREEZE_RECORD entry records that it was noticed, not that it was used.

## 2. Re-score against the frozen list exactly as committed in d1234dc

`events.csv`, `input_service_ex_boilerplate.csv` and `realtime_v1.py` were extracted with
`git show d1234dc:…`, their sha256 re-checked against FREEZE_RECORD, and the script re-run.
The output is identical to `results/results.json` (JSON equality). The amended run appends the
one row `GM,2022-06-03,2,…` to a scratch copy of the list; nothing amended is committed as input.

## 3. Every firing under both lists

"Hit" = an event of that tier in (end of the episode's first quarter, + 4 quarters]. The only
firings in the whole test are GM's (no other company produced one).

| Rule | Episode (quarters) | Tier 1: frozen | Tier 1: amended | Tier 1 or 2: frozen | Tier 1 or 2: amended |
|---|---|---|---|---|---|
| R1 3-sigma | 2024Q1 | hit* | hit* | hit* | hit* |
| R2 2-sigma ×2 | 2021Q2 | false positive | false positive | **false positive** | **hit** |
| R2 2-sigma ×2 | 2022Q2–Q3 | false positive | false positive | hit | hit |
| R2 2-sigma ×2 | 2024Q1–Q2 | hit* | hit* | hit* | hit* |
| R3 CUSUM | 2022Q2 | false positive | false positive | hit | hit |
| R3 CUSUM | 2023Q4 | hit* | hit* | hit* | hit* |
| R3 CUSUM | 2024Q3 | hit* | hit* | hit* | hit* |

\* "Hit" by the window definition, but the episode starts after the October 2023 crash, permit
suspension and nationwide pause were public, so it reacts to known news (PROTOCOL §4, RESULTS).

## 4. Verdict

**One classification changes:** R2's 2021Q2 alarm moves from false positive to hit in the
secondary (Tier 1 or 2) count only; no Tier 1 (headline) classification changes. As instructed,
the frozen-list result stays the headline, and the amended figure, where reported at all, is
labelled a post-hoc amendment.

| Count | Frozen (headline) | Amended (post-hoc) |
|---|---|---|
| R1 unfollowed, Tier 1 / Tier 1–2 | 0 / 0 | 0 / 0 |
| R2 unfollowed, Tier 1 / Tier 1–2 | 2 / 1 | 2 / 0 |
| R3 unfollowed, Tier 1 / Tier 1–2 | 1 / 0 | 1 / 0 |
