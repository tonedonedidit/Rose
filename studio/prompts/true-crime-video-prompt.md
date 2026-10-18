# Prompt: True Crime Short — script, story flow, animation style

Use this as the brief for the scriptwriter → producer handoff on the true-crime channel. It produces a script **and** a render spec for `studio/tools/render.py`. Paste it with the idea file attached, or say "follow studio/prompts/true-crime-video-prompt.md for <idea file>".

---

## ROLE
You write and storyboard a 61–75 second faceless true-crime Short for the channel "Case Closed in 60". Calm, precise, never sensational. Every fact is sourced. The output must pass the fact-checker and compliance-reviewer.

## INPUT
- One idea file (`studio/pipeline/01-ideas/…`) with the case, angle and source leads.
- Case rule: closed with a conviction or guilty plea, or officially unsolved. Never accuse an uncharged or acquitted person.

## STORY FLOW (beats and timing)
| Beat | Time | Job | Scene types that fit |
|---|---|---|---|
| 1. Hook | 0–4s | One line of tension or contradiction, ≤ 12 words. Start mid-mystery. | `silhouette`, `title`, `date` |
| 2. Stakes | 4–14s | How big / how long / how many. One hard number. | `counter`, `map` |
| 3. The wall | 14–24s | Why it was hard to solve. End on the open question. | `title`, `black` |
| 4. The turn | 24–36s | The event that set up the break. | `newspaper`, `date`, `title` |
| 5. Re-hook | ~30–40s | Pull them past the midpoint. **Vary the form**: a question, a time jump, a short fragment, a contradiction, or skip it. Do not reuse "But that wasn't the…" two videos in a row. | `black` |
| 6. The clue | 36–55s | The specific detail that cracked it, shown concretely. | `name`, `compare` |
| 7. Resolution | 55–68s | Arrest, plea or verdict, exact legal wording. | `map`, `cabin`, `verdict` |
| 8. Payoff | 68–75s | The meaning of the clue in one line. Rotate endings: loop back to the hook, a quiet fact, a question to the viewer, or an irony. | `ink`, `title` |

## SCRIPT RULES
- 155–190 words. One idea per sentence. Short sentences.
- Concrete over vague: dates, places, counts, names (sourced).
- Legal words exact: "convicted of", "pleaded guilty", "charged with", "acquitted".
- No gore, no method detail (how weapons were built or used), no victim names or minors' names unless central and public, no speculation about living private people.
- On-screen text never puts quote marks around a paraphrase.
- List every claim with its source under **Claims to check**.

## ANIMATION STYLE ("evidence noir")
- **Palette:** near-black warm background (#0C0B0A), paper cream (#E2DAC8), one accent per channel (true crime amber #E8A33D); red (#C8322D) only for deaths and verdicts.
- **Type:** headlines in a bold serif (typed on), labels in a monospace "case file" face, captions in heavy sans, ALL CAPS, 3 words at a time, current word in the accent color.
- **Motion:** slow push-in on every scene (about 4%); typewriter reveals; stamps slam in; pins drop; highlights sweep across documents; short cross-fades; hard cuts to black for re-hooks.
- **Texture:** film grain and vignette on every frame.
- **People:** never real photos without clear rights. Use silhouettes and name cards. No realistic AI faces (if any are used, the synthetic-content disclosure is ON).
- **Sound:** calm low male voice (`am_michael`), original low drone under the voice at about -20 dB, and the final mix normalised to -14 LUFS.

## OUTPUT
1. The script sections in the item file (Hook, Narration, Beat sheet, Claims to check, Word count).
2. `studio/specs/<id>.json`: one scene per beat, with `say` holding the exact narration for that beat, using only the scene types in `studio/tools/SPEC.md`.
3. Run `render.py SPEC --check` and adjust `speed` (1.0–1.2) until the total is 61–75s; if it's still over 75s at 1.2, cut words.
4. Run `--stills` and look at the contact sheet. Nothing may overlap the caption band (y > 1600) and no text may be cut off.

## OPTIONAL: AI image prompts (when image credits exist)
Use one style suffix on every prompt so a channel's videos look like one series:
`… , cinematic film noir still, dark warm shadows, single amber practical light, 35mm grain, shallow depth of field, no faces visible, no text, 9:16 vertical`
Examples:
- Hook: `empty rural post office counter at night, a brown paper package under a desk lamp, …`
- The clue: `two yellowed typed letters side by side on a kitchen table, a hand-held highlighter, …`
- Resolution: `a remote one-room wooden cabin in a pine forest at dusk, a lit window, …`
Never generate a real person's likeness.
