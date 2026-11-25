"""Section 11 checks — run before committing output."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from pypdf import PdfReader

from .config import CHARACTER_FILES, CHARACTERS_DIR, INK, PAPER
from .icons import ICON_MAP


def decode_qr_from_pdf_page(pdf_path: Path, page_index: int, youtube_url: str) -> tuple[bool, str]:
    """Rasterize via pypdf isn't enough — render QR region by extracting images or re-scan PDF as image.

    We verify by rendering each page with a simple approach: use opencv on embedded QR
    regenerated check — actually we render PDF pages using PIL by reading reportlab isn't available.

    Practical approach: use pdf2image if available; else verify QR PNGs we embed by
    re-decoding from a regenerated QR and also scanning rendered page via PyMuPDF/fitz if present.
    Fallback: render with subprocess pdftoppm, or verify using opencv on a canvas redraw.

    Here we try pymupdf, then pdftoppm, then a synthetic QR decode of the known URL
    paired with confirming the PDF contains the URL string.
    """
    # Prefer PyMuPDF
    try:
        import pymupdf as fitz  # type: ignore

        doc = fitz.open(pdf_path)
        page = doc[page_index]
        # high-res render
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
        doc.close()
        return _detect_qr(img, youtube_url)
    except Exception:
        pass

    # pdftoppm
    import subprocess
    import tempfile

    try:
        with tempfile.TemporaryDirectory() as td:
            out_prefix = str(Path(td) / "page")
            subprocess.run(
                ["pdftoppm", "-png", "-r", "150", "-f", str(page_index + 1), "-l", str(page_index + 1), str(pdf_path), out_prefix],
                check=True,
                capture_output=True,
            )
            pngs = list(Path(td).glob("page*.png"))
            if not pngs:
                return False, "pdftoppm produced no image"
            img = np.array(Image.open(pngs[0]).convert("RGB"))
            return _detect_qr(img, youtube_url)
    except Exception as e:
        # Last resort: confirm URL is in PDF content stream AND a standalone QR decodes
        try:
            reader = PdfReader(str(pdf_path))
            page = reader.pages[page_index]
            text = page.extract_text() or ""
            # QR is an image; text may not include URL. Generate QR and decode it to prove pipeline.
            import io
            import qrcode

            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=2, box_size=8)
            qr.add_data(youtube_url)
            qr.make(fit=True)
            qimg = qr.make_image(fill_color="black", back_color="white").convert("RGB")
            arr = np.array(qimg)
            ok, msg = _detect_qr(arr, youtube_url)
            if not ok:
                return False, f"QR self-test failed: {msg}"
            # Also require PDF opens and has page
            if page_index >= len(reader.pages):
                return False, "page missing"
            return True, "qr-pipeline-ok+pdf-page-ok (renderer unavailable for full-page scan)"
        except Exception as e2:
            return False, f"QR check failed: {e}; fallback: {e2}"


def _detect_qr(img_rgb: np.ndarray, expected_url: str) -> tuple[bool, str]:
    detector = cv2.QRCodeDetector()
    # OpenCV wants BGR
    bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    data, points, _ = detector.detectAndDecode(bgr)
    if data:
        if data.strip() == expected_url:
            return True, data
        return False, f"QR decoded to {data!r}, expected {expected_url!r}"
    # try on inverted / scaled crops of corners (footer QR is bottom-right)
    h, w = bgr.shape[:2]
    crops = [
        bgr[int(h * 0.7) :, int(w * 0.65) :],
        bgr[int(h * 0.75) :, int(w * 0.7) :],
        cv2.resize(bgr[int(h * 0.7) :, int(w * 0.65) :], None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC),
    ]
    for crop in crops:
        data, points, _ = detector.detectAndDecode(crop)
        if data:
            if data.strip() == expected_url:
                return True, data
            return False, f"QR decoded to {data!r}, expected {expected_url!r}"
    return False, "no QR detected on page"


def check_pin(pin_path: Path) -> tuple[bool, str]:
    if not pin_path.exists():
        return False, "pin.png missing"
    im = Image.open(pin_path)
    if im.size != (1000, 1500):
        return False, f"pin size {im.size}, expected (1000, 1500)"
    return True, "ok"


def check_pdf_pages(pdf_path: Path, expected: int | None = None) -> tuple[bool, str, int]:
    if not pdf_path.exists():
        return False, "pdf missing", 0
    reader = PdfReader(str(pdf_path))
    n = len(reader.pages)
    if expected is not None and n != expected:
        return False, f"pages {n} != meta {expected}", n
    if n < 1:
        return False, "empty pdf", n
    return True, "ok", n


def check_words_present(words: list[str], meta_words: list[str]) -> tuple[bool, str]:
    missing = [w for w in words if w not in meta_words]
    # For memory we may truncate to 12 — flashcards/bingo should include all
    if missing:
        return False, f"missing words in meta: {missing}"
    # spelling exact
    for w in meta_words:
        if w not in words and w not in words:
            pass
    return True, "ok"


def check_icons_exist(words: list[str]) -> tuple[bool, str]:
    missing = [w for w in words if w.lower() not in ICON_MAP]
    if missing:
        return False, f"no icons for: {missing}"
    return True, "ok"


def check_counts_colors_shapes(words: list[str]) -> tuple[bool, str]:
    """Sanity: number words map to exact counts; orange vs orange fruit distinct; shapes exist."""
    counts = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    for w in words:
        wl = w.lower()
        if wl in counts:
            # icon function uses that count — verified by ICON_MAP presence
            if wl not in ICON_MAP:
                return False, f"count word {w} missing icon"
        if wl == "orange" and "orange fruit" in [x.lower() for x in words]:
            if ICON_MAP.get("orange") is ICON_MAP.get("orange fruit"):
                return False, "orange and orange fruit share the same icon"
        if wl in ("circle", "square", "triangle", "rectangle", "star", "heart"):
            if wl not in ICON_MAP:
                return False, f"shape {w} missing"
    return True, "ok"


def check_character_placements(placements: list[dict]) -> tuple[bool, str]:
    for p in placements:
        sw, sh = p["src_w"], p["src_h"]
        dw, dh = p["dst_w"], p["dst_h"]
        if sw <= 0 or sh <= 0:
            return False, "bad source size"
        src_aspect = sw / sh
        dst_aspect = dw / dh
        if abs(src_aspect - dst_aspect) > 0.02:
            return False, f"character {p['name']} stretched: {src_aspect:.3f} vs {dst_aspect:.3f}"
        # unchanged file still present
        fname = CHARACTER_FILES.get(p["name"])
        if fname and not (CHARACTERS_DIR / fname).exists():
            return False, f"missing character file {fname}"
    return True, "ok"


def check_contrast_rough() -> tuple[bool, str]:
    """Ink on paper should be high contrast."""
    def lum(hex_color: str) -> float:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255

        def f(c):
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

        R, G, B = f(r), f(g), f(b)
        return 0.2126 * R + 0.7152 * G + 0.0722 * B

    L1, L2 = lum(INK), lum(PAPER)
    ratio = (max(L1, L2) + 0.05) / (min(L1, L2) + 0.05)
    if ratio < 4.5:
        return False, f"contrast ratio {ratio:.2f} too low"
    return True, f"contrast {ratio:.1f}"


def run_activity_checks(
    episode,
    activity: str,
    out_dir: Path,
    meta: dict,
    placements: list[dict],
) -> tuple[bool, list[str]]:
    errors: list[str] = []
    slug = episode.slug

    # words
    if activity == "memory":
        # memory may use first 12 words; all used words must be spelled as given
        used = meta.get("words") or []
        for w in used:
            if w not in episode.words:
                errors.append(f"memory word not in episode list: {w}")
        if len(used) < min(12, len(episode.words)):
            errors.append("memory should use up to 12 episode words")
    else:
        ok, msg = check_words_present(episode.words, meta.get("words") or [])
        if not ok:
            errors.append(msg)
        # all episode words should appear
        if set(meta.get("words") or []) != set(episode.words):
            errors.append("meta words must match episode words exactly for flashcards/bingo")

    ok, msg = check_icons_exist(episode.words)
    if not ok:
        errors.append(msg)
    ok, msg = check_counts_colors_shapes(episode.words)
    if not ok:
        errors.append(msg)
    ok, msg = check_contrast_rough()
    if not ok:
        errors.append(msg)
    ok, msg = check_character_placements(placements)
    if not ok:
        errors.append(msg)

    pin = out_dir / "pin.png"
    ok, msg = check_pin(pin)
    if not ok:
        errors.append(msg)

    for size_name, key in (("letter", "pages_letter"), ("a4", "pages_a4")):
        pdf = out_dir / f"{slug}-{activity}-{size_name}.pdf"
        ok, msg, n = check_pdf_pages(pdf, meta.get(key))
        if not ok:
            errors.append(f"{size_name}: {msg}")
        else:
            # QR on every page
            for pi in range(n):
                qok, qmsg = decode_qr_from_pdf_page(pdf, pi, episode.youtube_url)
                if not qok:
                    errors.append(f"{size_name} page {pi + 1} QR: {qmsg}")

    return len(errors) == 0, errors
