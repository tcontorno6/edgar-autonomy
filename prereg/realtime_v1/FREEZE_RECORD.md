# Freeze record: real-time detection test v1

Pushed to GitHub **before** `realtime_v1.py` was run on the real input. Nothing in the
protocol, rules, event list, input slice or script changes after this point.

| | |
|---|---|
| Pre-registration commit | `d1234dc8da4702291e192a134dce66ef2682321a`, 2026-10-25T18:13:00Z, branch `prereg/realtime-v1` (pushed) |
| `PROTOCOL.md` sha256 | `e467d86185862231c968764b3d7af0bc2f6371ca5cdc7cc1df0a42da10a8be0f` |
| `realtime_v1.py` sha256 | `e1cfa831ee84d07579b1a089e0bf190b2e7eb6358e9e0babe81d0a8a93e5f69e` |
| `events.csv` sha256 | `1b69a26b5e8e7841c6c92b364b394991bb35c6b78a91988939c13b37ad14a16d` |
| `input_service_ex_boilerplate.csv` sha256 | `249cedef8df5d17b6ae287c3727d132596b96e4db817c0cb518d95f3d882a800` |
| Source `stance_timeline.csv` sha256 | `3005c7c9659c4433adaa30ff73e207ecff0893b575c0afb464f26f3a4274f8ca` |

## Before the freeze

- The script was run only on synthetic data (two made-up tickers) to check that it runs and
  follows the protocol. No real company was scored.
- Executor context: the same cloud session wrote the rules and will run them. It had read GM's
  quarterly series (dashboard `GM` array), M4_NOTES, GM_BREAKPOINT_CHECK and the Finding 05 text
  before writing the rules, so it is not blind to GM (PROTOCOL §7). It had not looked at the
  other five companies' quarterly values.
- `events.csv` is generated from the table in PROTOCOL §5 (32 rows); the protocol table is the
  record if they ever differ.

## Deviations (added after running; none at freeze time)
