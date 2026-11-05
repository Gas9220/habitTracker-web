#!/usr/bin/env python3
"""Builds the website's pages in each language, from src/layout.html, src/pages/<page>.html and
src/strings/<language>.json.

    python3 build.py

Each page is src/layout.html (the head, the header and the footer) around its content, from
src/pages/. English is at the root (index.html, support/index.html, privacy/index.html), the other
languages in their own folder (it/index.html, it/support/index.html, …). GitHub Pages serves the
files this writes, so commit them together with the sources.

In the templates, {{key}} is replaced by that string as it is (strings may contain HTML, like
<br> or <strong>), and {{key|attr}} by the string escaped for an HTML attribute (alt texts,
meta descriptions). A key missing from a language stops the build, so no page is half translated.
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASE_URL = "https://gas9220.github.io/habitTracker-web/"

# The app's languages, in the order the menu lists them, with each one's own name (as the app's
# language picker shows them).
LANGUAGES = {
    "en": "English",
    "it": "Italiano",
    "fr": "Français",
    "es": "Español",
}
DEFAULT = "en"

# The pages, by the path each is served at in its language's folder: its template in src/pages/,
# then the strings for its title, its description, and its description where it's shared.
PAGES = {
    "": ("home", "title", "description", "og_description"),
    "support/": ("support", "support_title", "support_description", "support_description"),
    "privacy/": ("privacy", "policy_title", "policy_description", "policy_description"),
}

# On the English page, on the first visit only: open the page in the browser's language when it's
# one of the others, as the app follows the device's language. Choosing a language in the menu
# remembers it, and from then on nothing redirects.
REDIRECT_SCRIPT = """  <script>
    (function () {
      try {
        if (localStorage.getItem("language")) return;
      } catch (error) {
        return;
      }
      var supported = %(supported)s;
      var preferred = navigator.languages || [navigator.language];
      for (var i = 0; i < preferred.length; i++) {
        var code = (preferred[i] || "").slice(0, 2).toLowerCase();
        if (code === "en") return;
        if (supported.indexOf(code) >= 0) {
          location.replace(%(target)s);
          return;
        }
      }
    })();
  </script>"""


def folder(language):
    return "" if language == DEFAULT else language + "/"


def redirect_script(root, page):
    """The redirect to the same page in the browser's language, for the English pages."""
    target = (f"{json.dumps(root)} + " if root else "") + f'code + "/{page}" + location.hash'
    return REDIRECT_SCRIPT % {
        "supported": json.dumps([code for code in LANGUAGES if code != DEFAULT]),
        "target": target,
    }


def language_menu(current, root, strings, page):
    links = []
    for code, name in LANGUAGES.items():
        selected = code == current
        links.append(
            f'            <li><a href="{root + folder(code) + page or "./"}" hreflang="{code}" lang="{code}" data-language="{code}"'
            + (' aria-current="page"' if selected else "")
            + f'>{name}<svg class="tick" aria-hidden="true"><use href="#i-tick"/></svg></a></li>'
        )
    return "\n".join([
        '        <details class="language-menu">',
        f'          <summary aria-label="{html.escape(strings["language_label"], quote=True)}: {LANGUAGES[current]}">',
        '            <svg class="globe" aria-hidden="true"><use href="#i-globe"/></svg>',
        f'            <span>{LANGUAGES[current]}</span>',
        '            <svg class="chevron" aria-hidden="true"><use href="#i-chevron"/></svg>',
        '          </summary>',
        '          <ul>',
        *links,
        '          </ul>',
        '        </details>',
    ])


def alternates(page):
    lines = [
        f'  <link rel="alternate" hreflang="{code}" href="{BASE_URL}{folder(code)}{page}">'
        for code in LANGUAGES
    ]
    lines.append(f'  <link rel="alternate" hreflang="x-default" href="{BASE_URL}{page}">')
    return "\n".join(lines)


def sitemap():
    """Every page in every language, each with its translations, for search engines. A robots.txt
    can't point to it while the site is a project page: crawlers read that only at the domain's
    root, which belongs to another repository."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for page in PAGES:
        for language in LANGUAGES:
            lines.append("  <url>")
            lines.append(f"    <loc>{BASE_URL}{folder(language)}{page}</loc>")
            for code in LANGUAGES:
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{code}" href="{BASE_URL}{folder(code)}{page}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}{page}"/>')
            lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def build(language, page, layout, templates, strings):
    template, title_key, description_key, og_description_key = PAGES[page]
    # Relative links: up to the site's root for the stylesheet and images, and up to the
    # language's home page for its sections.
    home = "../" * page.count("/")
    root = ("" if language == DEFAULT else "../") + home
    values = dict(strings)
    values.update({
        "lang": language,
        "root": root,
        "home": home,
        "images": f"{root}images/{language}/",
        "base_url": BASE_URL,
        "page_url": BASE_URL + folder(language) + page,
        "page_title": strings[title_key],
        "page_description": strings[description_key],
        "page_og_description": strings[og_description_key],
        "alternates": alternates(page),
        "language_menu": language_menu(language, root, strings, page),
        "redirect_script": redirect_script(root, page) if language == DEFAULT else "",
    })

    missing = set()

    def replace(match):
        key, filter_ = match.group(1), match.group(2)
        if key not in values:
            missing.add(key)
            return ""
        value = values[key]
        # Attributes are in double quotes, so apostrophes can stay as they are.
        return html.escape(value, quote=False).replace('"', "&quot;") if filter_ == "attr" else value

    def fill(text):
        return re.sub(r"\{\{(\w+)(?:\|(\w+))?\}\}", replace, text)

    values["content"] = fill(templates[template])
    result = fill(layout)
    if missing:
        sys.exit(f"{language} {page or 'home'}: missing {', '.join(sorted(missing))}")
    return result


def main():
    layout = (ROOT / "src" / "layout.html").read_text(encoding="utf-8")
    templates = {
        template: (ROOT / "src" / "pages" / f"{template}.html").read_text(encoding="utf-8")
        for template, *_ in PAGES.values()
    }
    used = set(re.findall(r"\{\{(\w+)", layout + "".join(templates.values())))
    used |= {"language_label"} | {key for _, *keys in PAGES.values() for key in keys}
    english = json.loads((ROOT / "src" / "strings" / "en.json").read_text(encoding="utf-8"))

    for language in LANGUAGES:
        strings = json.loads((ROOT / "src" / "strings" / f"{language}.json").read_text(encoding="utf-8"))
        extra = set(strings) - set(english)
        if extra:
            sys.exit(f"{language}: keys English doesn't have: {', '.join(sorted(extra))}")
        unused = set(strings) - used
        if unused:
            sys.exit(f"{language}: keys the pages don't use: {', '.join(sorted(unused))}")

        for page in PAGES:
            output = ROOT / folder(language) / page / "index.html"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(build(language, page, layout, templates, strings), encoding="utf-8")
            print(f"wrote {output.relative_to(ROOT)}")

    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
