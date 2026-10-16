from pathlib import Path
import re

PAGES = Path(__file__).resolve().parents[1] / "pages"

def contact_block(prefix: str, field_prefix: str, with_id: bool = True) -> str:
    id_attr = ' id="get-in-touch"' if with_id else ""
    return f"""  <section class="pom-contact is-crowd"{id_attr}>
    <div class="pom-contact-layout">
      <div class="pom-contact-copy" data-pom-region="{prefix}-contact-copy">
        <div class="pom-fallback">
          <p class="pom-eyebrow">Get in Touch</p>
          <h2>We’d love to hear from you.</h2>
          <p class="pom-contact-lead">Have a question, need prayer, or want to help?</p>
          <div class="pom-contact-meta is-icons">
            <a href="tel:3305059087">330 505-9087 <span class="pom-meta-icon is-phone" aria-hidden="true"></span></a>
            <a href="mailto:terryolivia@currently.com">terryolivia@currently.com <span class="pom-meta-icon is-mail" aria-hidden="true"></span></a>
          </div>
        </div>
        <div class="pom-cms"><squarespace:block-field id="{prefix}-contact-copy" columns="12" /></div>
      </div>
      <div class="pom-form-card" data-pom-region="{prefix}-contact-form">
        <div class="pom-fallback">
          <p class="pom-form-cms-hint">Edit this page → click here → add a <strong>Form</strong> block to receive messages by email.</p>
          <form data-contact-form>
            <div class="pom-field"><label for="{field_prefix}-name">Name</label><input id="{field_prefix}-name" name="name" type="text"></div>
            <div class="pom-field"><label for="{field_prefix}-email">Email</label><input id="{field_prefix}-email" name="email" type="email"></div>
            <div class="pom-field"><label for="{field_prefix}-message">Message</label><textarea id="{field_prefix}-message" name="message"></textarea></div>
            <button class="pom-link" type="submit"><span class="pom-link-text">Send Message</span><span class="pom-arrow is-ne" aria-hidden="true"></span></button>
          </form>
        </div>
        <div class="pom-cms"><squarespace:block-field id="{prefix}-contact-form" columns="12" /></div>
      </div>
    </div>
  </section>"""


pat = re.compile(r'  <section class="pom-contact is-crowd"[^>]*>.*?  </section>', re.S)

mapping = {
    "about.page": ("about", "about", True),
    "services.page": ("services", "svc", False),
    "events.page": ("events", "events", True),
    "prayer.page": ("prayer", "prayer", True),
    "outreach.page": ("outreach", "outreach", True),
    "store.page": ("store", "store", True),
}

for name, (prefix, field, with_id) in mapping.items():
    path = PAGES / name
    text = path.read_text(encoding="utf-8")
    if not pat.search(text):
        print("NO MATCH", name)
        continue
    path.write_text(pat.sub(contact_block(prefix, field, with_id), text, count=1), encoding="utf-8")
    print("Updated", name)
