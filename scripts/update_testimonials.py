from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

NEW_QUOTES = """      <div class="pom-quote-wrap" data-quotes>
        <blockquote class="pom-quote is-active">
          <div class="pom-quote-mark" aria-hidden="true">“</div>
          <p>Two years ago, I was diagnosed with a degenerative back condition causing severe sciatic pain. I was taking Tylenol every 6 hours and was referred to a pain specialist. One day while in the hospital for a pacemaker, a nurse asked when I had surgery — I said I didn’t have surgery on my back. She said she could see scars on my back. Another nurse confirmed it. Then I realized I was overdue for my pain shot and I didn’t feel any pain. Praise God — He healed me supernaturally. I haven’t needed a shot since December 2025, and I don’t have any pain in my back. I give God all of the praise.</p>
          <cite>— God healed my back supernaturally</cite>
        </blockquote>
        <blockquote class="pom-quote">
          <div class="pom-quote-mark" aria-hidden="true">“</div>
          <p>In 1982 I was attacked by a hijacker. When I refused to give him my keys, he hit me over the head with a bottle and tried to kill me. As I was struggling, I saw an angel who spoke to me and said “not today,” and the hijacker left. During the struggle the car ran over my foot and it became paralyzed. After many years of walking with a paralyzed foot that affected my hip, in 2026 the pain became toxic. Doctors overmedicated me and I had a seizure. I was home alone, and because I’m diabetic, it meant my death in a short time. When I didn’t respond to my prayer warrior’s call, she knew something was wrong. She called the fire station; they found me dead, rushed me to the hospital, and brought me back to life. We give God praise for the miracle!</p>
          <cite>— God raised me from the dead and healed me</cite>
        </blockquote>
      </div>"""

QUOTE_RE = re.compile(
    r'      <div class="pom-quote-wrap" data-quotes>.*?</div>\n(?=    </div>|      </div>)',
    re.S,
)

# Product pages sometimes use slightly different indent for quotes inside gen template
QUOTE_RE_LOOSE = re.compile(
    r'<div class="pom-quote-wrap" data-quotes>.*?</div>\s*(?=<div class="pom-cms"|</div>\s*<div class="pom-cms"|</div>\s*</section>)',
    re.S,
)


def replace_in_text(text: str) -> tuple[str, int]:
    count = 0
    if QUOTE_RE.search(text):
        text, n = QUOTE_RE.subn(NEW_QUOTES + "\n", text)
        count += n
    elif QUOTE_RE_LOOSE.search(text):
        # preserve leading indent of match by replacing inner only
        def repl(m):
            indent = re.match(r"^(\s*)", m.group(0)).group(1)
            block = NEW_QUOTES
            if indent and indent != "      ":
                block = "\n".join(
                    (indent + line[6:]) if line.startswith("      ") else (indent + line.lstrip() if line.strip() else line)
                    for line in NEW_QUOTES.splitlines()
                )
            return block

        text, n = QUOTE_RE_LOOSE.subn(repl, text)
        count += n
    return text, count


def main() -> None:
    updated = []
    for path in sorted((ROOT / "pages").glob("*.page")):
        text = path.read_text(encoding="utf-8")
        if "pom-quote-wrap" not in text:
            continue
        new_text, n = replace_in_text(text)
        if n:
            path.write_text(new_text, encoding="utf-8")
            updated.append(f"{path.name} ({n})")

    products_list = ROOT / "collections" / "products.list"
    if products_list.exists():
        text = products_list.read_text(encoding="utf-8")
        if "pom-quote-wrap" in text:
            new_text, n = replace_in_text(text)
            if n:
                products_list.write_text(new_text, encoding="utf-8")
                updated.append(f"products.list ({n})")

    gen = ROOT / "scripts" / "gen_products.py"
    if gen.exists():
        text = gen.read_text(encoding="utf-8")
        if "pom-quote-wrap" in text:
            # Replace the testimonials quote block inside the Python string carefully
            gen_re = re.compile(
                r'(      <div class="pom-quote-wrap" data-quotes>.*?</div>\n)',
                re.S,
            )
            # In gen_products the indent may use spaces inside triple quotes
            if gen_re.search(text):
                text, n = gen_re.subn(NEW_QUOTES + "\n", text, count=1)
                if n:
                    gen.write_text(text, encoding="utf-8")
                    updated.append(f"gen_products.py ({n})")

    print("Updated:")
    for item in updated:
        print(" ", item)
    print("total", len(updated))


if __name__ == "__main__":
    main()
