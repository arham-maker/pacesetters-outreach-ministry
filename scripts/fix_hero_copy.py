from pathlib import Path
import re

root = Path(__file__).resolve().parents[1] / "pages"
for p in sorted(root.glob("*.page")):
    t = p.read_text(encoding="utf-8")
    o = t
    t = re.sub(
        r'<div class="pom-hero-copy pom-fallback" data-pom-region="([^"]+)">\s*<div class="pom-fallback">',
        r'<div class="pom-hero-copy" data-pom-region="\1">\n      <div class="pom-fallback">',
        t,
    )
    if t != o:
        p.write_text(t, encoding="utf-8", newline="\n")
        print("fixed", p.name)
print("done")
