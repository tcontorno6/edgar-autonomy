# Results: real-time detection test v1 (run 2026-10-25)

Run once, after the freeze (`FREEZE_RECORD.md`, pre-registration commit `d1234dc`, hashes pushed in
`b0e7d58`). All four frozen files were re-checked against their sha256 before the run. Command:
`python realtime_v1.py input_service_ex_boilerplate.csv events.csv results`. Full output:
`results/results.json` (every rule, every company) and `results/walk_forward.csv` (every quarter's
z-score, reference mean and SD, CUSUM value and firing flags).

## Verdict (against PROTOCOL §6)

**The published claim does not hold up as a real-time claim.** Run forward with only what had been
filed, the method gives no clean early warning of the December 2024 decision:

- The firings closest to the decision (R1 2024Q1, R2 2024Q1, R3 2023Q4) all come **after** the
  October 2023 pedestrian crash, the California permit suspension (2023-10-24) and Cruise's
  nationwide pause (2023-10-26, a Tier 1 event). They react to public news; they do not foresee it.
- The firings before that news (R2 2021Q2 and 2022Q2, R3 2022Q2) were **not followed by any Tier 1
  event within four quarters**. The 2022Q2 alarms were followed by Tier 2 events only (the
  September 2022 recall and the December 2022 NHTSA evaluation). The first Tier 1 event came six
  quarters after the 2022Q2 alarm.
- **The false-positive rate on the other five companies cannot be measured.** In the pre-registered
  view, four of the five never reach the eight eligible quarters a reference needs, and Tesla
  reaches it only in 2026Q3. So the cross-company check that would show whether these alarms mean
  anything is infeasible, and the view was not widened to rescue it.

## Phase 2: GM

31 eligible quarters (2019Q1 to 2026Q3); 23 evaluable (from 2021Q1, after 8 reference quarters).

| Rule | Firing quarters | First firing | Lead to 2024-12-10 | Episodes | Not followed by Tier 1 within 4 quarters | Not followed by Tier 1 or 2 |
|---|---|---|---|---|---|---|
| R1, z < −3 | 2024Q1 | 2024Q1 | 254 days (3 quarters) | 1 | 0 | 0 |
| R2, z < −2 twice running | 2021Q2; 2022Q2–Q3; 2024Q1–Q2 | 2021Q2 | 1,259 days (14 quarters) | 3 | 2 (2021Q2, 2022Q2) | 1 (2021Q2) |
| R3, CUSUM k 0.5, h 5 | 2022Q2; 2023Q4; 2024Q3 | 2022Q2 | 894 days (10 quarters) | 3 | 1 (2022Q2) | 0 |

Timing against the published 2023Q4 break:
- R1 does **not** fire at 2023Q4 (z = −2.83 against a reference of 19 quarters, mean 16.2, SD 7.1).
  It first fires one quarter later, at 2024Q1 (z = −3.00, just past the threshold).
- R3 fires at 2023Q4. Its lead to the decision is 345 days, but the quarter contains the crash,
  the permit suspension and the pause, so the alarm comes after the news.
- R2 fires early (2021Q2, z −2.85 and −2.33) with nothing following within a year, then at
  2022Q2–Q3, then at 2024Q1–Q2.

Why 2023Q4 does not stand out in real time: the reference is expanding, so GM's 2022–23 slide
enters it. The reference SD grows from 2.9 (2021Q1) to 7.1 (2023Q4) and 11.1 (2024Q4), and the
reference mean falls from 22.3 to 16.2. A drop that looks like a clean break with hindsight is,
quarter by quarter, the continuation of a decline that had already widened the yardstick.
(This is a description of the frozen rule's behaviour, not a reason to change it.)

## Phase 3: Tesla, Alphabet, Amazon, Uber, Lyft

| Company | Quarters with a row | Eligible (≥3 passages) | Evaluable | R1 | R2 | R3 |
|---|---|---|---|---|---|---|
| Tesla | 11 | 9 | 1 (2026Q3) | 0 firings | infeasible | 0 firings |
| Alphabet | 14 | 1 | 0 | infeasible | infeasible | infeasible |
| Amazon | 9 | 0 | 0 | infeasible | infeasible | infeasible |
| Uber | 21 | 3 | 0 | infeasible | infeasible | infeasible |
| Lyft | 11 | 1 | 0 | infeasible | infeasible | infeasible |

**False-positive count across the other five: 0 firings, in 1 evaluable company-quarter (Tesla
2026Q3, z = −1.74).** That zero carries no information. GM is the only company with enough
robotaxi passages outside boilerplate, quarter after quarter, for a company-specific trailing
baseline to exist. The only false positives that can be counted are GM's own: 2 (R2) and 1 (R3)
alarms with no Tier 1 event in the following year, against 0 for R1.

## Exploratory (not part of the result)

- The June 3, 2022 Cruise crash in San Francisco is in the event list only through the recall it
  led to (2022-09-01). Dated by the crash itself it would fall inside R2's 2021Q2 window, making
  that alarm "followed by Tier 2". It was not entered in the frozen list, so the counts above do
  not use it. Audit: this is the only classification it would change (`AUDIT_EVENT_LIST.md`);
  any figure that includes it is a post-hoc amendment.

Event-date check after scoring: the three dates that decide windows were checked against news
reports and are unchanged: Cruise nationwide pause 2023-10-26
([CNBC](https://www.cnbc.com/amp/2023/10/26/cruise-pauses-all-driverless-operations-after-collisions-suspensions.html)),
Cruise recall of 80 vehicles 2022-09-01
([TechCrunch](https://techcrunch.com/2022/09/01/gms-cruise-recalls-updates-software-in-80-robotaxis-following-crash)),
GM ends Cruise robotaxi funding 2024-12-10
([The Robot Report](https://www.therobotreport.com/gm-will-no-longer-fund-cruise-robotaxi-development/)).
