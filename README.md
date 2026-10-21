# HabitTracker website

The website of HabitTracker, the habit tracker for iPhone, iPad, Mac and Apple Watch: what the app does, screenshots, privacy and how to get in touch, in the app's four languages (English, Italian, French and Spanish). A static site: GitHub Pages serves the files as they are.

**Live at https://gas9220.github.io/habitTracker-web/**, published by GitHub Pages from the root of `main`: every push to `main` updates it within a minute or two. Pages is free only for public repositories, so this one stays public. `.nojekyll` tells Pages to serve the files as they are, without running Jekyll.

## Files

```
src/page.html          The page, with {{key}} where each language's text goes
src/strings/<lang>.json  The text in each language: en, it, fr, es
build.py               Writes the pages from those two
index.html             English, the root page (generated)
it/, fr/, es/          The other languages' pages (generated)
styles.css             Styles, with dark mode (prefers-color-scheme) and layouts for phones
images/                The app icon (app-icon, apple-touch-icon, favicon)
images/<lang>/         The screenshots in each language, resized for the web
```

## Changing the text or the page

Edit `src/page.html` or `src/strings/*.json`, never the generated `index.html` files, then run:

```bash
python3 build.py
```

and commit the sources together with the pages it writes. A key missing from a language, or one the page doesn't use, stops the build. Strings can contain HTML (`<br>`, `<span class="accent">`); `{{key|attr}}` in the template escapes a string for an attribute, like an `alt` text.

Each language uses the app's own words, from its string catalog: Italian keeps "check-in", French says "valider" and "vous", Spanish "registrar" and "tú"; a streak is "serie", "série", "racha"; menus are named as the app names them (Impostazioni › Assistenza, Réglages › Assistance, Ajustes › Soporte).

## Languages

A menu in the header lists the four languages by their own names, as the app's language picker does. English is at the root and the others in their own folder, each page linking to the others with `hreflang`. On the first visit to the English page, a browser set to Italian, French or Spanish opens that language instead; choosing one in the menu is remembered (`localStorage`), and from then on nothing redirects.

## Screenshots

The full-size originals are in `../assets/screenshots/<lang>/iphone/` and `<lang>/watch/` (outside this repository, next to the app), so they can be reused for the App Store page. They're taken in the iOS Simulator (iPhone 18 Pro Max and Apple Watch Series 12, 46mm) with the app's sample data, whose habit names are translated too:

```bash
xcrun simctl status_bar <iPhone> override --time 9:41 --dataNetwork wifi --wifiMode active --wifiBars 3 --cellularMode active --cellularBars 4 --batteryState charged --batteryLevel 100
xcrun simctl launch <iPhone> <bundle ID> -ui-testing -sample-data -AppleLanguages "(it)" -AppleLocale it_IT
xcrun simctl launch <watch> <bundle ID>.watchkitapp -ui-testing -sample-data -AppleLanguages "(it)" -AppleLocale it_IT
```

The screens, in order: the habit list, Statistics, its charts (scrolled to the heatmap), Read 20 Pages' page (from the Habits card), Stretch's timer and Morning Run's editor; on the watch, Today and Read 20 Pages. The copies in `images/<lang>/` are the iPhone screenshots at half size (660 × 1434) and the watch screenshots as they are:

```bash
sips -Z 1434 ../assets/screenshots/it/iphone/01-habits.png --out images/it/habits.png
```

The app icon is rendered from the app's `AppIcon.icon` with Icon Composer's `ictool` into `../assets/icon/`, then resized with `sips`.

## Preview

```bash
python3 -m http.server 8765 --directory .
```

Then open http://localhost:8765 (the pages in other languages need a server, since their links point to folders).

## Before release

- **Support email**: `support@example.com` is a placeholder, the same as `AppInfo.supportEmail` in the app. Replace both with the real address (it's in `src/page.html`).
- **App name**: "HabitTracker" is a working name.
- **App Store link**: the hero says the app is coming soon; add the badge and link once it's out.
- **Translations**: written to match the app's wording; a native speaker's review is still to do, as for the app.
