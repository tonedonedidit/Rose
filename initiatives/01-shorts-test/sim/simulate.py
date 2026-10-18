"""Monte Carlo model of a faceless Shorts operation over 180 days.

Every input below is an ESTIMATE or a platform rule, not measured channel data.
Run: python3 simulate.py   (prints markdown tables)
"""
import math
import random

DAYS = 180

# Platform rules (published thresholds)
YPP_SUBS = 1000
YPP_SHORTS_VIEWS_90D = 10_000_000
TT_FOLLOWERS = 10_000          # TikTok Creator Rewards: 10k followers,
TT_VIEWS_30D = 100_000         # 100k views in last 30 days, videos > 1 min

# Niche demand weights = 12-mo YouTube search interest from niche-research.md
NICHES = {
    "true crime": 69, "scary stories": 52, "reddit stories": 52, "brain rot": 22,
    "history documentary": 19, "make money online": 13, "ai stories": 8,
    "personal finance": 5, "dark history": 4, "space facts": 3,
}


def sample_world(rng):
    """Uncertain inputs, re-drawn each run. Ranges are ESTIMATES from creator benchmarks."""
    return {
        "base_median_views": rng.uniform(80, 300),     # median views/Short, new faceless channel, good quality
        "sigma": rng.uniform(1.5, 1.9),                # heavy tail: most flop, a few go viral
        "subs_per_1k_views": rng.uniform(0.5, 1.5),
        "rpm": rng.uniform(0.02, 0.08),                # $ per 1,000 Shorts views after YPP
        "base_reject": rng.uniform(0.10, 0.20),        # YPP rejection for original, reviewed content
        "template_reject": rng.uniform(0.55, 0.80),    # extra rejection for mass-produced/templated
        "strike_hazard_month": rng.uniform(0.02, 0.06),  # spam/inauthentic action per high-volume channel per month
        "tt_rpm": rng.uniform(0.40, 1.00),             # $ per 1,000 qualified TikTok views (>1 min videos)
        "tt_view_ratio": rng.uniform(0.5, 1.5),        # TikTok views vs YouTube for the same video
        "tt_follow_per_1k": rng.uniform(1.0, 3.0),
    }


def run(plan, seed):
    rng = random.Random(seed)
    w = sample_world(rng)
    ch_count, per_day, review_min_week = plan["channels"], plan["per_day"], plan["review_min_week"]
    uploads_day = ch_count * per_day
    review_per_video = review_min_week / 7 / max(uploads_day, 1)
    # quality: 3+ min of human review per video = full quality, floor 0.3
    q = max(0.3, min(1.0, review_per_video / 3) ** 0.5)
    # same channel splits its own test audience above ~3 uploads/day
    sat = 1.0 if per_day <= 3 else (3 / per_day) ** 0.5
    templated = per_day >= 5 and q < 0.7

    niches = sorted(NICHES, key=NICHES.get, reverse=True)[:ch_count]
    chans = []
    for n in niches:
        chans.append({"niche": n, "demand": (NICHES[n] / 69) ** 0.5, "subs": 0, "views": [],
                      "ypp": False, "next_apply": 0, "alive": True, "demonetized": False,
                      "rev": 0.0, "tt_f": 0, "tt_views": [], "tt_on": False, "tt_rev": 0.0,
                      "mom": 1.0})

    monthly = []
    for day in range(DAYS):
        for c in chans:
            if not c["alive"]:
                c["views"].append(0)
                c["tt_views"].append(0)
                continue
            m = w["base_median_views"] * c["demand"] * q * sat * (1 + c["subs"] / 2000) ** 0.6 * c["mom"]
            sig = w["sigma"] * (0.8 + 0.2 * q)   # low-retention videos rarely break out
            vids = [min(rng.lognormvariate(math.log(max(m, 1)), sig), 5e6) for _ in range(per_day)]
            v = sum(vids)
            # algorithm momentum: a breakout lifts the next weeks, decays back
            best = max(vids) / max(m, 1)
            c["mom"] = max(1.0, min(4.0, c["mom"] * 0.97 + (0.3 if best > 30 else 0)))
            # TikTok cross-post (only >1 min videos qualify for Creator Rewards)
            tv = v * w["tt_view_ratio"]
            c["tt_views"].append(tv)
            c["tt_f"] += tv / 1000 * w["tt_follow_per_1k"] * q
            if not c["tt_on"] and plan["over_1min"] and c["tt_f"] >= TT_FOLLOWERS \
                    and sum(c["tt_views"][-30:]) >= TT_VIEWS_30D:
                c["tt_on"] = True
            if c["tt_on"]:
                c["tt_rev"] += tv / 1000 * w["tt_rpm"] * (0.6 if templated else 1.0)
            c["views"].append(v)
            c["subs"] += v / 1000 * w["subs_per_1k_views"] * q
            if c["ypp"] and not c["demonetized"]:
                c["rev"] += v / 1000 * w["rpm"]
            # YPP application
            if not c["ypp"] and day >= c["next_apply"] and c["subs"] >= YPP_SUBS \
                    and sum(c["views"][-90:]) >= YPP_SHORTS_VIEWS_90D:
                p = w["base_reject"] + (w["template_reject"] if templated else 0)
                if rng.random() < p:
                    c["next_apply"] = day + 30
                else:
                    c["ypp"] = True
            # monthly enforcement for high-volume templated channels
            if day % 30 == 29 and templated:
                if rng.random() < w["strike_hazard_month"]:
                    c["demonetized"] = True
                if rng.random() < w["strike_hazard_month"] / 3:
                    c["alive"] = False
        if plan.get("double_down") and day in (59, 119):
            live = [c for c in chans if c["alive"]]
            if len(live) > 1:
                worst = min(live, key=lambda c: sum(c["views"][-30:]))
                worst["alive"] = False; worst["killed"] = True
                per_day = min(per_day + 1, 3)
        if day % 30 == 29:
            mo = day // 30 + 1
            lo, hi = day - 29, day + 1
            monthly.append({
                "month": mo,
                "views": sum(sum(c["views"][lo:hi]) for c in chans),
                "subs": sum(c["subs"] for c in chans),
                "ypp": sum(c["ypp"] and not c["demonetized"] for c in chans),
                "rev_cum": sum(c["rev"] for c in chans),
                "tt_on": sum(c["tt_on"] and c["alive"] for c in chans),
                "tt_cum": sum(c["tt_rev"] for c in chans),
                "dead": sum(not c["alive"] and not c.get("killed") for c in chans),
            })
    return w, q, sat, monthly, chans


def cost_per_month(plan, stack):
    vids = plan["channels"] * plan["per_day"] * 30
    return vids, stack["fixed"] + vids * stack["per_video"]


STACKS = {  # ESTIMATES; verify before buying
    "free/local (local TTS, stock, ffmpeg)": {"fixed": 0, "per_video": 0.0},
    "cheap paid (TTS tier + image credits)": {"fixed": 30, "per_video": 0.05},
    "premium (ElevenLabs + AI video)": {"fixed": 100, "per_video": 0.40},
}

PLANS = {
    "Your plan: 10 channels x 10/day": {"channels": 10, "per_day": 10, "review_min_week": 600,
                                        "over_1min": False},
    "Fixed plan: 3 channels x 2/day, 61s+, double down": {"channels": 3, "per_day": 2,
                                        "review_min_week": 600, "over_1min": True, "double_down": True},
}


def fmt(n):
    return f"{n/1e6:.1f}M" if n >= 1e6 else f"{n/1e3:.0f}k" if n >= 1e3 else f"{n:.0f}"


if __name__ == "__main__":
    for pname, plan in PLANS.items():
        print(f"\n## {pname}\n")
        vids, _ = cost_per_month(plan, STACKS["free/local (local TTS, stock, ffmpeg)"])
        print(f"Videos per month: {vids:,}. Monthly cost by tool stack (ESTIMATE):")
        for s, st in STACKS.items():
            print(f"- {s}: ${cost_per_month(plan, st)[1]:,.0f}")
        totals = []
        for i, seed in enumerate([11, 22, 33, 44, 55], 1):
            w, q, sat, monthly, chans = run(plan, seed)
            print(f"\n### Run {i} (median views/Short {w['base_median_views']:.0f}, "
                  f"RPM ${w['rpm']:.3f}, quality {q:.2f}, self-cannibalization {sat:.2f})\n")
            print("| Month | YT views that month | YT subs | YT channels paid | TikTok channels paid | Revenue to date (YT+TT) | Channels banned |")
            print("|---|---|---|---|---|---|---|")
            for r in monthly:
                print(f"| {r['month']} | {fmt(r['views'])} | {fmt(r['subs'])} | {r['ypp']} | {r['tt_on']} | "
                      f"${r['rev_cum'] + r['tt_cum']:,.0f} | {r['dead']} |")
            totals.append(monthly[-1])
        print(f"\n**5-run summary, month 6:** total revenue "
              f"${min(t['rev_cum']+t['tt_cum'] for t in totals):,.0f}–${max(t['rev_cum']+t['tt_cum'] for t in totals):,.0f}; "
              f"YT channels paid {min(t['ypp'] for t in totals)}–{max(t['ypp'] for t in totals)}; "
              f"TikTok channels paid {min(t['tt_on'] for t in totals)}–{max(t['tt_on'] for t in totals)}; "
              f"channels banned {min(t['dead'] for t in totals)}–{max(t['dead'] for t in totals)}")
