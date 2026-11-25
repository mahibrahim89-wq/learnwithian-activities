# Status

Updated: 2026-11-25 13:10 UTC

## What was made

- Look upgrade: all word pictures use **Google Noto Emoji** color PNGs (Apache 2.0) in `icons/`, with `NOTICE` credit. Words without a good emoji (soil, roots, shovel, watering can, wreath, stocking, ornament, candy cane, snowball, lights, rug, blanket, rectangle, color swatches, etc.) use Noto pieces or clean Noto-style composites — no plain geometric blobs.
- Characters: removed in-card cutouts and the cropped memory-page character. At most **one** full transparent character on the first page of each activity, in a corner.
- Pins: one small **Free** corner badge; titles do not start with FREE; framed episode YouTube thumbnail, “Goes with the episode …”, and learnwithian.com fill the bottom. PDF page titles no longer say Free (still in `meta.json` title/description).
- Episodes **1–7** rebuilt and overwritten under `output/`; **all section 11 checks passed**.

### Episodes

| Slug | Episode | Result |
|------|---------|--------|
| `zoo-day` | 1 — Ian's Zoo Day | PASS |
| `little-garden` | 2 — Ian's Little Garden | PASS |
| `shape-hunt` | 3 — Ian's Shape Hunt | PASS |
| `number-walk` | 4 — Ian's Number Walk | PASS |
| `ian-s-color-day` | 5 — Ian's Color Day | PASS |
| `ian-s-snowy-day` | 6 — Ian's Snowy Day | PASS |
| `ian-s-christmas-eve` | 7 — Ian's Christmas Eve | PASS |

## Files

- Output files under `output/`: **84** (42 PDF, 21 pin PNG, 21 JSON)
- Noto emoji PNGs in `icons/`: **152**
- Character PNGs: **7**
- Font files: **3**

## Problems

- No dedicated Unicode emoji for candy cane, shovel, watering can, wreath, stocking, or ornament — those use detailed Noto-style composites (plus Noto pieces where helpful).
- Official repo raw `png/512` URLs 404 here; PNGs were fetched from the Noto Emoji CDN on `fonts.gstatic.com`.
