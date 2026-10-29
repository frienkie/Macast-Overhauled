# Macast-Overhauled · Bilibili integrated edition for macOS

[简体中文](README_ZH.md) | [Build guide](BUILDING.md) | [Open-source licenses](THIRD_PARTY_NOTICES.md)

Want to watch a video from your phone on your Mac? Macast sits in the menu bar and receives videos, music, and pictures.

This edition builds on [xfangfang's Macast](https://github.com/xfangfang/Macast). The original repository's [last commit was in 2022](https://github.com/xfangfang/Macast/commits/main/), and [v0.7 is still its latest release](https://github.com/xfangfang/Macast/releases). macOS and phone casting protocols have kept moving, so this edition patches the gaps and brings Bilibili casting, a bundled MPV player, and [ModernZ](https://github.com/Samillion/ModernZ) controls together. You can install it without hunting down a separate player or plugin files.

This derivative is maintained independently. The installed app is still named **Macast.app**; the original download does not include these patches.

## Features

- **Phone casting** through standard DLNA or Bilibili's NVA protocol.
- **Bundled player** with MPV and its native libraries; Homebrew is not required to run it.
- **Quality selection** from the casting client using available DASH video tracks and matching audio.
- **Independent danmaku controls** for comments and ordinary subtitles, synchronized with the phone's danmaku switch.
- **Automatic UI scaling** for monitor DPI, window size, and fullscreen mode, with additional size presets.
- **Lightweight ModernZ interface** with blue accents and no extra thumbnail processes, video filters, or image enhancement passes.
- **Automatic plugin installation** for all eight companion plugins. Your customized copies stay in place when you install a newer build.

## Installation

### Requirements

- An Apple Silicon Mac (M-series chip). The current package is `arm64`.
- macOS 15 or later (the package-declared minimum; the release is built on macOS 15).
- Phone and Mac on the same local network, with communication between devices allowed.

### Steps

1. Download [**Macast-MacOS-v0.7-arm64.dmg**](https://github.com/frienkie/Macast-Overhauled/releases/latest/download/Macast-MacOS-v0.7-arm64.dmg) from Releases.
2. Open the DMG and drag **Macast.app** into **Applications**.
3. Open Macast from Applications. Its icon appears in the menu bar.
4. Allow local network access when prompted.

The current package uses local ad-hoc signing and has no Apple notarization. If macOS blocks launch, use the approval option offered in Privacy & Security. There is no need to disable SIP or Gatekeeper globally.

### Getting a newer build

This edition does not check for Macast updates online or show upstream version prompts. When a newer build is available from this project, open its DMG and replace the app in Applications. Bundled plugins that you have not changed update on the next launch; your own edits stay in place.

## Usage

### Bilibili casting

1. Open Macast's menu bar settings and select **NVA Protocol** and **MPV Renderer**.
2. Open a video in the phone's Bilibili client and tap its cast button.
3. Select **我的小电视** in the device list.
4. Control playback, seeking, and available quality levels from the phone or use the Mac player's controls.

Available quality levels depend on the video, server response, and account permissions. The application cannot unlock unavailable resolutions.

### Standard DLNA casting

Select the DLNA protocol in Macast, then discover and select the receiver from a DLNA-compatible phone application. The advertised device name follows your Macast settings.

### Player controls

Settings and player controls use English. Media titles, subtitle text, and danmaku keep their original language. Move the pointer toward the bottom of the player to reveal its controls.

| Control | Function |
| --- | --- |
| Play / Pause | Control the current video |
| Timeline | Seek to a playback position |
| Volume | Adjust volume or mute |
| **Subtitles** icon | Select an ordinary subtitle track, or **Off** |
| **Danmaku** speech bubble | Toggle comments independently; shown when danmaku is available |
| Fullscreen | Enter or leave fullscreen |

Subtitles and danmaku have independent switches. Turning subtitles off leaves danmaku available, and the phone's danmaku switch stays synchronized. The subtitle button may be unavailable if the video provides no ordinary captions. This interface and separation apply to the bundled **MPV Renderer**.

### Large and high-DPI displays

Open **Player UI Size** in Macast settings:

| Option | Effect |
| --- | --- |
| **Automatic (DPI)** | Scale with monitor DPI, window size, and fullscreen mode |
| **Automatic + 25%** | Enlarge the automatic size by 25% |
| **Automatic + 50%** | Enlarge the automatic size by 50% |

Changes apply immediately without restarting the player.

## Plugins and external players

Plugins install into the current user's configuration directory on first launch. Upgrades update managed, unmodified copies and back up replaced files; customized versions are preserved. Menus show only plugins compatible with the current platform.

| Plugin | Platform | Purpose |
| --- | --- | --- |
| Nirvana / NVA Protocol | macOS, Linux, Windows | Bilibili casting protocol |
| IINA | macOS | External IINA player |
| Bolan IINA | macOS | IINA extension with request headers |
| Live | macOS, Linux, Windows | Live source renderer |
| WebBrowser | macOS, Linux, Windows | Open media in a browser |
| PotPlayer | Windows | External PotPlayer |
| PotPlayer Advanced | Windows | Additional PotPlayer controls |
| PI-FM-RDS | Raspberry Pi / Linux | FM audio output |

Install IINA, PotPlayer, or other external players separately before selecting their plugins. Their interfaces and subtitle behavior are managed by those players. See [Macast-plugins](Macast-plugins/) for plugin source and versions.

## FAQ

### Phone cannot find the receiver?

Check that both devices share the same network, macOS allows Macast local network access, and the firewall permits incoming connections. Guest networks, wireless client isolation, and some VPNs can prevent discovery. Bilibili casting also requires **NVA Protocol**.

### Selected a device, but no player opened?

Check that **MPV Renderer** is selected. If using an external player plugin, make sure its application is installed. Select the video again and inspect the logs accessible through **Open Config Directory**.

### Why is 1080P unavailable?

First check that the video and account have access to that quality on the phone. The server response determines available tracks. Network errors, expired media URLs, or client protocol changes can also affect playback.

### Why does switching videos take a moment?

The player clears the previous frame and loads the new video. Quality and URL requests, transfer, decoder preparation, and buffering still take time. For unusually long delays, inspect stage timings in `latency.log` in the configuration directory.

### Configuration and issue reports

Choose **Open Config Directory** to open:

```text
~/Library/Application Support/Macast
```

The `renderer/` and `protocol/` folders contain player and protocol plugins. When reporting a problem, include the macOS version, Mac chip, selected protocol and player, phone client version, reproduction steps, and relevant logs. Remove account information, tokens, and complete media URLs before sharing logs. Identify this derivative edition so it can be distinguished from upstream.

## Good to know

- The current DMG targets macOS arm64. Plugins for other platforms do not make the DMG runnable on those platforms.
- Multi-segment `durl` videos are not supported. DRM, special audio tracks, and some client protocol combinations may not play.
- Client or service API changes may affect casting. The media service controls account and content access.

## Build from source

See [BUILDING.md](BUILDING.md). Use the included `Macast-plugins/` directory and build for the native architecture. The DMG includes bilingual documentation, license records, and a `Macast-Local-Source.tar.gz` snapshot of the modified application and plugins.

## Open-source projects and acknowledgements

This edition uses or derives from the following projects. Original authorship and licenses are retained.

| Project | Role | License |
| --- | --- | --- |
| [Macast — xfangfang](https://github.com/xfangfang/Macast) | Menu bar app, DLNA, and player framework; the base of this project | [GPL v3](LICENSE) |
| [Macast-plugins — xfangfang and contributors](https://github.com/xfangfang/Macast-plugins) | NVA, IINA, and other plugin foundations | [MIT](Macast-plugins/LICENSE) |
| [mpv](https://github.com/mpv-player/mpv) | Bundled video player | GPL/LGPL according to build configuration; see packaged notices |
| [ModernZ — Samillion](https://github.com/Samillion/ModernZ) | Player controls, extended with DPI scaling and independent danmaku controls | [LGPL v2.1](mpv_ui/LICENSE.ModernZ) |
| [FFmpeg](https://ffmpeg.org/) / [libass](https://github.com/libass/libass) | Media processing and ASS subtitle/danmaku rendering | FFmpeg: GPL/LGPL according to configuration; libass: ISC |
| [Fluent System Icons — Microsoft](https://github.com/microsoft/fluentui-system-icons) | Icon source for ModernZ | MIT |
| [Material Symbols — Google](https://github.com/google/material-design-icons) | Icon source for ModernZ | Apache 2.0 |
| [Vue](https://github.com/vuejs/vue) / [Element UI](https://github.com/ElemeFE/element) / [Vue Resource](https://github.com/pagekit/vue-resource) | Advanced settings page, components, English locale, and requests | MIT |
| [Python](https://www.python.org/) / [py2app](https://github.com/ronaldoussoren/py2app) | Runtime and macOS packaging | See original project licenses |
| [rumps](https://github.com/jaredks/rumps) / [PyObjC](https://github.com/ronaldoussoren/pyobjc) | Menu bar and Cocoa integration | See packaged notices |
| [CherryPy](https://github.com/cherrypy/cherrypy) / [cheroot](https://github.com/cherrypy/cheroot) | Local HTTP service | See packaged notices |
| [Requests](https://github.com/psf/requests) / [lxml](https://github.com/lxml/lxml) / [netifaces](https://github.com/al45tair/netifaces) / [pyperclip](https://github.com/asweigart/pyperclip) | HTTP, XML, network interface enumeration, and clipboard support | See packaged notices |

ModernZ builds on mpv OSC, maoiscat/mpv-osc-modern, cyl0/ModernX, and dexeonify/ModernX. Full credits are retained in the [original ModernZ documentation](mpv_ui/ModernZ-upstream-README.md).

See [SOURCE-REVISIONS.json](SOURCE-REVISIONS.json) for base application/plugin revisions and [UPSTREAM.json](mpv_ui/UPSTREAM.json) for the pinned ModernZ revision and modifications. Full license and dependency records are indexed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and the package's `Documentation/licenses/INVENTORY.json`. Each component remains under its own license.
