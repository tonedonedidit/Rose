# Studio pipeline

One markdown file per video moves through these folders. The file *is* the record.

```
01-ideas → 02-scripts → 03-review → 04-approved → 05-produced → 06-scheduled → 07-published
 trend-     scriptwriter  fact-checker   producer +     publisher      🔴 Tony posts
 researcher               compliance     packager       (schedule)     analyst reviews weekly
                          (PASS/FAIL) ──FAIL──► back to scriptwriter (max 2) ──► 99-rejected
```

## Agents (`.claude/agents/`)
showrunner (runs it) · trend-researcher · scriptwriter · fact-checker · compliance-reviewer · producer · packager · publisher · analyst

## Channels (5, from search data — see initiatives/01-shorts-test/niche-research.md)
| Channel | Demand index (scary stories = 100) | Trend | Daily cap |
|---|---|---|---|
| true-crime | 134 | flat | 1 (max 2) |
| scary-stories | 100 | seasonal dip | 1 (max 3) |
| history | 37 | slight dip | 1 (max 2) |
| mythology | 29 | flat | 1 (max 3) |
| ai-stories | 11 | rising fastest | 1 (max 3) |
Cut on data: brain rot (−83%), reddit stories (reused-content risk), conspiracy theories (misinformation risk).

## Human gates (Tony)
- 🔴 Every upload/post, account creation, any money spent.
- Review each approved script (~3 min). 5 videos/day ≈ 15 min/day.

## How to run
In a Claude Code session on this repo: "showrunner: run today's batch" (or "make 7 days of buffer for all channels").

## Known gaps (to build next)
- `studio/tools/render.py`: script + TTS + visuals + captions → 9:16 MP4 (ffmpeg is installed; TTS engine TBD, free/local first).
- Metrics intake: no YouTube/TikTok analytics connector; Tony pastes or exports weekly.
- Scheduled runs: optional daily showrunner task (🟡, needs Tony's yes).
