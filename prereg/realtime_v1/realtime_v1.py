"""Real-time detection test, v1. Implements PROTOCOL.md exactly; committed before any run.

Usage: python realtime_v1.py INPUT_CSV EVENTS_CSV OUT_DIR
"""
import sys
import json
import pandas as pd

MIN_PASSAGES = 3
MIN_REF = 8
R1_K = 3.0
R2_K, R2_N = 2.0, 2
R3_K, R3_H = 0.5, 5.0
TARGET = pd.Timestamp("2024-12-10")
WINDOW_Q = 4


def q_end(q):
    return pd.Period(q, freq="Q").end_time.normalize()


def eligible(df):
    e = df[(df.passages >= MIN_PASSAGES) & (df.autonomy_words > 0)]
    return e.sort_values("quarter").reset_index(drop=True)


def ref_stats(e, before_idx):
    """Mean and SD of x over eligible quarters strictly before row before_idx."""
    b = e.net_tone_delta_vs_baseline.iloc[:before_idx]
    if len(b) < MIN_REF:
        return None
    sd = b.std(ddof=1)
    if not sd > 0:
        return None
    return b.mean(), sd, len(b)


def evaluate_at(rows_to_T):
    """All three rules at T = last quarter in rows_to_T, using only those rows."""
    e = eligible(rows_to_T)
    T = rows_to_T.quarter.max()
    if e.empty or e.quarter.iloc[-1] != T:
        return None  # T not eligible
    i = len(e) - 1
    x = e.net_tone_delta_vs_baseline
    out = {"quarter": T, "x": float(x.iloc[i])}
    s = ref_stats(e, i)
    out["evaluable"] = s is not None
    if s:
        m, sd, n = s
        out.update(ref_n=n, ref_mean=m, ref_sd=sd, z=(x.iloc[i] - m) / sd)
        out["R1"] = bool(out["z"] < -R1_K)
    else:
        out["R1"] = None
    # R2: previous eligible quarter P and T against B_P
    out["R2"] = None
    if i >= 1:
        s2 = ref_stats(e, i - 1)
        if s2:
            m, sd, _ = s2
            zp, zt = (x.iloc[i - 1] - m) / sd, (x.iloc[i] - m) / sd
            out.update(r2_ref_n=s2[2], r2_zp=zp, r2_zt=zt)
            out["R2"] = bool(zp < -R2_K and zt < -R2_K)
    # R3: CUSUM rebuilt from the start using only rows <= T
    c = 0.0
    fired = False
    for j in range(len(e)):
        sj = ref_stats(e, j)
        if not sj:
            continue
        zj = (x.iloc[j] - sj[0]) / sj[1]
        c = max(0.0, c - zj - R3_K)
        fired = c > R3_H
        if fired and j < len(e) - 1:
            c = 0.0
    out["cusum"] = c
    out["R3"] = bool(fired) if out["evaluable"] else None
    return out


def walk(df):
    recs = []
    for T in sorted(df.quarter.unique()):
        r = evaluate_at(df[df.quarter <= T])  # truncate at T: no lookahead
        if r is not None:
            recs.append(r)
    return pd.DataFrame(recs)


def episodes(w, rule):
    ev = w[w[rule].notna()]
    eps, prev = [], False
    for _, r in ev.iterrows():
        if r[rule] and not prev:
            eps.append({"start": r.quarter, "quarters": [r.quarter]})
        elif r[rule] and prev:
            eps[-1]["quarters"].append(r.quarter)
        prev = bool(r[rule])
    return eps


def follow(ep_start, ev_t, tiers):
    lo = q_end(ep_start)
    hi = q_end(str(pd.Period(ep_start, freq="Q") + WINDOW_Q))
    hit = ev_t[(ev_t.date > lo) & (ev_t.date <= hi) & ev_t.tier.isin(tiers)]
    return hit


def main(inp, evp, outdir):
    d = pd.read_csv(inp)
    evs = pd.read_csv(evp, parse_dates=["date"])
    summary = {}
    walks = []
    for tk in sorted(d.ticker.unique()):
        w = walk(d[d.ticker == tk])
        w.insert(0, "ticker", tk)
        walks.append(w)
        ev_t = evs[evs.ticker == tk]
        n_elig = len(eligible(d[d.ticker == tk]))
        res = {"eligible_quarters": n_elig,
               "evaluated_quarters": int(w.evaluable.sum()) if len(w) else 0}
        for rule in ["R1", "R2", "R3"]:
            n_eval = int(w[rule].notna().sum()) if len(w) else 0
            if n_eval == 0:
                res[rule] = {"feasible": False}
                continue
            eps = episodes(w, rule)
            for ep in eps:
                ep["end_date"] = str(q_end(ep["start"]).date())
                ep["tier1_after"] = follow(ep["start"], ev_t, [1]).event.tolist()
                ep["tier12_after"] = follow(ep["start"], ev_t, [1, 2]).event.tolist()
                ep["events_in_or_before_quarter"] = ev_t[ev_t.date <= q_end(ep["start"])].event.tolist()
            r = {"feasible": True, "evaluated": n_eval,
                 "firing_quarters": w.loc[w[rule] == True, "quarter"].tolist(),
                 "episodes": eps,
                 "unfollowed_tier1": sum(1 for e in eps if not e["tier1_after"]),
                 "unfollowed_tier12": sum(1 for e in eps if not e["tier12_after"])}
            if tk == "GM" and eps:
                first = eps[0]["start"]
                lead = (TARGET - q_end(first)).days
                r["first_firing"] = first
                r["lead_days_to_2024_12_10"] = lead
                r["lead_quarters"] = int(pd.Period("2024Q4", freq="Q").ordinal - pd.Period(first, freq="Q").ordinal)
            res[rule] = r
        summary[tk] = res
    pd.concat(walks).to_csv(f"{outdir}/walk_forward.csv", index=False, lineterminator="\n", float_format="%.4f")
    with open(f"{outdir}/results.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(summary, f, indent=1, default=str)
    print(json.dumps(summary, indent=1, default=str))


if __name__ == "__main__":
    main(*sys.argv[1:4])
