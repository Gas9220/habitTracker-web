#!/bin/zsh
# Writes the images the pages show, in WebP, from the full-size originals in ../assets, which stay
# out of this repository: the screenshots into images/<lang>/, each with a -dark version for the
# site's dark theme, and the app icon into images/. The watch's screens are dark in both themes.
# At this size WebP looks the same as PNG in about a fifteenth of the room, which counts on a phone.
# Run it after new screenshots, then draw the pictures for shared links again
# (make-social-images.swift). It needs cwebp: brew install webp.
#
#     ./make-images.sh
set -eu
cd "$(dirname "$0")"
assets=../assets

# webp <source> <width, 0 to keep it> <destination>
webp() {
  if (( $2 )); then
    cwebp -quiet -q 82 -m 6 -sharp_yuv -resize $2 0 "$1" -o "$3"
  else
    cwebp -quiet -q 82 -m 6 -sharp_yuv "$1" -o "$3"
  fi
}

for language in en it fr es; do
  source=$assets/screenshots/$language
  output=images/$language
  for screen in 01-habits:habits 02-statistics:statistics 03-charts:charts 04-habit-year:habit-year \
                05-timer:timer 06-lock-screen:lock-screen 07-control:control 08-day-note:day-note \
                09-editor:editor 10-templates:templates; do
    webp $source/iphone/${screen%%:*}.png 660 $output/${screen##*:}.webp
    webp $source/iphone-dark/${screen%%:*}.png 660 $output/${screen##*:}-dark.webp
  done
  webp $source/watch/01-today.png 0 $output/watch-today.webp
  webp $source/watch/02-habit.png 0 $output/watch-habit.webp
  webp $source/mac/01-window.png 1100 $output/mac-window.webp
  webp $source/mac-dark/01-window.png 1100 $output/mac-window-dark.webp
  webp $source/mac/02-menu-bar.png 360 $output/mac-menu-bar.webp
  webp $source/mac-dark/02-menu-bar.png 360 $output/mac-menu-bar-dark.webp
  echo "wrote images/$language: $(du -sk $output/*.webp | awk '{sum += $1} END {print sum}') KB"
done

# Three times the largest it's shown at, the 88 points of the home page.
webp $assets/icon/AppIcon-1024.png 264 images/app-icon.webp
echo "wrote images/app-icon.webp"
