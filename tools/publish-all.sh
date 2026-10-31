#!/usr/bin/env bash
# Publish the whole Bloodfeed suite: hub (this tree), 8 piece repos, and the update to bloodfeed-global.
# Safe to re-run: skips repos/releases that already exist.
set -euo pipefail
B=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
K=$HOME/Documents/"Bloodfeed Release"
O=numbpill3d
CO="Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"


publish() {  # dir repo description tarball tags...
    local dir=$1 repo=$2 desc=$3 tar=$4; shift 4
    cd "$dir"
    [[ -d .git ]] || git init -q -b main
    git add -A
    git diff --cached --quiet || git commit -q -m "${repo}: Bloodfeed v1.0

$CO"
    git rev-parse -q --verify refs/tags/v1.0 >/dev/null || git tag -a v1.0 -m "$repo v1.0"
    if ! gh repo view "$O/$repo" >/dev/null 2>&1; then
        gh repo create "$O/$repo" --public --source . --description "$desc" >/dev/null
    fi
    git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$O/$repo.git"
    git push -q -u origin main
    git push -q origin v1.0
    local a=(); for t in "$@"; do a+=(--add-topic "$t"); done
    gh repo edit "$O/$repo" "${a[@]}" >/dev/null
    if ! gh release view v1.0 -R "$O/$repo" >/dev/null 2>&1; then
        if [[ -n $tar ]]; then gh release create v1.0 "$tar" -R "$O/$repo" --title "$repo v1.0" --notes "$desc" >/dev/null
        else gh release create v1.0 -R "$O/$repo" --title "$repo v1.0" --notes "$desc" >/dev/null; fi
    fi
    echo "ok  https://github.com/$O/$repo"
}

for d in "$B"/repos/bloodfeed-*; do
    r=$(basename "$d"); [[ $r == bloodfeed-global ]] && continue
    L="$K/$r/STORE-LISTING.txt"
    desc=$(awk '/^SUMMARY:/{getline; print; exit}' "$L")
    mapfile -t tags < <(sed -n 's/^TAGS: //p' "$L" | tr ',' '\n' | tr -d ' ' | awk 'NF && !seen[$0]++' | head -20)
    publish "$d" "$r" "$desc" "$K/$r/$r.tar.gz" "${tags[@]}"
done

# global: push the README update
cd "$B/repos/bloodfeed-global" && git push -q origin main && echo "ok  https://github.com/$O/bloodfeed-global (updated)"

# hub: the source tree with every generator
publish "$B" bloodfeed "Bloodfeed: a crimson VHS theme suite for KDE Plasma 6. SDDM, Plymouth, global theme, Plasma style, Aurorae, Kvantum, icons, Konsole, all generated from one palette." "" \
    bloodfeed kde plasma6 plasma-6 dark vhs scanlines crimson red blood horror analog-horror retro glow sddm plymouth aurorae kvantum kde-theme theme-suite
