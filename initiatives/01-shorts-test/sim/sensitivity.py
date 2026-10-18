"""What per-video performance is needed before each plan earns in 6 months?
Forces the median views per Short; 5 seeds each. Same model as simulate.py."""
import simulate as S

orig = S.sample_world
for pname, plan in S.PLANS.items():
    print(f"\n### {pname}\n")
    print("| Median views per Short (good quality) | Month-6 revenue, 5 runs | YT channels paid | TikTok channels paid | Banned |")
    print("|---|---|---|---|---|")
    for med in (300, 1000, 3000, 10000):
        def world(rng, med=med):
            w = orig(rng); w["base_median_views"] = med; return w
        S.sample_world = world
        res = [S.run(plan, seed)[3][-1] for seed in (11, 22, 33, 44, 55)]
        rev = [r["rev_cum"] + r["tt_cum"] for r in res]
        print(f"| {med:,} | ${min(rev):,.0f}–${max(rev):,.0f} | {min(r['ypp'] for r in res)}–{max(r['ypp'] for r in res)} | "
              f"{min(r['tt_on'] for r in res)}–{max(r['tt_on'] for r in res)} | {min(r['dead'] for r in res)}–{max(r['dead'] for r in res)} |")
    S.sample_world = orig
