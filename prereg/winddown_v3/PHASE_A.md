# edgar-autonomy: out-of-sample wind-down vocabulary, Phase A (derive and freeze)

You are working on Tyler Contorno's edgar-autonomy project in `C:\Users\Tyler\Desktop\edgar-autonomy`.
This session does **Phase A only**: derive a list of terms that SEC filings use when a company
exits an autonomous-vehicle business, using **only three non-GM exits**, freeze the list, commit
it, report, and stop. A later, separate session applies the frozen list; this session never does.

The list must be provably derived without reference to the company it will later be applied to,
and it cannot be changed once committed. Follow every step literally. Where this protocol does not
cover a situation, stop and report rather than improvise.

## Standing rules

- Zero paid APIs. EDGAR only. User-Agent exactly `Tyler Contorno tyler.contorno1234@gmail.com`.
  At most 5 requests per second. On HTTP 403 or 429, wait 10 minutes and retry.
- Write only inside `Desktop\edgar-autonomy\data\winddown_v3\`. The edgar-tok, edgar-verify and
  ma-target-screener projects are read-only. Do not edit any existing script, config or file, and
  write nothing into the existing raw corpus. Do not push to GitHub. Do not touch Hugging Face.
- Windows/PowerShell. Activate the project venv with `.\.venv\Scripts\Activate.ps1`.
- Write every file from Python with `encoding="utf-8"` (no BOM) and `newline="\n"` (pandas:
  `lineterminator="\n"`). Never create or modify these files with PowerShell redirection,
  `Out-File` or `Set-Content`.

## Blindness rules (whole of Phase A)

- Do not open, load, print, count or summarize any GM data: no GM rows of `passages.csv`, no GM
  filing, nothing under `data\dashboard\`, nothing under `data\m4\` except `passages.csv` read as
  in A3, no notes or markdown files (`M*_NOTES.md`, `M*_REVIEW.md`, `WRITEUP.md`, `README.md`),
  and no output of any earlier tone, stance or wind-down analysis.
- Code: you may list a module's names with `dir()` and print the source of the specific functions
  you need (fetch, clean, sentence split, section tag) with `inspect.getsource()`. Do not open whole
  files under `scripts\`, and never print or search for keyword or vocabulary lists in them.
- Log every file path you open or read in `data\winddown_v3\phase_a_files_read.txt`.
- Before starting, check whether any CLAUDE.md, memory file or other context loaded into this
  session mentions GM, Cruise, or wind-down vocabulary. Record your answer verbatim; it goes in the
  freeze file as `context_contamination`. Proceed either way.
- Save this protocol, byte for byte as fetched, as `data\winddown_v3\protocol_received.md`.

## A0. One shared matcher

Write `data\winddown_v3\scripts\common.py` with:

- `normalize(text)`: Unicode NFKC; U+00A0, U+2007, U+202F and every whitespace run become one
  space; U+2010 to U+2015 and U+2212 become `-`; curly single and double quotes become ASCII.
- `term_regex(term)`: split `normalize(term).lower()` into tokens on spaces and hyphens, escape
  each, join with `[ \-]+`, and wrap as `(?<![a-z0-9])` ... `(?![a-z0-9])`.
- `matches(text, regex)`: search the compiled regex in `normalize(text).lower()`.

This matcher is used for every step below and is reused unchanged by the later session. No
stemmed, lemmatized or inflected variant of any term is ever generated.

## A1. Filings

CIKs: Uber 0001543151, Lyft 0001759509, Ford Motor Co 0000037996 (never Ford Motor Credit
0000038009). Verify each against `https://www.sec.gov/files/company_tickers.json` and the `name`
field of its submissions JSON. Enumerate filings from
`https://data.sec.gov/submissions/CIK##########.json` **and every older page listed in its
`filings.files` array**. Forms must be exactly `8-K`, `10-Q` or `10-K` (no `/A`).

Exits:
- **E1** Uber's sale of its Advanced Technologies Group (ATG) to Aurora. Announced 2020-12-07.
- **E2** Lyft's sale of its Level 5 unit to Woven Planet (Toyota). Announced 2021-04-26.
- **E3** Ford's exit from Argo AI. Announced 2022-10-26.

For each exit include:
(a) every 8-K filed from 7 days before the announcement through the filing date of the 10-K
covering the fiscal year in which the exit closed (E1 and E2: fiscal 2021; E3: fiscal 2022),
taking the main document and every EX-99.x exhibit, kept only if an A2 anchor occurs in it; and
(b) every 10-Q and 10-K filed on or after the announcement date, up to and including that 10-K.
Expected: E1 = 10-K FY2020, 10-Q Q1 to Q3 2021, 10-K FY2021; E2 = 10-Q Q1 to Q3 2021,
10-K FY2021; E3 = 10-Q Q3 2022, 10-K FY2022; plus any anchored 8-Ks. If a window holds no
anchored 8-K, log it and continue. Never use non-EDGAR sources.

Also fetch Ford's 10-K for fiscal 2021 (reference only, see A3).

Cross-check 8-K coverage with EDGAR full-text search
(`https://efts.sec.gov/LATEST/search-index?q="<anchor>"&ciks=<10-digit CIK>&forms=8-K&startdt=<YYYY-MM-DD>&enddt=<YYYY-MM-DD>`)
for each anchor and window, and confirm every hit is in your list.

Save documents under `data\winddown_v3\raw\<exit_id>\<accession>\` (Uber and Lyft documents
already in the corpus may be copied after checking the accession). Skip PDF and image exhibits and
log them. Write `a1_candidates.csv`: exit_id, accession, form, items, filed, period_of_report, doc,
url, sha256_raw, anchor_hits, included, reason.

## A2. Exit passages

Anchors, each applied only to its own exit's documents:
E1 `ATG`, `Advanced Technologies Group`, `Aurora`; E2 `Level 5`, `Woven Planet`, `Toyota`;
E3 `Argo`. Match anchors with the A0 matcher. If an anchored sentence assigns a defined term (a
quoted term inside parentheses), that term is also an anchor within that same document only;
log each one.

Clean every exit document and the Ford FY2021 10-K from the raw HTML with the same cleaner that
built the project corpus. A paragraph is the cleaner's block unit (text between blank lines if it
returns flat text). Split sentences with the splitter the project used to build `passages.csv`;
if none exists, split on `[.!?]` followed by whitespace and an uppercase letter, but not after
Inc., Corp., Co., Ltd., LLC, L.L.C., U.S., No., Mr., Ms. or Dr. Handle tables exactly as that
cleaner does and log how many anchor hits fall inside tables. Record the module, function name and
git blob hash of the cleaner, splitter and section tagger in the freeze file.

A passage is the anchored sentence plus one sentence either side within the same paragraph,
merged when windows overlap. If a heading (a block of 12 words or fewer with no terminal
punctuation) contains an anchor, the passage is the whole next paragraph. `section` comes from the
function that produced the `section` column of `passages.csv`, called unchanged; write `untagged`
if it fails or returns one label for a whole 10-K or 10-Q, and `exhibit` if it returns none for an
8-K exhibit. Keep every section; nothing in Phase A filters on section.

Write `exit_passages.csv`: exit_id, company, accession, form, doc, filed, period_of_report, url,
section, para_id, anchor_hit, anchor_type (unit, counterparty, defined_term, heading), text.

Check: every 10-K and 10-Q selected in A1 has at least one anchor hit. If one has zero, fix
normalization or splitting only (never the anchor list), rerun, and log the change.

## A3. Reference passages (for the specificity filter)

Stream `data\m4\passages.csv` with `csv.DictReader(encoding="utf-8")`. Keep a row only if its
ticker is `UBER` or `LYFT`, deciding before the row is stored; never print, count or summarize any
other ticker. Keep rows filed strictly before that company's announcement (Uber before 2020-12-07,
Lyft before 2021-04-26) whose section is not `risk_factors` or `fls_legend`. Add the Ford FY2021
10-K passages built with the A2 procedure and E3 anchors, unchanged. Use the `text` field. Write
`reference_passages.csv` (source, accession, filed, section, text) and log row counts and mean
word counts per source.

## A4. Manifest and lock

Write `a1_manifest.csv`: per document, exit_id, accession, form, filed, url, found (yes/no) and
number of A2 passages; plus total A2 and A3 row counts. Check it for completeness now. From the
moment A5 starts, A1 to A3 outputs are locked: no filing added or removed, no anchor, window or
segmentation change, no rerun of A5. Never compare candidate or final terms with any previously
used vocabulary list.

## A5. Blind extraction (one fresh subagent)

Copy `exit_passages.csv` alone to `data\winddown_v3\blind\exit_passages.csv`. Spawn exactly one
fresh subagent. Its prompt is exactly the instruction below, followed by the passages as lines
`exit_id<TAB>text` pasted inline. If that would exceed 150,000 characters, give instead only the
absolute path of the blind copy and add the sentence "Read only that one file." Add nothing else:
no background, no examples, no description of the study, nothing about any other company.

> Below are passages from SEC filings by three companies about autonomous-driving units or
> programs they ended their involvement in. List every word or short phrase (1 to 3 words) these
> passages use to describe what happened to the unit or program, or how the company ended its
> involvement in it. Output one term per line as: term<TAB>exit_id<TAB>verbatim quote (the
> sentence containing the term, copied exactly). Use only wording that appears in the passages;
> do not add terms from general knowledge. Do not use any tools.

Save the exact prompt as `a4_prompt.txt` and the full, unedited reply as `a4_response.txt`.
Record the subagent's model id and number of tool calls. Run it once; rerun only if a call
returns nothing, and log any rerun. **If you have no subagent tool, stop after A4, report that,
and wait. Never do A5 yourself.**

## A6. Mechanical filters (in order; log every drop and its rule in `filter_log.csv`)

- **F1 attestation.** Keep a term only if `term_regex(term)` matches at least one exit passage.
  A term not found is dropped, never corrected to a nearby form. Deduplicate case-insensitively.
- **F2 names and numbers.** Drop a term if it contains a digit, a currency symbol or a month
  name; or if it equals or contains any of: Uber, Lyft, Ford, Aurora, Woven, Planet, Toyota, Argo,
  ATG, Advanced Technologies Group, Level 5, Volkswagen, VW; or if any of its tokens has at least
  one occurrence in the exit passages that is not sentence-initial and is capitalized in every such
  occurrence. A multi-word term is dropped whole, never trimmed.
- **F3 specificity.** Reference rate = reference passages whose `text` matches the term, divided
  by all reference passages, pooled over Uber, Lyft and Ford. Drop the term if its rate is strictly
  greater than 0.05. Log the pooled numerator and denominator and the separate per-source rates;
  only the pooled rate decides.

No other filter, semantic or otherwise, is applied. The **primary** list uses 0.05. Also record,
labeled **secondary**, the lists that thresholds 0.02 and 0.10 would produce with the identical
pipeline. For each term, compute mechanically which exits' passages it matches and how often
(`exit_ids`, `per_exit_counts`); keep the subagent's own exit_id and quote in separate fields.
If the primary list is empty, freeze and report that; never loosen a filter.

## A7. Freeze and commit

Write `data\winddown_v3\frozen_winddown_terms_v3.json` containing: `created_utc`;
`protocol_sha256` (of `protocol_received.md`); exit definitions and source accessions with URLs;
cleaner, splitter and section-tagger names with blob hashes; thresholds; the primary terms (term,
regex string, exit_ids, per_exit_counts, reference_rate, subagent exit_id and quote); the two
secondary lists; `context_contamination`; the subagent model id and tool-call count; the sha256
of every other committed file; and this note, verbatim:

> Frozen before this list was applied to any GM text. This session's instructions contained no GM
> results and no earlier wind-down list. The term-selection subagent received only the A5
> instruction and the exit-passage text. No GM row, GM filing, project note or earlier wind-down
> output was opened during Phase A (see phase_a_files_read.txt). The session and the subagent are
> language models whose training may include public reporting on GM and Cruise; the attestation
> filter limits terms to wording used in the three non-GM exit filings. All later intervals are
> conditional on this single extraction.

Also add `data\winddown_v3\.gitattributes` containing the line `* -text`.

Make **one** commit containing exactly the files under `data\winddown_v3\` except `raw\` (the
JSON, `exit_passages.csv`, `reference_passages.csv`, `a1_candidates.csv`, `a1_manifest.csv`,
`filter_log.csv`, `a4_prompt.txt`, `a4_response.txt`, `protocol_received.md`,
`phase_a_files_read.txt`, `blind\exit_passages.csv`, `scripts\*`, `.gitattributes`):

```
git check-ignore -v <paths>            # if any path is ignored, use git add -f for exactly those paths
git -c core.autocrlf=false add <paths>
git -c core.autocrlf=false commit -m "Freeze out-of-sample wind-down list v3 (before any GM scoring)" -- <paths>
```

Use the repo's configured git identity. If none is configured, add
`-c user.name="Claude (edgar-autonomy)" -c user.email="noreply@anthropic.com"` to the commit
command only. After committing, compute in Python the sha256 of the bytes returned by
`git show <SHA>:<path>` for the JSON and each CSV, and check they equal the recorded hashes.

## A8. Report and stop

End with one message in the thread (it cannot take file attachments, so paste) containing:
1. the freeze commit SHA and its UTC time;
2. the sha256 of `frozen_winddown_terms_v3.json` computed from `git show` bytes, and the output of
   `git ls-tree <SHA> data/winddown_v3`;
3. the full frozen JSON in one code block, exactly as committed;
4. per exit: documents found and passages extracted; counts dropped by F1, F2 and F3;
5. the `context_contamination` answer and the path of this session's transcript.

Then stop. Do not open any GM data, do not apply the list to any company, and do not start any
other analysis. A separate session continues from the frozen commit.
