# Simulation: 10 channels × 10 Shorts/day vs a fixed plan, 6 months, 5 runs each

Run on 2026-10-18 with `sim/simulate.py` and `sim/sensitivity.py`. **This is a model, not real channel data.** Every input is either a platform rule or an ESTIMATE taken from benchmarks (listed at the bottom). Each run re-draws the uncertain inputs (views per Short, ad rate, sub rate, enforcement risk), so the 5 runs show the spread.

## Bottom line
1. **Your plan (10 channels × 10 a day = 3,000 videos a month): $0 in all 5 runs.** It gets lots of total views (about 350–580k a month) but no channel ever qualifies for pay. Each video is too weak, the views are split 10 ways, and templated mass uploads get rejected for the YouTube Partner Program (YPP).
2. **Fixed plan (3 channels × 2 a day, 61s+ videos, cut the weakest channel at days 60 and 120): also $0 in all 5 runs at today's assumed views per Short (100–300).** Six months is short. Neither plan pays if the videos are average.
3. **Sensitivity is what decides this.** Once the videos are good, the fixed plan wins at every level of per-video performance:

| Median views per Short | Your plan, month-6 revenue | Fixed plan, month-6 revenue |
|---|---|---|
| 300 | $0 | $0 |
| 1,000 | $0 | $0–$1,698 |
| 3,000 | $0 | $886–$19,850 |
| 10,000 (rare for faceless channels) | $0–$6,470 | $34,039–$205,950 |

**What drives money is views per video (hook + retention), not video count.** Your plan scales count and pushes per-video quality down, so it loses even when the content is good.

## What happens to your plan, and the fix for each problem

| # | Problem (when it hits) | Why | Fix, built into the plan now |
|---|---|---|---|
| 1 | **Rejected for YPP / demonetized** (as soon as you apply) | 3,000 near-identical AI videos a month is exactly what the "inauthentic content" rule describes. It's enforced per channel, and linked channels share one AdSense account | Max 3 uploads a day per channel; every script original and approved by you; vary the story structure, not just names |
| 2 | **Not enough review time** (week 1) | 100 videos a day at 10 h/week of review is about 51 seconds per video. The model's quality falls to 0.53 | Volume = review capacity: about 3 min per video. 10 h/week covers about 28 videos a day; 100 a day needs about 35 h/week (corrected 2026-10-18; earlier text said 4 a day, which was wrong) |
| 3 | **Channels compete with themselves** (week 1) | 10 a day from one channel splits its own test audience. The model applies a 0.55 multiplier to every video | ≤3 a day per channel |
| 4 | **Upload limits** (day 1 of automation) | YouTube Data API default quota: uploads cost about 1,600 of 10,000 daily units, so about 6 uploads a day per project. Uploads from unaudited API projects are locked private. ESTIMATE (from my knowledge of the API; verify) | Schedule uploads in YouTube Studio in weekly batches; apply for the API audit only once a channel proves itself |
| 5 | **TikTok pays nothing** | Creator Rewards needs videos over 1 minute plus 10k followers and 100k views in 30 days. Unaudited apps can only post privately | Cut every video to 61–75s; post through the TikTok app or its own scheduler |
| 6 | **Budget blown** (month 1) | 3,000 videos: about $180/mo on a cheap stack, about $1,300 on premium (ESTIMATE). The fixed plan is $0–172 | Free local voice + stock to start; pay for premium voice only on a channel that's winning |
| 7 | **Running out of ideas / true-crime legal risk** | 300 unique stories a month per channel; true crime at 10 a day can't be fact-checked → defamation risk | True crime at ≤2 a day with sources in the description; fiction channels carry the volume |
| 8 | **Copyright claims** | Music and stock footage at scale | YouTube Audio Library and licensed stock only, with the license logged |
| 9 | **Bad niches** | 10 channels forces niches 4–10: brain rot (down 83%), space facts, personal finance (low search) | Only the top niches by search data (true crime, scary/AI stories, history) |
| 10 | **6 months of $0 and quitting** | Even good plans can show $0 at month 6 | Day-30 gates: median views < 500 → change hook/format; cut the weakest channel at days 60 and 120; add affiliate or product income that doesn't wait for YPP |
| 11 | **Storage** | 3,000 renders × ~30 MB ≈ 90 GB a month | Keep project files, delete renders after upload |
| 12 | **Bans spread across channels** | 1 of 10 channels banned in 4 of 5 runs of your plan; linked accounts share risk | Fewer, cleaner channels; nothing spammy on the AdSense account you'll depend on |

## Limits of this model (read before trusting it)
- None of the inputs are measured from your channels. Your real first 30 days will replace the guesses.
- Long-form videos aren't modeled. Long-form is the other way into YPP (4,000 watch hours) and pays far more per view.
- How the algorithm boosts a channel that's working is a rough guess. Real viral hits are lumpier than the model.
- The top rows (10,000 median views) are rare for new faceless channels. Treat them as "what has to be true", not a forecast.

## Inputs
- **Platform rules:** YPP Shorts path is 1,000 subs + 10M Shorts views in 90 days. TikTok Creator Rewards is 10k followers + 100k views in 30 days + videos over 1 minute.
- **Niche demand:** Google Trends YouTube search, US, 12 months (`niche-research.md`).
- **ESTIMATES (vendor blogs, creator reports):**
  - median views per Short 80–300 (new, good-quality channel)
  - Shorts ad rate (RPM) $0.02–0.08 per 1,000 views
  - TikTok $0.40–1.00 per 1,000 qualified views
  - 0.5–1.5 subs per 1,000 views
  - YPP rejection 10–20% for original content, +55–80% for templated mass uploads
  - 2–6% monthly enforcement risk per high-volume templated channel

---

# Full results: every run, month by month

## Your plan: 10 channels x 10/day

Videos per month: 3,000. Monthly cost by tool stack (ESTIMATE):
- free/local (local TTS, stock, ffmpeg): $0
- cheap paid (TTS tier + image credits): $180
- premium (ElevenLabs + AI video): $1,300

### Run 1 (median views/Short 180, RPM $0.048, quality 0.53, self-cannibalization 0.55)

| Month | YT views that month | YT subs | YT channels paid | TikTok channels paid | Revenue to date (YT+TT) | Channels banned |
|---|---|---|---|---|---|---|
| 1 | 338k | 257 | 0 | 0 | $0 | 0 |
| 2 | 355k | 527 | 0 | 0 | $0 | 0 |
| 3 | 375k | 813 | 0 | 0 | $0 | 0 |
| 4 | 465k | 1k | 0 | 0 | $0 | 0 |
| 5 | 554k | 2k | 0 | 0 | $0 | 0 |
| 6 | 578k | 2k | 0 | 0 | $0 | 0 |

### Run 2 (median views/Short 291, RPM $0.080, quality 0.53, self-cannibalization 0.55)

| Month | YT views that month | YT subs | YT channels paid | TikTok channels paid | Revenue to date (YT+TT) | Channels banned |
|---|---|---|---|---|---|---|
| 1 | 390k | 109 | 0 | 0 | $0 | 0 |
| 2 | 376k | 214 | 0 | 0 | $0 | 0 |
| 3 | 408k | 329 | 0 | 0 | $0 | 0 |
| 4 | 431k | 449 | 0 | 0 | $0 | 0 |
| 5 | 412k | 565 | 0 | 0 | $0 | 0 |
| 6 | 427k | 684 | 0 | 0 | $0 | 0 |

### Run 3 (median views/Short 205, RPM $0.037, quality 0.53, self-cannibalization 0.55)

| Month | YT views that month | YT subs | YT channels paid | TikTok channels paid | Revenue to date (YT+TT) | Channels banned |
|---|---|---|---|---|---|---|
| 1 | 361k | 254 | 0 | 0 | $0 | 0 |
| 2 | 490k | 599 | 0 | 0 | $0 | 0 |
| 3 | 478k | 936 | 0 | 0 | $0 | 0 |
| 4 | 392k | 1k | 0 | 0 | $0 | 0 |
| 5 | 455k | 2k | 0 | 0 | $0 | 0 |
| 6 | 525k | 2k | 0 | 0 | $0 | 0 |

### Run 4 (median views/Short 170, RPM $0.031, quality 0.53, self-cannibalization 0.55)

| Month | YT views that month | YT subs | YT channels paid | TikTok channels paid | Revenue to date (YT+TT) | Channels banned |
|---|---|---|---|---|---|---|
| 1 | 309k | 225 | 0 | 0 | $0 | 0 |
| 2 | 357k | 485 | 0 | 0 | $0 | 1 |
| 3 | 316k | 715 | 0 | 0 | $0 | 1 |
| 4 | 335k | 959 | 0 | 0 | $0 | 1 |
| 5 | 312k | 1k | 0 | 0 | $0 | 1 |
| 6 | 440k | 2k | 0 | 0 | $0 | 1 |

### Run 5 (median views/Short 100, RPM $0.064, quality 0.53, self-cannibalization 0.55)

| Month | YT views that month | YT subs | YT channels paid | TikTok channels paid | Revenue to date (YT+TT) | Channels banned |
|---|---|---|---|---|---|---|
| 1 | 305k | 106 | 0 | 0 | $0 | 0 |
| 2 | 323k | 218 | 0 | 0 | $0 | 0 |
| 3 | 418k | 363 | 0 | 0 | $0 | 0 |
| 4 | 432k | 514 | 0 | 0 | $0 | 0 |
| 5 | 462k | 674 | 0 | 0 | $0 | 0 |
| 6 | 345k | 794 | 0 | 0 | $0 | 0 |

**5-run summary, month 6:** total revenue $0–$0; YT channels paid 0–0; TikTok channels paid 0–0; channels banned 0–1

## Fixed plan: 3 channels x 2/day, 61s+, double down

Videos per month: 180. Monthly cost by tool stack (ESTIMATE):
- free/local (local TTS, stock, ffmpeg): $0
- cheap paid (TTS tier + image credits): $39
- premium (ElevenLabs + AI video): $172

### Run 1 (median views/Short 180, RPM $0.048, quality 1.00, self-cannibalization 1.00)

| Month | YT views that month | YT subs | YT channels paid | TikTok channels paid | Revenue to date (YT+TT) | Channels banned |
|---|---|---|---|---|---|---|
| 1 | 158k | 226 | 0 | 0 | $0 | 0 |
| 2 | 122k | 399 | 0 | 0 | $0 | 0 |
| 3 | 82k | 516 | 0 | 0 | $0 | 0 |
| 4 | 128k | 698 | 0 | 0 | $0 | 0 |
| 5 | 48k | 766 | 0 | 0 | $0 | 0 |
| 6 | 70k | 866 | 0 | 0 | $0 | 0 |

### Run 2 (median views/Short 291, RPM $0.080, quality 1.00, self-cannibalization 1.00)

| Month | YT views that month | YT subs | YT channels paid | TikTok channels paid | Revenue to date (YT+TT) | Channels banned |
|---|---|---|---|---|---|---|
| 1 | 175k | 92 | 0 | 0 | $0 | 0 |
| 2 | 173k | 182 | 0 | 0 | $0 | 0 |
| 3 | 168k | 270 | 0 | 0 | $0 | 0 |
| 4 | 136k | 342 | 0 | 0 | $0 | 0 |
| 5 | 75k | 381 | 0 | 0 | $0 | 0 |
| 6 | 87k | 426 | 0 | 0 | $0 | 0 |

### Run 3 (median views/Short 205, RPM $0.037, quality 1.00, self-cannibalization 1.00)

| Month | YT views that month | YT subs | YT channels paid | TikTok channels paid | Revenue to date (YT+TT) | Channels banned |
|---|---|---|---|---|---|---|
| 1 | 98k | 129 | 0 | 0 | $0 | 0 |
| 2 | 159k | 338 | 0 | 0 | $0 | 0 |
| 3 | 235k | 648 | 0 | 0 | $0 | 0 |
| 4 | 136k | 827 | 0 | 0 | $0 | 0 |
| 5 | 65k | 913 | 0 | 0 | $0 | 0 |
| 6 | 65k | 998 | 0 | 0 | $0 | 0 |

### Run 4 (median views/Short 170, RPM $0.031, quality 1.00, self-cannibalization 1.00)

| Month | YT views that month | YT subs | YT channels paid | TikTok channels paid | Revenue to date (YT+TT) | Channels banned |
|---|---|---|---|---|---|---|
| 1 | 146k | 199 | 0 | 0 | $0 | 0 |
| 2 | 117k | 358 | 0 | 0 | $0 | 0 |
| 3 | 114k | 514 | 0 | 0 | $0 | 0 |
| 4 | 153k | 723 | 0 | 0 | $0 | 0 |
| 5 | 52k | 794 | 0 | 0 | $0 | 0 |
| 6 | 36k | 843 | 0 | 0 | $0 | 0 |

### Run 5 (median views/Short 100, RPM $0.064, quality 1.00, self-cannibalization 1.00)

| Month | YT views that month | YT subs | YT channels paid | TikTok channels paid | Revenue to date (YT+TT) | Channels banned |
|---|---|---|---|---|---|---|
| 1 | 124k | 81 | 0 | 0 | $0 | 0 |
| 2 | 164k | 187 | 0 | 0 | $0 | 0 |
| 3 | 123k | 267 | 0 | 0 | $0 | 0 |
| 4 | 126k | 349 | 0 | 0 | $0 | 0 |
| 5 | 51k | 382 | 0 | 0 | $0 | 0 |
| 6 | 62k | 422 | 0 | 0 | $0 | 0 |

**5-run summary, month 6:** total revenue $0–$0; YT channels paid 0–0; TikTok channels paid 0–0; channels banned 0–0

# Sensitivity

### Your plan: 10 channels x 10/day

| Median views per Short (good quality) | Month-6 revenue, 5 runs | YT channels paid | TikTok channels paid | Banned |
|---|---|---|---|---|
| 300 | $0–$0 | 0–0 | 0–0 | 0–1 |
| 1,000 | $0–$0 | 0–0 | 0–0 | 0–1 |
| 3,000 | $0–$0 | 0–0 | 0–0 | 0–1 |
| 10,000 | $0–$6,470 | 0–5 | 0–0 | 0–1 |

### Fixed plan: 3 channels x 2/day, 61s+, double down

| Median views per Short (good quality) | Month-6 revenue, 5 runs | YT channels paid | TikTok channels paid | Banned |
|---|---|---|---|---|
| 300 | $0–$0 | 0–0 | 0–0 | 0–0 |
| 1,000 | $0–$1,698 | 0–0 | 0–1 | 0–0 |
| 3,000 | $886–$19,850 | 0–2 | 1–1 | 0–0 |
| 10,000 | $34,039–$205,950 | 2–2 | 1–1 | 0–0 |
