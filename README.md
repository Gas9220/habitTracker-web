# HabitTracker website

The website of HabitTracker, the habit tracker for iPhone, iPad, Mac and Apple Watch: what the app does, screenshots, privacy and how to get in touch. A static site with no build step.

**Live at https://gas9220.github.io/habitTracker-web/**, published by GitHub Pages from the root of `main`: every push to `main` updates it within a minute or two. Pages is free only for public repositories, so this one stays public. `.nojekyll` tells Pages to serve the files as they are, without running Jekyll.

## Files

```
index.html     The whole site: hero, features, screenshots, Apple Watch, privacy, contact and FAQ
styles.css     Styles, with dark mode (prefers-color-scheme) and layouts for phones
images/        The app icon (app-icon, apple-touch-icon, favicon) and the screenshots, resized for the web
```

## Preview

```bash
python3 -m http.server 8765 --directory .
```

Then open http://localhost:8765. Opening `index.html` straight from Finder works too.

## Screenshots

The full-size originals are in `../assets/screenshots/` (outside this repository, next to the app), so they can be reused for the App Store page. They were taken in the iOS Simulator (iPhone 18 Pro Max and Apple Watch Series 12, 46mm) with the app's sample data, launched with `-ui-testing -sample-data`, and the status bar set to 9:41 with `xcrun simctl status_bar`.

The copies in `images/` are the iPhone screenshots at half size (660 × 1434) and the watch screenshots as they are:

```bash
sips -Z 1434 ../assets/screenshots/iphone/01-habits.png --out images/iphone-habits.png
```

The app icon is rendered from the app's `AppIcon.icon` with Icon Composer's `ictool` into `../assets/icon/`, then resized with `sips`.

## Before publishing

- **Support email**: `support@example.com` is a placeholder, the same as `AppInfo.supportEmail` in the app. Replace both with the real address.
- **App name**: "HabitTracker" is a working name.
- **App Store link**: the hero says "Coming soon to the App Store"; add the badge and link once the app is out.
