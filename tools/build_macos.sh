#!/bin/bash
# Run with bash tools/build_macos.sh from the repository root.
set -euo pipefail
cd "$(dirname "$0")/.."
test "$(uname -s)" = Darwin || { echo 'Build on macOS.' >&2; exit 1; }
arch="$(uname -m)"
python_bin="${PYTHON:-python3}"
test "$("$python_bin" -c 'import platform; print(platform.machine())')" = "$arch" || {
  echo 'Use native Python and Homebrew, without Rosetta.' >&2; exit 1;
}
mpv_bin="$(command -v mpv)"
lipo -archs "$mpv_bin" | tr ' ' '\n' | grep -qx "$arch"
command -v dylibbundler >/dev/null
command -v create-dmg >/dev/null
command -v msgfmt >/dev/null
test ! -e build && test ! -e dist || {
  echo 'Use a fresh checkout or move existing build/ and dist/ aside.' >&2; exit 1;
}
for file in i18n/*; do
  msgfmt -o "$file/LC_MESSAGES/macast.mo" "$file/LC_MESSAGES/macast.po"
done
"$python_bin" setup_py2app.py py2app --arch="$arch"
app='dist/Macast.app'
resources="$app/Contents/Resources"
mkdir -p "$resources/bin/MacOS"
cp "$mpv_bin" "$resources/bin/MacOS/mpv"
chmod u+w "$resources/bin/MacOS/mpv"
dylibbundler -od -b -x "$resources/bin/MacOS/mpv" \
  -d "$resources/bin/lib" -p '@executable_path/../lib/'
"$python_bin" tools/normalize_rpaths.py "$resources/bin"
"$python_bin" tools/prepare_distribution.py "$app"
# These are local test builds. Distribution additionally requires Developer ID
# signing and notarization; ad-hoc signing does not satisfy Gatekeeper.
codesign --force --deep --sign - "$app"
codesign --verify --deep --strict "$app"
"$resources/bin/MacOS/mpv" --version
if [[ "${MACAST_SKIP_SMOKE:-0}" != 1 ]]; then
  "$app/Contents/MacOS/Macast" >/dev/null 2>&1 &
  smoke_pid=$!
  sleep 5
  kill -0 "$smoke_pid"
  kill "$smoke_pid"
  wait "$smoke_pid" || true
fi
version="$(tr -d '\r\n' < macast/.version)"
create-dmg --skip-jenkins --volname "Macast $version ($arch)" \
  --window-size 800 400 --icon-size 100 --icon Macast.app 200 190 \
  --app-drop-link 600 185 "Macast-MacOS-v${version}-${arch}.dmg" dist/
