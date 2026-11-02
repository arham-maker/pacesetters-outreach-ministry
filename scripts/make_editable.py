"""
Make images + text areas independently editable in Squarespace 7.0 Edit mode
via nested block-fields (closest equivalent to 7.1 click-to-edit).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MEDIA_SRC = {
    "is-hands": "/assets/home-purpose.png",
    "is-bible": "/assets/home-snl-hires.png",
    "is-books": "/assets/homw/blackhome.jpg",
    "is-about-story": "/assets/about/about-story.png",
    "is-about-faith": "/assets/about/about-faith.png",
    "is-about-reach": "/assets/about/about-reach.png",
    "is-svc-outreach": "/assets/services/services-outreach.png",
    "is-svc-prayer": "/assets/services/services-prayer.png",
    "is-svc-online": "/assets/services/services-online.png",
    "is-svc-resources": "/assets/services/services-resources.png",
    "is-prayer-alone": "/assets/prayer/prayer-alone.png",
    "is-prayer-support": "/assets/prayer/prayer-support.png",
    "is-outreach-reach": "/assets/outreach/outreach-reach.png",
    "is-events-feature": "/assets/events/events-feature.png",
    "is-store-cat-music": "/assets/store/store-cat-music.png",
    "is-store-cat-sermons": "/assets/store/store-cat-sermons.png",
    "is-store-cat-books": "/assets/store/store-cat-books.png",
    "is-store-p01": "/assets/store/store-product-01.png",
    "is-store-p02": "/assets/store/store-product-02.png",
    "is-store-p03": "/assets/store/store-product-03.png",
    "is-store-p04": "/assets/store/store-product-04.png",
    "is-store-p05": "/assets/store/store-product-05.png",
    "is-store-p06": "/assets/store/store-product-06.png",
    "is-product-p01": "/assets/store/store-product-01.png",
    "is-product-p02": "/assets/store/store-product-02.png",
    "is-product-p03": "/assets/store/store-product-03.png",
    "is-product-p04": "/assets/store/store-product-04.png",
    "is-product-p05": "/assets/store/store-product-05.png",
    "is-product-p06": "/assets/store/store-product-06.png",
    "is-checkout-item": None,  # resolved via product class
}

HERO_BG = {
    "home-hero": "/assets/home-hero.png",
    "about-hero": "/assets/about/about-hero.png",
    "services-hero": "/assets/services/services-hero.png",
    "events-hero": "/assets/events/events-hero.png",
    "store-hero": "/assets/store/store-hero.png",
    "prayer-hero": "/assets/prayer/prayer-hero.png",
    "outreach-hero": "/assets/outreach/outreach-hero.png",
    "contact-hero": "/assets/contact/contact-hero.png",
}

MEDIA_OPEN = re.compile(
    r'<div\s+class="([^"]*\bpom-media\b[^"]*)"([^>]*)>(\s*)</div>',
    re.I,
)


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "item"


def media_src(classes: str) -> str | None:
    parts = classes.split()
    for key, src in MEDIA_SRC.items():
        if key in parts and src:
            return src
    for p in parts:
        if p.startswith("is-product-p") or p.startswith("is-store-p"):
            num = p.split("p")[-1]
            return f"/assets/store/store-product-{num.zfill(2)}.png"
        if p.startswith("is-checkout-item"):
            continue
    if "is-checkout-item" in parts:
        for p in parts:
            m = re.search(r"is-product-p(\d+)", p)
            if m:
                return f"/assets/store/store-product-{m.group(1).zfill(2)}.png"
    return None


def wrap_media(html: str, page_stem: str) -> str:
    counter = {"n": 0}

    def repl(match: re.Match) -> str:
        classes = match.group(1)
        attrs = match.group(2) or ""
        if "data-pom-region=" in attrs or "pom-cms" in match.group(0):
            return match.group(0)
        # Already converted (has children) — skip empty-only matcher handled by regex
        src = media_src(classes)
        if not src:
            return match.group(0)
        alt = ""
        alt_m = re.search(r'aria-label="([^"]*)"', attrs)
        if alt_m:
            alt = alt_m.group(1)
        counter["n"] += 1
        region = f"{page_stem}-media-{counter['n']}"
        # Prefer semantic id from class
        for key in MEDIA_SRC:
            if key in classes.split():
                region = f"{page_stem}-{key.replace('is-', '')}"
                break
        return (
            f'<div class="{classes}"{attrs} data-pom-region="{region}">\n'
            f'        <div class="pom-fallback">\n'
            f'          <img src="{src}" alt="{alt}" loading="lazy" decoding="async">\n'
            f"        </div>\n"
            f'        <div class="pom-cms"><squarespace:block-field id="{region}" columns="12" /></div>\n'
            f"      </div>"
        )

    return MEDIA_OPEN.sub(repl, html)


COPY_TARGETS = [
    ("pom-split-copy", "copy"),
    ("pom-hero-copy", "hero-copy"),
    ("pom-testimonials-intro", "testimonials-intro"),
    ("pom-faq-intro", "faq-intro"),
    ("pom-contact-copy", "contact-copy"),
]


def wrap_copy_blocks(html: str, page_stem: str) -> str:
    """Wrap known copy containers with their own block-field if missing."""
    for cls, suffix in COPY_TARGETS:
        html = _wrap_simple_div(html, cls, f"{page_stem}-{suffix}")
    return html


def _wrap_simple_div(html: str, cls: str, region_base: str) -> str:
    """Wrap outermost divs with class containing cls that lack data-pom-region."""
    out = []
    i = 0
    n = 0
    token = f'class="'
    while i < len(html):
        idx = html.find("<div", i)
        if idx < 0:
            out.append(html[i:])
            break
        out.append(html[i:idx])
        # find end of opening tag
        gt = html.find(">", idx)
        if gt < 0:
            out.append(html[idx:])
            break
        open_tag = html[idx : gt + 1]
        if cls not in open_tag or "data-pom-region=" in open_tag or "pom-media" in open_tag:
            out.append(open_tag)
            i = gt + 1
            continue
        # parse balanced div
        depth = 1
        pos = gt + 1
        while pos < len(html) and depth:
            next_open = html.find("<div", pos)
            next_close = html.find("</div>", pos)
            if next_close < 0:
                break
            if next_open >= 0 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                if depth == 0:
                    inner = html[gt + 1 : next_close]
                    end = next_close + len("</div>")
                    if "squarespace:block-field" in inner and "data-pom-region" in open_tag:
                        out.append(html[idx:end])
                    elif 'class="pom-cms"' in inner and inner.strip().startswith('<div class="pom-fallback"'):
                        # already structured; inject region on outer
                        n += 1
                        region = region_base if n == 1 else f"{region_base}-{n}"
                        new_open = open_tag[:-1] + f' data-pom-region="{region}">'
                        if f'id="{region}"' not in inner:
                            inner = (
                                inner
                                + f'\n        <div class="pom-cms"><squarespace:block-field id="{region}" columns="12" /></div>\n      '
                            )
                        out.append(new_open + inner + "</div>")
                    else:
                        n += 1
                        region = region_base if n == 1 else f"{region_base}-{n}"
                        # extract class from open_tag
                        cm = re.search(r'class="([^"]*)"', open_tag)
                        classes = cm.group(1) if cm else cls
                        other = re.sub(r'\sclass="[^"]*"', "", open_tag[4:-1]).strip()
                        other = f" {other}" if other else ""
                        if 'class="pom-fallback"' in inner[:200]:
                            body = inner
                            if "squarespace:block-field" not in inner:
                                body = (
                                    inner
                                    + f'\n        <div class="pom-cms"><squarespace:block-field id="{region}" columns="12" /></div>\n      '
                                )
                            out.append(
                                f'<div class="{classes}" data-pom-region="{region}"{other}>{body}</div>'
                            )
                        else:
                            out.append(
                                f'<div class="{classes}" data-pom-region="{region}"{other}>\n'
                                f'        <div class="pom-fallback">{inner}</div>\n'
                                f'        <div class="pom-cms"><squarespace:block-field id="{region}" columns="12" /></div>\n'
                                f"      </div>"
                            )
                    i = end
                    break
                pos = next_close + 6
        else:
            out.append(open_tag)
            i = gt + 1
    return "".join(out)


def add_hero_image_layer(html: str, page_stem: str) -> str:
    """For hero sections with CSS background, add editable image layer."""
    hero_re = re.compile(
        r'(<section\s+class="[^"]*\bpom-hero\b[^"]*")([^>]*>)(.*?)(</section>)',
        re.S | re.I,
    )

    def repl(m: re.Match) -> str:
        open_start, open_rest, body, close = m.groups()
        if "pom-hero-media" in body:
            return m.group(0)
        # find region id from data-pom-region on section or invent
        region_m = re.search(r'data-pom-region="([^"]+)"', open_start + open_rest)
        base = region_m.group(1) if region_m else f"{page_stem}-hero"
        img_region = f"{base}-image"
        src = HERO_BG.get(base) or HERO_BG.get(f"{page_stem}-hero") or None
        # guess from page
        if not src:
            for key, path in HERO_BG.items():
                if key.startswith(page_stem) or page_stem in key:
                    src = path
                    break
        if not src:
            # try assets path from common pattern
            guesses = [
                f"/assets/{page_stem}/{page_stem}-hero.png",
                f"/assets/{page_stem}-hero.png",
            ]
            for g in guesses:
                if (ROOT / g.lstrip("/")).exists():
                    src = g
                    break
        if not src:
            return m.group(0)
        layer = (
            f'\n    <div class="pom-hero-media" data-pom-region="{img_region}">\n'
            f'      <div class="pom-fallback">\n'
            f'        <img src="{src}" alt="" loading="eager" decoding="async">\n'
            f"      </div>\n"
            f'      <div class="pom-cms"><squarespace:block-field id="{img_region}" columns="12" /></div>\n'
            f"    </div>\n"
        )
        return open_start + open_rest + layer + body + close

    return hero_re.sub(repl, html, count=1)


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    stem = path.stem.replace(".page", "") if path.suffix == ".page" else path.stem
    if path.name.endswith(".page"):
        stem = path.name.replace(".page", "")
    html = original
    html = wrap_media(html, stem)
    html = add_hero_image_layer(html, stem)
    html = wrap_copy_blocks(html, stem)
    if html != original:
        path.write_text(html, encoding="utf-8", newline="\n")
        return True
    return False


def patch_site_region() -> bool:
    path = ROOT / "site.region"
    text = path.read_text(encoding="utf-8")
    original = text
    if 'data-pom-region="site-header-join"' not in text:
        old = """    <div class="pom-header-tools">
      <a class="pom-btn pom-join-btn" href="/events">
        <span class="pom-link-text">Join Now</span>
        <span class="pom-arrow is-ne" aria-hidden="true"></span>
      </a>"""
        new = """    <div class="pom-header-tools">
      <div class="pom-join-wrap" data-pom-region="site-header-join">
        <div class="pom-fallback">
          <a class="pom-btn pom-join-btn" href="/events">
            <span class="pom-link-text">Join Now</span>
            <span class="pom-arrow is-ne" aria-hidden="true"></span>
          </a>
        </div>
        <div class="pom-cms"><squarespace:block-field id="site-header-join" columns="12" /></div>
      </div>"""
        if old in text:
            text = text.replace(old, new, 1)
    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    changed = []
    for path in sorted((ROOT / "pages").glob("*.page")):
        if process_file(path):
            changed.append(path.name)
    if patch_site_region():
        changed.append("site.region")
    # also collections list if any media
    products = ROOT / "collections" / "products.list"
    if products.exists() and process_file(products):
        changed.append("collections/products.list")
    print("updated:", len(changed))
    for name in changed:
        print(" ", name)


if __name__ == "__main__":
    main()
