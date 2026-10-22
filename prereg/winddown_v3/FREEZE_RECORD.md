# Freeze record: wind-down list v3 (committed before any GM scoring)

This file is pushed to GitHub after the Phase A freeze and **before** the frozen list is applied
to GM. It is a public hash commitment: the full frozen file is added to this repository later,
and its sha256 must equal the value below.

| | |
|---|---|
| Protocol | `PHASE_A.md` at commit ed97fa9; copy received on the Desktop has sha256 `fabc7fe4de0f8ecda41a0bb144719c238011d0e7c2f077d6876eaee215897c20` (identical) |
| Desktop freeze commit | `081dfacdc43a02be75894b003fe88636178c0f38`, 2026-10-22T02:50:27Z, local repo `Desktop\edgar-autonomy` (not pushed; 26 Phase A files) |
| Frozen file | `data/winddown_v3/frozen_winddown_terms_v3.json`, 132,499 bytes |
| **sha256 (from `git show` bytes)** | **`b884c0c7f75e4a84fde25bd0aecf6895d23a4152046334a0147f088044ca5d74`** |
| Tree id of `data/winddown_v3` at the freeze commit | `c6be0b3a3196faecb8b193d2f5df30ef0662bb47` |

## Inputs

- 28 exit documents: E1 Uber/ATG 12 (2 10-K, 3 10-Q, 7 8-K documents), E2 Lyft/Level 5 11
  (1 10-K, 3 10-Q, 7 8-K documents), E3 Ford/Argo 4 (1 10-K, 1 10-Q, 2 8-K EX-99). EDGAR full-text
  search cross-check: 34 hits, all in the list. 58 8-K documents without an anchor excluded.
- 480 exit passages (E1 317, E2 123, E3 40); 36 anchor hits inside tables.
- 125 reference passages: Uber 67 (pre-2020-12-07), Lyft 46 (pre-2021-04-26), Ford FY2021
  10-K 12.

## Primary list (threshold 0.05), 41 terms

Per term: exits whose passages it matches (passage counts), and pooled reference rate when
non-zero (denominator 125).

acquire (E1 5, E2 1; 1/125) · merger transactions (E1 5) · sell (E1 8) · sale (E1 129, E2 23,
E3 3) · completed the sale (E1 30) · previously announced sale (E1 22) · sold (E1 12) · sales
(E1 2, E2 1; 1/125) · divesting (E1 1) · divestiture (E1 64, E2 39) · divestitures (E1 35, E2 7)
· business divestitures (E1 12) · divested (E1 10) · divestments (E1 1) · closed (E1 6, E2 8) ·
held for sale (E1 10, E2 2) · merging (E1 2) · merger (E1 15) · settled (E1 20) · transferred
(E1 28, E2 1) · disposal (E1 4) · join (E2 1) · joining (E2 1) · pending sale (E2 1) · proposed
sale (E2 1) · completed a transaction (E2 16, E3 4; 1/125) · multi-element transaction (E2 6) ·
closed the sale (E2 3) · prior initiative (E2 6) · eliminated (E2 2) · no longer develop (E2 3)
· derecognized (E1 8, E2 2) · wound down (E3 1) · wind down operations (E3 4) · exiting (E3 4) ·
orderly conclusion (E3 2) · going concern (E3 4) · impairment (E1 3, E3 17) · strategic decision
(E3 5) · shift (E1 8, E2 4, E3 5) · deconsolidated (E3 5; 1/125)

Secondary: threshold 0.02 gives the identical list; threshold 0.10 adds "acquisition"
(E1 6, E2 3; 7/125).

Filter counts: the subagent returned 49 term lines; 7 case-insensitive duplicates; 42 unique;
F1 dropped 0, F2 dropped 0, F3 dropped 1 ("acquisition", 7/125 = 0.056).

## Deviations and decisions logged during Phase A (all before the freeze)

- **iXBRL stubs.** The first fetch saved iXBRL viewer pages (`/ix?doc=` links). Links were fixed
  and everything re-fetched before any passage existed.
- **Defined-term anchors, one pass.** A first A2 run let defined terms define further terms
  (pulling in SoftBank, Preferred Units, SPAC). It was replaced, before the A4 lock, with a single
  pass over sentences hit by the listed anchors. Generic labels such as "Company" and "Lyft" still
  became anchors in the documents where an anchored sentence defined them, so some exit passages
  are not about the exit itself.
- **Subagent input.** The inline prompt would have been 215,761 characters, so the subagent got
  the file path (as the protocol allows). Its instruction says both "do not use any tools" and
  "read only that one file"; it used Read and Grep on that file only (12 tool calls). Model
  inherited from the session; no serving model id reported. One run.
- **A6 re-runs.** A6 was re-run twice on the same locked inputs after aligning the F2 tokenizer;
  results identical.
- **Executor context.** No CLAUDE.md loaded. Before Phase A the executing session opened its own
  memory file, which contains GM tone and wind-down findings (yes) but no wind-down word list
  (no). It also saw a `data\m4` file name and a variable name in `scripts\tone.py` that refer to
  the earlier GM test, without opening either. No GM row or filing was opened during Phase A.

## Weaknesses visible before GM scoring (stated now so they cannot be added after)

- Many terms are generic transaction or accounting words (sale, sales, sold, closed, transferred,
  settled, merger, acquire, join, shift, impairment, eliminated). Their low reference rates rest
  on a small reference set (125 passages). They can fire on any deal, financing or accounting
  sentence, not only on an exit.
- E1 (Uber) supplies most matches, so the list leans toward the vocabulary of a sale.
- The list is the output of one extraction by one model; all later intervals are conditional on
  it.

The list is not edited after this point. If it does not separate GM's periods, that is reported
as the result.
