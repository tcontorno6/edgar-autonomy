# Provenance of the 45 M4 stance labels (audit, 2026-10-25)

Scope: repository artifacts only (this repo's files and git history), plus the project's shared
M4 notes where they are the cited source. Nothing was re-rated or re-run.

## Artifacts that produce or record the labels

| Artifact | What it holds |
|---|---|
| `data/validation/stance_validation_v1.csv`, `_v2.csv` (added 6ef99ab, 2026-10-22) | 45 rows each: `sample_id` (e.g. `most_positive-14`), `model_label`, passage text, `human_label`, `match`, `note`. One rater label column; no second rater. |
| `analysis/stance_kappa.py` (6ef99ab) | Cohen's kappa between `model_label` and `human_label`. |
| `data/validation/README.md` (6ef99ab) | States the rater was Claude, the assistant that built the scorer, and saw `model_label`. |
| `WRITEUP.md` at 1369eee (2026-10-17, first publish) | Says "10/15 positive extremes matched a human read" **and** "All labels were set by one reviewer (Claude, with Tyler approving each rule change)". Names `scripts\label_m4.py` as where M4 labels are stored. |
| M4 notes (project files, 2026-10-01) | Define "match" as "the human read agrees with the label"; labels "in `scripts/label_m4.py`". |
| `scripts\label_m4.py` | **Not in this repository** (the code exists only on the owner's Desktop). The contemporaneous labelling record was not examined. |

## What the record supports

- **Who assigned the labels.** The only explicit statements name Claude (WRITEUP at first
  publish: "one reviewer (Claude…)"; validation README). The earlier "human read" wording in the
  M4 notes and first WRITEUP describes the kind of reading, not a person, and no artifact names a
  human rater. Labels were stored as code in a labelling script, and the v2 file appears 7 minutes
  after the v1 review (03:35 to 03:42 UTC, 2026-10-01). **Supported: the labels were set by
  Claude.** Not directly verified: the labelling script itself, which is not in the repo.
- **Whether the rater saw the model's label first.** Yes, from the files themselves: every row
  carries `model_label` next to the text, the `sample_id` names the class, and the notes evaluate
  the model's label ("label right, but 'May Mobility' was counted as the modal 'may'"). **Unblinded.**
- **A second rater.** None. Each file has one rater column; no other ratings exist in the repo.
- **What kappa was computed between.** `model_label` (the scorer) and `human_label` (the
  scorer-builder's unblinded read). It is not inter-rater agreement.

## Consequence for the page

The validation section is changed to describe this procedure: the 80% is labelled an unblinded
self-check (upper bound), the kappa row is removed from the validation table, and the text says
why the number is no longer reported as validation.
