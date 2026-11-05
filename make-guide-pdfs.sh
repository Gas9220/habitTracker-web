#!/bin/zsh
# Prints each language's guide page to <lang>/guide/habittracker-guide.pdf, the file its Download PDF
# button saves, with Chrome or Edge (headless, in a profile of its own that's deleted afterwards).
# The page's print styles hide the header's menus, the footer and the button. Run it after
# `python3 build.py` whenever the guide changes:
#
#     ./make-guide-pdfs.sh
set -eu
cd "$(dirname "$0")"

browser=""
for candidate in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
                 "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"; do
  if [[ -z "$browser" && -x "$candidate" ]]; then browser=$candidate; fi
done
if [[ -z "$browser" ]]; then
  echo "Chrome or Edge is needed to print the PDFs." >&2
  exit 1
fi

# Through a server, as the pages are online: their links point to folders.
port=8799
python3 -m http.server $port --bind 127.0.0.1 > /dev/null 2>&1 &
server=$!
profile=$(mktemp -d)
trap 'kill $server; rm -rf "$profile"' EXIT
sleep 1

for language in en it fr es; do
  folder=$([[ $language == en ]] && echo "" || echo "$language/")
  # English, so the English page doesn't send the browser to its own language's.
  "$browser" --headless --disable-gpu --no-first-run --lang=en-US --user-data-dir="$profile" \
    --no-pdf-header-footer --print-to-pdf="${folder}guide/habittracker-guide.pdf" \
    "http://127.0.0.1:$port/${folder}guide/" 2> /dev/null
  echo "wrote ${folder}guide/habittracker-guide.pdf"
done
