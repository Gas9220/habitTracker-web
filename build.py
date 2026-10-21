#!/usr/bin/env python3
"""Builds the website's pages, one per language, from src/page.html and src/strings/<language>.json.

    python3 build.py

English is the root page (index.html), the others are in their own folder (it/index.html, …).
GitHub Pages serves the files this writes, so commit them together with the sources.

In the template, {{key}} is replaced by that string as it is (strings may contain HTML, like
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
      var supported = %s;
      var preferred = navigator.languages || [navigator.language];
      for (var i = 0; i < preferred.length; i++) {
        var code = (preferred[i] || "").slice(0, 2).toLowerCase();
        if (code === "en") return;
        if (supported.indexOf(code) >= 0) {
          location.replace(code + "/" + location.hash);
          return;
        }
      }
    })();
  </script>"""


def folder(language):
    return "" if language == DEFAULT else language + "/"


def language_menu(current, root, strings):
    links = []
    for code, name in LANGUAGES.items():
        selected = code == current
        links.append(
            f'            <li><a href="{root + folder(code) or "./"}" hreflang="{code}" lang="{code}" data-language="{code}"'
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


def alternates():
    lines = [
        f'  <link rel="alternate" hreflang="{code}" href="{BASE_URL}{folder(code)}">'
        for code in LANGUAGES
    ]
    lines.append(f'  <link rel="alternate" hreflang="x-default" href="{BASE_URL}">')
    return "\n".join(lines)


def build(language, template, strings):
    root = "" if language == DEFAULT else "../"
    values = dict(strings)
    values.update({
        "lang": language,
        "root": root,
        "images": f"{root}images/{language}/",
        "base_url": BASE_URL,
        "page_url": BASE_URL + folder(language),
        "alternates": alternates(),
        "language_menu": language_menu(language, root, strings),
        "redirect_script": REDIRECT_SCRIPT % json.dumps([c for c in LANGUAGES if c != DEFAULT])
        if language == DEFAULT else "",
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

    page = re.sub(r"\{\{(\w+)(?:\|(\w+))?\}\}", replace, template)
    if missing:
        sys.exit(f"{language}: missing {', '.join(sorted(missing))}")
    return page


def main():
    template = (ROOT / "src" / "page.html").read_text(encoding="utf-8")
    used = set(re.findall(r"\{\{(\w+)", template)) | {"language_label"}
    english = json.loads((ROOT / "src" / "strings" / "en.json").read_text(encoding="utf-8"))

    for language in LANGUAGES:
        strings = json.loads((ROOT / "src" / "strings" / f"{language}.json").read_text(encoding="utf-8"))
        extra = set(strings) - set(english)
        if extra:
            sys.exit(f"{language}: keys English doesn't have: {', '.join(sorted(extra))}")
        unused = set(strings) - used
        if unused:
            sys.exit(f"{language}: keys the page doesn't use: {', '.join(sorted(unused))}")

        output = ROOT / folder(language) / "index.html"
        output.parent.mkdir(exist_ok=True)
        output.write_text(build(language, template, strings), encoding="utf-8")
        print(f"wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
