# Render spec (`studio/specs/<id>.json`)

```json
{
  "id": "<channel>-<yyyymmdd>-<slug>",
  "voice": "am_michael",        // Kokoro voice id (see table below)
  "speed": 1.15,                // tune until total is 61–75s (render --check prints it)
  "accent": "#E8A33D",          // channel highlight color from STYLE.md
  "caption_words": 3,           // words per caption chunk
  "sentence_gap": 0.12,         // seconds of silence between sentences
  "scenes": [ { "type": "...", "say": "narration for this scene", "pad": 0.25, ...params } ]
}
```
Each scene lasts exactly as long as its narration (plus `pad`). Captions come from `say`.

## Scene types
| type | params | use for |
|---|---|---|
| `title` | `text` (typed on), `sub` | hook statement, key claim |
| `black` | `text` | re-hook / hard cut question |
| `silhouette` | `label`, `sub` | unknown suspect / "nobody had seen" |
| `counter` | `number`, `label`, `second`, `marked` (list of 1-based squares to turn red) | counts, victims, years |
| `newspaper` | `masthead` (don't use real paper logos), `date`, `stamp` | publication, headlines |
| `date` | `date`, `label` | a turning-point date |
| `name` | `name`, `role` | introducing a real person (no photo) |
| `compare` | `left`, `right`, `verdict`, `highlight` (line indexes) | evidence match, then/now |
| `map` | `lat`, `lon`, `zoom`, `label`, `sub` | real US location (lower 48) |
| `cabin` | `label` | night location / arrest scene |
| `verdict` | `stamp`, `lines` | plea, verdict, sentence |
| `ink` | — | ending; handwriting then fade to black (loops to opening) |

## Voices (Kokoro, free)
True crime: `am_michael` (calm) or `am_onyx` (deeper). Scary: `am_fenrir`, `bm_lewis`. History: `bm_george`, `bm_daniel`. Mythology: `bm_fable`. AI stories: `am_puck`, `af_nova` (`af_*` voices are female).

## Commands
```
python3 studio/tools/setup_assets.py                  # once
python3 studio/tools/render.py SPEC --check           # voice only: prints duration
python3 studio/tools/render.py SPEC --stills DIR      # contact sheet, one frame per scene (fast QA)
python3 studio/tools/render.py SPEC                   # full MP4 → studio/output/<id>.mp4 (~4–5 min for 75s)
```
