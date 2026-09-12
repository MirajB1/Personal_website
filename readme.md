# Miraj Bhattarai — Portfolio

Source for [www.mirajbhattarai.com.np](https://www.mirajbhattarai.com.np).

Hand-written HTML, CSS and vanilla JavaScript. No framework, no build step, no npm.
Open `index.html` and it runs.

## What's in it

A terminal / dev-console interface with a light and a dark theme, an intro animation,
and six sections: about, experience, projects, skills, education and contact.

| | |
|---|---|
| **Intro** | The name rises out of a mask in two lines, an accent rule draws underneath, then the whole panel lifts away to reveal the page. ~1.9s, plays on every load, skippable with any key or click, bypassed entirely under `prefers-reduced-motion`, and a 3.5s failsafe clears it no matter what. |
| **Theme** | Follows the visitor's OS by default and keeps following it until they press the toggle; after that their choice is remembered in `localStorage`. Applied before first paint, so there's no flash of the wrong theme. |
| **Projects** | A file-browser: pick a project from the list, read it in the panel. Each one is broken into problem → approach → build → result rather than a wall of features. Keyboard accessible (arrow keys, Home, End). |
| **Visitor counter** | Counted once per browser session via `abacus.jasoncameron.dev`, shown in the top bar. Free and keyless. If it fails, the chip simply hides. |

## Search and answer-engine optimisation

**Classic SEO** — a 61-character title and 155-character description that both fit
without truncation; `robots` and `googlebot` directives with `max-image-preview:large`;
canonical URL and `hreflang`; Open Graph and Twitter cards with image alt text; an image
sitemap.

**Real headings.** The section headings are styled as shell commands, which would read to
a crawler as `01$ cat about.md`. Each one therefore carries a visually-hidden real title
(`About Miraj Bhattarai`, `Experience`, and so on) and the decorative command is marked
`aria-hidden`. Screen readers announce the real title, and so does the accessibility tree.

**Local / geographic** — `geo.region` (NP-BA), `geo.placename`, `geo.position` and `ICBM`
meta tags; `PostalAddress`, `homeLocation` with coordinates, `workLocation` and
`occupationLocation` in the structured data; the location also appears as visible text in
the hero.

**Answer engines (GEO)** — a `schema.org` `@graph` with seven linked entities: `WebSite`,
`ProfilePage`, a fully described `Person` (role, employer, education, awards, languages,
`knowsAbout`, `sameAs`) and one `CreativeWork` per project, each pointing back at the
person by `@id`. `robots.txt` explicitly welcomes GPTBot, ClaudeBot, PerplexityBot,
Google-Extended, Applebot-Extended and friends, and `llms.txt` gives them a clean plain-text
summary of who Miraj is, what he has built and how to get in touch — so an AI answer can
cite something accurate rather than guessing from markup.

Keep `llms.txt`, the JSON-LD and the visible page in agreement when you edit; a mismatch is
worse than none of it.

## Structure

```
index.html          the whole page
404.html            not-found page, same theme
css/style.css       tokens, layout, motion — both themes
js/script.js        intro, theme, reveal, project tabs, visitor count
images/             portrait (background removed), share image
docs/               résumé, PDF and DOCX
favicon.svg / .png
robots.txt          crawler rules, AI crawlers included
llms.txt            plain-text summary for AI answer engines
sitemap.xml         sitemap with image entry
CNAME
```

## Things worth knowing before editing

- **Colours** are all CSS custom properties at the top of `style.css`, defined twice —
  once under `[data-theme="dark"]`, once under `[data-theme="light"]`. Never hard-code a
  colour anywhere else and both themes stay in sync automatically.
- **Motion is one-shot.** Each section fades up once as it scrolls in, then the transition
  is removed from the element entirely, so the finished page is completely static.
- **Without JavaScript** the page renders complete and fully visible — elements are only
  hidden for the reveal once a script is present to reveal them again, and the intro panel
  never shows at all.
- **Responsive** down to 320px with no horizontal scroll. On narrow screens the portrait
  sits above the intro text at a size that still leaves the name on the first screen, and
  the project list becomes a plain vertical stack so nothing hides behind an invisible
  sideways scroll.
- **The résumé** lives at `docs/Miraj_Bhattarai_CV.pdf`. `docs/Miraj_Bhattarai.pdf` is an
  identical copy kept so older links keep working — replace both together.

## Running it locally

```bash
python3 -m http.server 8000
# http://localhost:8000
```

---

Miraj Bhattarai · Kathmandu, Nepal
