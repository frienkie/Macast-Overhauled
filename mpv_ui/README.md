# Macast MPV UI

Based on [ModernZ](https://github.com/Samillion/ModernZ), pinned to commit `579897e8c974c380caa5017dc7b27a69123c1333`.
The original LGPL 2.1 license is included in LICENSE.ModernZ. The original icon font and locale files are bundled offline.

Macast changes:
- Blue accent, larger timeline, text and controls; native macOS window frame retained.
- Physical DPI scaling via MPV display-hidpi-scale, with bounded additional scaling for large windows and a separate fullscreen multiplier.
- Resizes and display changes trigger updates; no background DPI polling.
- Live UI scaling from the Macast menu, without restarting playback.
- Bundled locale lookup and a directory-packaged script.
- UI redraws limited to 30 Hz; glow, thumbnail generation, download UI and persistent overlays disabled. Video decoding and shaders are unchanged.

The upstream file hashes and local changes are recorded in UPSTREAM.json. The modified Lua source is scripts/modernz/main.lua. Visual results and playback performance remain for the user to verify.

The interface is fixed to English. A vector speech-bubble Danmaku toggle controls the secondary ASS plane; Subtitles selects only non-danmaku primary tracks. The normal subtitle visibility and danmaku visibility are independent, and the phone danmaku switch remains synchronized.

The integrated preset hides ModernZ's audio-track and in-player pin selectors. The Macast menu keeps the Player Ontop setting. The Danmaku bubble is an added glyph in the bundled icon font with the same metrics and baseline as the subtitle icon; its source is `tools/add_danmaku_icon.py`. Volume controls remain available.
