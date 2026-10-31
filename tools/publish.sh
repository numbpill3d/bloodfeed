#!/usr/bin/env bash
# Publish repos/bloodfeed-global to GitHub: public repo, topics, v1.0 tag + release.
set -euo pipefail
B=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
R=numbpill3d/bloodfeed-global
cd "$B/repos/bloodfeed-global"
gh repo create "$R" --public --source . --push \
  --description "Bloodfeed: crimson VHS global theme for KDE Plasma 6. Red-black surfaces, scanlines, tape grain, crimson glow, rewind/play splash. The blood cut of Nightfeed."
git push origin v1.0
topics=(); while read -r t; do topics+=(--add-topic "$t"); done < "$B/dist/topics.txt"
gh repo edit "$R" "${topics[@]}"
gh release create v1.0 "$B/dist/scorn.bloodfeed.tar.gz" "$B/dist/bloodfeed-global-v1.0.tar.gz" -R "$R" \
  --title "Bloodfeed v1.0" --notes "First release of the Bloodfeed global theme for Plasma 6.

- \`scorn.bloodfeed.tar.gz\`: the look-and-feel package and splash alone (System Settings → Global Theme → Install from File).
- \`bloodfeed-global-v1.0.tar.gz\`: everything: global theme plus colour scheme, Plasma style, Aurorae, Kvantum and icons. Run \`./install.sh --apply\`."
gh repo view "$R" --json url,repositoryTopics --jq '.url, ([.repositoryTopics[].name]|join(" "))'
