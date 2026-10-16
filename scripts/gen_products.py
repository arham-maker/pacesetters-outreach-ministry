# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "pages"

PRODUCTS = [
    {
        "slug": "songs-of-encouragement",
        "title": "Songs of Encouragement",
        "cat": "Music &amp; CDs",
        "price": "$20.00",
        "img": "p01",
        "lede": "Worship music to lift your heart and draw you closer to God.",
        "short": "A collection of encouraging songs for quiet time, family worship, and everyday faith.",
        "about1": "Songs of Encouragement gathers music from our ministry to support worship and reflection throughout the week.",
        "about2": "Play these recordings when you need peace, praise, or a reminder of God's faithfulness in every season.",
    },
    {
        "slug": "hope-for-every-season",
        "title": "Hope for Every Season",
        "cat": "Sermons",
        "price": "$18.00",
        "img": "p02",
        "lede": "Biblical teaching to strengthen your faith through life's changing seasons.",
        "short": "Audio sermons rooted in God's Word for encouragement and spiritual growth.",
        "about1": "Hope for Every Season offers messages that speak to joy, struggle, waiting, and renewal.",
        "about2": "Listen again when you need fresh courage and a deeper walk with Christ.",
    },
    {
        "slug": "rooted-in-faith",
        "title": "Rooted in Faith",
        "cat": "Books",
        "price": "$22.00",
        "img": "p03",
        "lede": "Reading that grounds your walk with Christ in Scripture and prayer.",
        "short": "A book of encouragement for personal study, small groups, and everyday discipleship.",
        "about1": "Rooted in Faith invites you to return to God's Word with clarity and hope.",
        "about2": "Use it for morning reflection, family reading, or sharing with someone who needs encouragement.",
    },
    {
        "slug": "praise-and-reflection",
        "title": "Praise &amp; Reflection",
        "cat": "Music &amp; CDs",
        "price": "$20.00",
        "img": "p04",
        "lede": "Music for worship, quiet prayer, and moments of thanksgiving.",
        "short": "Songs that help you praise God and rest in His presence.",
        "about1": "Praise &amp; Reflection is crafted for personal devotion and shared worship times.",
        "about2": "Let these tracks accompany prayer, study, and everyday moments of gratitude.",
    },
    {
        "slug": "daily-words-of-hope",
        "title": "Daily Words of Hope",
        "cat": "Books",
        "price": "$16.00",
        "img": "p05",
        "lede": "Short readings to encourage your faith one day at a time.",
        "short": "Simple, Scripture-centered encouragement for busy seasons of life.",
        "about1": "Daily Words of Hope offers brief reflections you can return to throughout the week.",
        "about2": "Keep it nearby for morning quiet time or evening prayer.",
    },
    {
        "slug": "walking-with-christ",
        "title": "Walking with Christ",
        "cat": "Sermons",
        "price": "$18.00",
        "img": "p06",
        "lede": "Messages that encourage a faithful walk with Jesus day by day.",
        "short": "Sermon recordings to support growth, prayer, and perseverance.",
        "about1": "Walking with Christ gathers teaching that points back to the gospel with clarity and care.",
        "about2": "Listen alone or share with a small group seeking encouragement together.",
    },
]

SHIPPING = 4.0


def money(amount: float) -> str:
    return f"${amount:.2f}"


def price_num(p: dict) -> float:
    return float(p["price"].replace("$", ""))


def related_html(current_slug: str) -> str:
    bits = []
    for o in PRODUCTS:
        if o["slug"] == current_slug:
            continue
        if len(bits) >= 3:
            break
        bits.append(
            f"""      <article class="pom-product">
        <a href="/{o['slug']}">
          <div class="pom-media is-store-{o['img']}" role="img" aria-label="{o['title'].replace('&amp;', 'and')}"></div>
          <div class="pom-product-meta">
            <div class="pom-product-row">
              <h3>{o['title']}</h3>
              <span class="pom-product-price">{o['price']}</span>
            </div>
            <p class="pom-product-cat">{o['cat']}</p>
          </div>
          <span class="pom-link"><span class="pom-link-text">View Details</span><span class="pom-arrow is-ne" aria-hidden="true"></span></span>
        </a>
      </article>"""
        )
    return "\n".join(bits)


def gallery_slides(p: dict) -> str:
    imgs = [p["img"]]
    for o in PRODUCTS:
        if o["img"] not in imgs:
            imgs.append(o["img"])
        if len(imgs) >= 3:
            break
    slides = []
    dots = []
    for i, img in enumerate(imgs):
        active = " is-active" if i == 0 else ""
        slides.append(
            f'      <div class="pom-media is-product-{img}{active}" data-slide="{i}" role="img" aria-label="{p["title"].replace("&amp;", "and")} image {i + 1}"></div>'
        )
        if i == 0:
            dots.append(f'<span class="is-active" data-dot="{i}"></span>')
        else:
            dots.append(f'<span data-dot="{i}"></span>')
    return "\n".join(slides), "".join(dots)


def checkout_html(p: dict) -> str:
    s = p["slug"]
    sub = price_num(p)
    total = sub + SHIPPING
    return f"""  <div class="pom-page-checkout" data-order-view hidden id="order" data-unit-price="{sub:.2f}" data-shipping="{SHIPPING:.2f}">
    <section class="pom-checkout" data-pom-region="{s}-checkout">
      <div class="pom-fallback">
        <div class="pom-checkout-main">
          <button class="pom-back is-ink" type="button" data-back-product><span class="pom-arrow is-back" aria-hidden="true"></span> Back to Product</button>
          <h1>Checkout</h1>
          <p class="pom-lede">Complete your order and bring encouragement home.</p>

          <form class="pom-checkout-form" data-checkout-form novalidate>
            <div class="pom-checkout-section">
              <h2><span>01</span> Contact details</h2>
              <div class="pom-field"><label for="{s}-chk-name">Name</label><input id="{s}-chk-name" name="name" type="text" autocomplete="name" required></div>
              <div class="pom-field"><label for="{s}-chk-email">Email</label><input id="{s}-chk-email" name="email" type="email" autocomplete="email" required></div>
              <div class="pom-field"><label for="{s}-chk-phone">Phone number</label><input id="{s}-chk-phone" name="phone" type="tel" autocomplete="tel"></div>
            </div>

            <div class="pom-checkout-section">
              <h2><span>02</span> Shipping details</h2>
              <div class="pom-field"><label for="{s}-chk-street">Street Address</label><input id="{s}-chk-street" name="street" type="text" autocomplete="address-line1" required></div>
              <div class="pom-field"><label for="{s}-chk-apt">Apartment, Suite, etc. (Optional)</label><input id="{s}-chk-apt" name="apt" type="text" autocomplete="address-line2"></div>
              <div class="pom-field-row">
                <div class="pom-field"><label for="{s}-chk-city">City</label><input id="{s}-chk-city" name="city" type="text" autocomplete="address-level2" required></div>
                <div class="pom-field"><label for="{s}-chk-state">State</label><input id="{s}-chk-state" name="state" type="text" autocomplete="address-level1" required></div>
              </div>
              <div class="pom-field-row">
                <div class="pom-field"><label for="{s}-chk-zip">Zip Code</label><input id="{s}-chk-zip" name="zip" type="text" autocomplete="postal-code" required></div>
                <div class="pom-field"><label for="{s}-chk-country">Country</label><input id="{s}-chk-country" name="country" type="text" autocomplete="country-name" required></div>
              </div>
            </div>

            <div class="pom-checkout-section">
              <h2><span>03</span> Payment details</h2>
              <div class="pom-field"><label for="{s}-chk-card">Card number</label><input id="{s}-chk-card" name="card" type="text" inputmode="numeric" autocomplete="cc-number" required></div>
              <div class="pom-field-row">
                <div class="pom-field"><label for="{s}-chk-exp">MM / YY</label><input id="{s}-chk-exp" name="exp" type="text" autocomplete="cc-exp" placeholder="MM / YY" required></div>
                <div class="pom-field"><label for="{s}-chk-cvc">CVC</label><input id="{s}-chk-cvc" name="cvc" type="text" inputmode="numeric" autocomplete="cc-csc" required></div>
              </div>
              <div class="pom-field"><label for="{s}-chk-cardname">Name on card</label><input id="{s}-chk-cardname" name="cardName" type="text" autocomplete="cc-name" required></div>
              <p class="pom-secure"><span class="pom-meta-icon is-lock" aria-hidden="true"></span> Your payment details are encrypted.</p>
              <label class="pom-check"><input type="checkbox" name="terms" required checked><span>I agree to the Terms &amp; Conditions and Privacy Policy.</span></label>
            </div>

            <button class="pom-btn-dark" type="submit"><span class="pom-link-text" data-order-pay>Pay {money(total)}</span><span class="pom-arrow is-ne" aria-hidden="true"></span></button>
            <p class="pom-form-error" data-checkout-error hidden>Please fill in all required fields to continue.</p>
          </form>
        </div>

        <aside class="pom-checkout-summary">
          <p class="pom-eyebrow">Your Order Summary</p>
          <h3>{p['title']}.</h3>
          <p class="pom-product-cat">{p['cat']}</p>
          <div class="pom-media is-checkout-item is-product-{p['img']}" role="img" aria-label="{p['title'].replace('&amp;', 'and')}"></div>
          <div class="pom-summary-row">
            <span data-order-qty>Quantity : 01</span>
            <button class="pom-edit" type="button" data-back-product>Edit</button>
          </div>
          <div class="pom-summary-lines">
            <div><span>Subtotal</span><strong data-order-subtotal>{p['price']}</strong></div>
            <div><span>Shipping</span><strong data-order-shipping>{money(SHIPPING)}</strong></div>
            <div><span>Tax</span><strong>$0.00</strong></div>
          </div>
          <div class="pom-summary-total"><span>Total</span><strong data-order-total>{money(total)}</strong></div>
          <p class="pom-summary-note">Thank you for supporting Pacesetters Outreach Ministry.</p>
          <p class="pom-summary-help">Need help with your order? <a href="/contact">Contact us</a></p>
        </aside>
      </div>
    </section>

    <div class="pom-modal is-order-confirmed" data-order-modal hidden>
      <div class="pom-modal-card" role="dialog" aria-modal="true" aria-labelledby="{s}-order-success-title">
        <button class="pom-modal-close" type="button" data-modal-close aria-label="Close">&times;</button>
        <div class="pom-modal-check" aria-hidden="true"></div>
        <h2 id="{s}-order-success-title">Thank You for Your Purchase!</h2>
        <p>Your order for {p['title']} is confirmed. We appreciate your support of the ministry.</p>
        <a class="pom-link" href="/store"><span class="pom-link-text">Back to Store</span><span class="pom-arrow is-ne" aria-hidden="true"></span></a>
      </div>
    </div>
  </div>
"""


def page_html(p: dict) -> str:
    related = related_html(p["slug"])
    slides, dots = gallery_slides(p)
    return f"""<div class="pom-page pom-page-product" data-product-page>
  <div data-product-view>
  <section class="pom-product-head">
    <a class="pom-back is-ink" href="/store"><span class="pom-arrow is-back" aria-hidden="true"></span> Back to Store</a>
    <h1>Product Details</h1>
    <p class="pom-lede">{p['lede']}</p>
  </section>

  <section class="pom-product-main">
    <div class="pom-product-gallery" data-gallery>
{slides}
      <div class="pom-gallery-nav">
        <button class="pom-icon-btn is-prev" type="button" data-gallery-prev aria-label="Previous image"><span class="pom-arrow"></span></button>
        <button class="pom-icon-btn is-next" type="button" data-gallery-next aria-label="Next image"><span class="pom-arrow"></span></button>
      </div>
      <div class="pom-gallery-dots" data-gallery-dots>{dots}</div>
    </div>
    <div class="pom-product-info">
      <p class="pom-eyebrow">{p['cat']}</p>
      <h2>{p['title']}</h2>
      <p class="pom-prose">{p['short']}</p>
      <div class="pom-qty" data-qty>
        <span>Quantity</span>
        <div class="pom-qty-ctrl">
          <button type="button" data-qty-minus aria-label="Decrease quantity">−</button>
          <input type="text" value="1" readonly aria-label="Quantity">
          <button type="button" data-qty-plus aria-label="Increase quantity">+</button>
        </div>
      </div>
      <a class="pom-btn-dark" href="#order" data-buy-now><span class="pom-link-text">Buy Now</span><span class="pom-arrow is-ne" aria-hidden="true"></span></a>
    </div>
  </section>

  <section class="pom-product-about">
    <h2>About this resource</h2>
    <p class="pom-prose">{p['about1']}</p>
    <p class="pom-prose">{p['about2']}</p>
  </section>

  <section class="pom-related">
    <p class="pom-eyebrow">You May Also Like</p>
    <h2>More resources for your walk of faith.</h2>
    <div class="pom-related-grid">
{related}
    </div>
  </section>

  <section class="pom-testimonials" data-pom-region="product-{p['slug']}-testimonials">
    <div class="pom-fallback">
      <div class="pom-testimonials-intro">
        <div>
          <p class="pom-eyebrow">Testimonials</p>
          <h2>Stories of faith<br>and hope.</h2>
          <div class="pom-quote-nav">
            <button class="pom-icon-btn is-prev" type="button" data-quote="prev" aria-label="Previous story"><span class="pom-arrow"></span></button>
            <button class="pom-icon-btn is-next" type="button" data-quote="next" aria-label="Next story"><span class="pom-arrow"></span></button>
          </div>
        </div>
      </div>
      <div class="pom-quote-wrap" data-quotes>
        <blockquote class="pom-quote is-active">
          <div class="pom-quote-mark" aria-hidden="true">“</div>
          <p>These resources have encouraged my faith and given me words and music to return to throughout the week.</p>
          <cite>— Jane Doe</cite>
        </blockquote>
        <blockquote class="pom-quote">
          <div class="pom-quote-mark" aria-hidden="true">“</div>
          <p>Being part of this community has strengthened my faith and given me a place to belong.</p>
          <cite>— Michael R.</cite>
        </blockquote>
        <blockquote class="pom-quote">
          <div class="pom-quote-mark" aria-hidden="true">“</div>
          <p>The teaching and prayer leave me encouraged for the week ahead.</p>
          <cite>— Sarah L.</cite>
        </blockquote>
      </div>
    </div>
    <div class="pom-cms"><squarespace:block-field id="product-{p['slug']}-testimonials" columns="12" /></div>
  </section>

  <section class="pom-contact is-crowd" id="get-in-touch" data-pom-region="product-{p['slug']}-contact">
    <div class="pom-fallback">
      <div class="pom-contact-copy">
        <p class="pom-eyebrow">Get in Touch</p>
        <h2>We’d love to hear from you.</h2>
        <p class="pom-contact-lead">Have a question, need prayer, or want to help?</p>
        <div class="pom-contact-meta is-icons">
          <a href="tel:3305059087">330 505-9087 <span class="pom-meta-icon is-phone" aria-hidden="true"></span></a>
          <a href="mailto:terryolivia@currently.com">terryolivia@currently.com <span class="pom-meta-icon is-mail" aria-hidden="true"></span></a>
        </div>
      </div>
      <form class="pom-form-card" data-contact-form>
        <div class="pom-field"><label for="{p['slug']}-name">Name</label><input id="{p['slug']}-name" name="name" type="text"></div>
        <div class="pom-field"><label for="{p['slug']}-email">Email</label><input id="{p['slug']}-email" name="email" type="email"></div>
        <div class="pom-field"><label for="{p['slug']}-message">Message</label><textarea id="{p['slug']}-message" name="message"></textarea></div>
        <button class="pom-link" type="submit"><span class="pom-link-text">Send Message</span><span class="pom-arrow is-ne" aria-hidden="true"></span></button>
        <p class="pom-form-note" hidden>Thank you. Add a Squarespace Form block to deliver messages.</p>
      </form>
    </div>
    <div class="pom-cms"><squarespace:block-field id="product-{p['slug']}-contact" columns="12" /></div>
  </section>
  </div>

{checkout_html(p)}</div>
"""


def store_cards() -> str:
    cats = {
        "p01": "music",
        "p02": "sermons",
        "p03": "books",
        "p04": "music",
        "p05": "books",
        "p06": "sermons",
    }
    bits = []
    for p in PRODUCTS:
        bits.append(
            f"""        <article class="pom-product" data-category="{cats[p['img']]}">
          <a href="/{p['slug']}">
            <div class="pom-media is-store-{p['img']}" role="img" aria-label="{p['title'].replace('&amp;', 'and')}"></div>
            <div class="pom-product-meta">
              <div class="pom-product-row">
                <h3>{p['title']}</h3>
                <span class="pom-product-price">{p['price']}</span>
              </div>
              <p class="pom-product-cat">{p['cat']}</p>
            </div>
            <span class="pom-link"><span class="pom-link-text">View Details</span><span class="pom-arrow is-ne" aria-hidden="true"></span></span>
          </a>
        </article>"""
        )
    return "\n".join(bits)


def standalone_checkout(p: dict) -> str:
    """Full-page order template (optional CMS page at /order)."""
    inner = checkout_html(p)
    # standalone: remove hidden, use link back instead of button toggle
    inner = inner.replace(' data-order-view hidden id="order"', "")
    inner = inner.replace(
        '<button class="pom-back is-ink" type="button" data-back-product><span class="pom-arrow is-back" aria-hidden="true"></span> Back to Product</button>',
        f'<a class="pom-back is-ink" href="/{p["slug"]}"><span class="pom-arrow is-back" aria-hidden="true"></span> Back to Product</a>',
    )
    inner = inner.replace(
        '<button class="pom-edit" type="button" data-back-product>Edit</button>',
        f'<a class="pom-edit" href="/{p["slug"]}">Edit</a>',
    )
    return f'<div class="pom-page pom-page-checkout">\n{inner}\n</div>\n'


def main() -> None:
    for p in PRODUCTS:
        conf_title = p["title"].replace("&amp;", "&")
        conf = (
            "{\n"
            f'  "title": "{conf_title}",\n'
            f'  "description": "Product detail for {conf_title}. Create at URL /{p["slug"]} (Not Linked)."\n'
            "}\n"
        )
        (PAGES / f"{p['slug']}.page").write_text(page_html(p), encoding="utf-8")
        (PAGES / f"{p['slug']}.page.conf").write_text(conf, encoding="utf-8")
        print("Wrote", p["slug"])

    first = PRODUCTS[0]
    (PAGES / "product-details.page").write_text(page_html(first), encoding="utf-8")
    print("Updated product-details.page")

    # Standalone order page template (Buy Now works on product pages without this)
    (PAGES / "order.page").write_text(standalone_checkout(first), encoding="utf-8")
    (PAGES / "order.page.conf").write_text(
        '{\n'
        '  "title": "Order",\n'
        '  "description": "Optional standalone checkout at /order. Buy Now also opens checkout on each product page."\n'
        "}\n",
        encoding="utf-8",
    )
    print("Wrote order.page")

    # Keep checkout.page in sync as alias of order
    (PAGES / "checkout.page").write_text(standalone_checkout(first), encoding="utf-8")
    print("Updated checkout.page")

    # Patch store.page product grid
    store_path = PAGES / "store.page"
    store = store_path.read_text(encoding="utf-8")
    new_grid = (
        '<div class="pom-products" data-product-grid>\n'
        + store_cards()
        + "\n      </div>"
    )
    marker_end = '      </div>\n    </div>\n    <div class="pom-cms"><squarespace:block-field id="store-grid"'
    start = store.index('<div class="pom-products" data-product-grid>')
    end = store.index(marker_end)
    store = (
        store[:start]
        + new_grid
        + "\n    </div>\n    <div class=\"pom-cms\"><squarespace:block-field id=\"store-grid\""
        + store[end + len(marker_end) :]
    )
    store_path.write_text(store, encoding="utf-8")
    print("Updated store.page")

    list_path = ROOT / "collections" / "products.list"
    plist = list_path.read_text(encoding="utf-8")
    start_marker = '        {.or}\n        <article class="pom-product" data-category="music">'
    end_marker = (
        "\n        {.end}\n      </div>\n    </div>\n"
        '    <div class="pom-cms"><squarespace:block-field id="store-grid"'
    )
    start = plist.index(start_marker)
    end = plist.index(end_marker, start)
    cats = {
        "p01": "music",
        "p02": "sermons",
        "p03": "books",
        "p04": "music",
        "p05": "books",
        "p06": "sermons",
    }
    fallback = "\n".join(
        f"""        <article class="pom-product" data-category="{cats[p['img']]}">
          <a href="/{p['slug']}">
            <div class="pom-media is-store-{p['img']}" role="img" aria-label="{p['title'].replace('&amp;', 'and')}"></div>
            <div class="pom-product-meta">
              <div class="pom-product-row">
                <h3>{p['title']}</h3>
                <span class="pom-product-price">{p['price']}</span>
              </div>
              <p class="pom-product-cat">{p['cat']}</p>
            </div>
            <span class="pom-link"><span class="pom-link-text">View Details</span><span class="pom-arrow is-ne" aria-hidden="true"></span></span>
          </a>
        </article>"""
        for p in PRODUCTS
    )
    plist = plist[:start] + "        {.or}\n" + fallback + plist[end:]
    list_path.write_text(plist, encoding="utf-8")
    print("Updated products.list")


if __name__ == "__main__":
    main()
