"""Checks every activity folder; sets checks_passed in meta.json. Usage: check.py OUT_DIR"""
import glob, json, os, subprocess, sys, tempfile
import cv2
from pypdf import PdfReader
ok_all = True
for meta in sorted(glob.glob(f"{sys.argv[1]}/*/*/meta.json")):
    m = json.load(open(meta)); folder = os.path.dirname(meta); errs = []
    want = f"https://www.youtube.com/watch?v={m['youtube_id']}"
    for size, dims in (("letter", (612, 792)), ("a4", (595, 842))):
        p = glob.glob(f"{folder}/*-{size}.pdf")
        if not p: errs.append(f"no {size} pdf"); continue
        r = PdfReader(p[0]); pg = r.pages[0].mediabox
        if len(r.pages) != 1: errs.append(f"{size} pages {len(r.pages)}")
        if (round(float(pg.width)), round(float(pg.height))) != dims: errs.append(f"{size} size")
        q = ""
        for dpi in ("200", "300", "150"):
            t = tempfile.mkdtemp(); subprocess.run(["pdftoppm", "-r", dpi, "-png", "-singlefile", p[0], f"{t}/p"], check=True)
            img = cv2.imread(f"{t}/p.png"); h, w = img.shape[:2]
            q = cv2.QRCodeDetector().detectAndDecode(img[int(h * 0.85):, int(w * 0.7):])[0]  # footer corner only
            if q == want: break
        if q != want: errs.append(f"{size} QR '{q}'")
        if os.path.getsize(p[0]) > 4_000_000: errs.append(f"{size} too big")
    from PIL import Image
    pin = f"{folder}/pin.png"
    if not os.path.exists(pin) or Image.open(pin).size != (1000, 1500): errs.append("pin")
    m["checks_passed"] = not errs; json.dump(m, open(meta, "w"), indent=2)
    print(("OK  " if not errs else "FAIL") , folder, errs)
    ok_all &= not errs
sys.exit(0 if ok_all else 1)
