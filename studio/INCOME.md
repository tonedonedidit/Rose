# Income streams — what's automated and what needs Tony

One video → many products. `studio/tools/repurpose.py` builds them; the **monetizer** agent runs it. Nothing is posted or sold without Tony's 🔴 yes.

| # | Stream | Automated now | Tony does (once) | Tony does (each time) | Eligible when |
|---|---|---|---|---|---|
| 1 | YouTube Shorts | ✅ upload kit: title, description, sources, affiliate link, AI note, thumbnail | Create channel | Upload/schedule in Studio (🔴) | Now (pay after YPP) |
| 2 | TikTok | ✅ caption kit | Create account | Post (🔴) | Now (pay after Creator Rewards) |
| 3 | Instagram + Facebook Reels | ✅ caption kits | Create accounts | Post (🔴) | Now |
| 4 | Snapchat Spotlight | ✅ auto-checks the 60s limit | Create account | Post (🔴) | Only videos ≤ 60s |
| 5 | Amazon affiliate links | ✅ added to every description (search links, disclosed) | Sign up for Amazon Associates, put tag in `monetize.json` | — | Now; account needs 3 sales in 180 days |
| 6 | Long-form compilations | ✅ `repurpose.py compile` (16:9, chapters) | — | Upload (🔴) | Once a channel has ~7+ videos (8+ min for mid-rolls) |
| 7 | Podcast | ✅ `repurpose.py podcast` (mp3, chapters) | Create a podcast host account (e.g. Spotify for Creators) | Publish (🔴) | Now |
| 8 | Ebooks of original stories | ✅ `repurpose.py ebook` (EPUB) | Gumroad and/or KDP account | List for sale (🔴); KDP AI disclosure | ~20 stories per channel |
| 9 | YouTube ads + fan funding | Tracked by analyst | Apply when eligible (🔴) | — | 500 subs + 3M Shorts views/90d (fan funding); 1k + 10M/90d or 4k watch hours (ads) |
| 10 | TikTok Creator Rewards | Tracked by analyst | Apply (🔴) | — | 10k followers + 100k views/30d, videos > 1 min |
| 11 | Done-for-you Shorts for local businesses | ⏳ render tool works; offer sheet + outreach not built | Approve offer + price | Every outreach message (🔴) | Now — fastest cash |
| 12 | Sponsorships / brand deals | ⏳ media kit later | — | Every deal (🔴) | Needs an audience |

## Automation status
- **Built and verified 2026-10-18:** render → package → compile → podcast → ebook on the first true-crime video.
- **Not automated, by rule:** posting, signing up, selling, outreach (🔴).
- **Optional next:** a scheduled daily run (showrunner makes the batch, monetizer builds kits, you get a list to approve). Needs your 🟡 yes.
- **Why posting isn't automated:** YouTube API uploads from unaudited projects are locked private with a small daily quota; TikTok's posting API needs an app audit. A scheduler service could be added later once channels prove themselves.
