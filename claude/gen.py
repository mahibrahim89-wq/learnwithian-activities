"""Learn with Ian - free activity maker (story order, picture puzzle, memory match).

Uses only the channel's own pictures: 4 stills from the episode + the character art.
Usage: python3 gen.py episode.json STILLS_DIR OUT_DIR
episode.json = {"episode": 7, "title": "Ian's Christmas Eve", "theme": "Christmas Eve",
  "youtube_id": "...", "slug": "...", "puzzle": 2,
  "story": [{"still": 1, "caption": "...", "key": "lights"}, ... 4 items in the TRUE order]}
Writes OUT_DIR/<slug>/<kind>/<slug>-<kind>-letter.pdf, -a4.pdf, pin.png, meta.json
"""
import io, json, os, sys
import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor

ASSETS = os.environ.get("ACT_ASSETS", "/tmp/acts")  # fonts/ and characters/
pdfmetrics.registerFont(TTFont("Baloo", f"{ASSETS}/fonts/Baloo2-ExtraBold.ttf"))
pdfmetrics.registerFont(TTFont("Atk", f"{ASSETS}/fonts/AtkinsonHyperlegible-Regular.ttf"))
pdfmetrics.registerFont(TTFont("AtkB", f"{ASSETS}/fonts/AtkinsonHyperlegible-Bold.ttf"))
HEX = dict(navy="#1d2b45", blue="#2f8fe6", green="#3fae5a", pink="#ec4f7b", sand="#ecdcbc", yel="#ffb321", cream="#fff9ef", grey="#8a8f99")
C = {k: HexColor(v) for k, v in HEX.items()}
WHITE = HexColor("#ffffff")
SHUFFLE = [2, 0, 3, 1]  # order the 4 story cards are shown in (never the true order)
KINDS = {"story": "Story order cards", "puzzle": "Picture puzzle", "memory": "Memory match game"}
CHARS = [("ian", "Ian"), ("mama_sana", "Mama"), ("papa", "Papa"), ("latte", "Latte"), ("lisa", "Lisa"), ("lorie", "Lorie")]


def jpg(im, w=1400, q=85):
    im = im.convert("RGB")
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True); b.seek(0)
    return ImageReader(b)


def png(im):
    b = io.BytesIO(); im.save(b, "PNG", optimize=True); b.seek(0)
    return ImageReader(b)


def rounded(im, w=1100, r=36, border=12):
    im = im.convert("RGB"); im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).convert("RGBA")
    W, H = im.size
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 1, H - 1), r, fill=255); im.putalpha(m)
    bg = Image.new("RGBA", (W + 2 * border, H + 2 * border), (0, 0, 0, 0))
    ImageDraw.Draw(bg).rounded_rectangle((0, 0, W + 2 * border - 1, H + 2 * border - 1), r + border, fill=(255, 255, 255, 255))
    bg.alpha_composite(im, (border, border))
    flat = Image.new("RGB", bg.size, (255, 249, 239)); flat.paste(bg, (0, 0), bg)
    return flat


class Maker:
    def __init__(self, ep, stills_dir):
        self.ep = ep
        self.S = {i: Image.open(os.path.join(stills_dir, f"still-{i}.png")).convert("RGB") for i in range(1, 5)}
        self.url = f"https://www.youtube.com/watch?v={ep['youtube_id']}"
        self.qr = qrcode.make(self.url, border=1).convert("RGB")
        self.chars = {}
        for f, _ in CHARS:
            im = Image.open(f"{ASSETS}/characters/{f}.png").convert("RGBA"); im = im.crop(im.getbbox()); im.thumbnail((600, 600))
            flat = Image.new("RGB", im.size, (255, 255, 255)); flat.paste(im, (0, 0), im)
            self.chars[f] = flat

    def frame(self, c, W, H, title, sub):
        c.setFillColor(C["cream"]); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(C["navy"]); c.setFont("Baloo", 34); c.drawCentredString(W / 2, H - 0.95 * inch, title)
        c.setFillColor(C["blue"]); c.setFont("AtkB", 14); c.drawCentredString(W / 2, H - 1.25 * inch, sub)
        c.setStrokeColor(C["sand"]); c.setLineWidth(1.5); c.line(0.5 * inch, 1.15 * inch, W - 0.5 * inch, 1.15 * inch)
        c.drawImage(png(self.qr), W - 1.4 * inch, 0.25 * inch, 0.85 * inch, 0.85 * inch)
        c.setFillColor(C["navy"]); c.setFont("AtkB", 11)
        c.drawRightString(W - 1.5 * inch, 0.82 * inch, f"Goes with the episode: {self.ep['title']}")
        c.setFont("Atk", 10); c.drawRightString(W - 1.5 * inch, 0.6 * inch, "Scan to watch together  ·  learnwithian.com")
        c.setFont("Baloo", 16); c.setFillColor(C["pink"]); c.drawString(0.5 * inch, 0.6 * inch, "Learn with Ian")
        c.setFont("Atk", 9); c.setFillColor(C["navy"]); c.drawString(0.5 * inch, 0.4 * inch, "For home and classroom use · ages 2 to 6")

    def story(self, c, W, H):
        self.frame(c, W, H, "Put the story in order", "Look at the pictures. Write 1, 2, 3, 4 in the circles.")
        st = self.ep["story"]
        cw = (W - 1.3 * inch) / 2; ch = cw * 720 / 1280
        xs = [0.55 * inch, W - 0.55 * inch - cw]
        gap = (H - 1.55 * inch - 1.5 * inch - 2 * (ch + 0.75 * inch)) / 3
        ys = [H - 1.55 * inch - gap - ch, H - 1.55 * inch - 2 * gap - 2 * ch - 0.75 * inch]
        for k, idx in enumerate(SHUFFLE):
            item = st[idx]; x, y = xs[k % 2], ys[k // 2]
            c.drawImage(jpg(rounded(self.S[item["still"]]), w=1200, q=88), x, y, cw, ch)
            c.setFillColor(WHITE); c.setStrokeColor(C["pink"]); c.setLineWidth(3); c.setDash(6, 4)
            c.circle(x + 0.32 * inch, y - 0.38 * inch, 0.28 * inch, fill=1, stroke=1); c.setDash()
            c.setFillColor(C["navy"]); c.setFont("AtkB", 12.5)
            c.drawString(x + 0.7 * inch, y - 0.43 * inch, item["caption"])
        c.setFont("Atk", 8); c.setFillColor(C["grey"])
        c.drawCentredString(W / 2, 1.25 * inch, "Grown-ups: " + " · ".join(f'{s["key"]} {i + 1}' for i, s in enumerate(st)))

    def puzzle(self, c, W, H):
        self.frame(c, W, H, "Picture puzzle", "Cut on the dashed lines, mix the pieces, then put the picture back together.")
        im = self.S[self.ep.get("puzzle", 4)]
        pw = 6.5 * inch; ph = pw * 720 / 1280; x = (W - pw) / 2
        y1 = H - 1.5 * inch - ph
        c.drawImage(jpg(im), x, y1, pw, ph)
        for col, lw, d in ((WHITE, 4, None), (C["navy"], 2, (8, 5))):
            c.setStrokeColor(col); c.setLineWidth(lw)
            if d: c.setDash(*d)
            c.rect(x, y1, pw, ph, stroke=1, fill=0)
            for k in (1, 2): c.line(x + pw * k / 3, y1, x + pw * k / 3, y1 + ph)
            c.line(x, y1 + ph / 2, x + pw, y1 + ph / 2); c.setDash()
        c.setFont("AtkB", 12); c.setFillColor(C["pink"]); c.drawString(x, y1 - 0.25 * inch, "Cut here")
        y2 = 1.4 * inch
        faint = Image.blend(im, Image.new("RGB", im.size, (255, 255, 255)), 0.78)
        c.drawImage(jpg(faint), x, y2, pw, ph)
        c.setStrokeColor(C["sand"]); c.setLineWidth(2)
        c.rect(x, y2, pw, ph, stroke=1, fill=0)
        for k in (1, 2): c.line(x + pw * k / 3, y2, x + pw * k / 3, y2 + ph)
        c.line(x, y2 + ph / 2, x + pw, y2 + ph / 2)
        c.setFont("AtkB", 12); c.setFillColor(C["green"]); c.drawString(x, y2 + ph + 0.08 * inch, "Put your pieces here")

    def memory(self, c, W, H):
        self.frame(c, W, H, "Memory match", "Cut out the cards, turn them over and find the pairs.")
        cards = CHARS + CHARS
        cw, chh = 2.2 * inch, 1.95 * inch; gx = (W - 3 * cw) / 4
        top = H - 1.55 * inch
        for k, (f, n) in enumerate(cards):
            col, row = k % 3, k // 3
            x = gx + col * (cw + gx); y = top - (row + 1) * chh - row * 0.08 * inch
            c.setFillColor(WHITE); c.setStrokeColor(C["navy"]); c.setLineWidth(1.5); c.setDash(6, 4)
            c.roundRect(x, y, cw, chh - 0.05 * inch, 14, fill=1, stroke=1); c.setDash()
            im = self.chars[f]; iw, ih = im.size; s = min((cw - 0.3 * inch) / iw, (chh - 0.55 * inch) / ih)
            c.drawImage(jpg(im, w=600, q=88), x + (cw - iw * s) / 2, y + 0.38 * inch, iw * s, ih * s)
            c.setFillColor(C["navy"]); c.setFont("Baloo", 15); c.drawCentredString(x + cw / 2, y + 0.12 * inch, n)

    def pdf(self, kind, path, size):
        W, H = size
        c = canvas.Canvas(path, pagesize=size, invariant=1)
        c.setTitle(f"{self.ep['title']} - {KINDS[kind]} - Learn with Ian"); c.setAuthor("Learn with Ian")
        getattr(self, kind)(c, W, H); c.showPage(); c.save()

    def pin(self, kind, letter_pdf, path):
        import subprocess, tempfile
        tmp = tempfile.mkdtemp()
        subprocess.run(["pdftoppm", "-r", "110", "-png", "-singlefile", letter_pdf, f"{tmp}/p"], check=True)
        page = Image.open(f"{tmp}/p.png").convert("RGB")
        W, H = 1000, 1500
        navy, pink, cream, yel, blue = [tuple(int(HEX[k][i:i + 2], 16) for i in (1, 3, 5)) for k in ("navy", "pink", "cream", "yel", "blue")]
        im = Image.new("RGB", (W, H), cream); d = ImageDraw.Draw(im)
        B = lambda s: ImageFont.truetype(f"{ASSETS}/fonts/Baloo2-ExtraBold.ttf", s)
        T = lambda s: ImageFont.truetype(f"{ASSETS}/fonts/AtkinsonHyperlegible-Bold.ttf", s)

        def ctr(y, t, f, col):
            while d.textlength(t, font=f) > W - 70 and f.size > 20:
                f = f.font_variant(size=f.size - 4)
            d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=col)
        ctr(32, self.ep["theme"], B(96), navy)
        ctr(148, KINDS[kind] + " for preschool", T(42), blue)
        pw = 760; page = page.resize((pw, round(page.height * pw / page.width)), Image.LANCZOS)
        x = (W - pw) // 2; y = 222
        d.rounded_rectangle((x - 10, y - 10, x + pw + 10, y + page.height + 10), 18, fill=(225, 215, 195))
        im.paste(page, (x, y))
        yb = y + page.height + 30
        ctr(yb, f"Goes with the episode {self.ep['title']}", T(32), navy)
        ctr(yb + 48, "Ages 2 to 6  ·  print at home or in class", T(28), navy)
        ctr(H - 112, "learnwithian.com", B(52), pink)
        f = T(30); tw = d.textlength("FREE PDF", font=f)
        d.rounded_rectangle((965 - tw - 40, H - 70, 965, H - 20), 26, fill=yel); d.text((965 - tw - 20, H - 64), "FREE PDF", font=f, fill=navy)
        im.save(path, optimize=True)

    def build(self, out):
        ep = self.ep; res = {}
        for kind in KINDS:
            folder = os.path.join(out, ep["slug"], kind); os.makedirs(folder, exist_ok=True)
            base = f"{ep['slug']}-{kind}"
            lp, ap = f"{folder}/{base}-letter.pdf", f"{folder}/{base}-a4.pdf"
            self.pdf(kind, lp, letter); self.pdf(kind, ap, A4)
            self.pin(kind, lp, f"{folder}/pin.png")
            name = KINDS[kind]
            meta = {
                "episode": ep["episode"], "episode_title": ep["title"], "youtube_id": ep["youtube_id"], "activity": kind,
                "title": f"{ep['theme']} {name} for Toddlers and Preschool",
                "description": f"Printable {name.lower()} made from the Learn with Ian episode {ep['title']}. "
                               f"Ages 2 to 6. Free PDF in US Letter and A4. Watch the episode together, then play. learnwithian.com",
                "checks_passed": False,
            }
            json.dump(meta, open(f"{folder}/meta.json", "w"), indent=2)
            res[kind] = folder
        return res


if __name__ == "__main__":
    ep = json.load(open(sys.argv[1]))
    print(Maker(ep, sys.argv[2]).build(sys.argv[3]))
