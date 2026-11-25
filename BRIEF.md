# CURSOR BRIEF: Learn with Ian, free printable activities machine

Paste this whole document into a Cursor cloud agent that works on the GitHub repo
`mahibrahim89-wq/learnwithian-activities`.

## 1. Mission

Build a small, reusable Python "activity machine" in this repo. Given an episode
(title, YouTube link, teaching words) it makes FREE printable activities for
toddlers and preschoolers (ages 2 to 6) plus a Pinterest image for each one.

The activities are free. Their only goal is to get families and teachers to watch
the Learn with Ian episode on YouTube. Every activity says, in a friendly way, that
it goes with the episode, and has a QR code that opens that exact episode.

You build the machine once and run it for episodes 1 to 7. After that, a GitHub
Action in this repo runs the machine by itself for every new episode. Nobody will
open Cursor again for new episodes.

Do not publish, sell, price or list anything. Do not touch any other repo, store,
Google Drive folder or Pinterest account.

## 2. Channel and audience

- Channel: Learn with Ian, https://www.youtube.com/@LearnWithIanKids
- Short, calm English cartoons for children ages 2 to 6. Made for Kids on YouTube.
- Readers of the activities: parents and preschool teachers (mainly USA and
  English-speaking Africa).
- Tone: bright, warm, gentle, simple English.

## 3. Characters (use the reference images exactly)

Download the seven official character images before anything else:

```
pip install gdown
gdown --folder "https://drive.google.com/drive/folders/1fsonZ28knmKOUPnuChpwcJbBn6-sASoj" -O characters/
```

You must end up with: `characters/ian.png`, `mama_sana.png`, `papa.png`, `liam.png`,
`latte.png`, `lisa.png`, `lorie.png`. Commit them to the repo so the GitHub Action
has them too. If the download fails, stop and write the problem in `STATUS.md`.

Rules:
- Never redraw, regenerate, restyle or recolor a character. You may scale, crop
  empty background, or place the cutout on a page.
- Ian: toddler boy, light blue cloud t-shirt, jeans. Mama Sana: his mother.
  Papa: his father, never give him a name. Liam: Ian's friend (never call him Max);
  for liam.png use only the front-facing standing pose on the left.
  Latte: orange-brown Persian cat (spelled Latte). Lisa: husky dog. Lorie: white cat.
- Only these seven characters. No other people, no clip-art people or pets.
- No real photos of children anywhere.

## 4. Look and brand (must match the website learnwithian.com)

- Paper `#fff9ef`, ink `#1d2b45`, berry `#ec4f7b`, sun `#ffb321`, leaf `#3fae5a`,
  sky `#2f8fe6`, grape `#8e5ce6`, card borders `#ecdcbc`.
- Headings: Baloo 2 (weight 800). Body: Atkinson Hyperlegible. Both are free
  (Google Fonts); bundle the font files in the repo.
- Rainbow "LEARN WITH IAN" wordmark at the top of each page (letters in berry, sun,
  leaf, sky, grape, repeating).
- Big, very readable type. Lots of white space. High contrast (no pale text on white).
- You are free to make the design beautiful; stay inside these colors and fonts.

## 5. Safety and accuracy rules

- English only, correct American spelling.
- Nothing scary, no weapons, no brands, no copyrighted characters.
- No kissing or romance. No nudity.
- Season-correct clothes and props (snow means coats, hats, scarves, gloves,
  snow boots).
- Pets stay on the floor; never on tables or touching food.
- Counts must be exact (a "5" card shows exactly 5 objects). Colors and shapes
  must be clearly right. In the Colors episode, "orange" (color) and
  "orange fruit" must not be confused.
- Do not use any image-generation model or paid API. Simple icons you draw in code
  (circles, stars, a red ball, a snowflake) are fine.

## 6. YouTube rule (important)

Never write "watch to get this", "watch to unlock" or anything that rewards watching.
The activity is always free. Use friendly lines like "Goes with the episode
Ian's Snowy Day. Watch it together, then play!".

## 7. Activities to make for each episode

For each episode make these three activities:

1. **Word flashcards**: one word per card with a simple picture; some cards include
   a character. Several cards per page with light cut lines.
2. **Bingo**: a call sheet for the grown-up and at least 4 different player boards
   (3x3 grid for this age), pictures plus words, plus a short rules box.
3. **Memory game**: pairs of picture cards (always the same pairing rule), cut lines,
   short rules box.

Every page of every activity has a footer with:
- left: `Learn with Ian · learnwithian.com`
- right: the text "Scan to watch the episode" and a QR code (at least 0.8 inch)
  that opens the episode's YouTube link. The QR must decode (test it in code with
  OpenCV or pyzbar).

The first page of each activity has a small line: "Goes with the episode: <title>".

## 8. Files to produce

For every activity, write to `output/<episode-slug>/<activity>/`
(activity = `flashcards`, `bingo`, `memory`):

- `<episode-slug>-<activity>-letter.pdf` (US Letter, 0.5 inch safe margins)
- `<episode-slug>-<activity>-a4.pdf` (A4, 12.7 mm safe margins)
- `pin.png`: Pinterest image, exactly 1000 x 1500 px, vertical. A big, clear
  preview of the activity, the title in large text (for example
  "FREE Christmas Bingo for Toddlers"), the word FREE clearly visible, a small
  episode still or character, and `learnwithian.com` at the bottom. No QR on the
  pin image.
- `meta.json`:

```json
{
  "episode": 7,
  "episode_title": "Ian's Christmas Eve",
  "youtube_id": "TAyFj_YT8KM",
  "activity": "bingo",
  "title": "Free Christmas Bingo for Toddlers and Preschool",
  "description": "A free printable Christmas bingo game for ages 2 to 6 ... (max 450 characters, parent and teacher friendly, mentions the episode)",
  "keywords": ["christmas bingo for toddlers", "free printable", "preschool christmas game"],
  "words": ["tree", "star", "bell"],
  "pages_letter": 3,
  "pages_a4": 3,
  "checks_passed": true
}
```

Episode slugs (use exactly these, they match the website):
`zoo-day`, `little-garden`, `shape-hunt`, `number-walk`, `ian-s-color-day`,
`ian-s-snowy-day`, `ian-s-christmas-eve`. For a new episode, the slug is the
episode title in lowercase with every non-letter/number replaced by `-`, unless
the input gives one.

## 9. Episode input

The machine reads episodes from this public CSV (the website's extras sheet):

```
https://docs.google.com/spreadsheets/d/1oxDQWj9UmokHvhHp05L9GPgZxyOlyMZ3ctli8nORgsc/export?format=csv
```

Useful columns: `youtube_id`, `episode`, `activity_words` (15 to 20 English words,
separated by ` | `). The episode title comes from the YouTube page title
(`https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=<id>&format=json`).
A row is "new" when `output/<slug>/` does not exist yet and `activity_words`
is filled.

For the first run, also keep a local file `episodes.json` with episodes 1 to 7 and
these words, so you can build without the sheet:

- Ep1 Zoo Day (baG8fJsSXFg): elephant, giraffe, zebra, lion, tiger, cheetah, gorilla, penguin, hippo, rhino, panda, koala, kangaroo, flamingo, bear
- Ep2 Little Garden (oUq2iLSBxUU): seed, soil, shovel, watering can, dig, plant, water, sunlight, roots, sprout, flower, bee, worm, ladybug, butterfly, tomato, carrot, sunflower
- Ep3 Shape Hunt (E2k4atUZDsg): circle, square, triangle, rectangle, star, heart, plate, clock, cracker, block, sandwich, flag, door, book, rug, cookie
- Ep4 Number Walk (_5Jwth51cnc): one, two, three, four, five, ball, cats, cookies, cups, tomatoes, ducks, steps, walk, count
- Ep5 Color Day (5Cwxl4TWipE): red, blue, yellow, orange, green, purple, yarn, ball, banana, orange fruit, boots, grass, blanket, picnic
- Ep6 Snowy Day (g-E2RaXlU0s): snow, snowflake, snowman, snowball, cold, warm, hat, scarf, gloves, boots, coat, blanket, winter, window, ice
- Ep7 Christmas Eve (TAyFj_YT8KM): tree, wreath, stocking, lights, bell, ornament, candy cane, reindeer, star, present, candle, cookie, card, box, ribbon, bow

## 10. Build it to run by itself

- Python project with `requirements.txt` and a short `README.md`
  (how to run for all episodes and for one episode).
- `make_activities.py --all` and `make_activities.py --episode <youtube_id>`.
- Free libraries only (ReportLab or Playwright/Chromium for PDFs, Pillow, qrcode,
  opencv-python-headless or pyzbar for QR tests).
- GitHub Action `.github/workflows/activities.yml`:
  - runs every 6 hours and on manual dispatch,
  - reads the CSV, makes activities for every new episode,
  - runs the checks (section 11),
  - commits only the new `output/` folders, with the message
    "New activities for <slug>".
  - If a check fails, it does not commit that episode and writes the reason in
    `STATUS.md`.

## 11. Checks (in code, before anything is committed)

- Every word spelled as given; no word missing.
- Counts, colors and shapes correct.
- Nothing overflows the safe margins or sits on a cut line.
- Text large and high contrast.
- Every page's QR decodes to the episode's YouTube link.
- `pin.png` is exactly 1000 x 1500.
- PDFs open and have the page counts written in `meta.json`.
- Characters unchanged (compare against the reference files; no stretching).

## 12. When you finish

1. Run the machine for episodes 1 to 7 and commit everything in `output/`.
2. Write `STATUS.md`: what was made, any problems, and how many files.
3. Do not open pull requests to any other repo. Push to `main` of this repo only.
