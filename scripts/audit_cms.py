from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
pages = root / "pages"
missing = []
ok = []

for p in sorted(pages.glob("*.page")):
    text = p.read_text(encoding="utf-8")
    sections = list(re.finditer(r"<(section|article)\b([^>]*)>(.*?)</\1>", text, re.S | re.I))
    for m in sections:
        attrs, body = m.group(2), m.group(3)
        has_cms = "squarespace:block-field" in body or "data-pom-region" in attrs or "data-pom-region" in body
        cls = re.search(r'class="([^"]+)"', attrs)
        label = cls.group(1)[:70] if cls else attrs.strip()[:40]
        if not has_cms and len(body.strip()) > 60:
            missing.append(f"{p.name} :: {label}")
        elif has_cms:
            ok.append(f"{p.name} :: {label}")

print("MISSING CMS:")
for line in missing:
    print(" ", line)
print("missing count:", len(missing))
print("ok count:", len(ok))

# site.region check
region = (root / "site.region").read_text(encoding="utf-8")
for name, needle in [
    ("mainNav", "mainNav"),
    ("footerNav", "footerNav"),
    ("legalNav", "legalNav"),
    ("footer social", "site-footer-social"),
    ("header logo cms", "site-header-logo"),
    ("footer logo cms", "site-footer-logo"),
]:
    print(f"site.region {name}:", "YES" if needle in region else "NO")
