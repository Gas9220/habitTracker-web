# HabitTracker website

The website of HabitTracker, the habit tracker for iPhone, iPad, Mac and Apple Watch: what the app does, screenshots, privacy and how to get in touch, in the app's four languages (English, Italian, French and Spanish). A static site: GitHub Pages serves the files as they are.

**Live at https://gas9220.github.io/habitTracker-web/**, published by GitHub Pages from the root of `main`: every push to `main` updates it within a minute or two. Pages is free only for public repositories, so this one stays public. `.nojekyll` tells Pages to serve the files as they are, without running Jekyll.

## Files

```
src/layout.html        The head, header and footer every page shares, with {{key}} where each language's text goes
src/pages/             Each page's content: home, support (questions and answers, contact), privacy (the policy) and guide
src/guide/<lang>.html  The guide's text in each language: long, so in files of its own rather than strings
src/strings/<lang>.json  The text in each language: en, it, fr, es
build.py               Writes the pages from those, and sitemap.xml with every page in every language
make-social-images.swift  Draws images/<lang>/social.jpg, the picture shown with links to the site
make-guide-pdfs.sh     Prints each language's guide to its guide/habittracker-guide.pdf
index.html             English, the home page (generated), with support/, privacy/ and guide/ beside it
it/, fr/, es/          The other languages' pages, the same four in each (generated)
styles.css             Styles, with dark mode (prefers-color-scheme) and layouts for phones
images/                The app icon (app-icon, apple-touch-icon, favicon)
images/<lang>/         The screenshots in each language, resized for the web, and social.jpg
```

## Changing the text or the page

Edit `src/layout.html`, `src/pages/*.html`, `src/guide/*.html` or `src/strings/*.json`, never the generated `index.html` files, then run:

```bash
python3 build.py
```

and commit the sources together with the pages it writes. A key missing from a language, or one the page doesn't use, stops the build. Strings can contain HTML (`<br>`, `<span class="accent">`); `{{key|attr}}` in the template escapes a string for an attribute, like an `alt` text.

Each language uses the app's own words, from its string catalog: Italian keeps "check-in", French says "valider" and "vous", Spanish "registrar" and "tú"; a streak is "serie", "série", "racha"; menus are named as the app names them (Impostazioni › Assistenza, Réglages › Assistance, Ajustes › Soporte).

## The guide

`guide/` explains every feature, written from the app's CLAUDE.md, and names each button and setting in the words the app uses for it in each language (its string catalog), so what the guide says is what's on screen. When a feature ships or changes, change the guide with it, in all four files of `src/guide/`. `build.py` makes the table of contents from their `<h2 id="…">` headings.

The Download PDF button saves a PDF printed from the page itself, with Chrome or Edge, so print them again after any change:

```bash
python3 build.py
./make-guide-pdfs.sh
```

The print styles at the end of `styles.css` decide how they look: A4, the brand on top, without the menus, the footer or the button.

## Languages

A menu in the header lists the four languages by their own names, as the app's language picker does. English is at the root and the others in their own folder, each page linking to the others with `hreflang`. On the first visit to the English page, a browser set to Italian, French or Spanish opens that language instead; choosing one in the menu is remembered (`localStorage`), and from then on nothing redirects.

## Screenshots

The full-size originals are in `../assets/screenshots/<lang>/iphone/` and `<lang>/watch/` (outside this repository, next to the app), so they can be reused for the App Store page. They're taken in the iOS Simulator (iPhone 18 Pro Max and Apple Watch Series 12, 46mm) with the app's sample data, whose habit names are translated too:

```bash
xcrun simctl status_bar <iPhone> override --time 9:41 --dataNetwork wifi --wifiMode active --wifiBars 3 --cellularMode active --cellularBars 4 --batteryState charged --batteryLevel 100
xcrun simctl launch <iPhone> <bundle ID> -ui-testing -sample-data -AppleLanguages "(it)" -AppleLocale it_IT
xcrun simctl launch <watch> <bundle ID>.watchkitapp -ui-testing -sample-data -AppleLanguages "(it)" -AppleLocale it_IT
```

The screens, in order: the habit list, Statistics, its charts (scrolled to the heatmap), Read 20 Pages' page (from the Habits card), Stretch's timer, the Lock Screen with Stretch's timer running, Control Center with the Habit Timer control, a day note on Read 20 Pages, Morning Run's editor and the templates (New Habit › Start from a Template); on the watch, Today and Read 20 Pages.

- The Lock Screen, Control Center, the day note and the templates were taken by a throwaway UI test (never committed), as the app's workflow describes for screenshots. The day note was saved and opened again, so the keyboard is gone.
- The Lock Screen is Notification Center, pulled down over the Home Screen: it looks the same and shows the timer's Live Activity, but with the phone unlocked. Locked, the simulator draws the countdown without its seconds ("9:––"), however the screen is woken. Its clock is the real time, since any `--time` override freezes the countdown too, and its date and Control Center are drawn by the system in the simulator's own language: for each language, set the simulator's first (`AppleLanguages` and `AppleLocale` in its `.GlobalPreferences.plist`, then a reboot). A timer's first Live Activity asks to be allowed, and later whether to keep allowing them: Allow, then Always Allow.
- Control Center has the Habit Timer control, added by hand once (set to Next Timer, two columns wide so its name shows); the simulator's Control Center has nothing else.

The Mac's, in `../assets/screenshots/<lang>/mac/`, are the window on Read 20 Pages' statistics and the menu bar's panel, drawn by the app itself in a light appearance by a temporary hook (as the app's CLAUDE.md describes for looking at a Mac view), so the window has no shadow or desktop around it. macOS 26's glass doesn't draw that way: the sidebar's list is drawn on its own and put in its place, and the glass behind it and behind the panel comes out transparent, so it's filled with light gray (`#F2F2F5` and `#F7F7F9`), as it looks on a light desktop.

The copies in `images/<lang>/` are the iPhone screenshots at half size (660 × 1434), the watch screenshots as they are, and the Mac's window 1100 wide (`mac-window.png`) and panel 360 wide (`mac-menu-bar.png`):

```bash
sips -Z 1434 ../assets/screenshots/it/iphone/01-habits.png --out images/it/habits.png
sips --resampleWidth 1100 ../assets/screenshots/it/mac/01-window.png --out images/it/mac-window.png
```

The app icon is rendered from the app's `AppIcon.icon` with Icon Composer's `ictool` into `../assets/icon/`, then resized with `sips`.

After new screenshots or a change to the title or tagline, draw the pictures for shared links again: `swift make-social-images.swift`.

## Search engines

`sitemap.xml` lists every page in every language, with its translations; submit it in Google Search Console. A `robots.txt` pointing to it would be ignored here: crawlers read one only at the domain's root, `gas9220.github.io`, which isn't this repository. With a domain of its own the site would be at the root, and one could be added.

## Preview

```bash
python3 -m http.server 8765 --directory .
```

Then open http://localhost:8765 (the pages in other languages need a server, since their links point to folders).

## Before release

- **Support email**: `support@example.com` is a placeholder, the same as `AppInfo.supportEmail` in the app. Replace both with the real address (it's in `src/pages/home.html`, `support.html` and `privacy.html`).
- **App name**: "HabitTracker" is a working name.
- **App Store link**: the hero says the app is coming soon; add the badge and link once it's out.
- **Translations**: written to match the app's wording; a native speaker's review is still to do, as for the app.
- **Privacy policy** (`privacy/`): it describes the app as it is. If HabitTracker Pro ships, add how its purchases work (Apple handles them; the app only checks them on the device), and change the date at the top in every language.
