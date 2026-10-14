# Pacesetters Outreach Ministry

Squarespace 7.0 Developer Mode template for the Pacesetters Outreach Ministry design.

Source file: [Square Space Projects (Copy)](https://www.figma.com/design/ZsOAf3DSsOuQZuqQLI9eUL/Square-Space-Projects--Copy-?node-id=640-2)

Canvas: `640:2` Pacesetters Outreach Ministry.

This is JSON-T, LESS, and plain JavaScript. It does not use Squarespace 7.1 fluid sections, React, or a Shopify theme.

## Page to Figma frame

| Layout in this template | Recommended URL | Figma frame | Node |
| --- | --- | --- | --- |
| Home | `/` (set as homepage) | Pacesetters Outreach Ministry [Home] | `641:4` |
| About | `/about` | Pacesetters Outreach Ministry [About] | `698:2` |
| Services | `/services` | Pacesetters Outreach Ministry [Main Service List] | `645:413` |
| Community Outreach | `/community-outreach` | Pacesetters Outreach Ministry [Services 1] | `701:227` |
| Prayer | `/prayer` | Pacesetters Outreach Ministry [Services 2] | `702:441` |
| Events | `/events` | Pacesetters Outreach Ministry [Events] | `702:616` |
| Ministry Store (products collection) | `/store` | Pacesetters Outreach Ministry [Store] | `702:837` |
| Contact | `/contact` | No separate frame. Reuses Get in Touch | — |
| Privacy Policy | `/privacy-policy` | Footer link only | — |
| Terms and Conditions | `/terms` | Footer link only | — |
| Help and Support | `/help` | Footer link only | — |

Hidden frames that were not built as custom screens: `702:1381` Store Cart and Order Summary, `702:1382` Music CD product detail. The store list matches the visible Store frame. Product detail uses the same type and color system so a product can be purchased. Checkout and account screens stay on Squarespace’s system pages.

## CMS wiring

1. Turn on Developer Mode for the Squarespace 7.0 site and connect this repository when you are ready to push.
2. In Pages, add a page for each layout above and choose that layout from the template page list.
3. Set the URL slugs in the table so the template links resolve.
4. Set the Home layout as the site homepage.
5. Add a Store page. The products collection uses `collections/products.list` and `collections/products.item`. Set its URL to `/store`.
6. Add products with categories `Music & CDs`, `Sermons`, and `Books`. Those categories drive the store filters. Until products exist, the six placeholder cards from the design are shown.
7. In Design, fill Main Navigation with About, Services, Events, Store, and Contact. Fill Footer Navigation with the same links. Fill Legal Navigation with Privacy Policy, Terms & Conditions, and Help & Support. Until a navigation has links, the template shows the same list as a fallback.
8. Each designed region includes a `squarespace:block-field`. On the public site the visual fallback is what visitors see. After you add a block inside a region, the fallback hides and the blocks are shown. In the editor, empty regions are exposed so blocks can be added.
9. Replace each contact form with a Squarespace Form block (Name, Email, Message) inside that page’s contact region. The drawn form is only a visual fallback and does not deliver mail.
10. Replace the gradient image panels with the photographs from Figma. Drop the exports into `/assets` and point the `.pom-media` / `.pom-hero` backgrounds at them, or upload them into the matching block fields.
11. Set the real Facebook and Instagram URLs in `site.region`. The icons are in the footer; the file did not include profile URLs.
12. Update the phone and email if `330-505-9062` and `larry.vicks@currently.com` are placeholders.

## Design tokens

Sampled from the desktop screenshots:

| Token | Value | Use |
| --- | --- | --- |
| Ink | `#262625` | Text, footer, dark bands |
| Cream | `#F7F4ED` | FAQ, feature bands, page ground |
| Paper | `#FEFEFE` | White panels and testimonial field |
| Gold | `#C4A36A` | Eyebrows |
| Gold soft | `#E4D2AE` | FAQ and step circles |

Type: Instrument Serif for headlines, Manrope for interface and body. Exact Figma font names were not returned before the Figma export limit, so these are the closest match to the serif headlines and plain sans body. Change them in `site.region` and `styles/tokens.less` if the file uses different families.

## How a region stays editable

```html
<section data-pom-region="home-purpose">
  <div class="pom-fallback"><!-- design markup --></div>
  <div class="pom-cms">
    <squarespace:block-field id="home-purpose" columns="12" />
  </div>
</section>
```

`scripts/site.js` adds `has-cms` when the region contains a Squarespace block, which hides the fallback.

## Present vs missing

Photography, the original logo vector (`660:39`), and the exact font names are missing across every page. Figma’s MCP tool hit the Starter plan limit after the Home, About, Services, and Community Outreach screenshots. Services 2, Events, and Store were built from the frame tree and text layers. Their hero frames (`Frame 1`, 824px) contained no exported text nodes.

### Home (`641:4`)

Present: hero (“Faith. Hope. A place to belong.”), purpose triptych, Saturday Night Live split, store promo, testimonials, FAQ, Get in Touch, footer.

Missing: original photos. Closed FAQ rows have no answer in the file, so those panels open empty.

### About (`698:2`)

Present: hero, story triptych, purpose plus three commitments, “Faith shapes how we serve.”, growing reach, testimonials, FAQ, contact, footer.

Missing: original photos. Hero supporting line was read from the screenshot, not a text node.

### Services (`645:413`)

Present, in order: hero “Faith in action.”, Community Outreach, Prayer & Encouragement, Online Fellowship, Ministry Resources, testimonials, FAQ, contact (“Find your next step.”), footer.

Missing: original photos.

### Community Outreach (`701:227`)

Present: back link, hero, “A light in our communities.”, who we reach, testimonials, FAQ, contact, footer.

Missing: original photos.

### Prayer (`702:441`)

Present: “You don’t have to walk alone.”, how we can support you, testimonials, prayer FAQ, contact, footer.

Missing: screenshot confirmation. Hero title “Prayer & Encouragement” follows the Outreach hero pattern and the services-list name. The hero subtitle was not in the file. Image side of the first split was not visible.

### Events (`702:616`)

Present: Night Live split, What to expect, Upcoming Gatherings (including the “Micheal” spelling from the file), How to join, testimonials, events FAQ, contact, footer.

Missing: screenshot. The 824px hero had no text layer, so it is a photo band with a screen-reader title only. The visible headline is “Night Live” in the next section.

### Store (`702:837`)

Present: ministry resources intro, three category cards, filters, six resource cards, encouragement points, testimonials, store FAQ, contact, footer.

Missing: screenshot and hero text. Product cards use the file’s “Lorem ipsum” and “$XX.XX” until real products are added. Cart and the hidden CD detail frame are not custom screens.

### Contact, privacy, terms, help

Present so the header and footer links have destinations. Contact reuses Get in Touch. The three legal pages are simple text pages because Figma only shows the footer labels.

## Local check

Squarespace compiles the LESS when the template is pushed. `styles/site.less` was compiled locally with `lessc` and produced no errors. The template cannot be browsed as a finished site without Squarespace’s developer server.
