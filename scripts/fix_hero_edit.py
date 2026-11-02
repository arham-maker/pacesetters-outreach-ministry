"""Remove outer hero region when nested image/copy slots already exist."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "pages"

HERO_RE = re.compile(
    r'(<section\s+class="[^"]*\bpom-hero\b[^"]*")(\s+data-pom-region="([^"]+)")([^>]*>)(.*?)(</section>)',
    re.S | re.I,
)


def fix_hero(m: re.Match) -> str:
    open_start, _region_attr, region, after_attrs, body, close = m.groups()
    if "pom-hero-media" not in body and "hero-copy" not in body:
        return m.group(0)

    open_tag = open_start + after_attrs
    body = re.sub(
        rf'\n?\s*<div class="pom-cms"><squarespace:block-field id="{re.escape(region)}" columns="12" /></div>\s*',
        "\n",
        body,
        count=1,
    )

    # Unwrap pom-fallback that wraps hero-copy (+ optional bars)
    body = re.sub(
        r'<div class="pom-fallback">\s*'
        r'(<div class="pom-hero-copy\b[^>]*>[\s\S]*?</div>)\s*'
        r'(<div class="pom-hero-bars">[\s\S]*?</div>)?\s*'
        r"</div>",
        lambda mm: mm.group(1) + (("\n    " + mm.group(2)) if mm.group(2) else ""),
        body,
        count=1,
    )

    # If bars are outside hero-copy, fold them into the copy fallback so one edit region
    def fold_bars(mm: re.Match) -> str:
        copy_open, copy_inner, copy_cms, bars = mm.groups()
        if 'class="pom-fallback"' in copy_inner:
            copy_inner = re.sub(
                r"(</div>\s*)$",
                bars + r"\1",
                copy_inner,
                count=1,
            )
            return f"{copy_open}{copy_inner}{copy_cms}"
        return (
            f"{copy_open}\n"
            f'      <div class="pom-fallback">{copy_inner}{bars}</div>\n'
            f"      {copy_cms}"
        )

    body = re.sub(
        r'(<div class="pom-hero-copy\b[^>]*>)([\s\S]*?)'
        r'(<div class="pom-cms"><squarespace:block-field id="[^"]+" columns="12" /></div>\s*</div>)\s*'
        r'(<div class="pom-hero-bars">[\s\S]*?</div>)',
        fold_bars,
        body,
        count=1,
    )

    return open_tag + body + close


def main() -> None:
    for path in sorted(ROOT.glob("*.page")):
        original = path.read_text(encoding="utf-8")
        updated = HERO_RE.sub(fix_hero, original, count=1)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            print("fixed", path.name)


if __name__ == "__main__":
    main()
