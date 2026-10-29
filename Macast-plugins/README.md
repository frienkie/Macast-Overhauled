# Macast plugins — integrated build

[简体中文](README_ZH.md) · [Application guide](../README.md) · [MIT license](LICENSE)

This local plugin set accompanies the modified Macast application. All eight plugins are embedded in the DMG and installed into the user configuration directory on first launch. Managed, unmodified copies update automatically with backups; custom copies are preserved. Menus show compatible platforms only. External players such as IINA and PotPlayer are installed separately.

For Bilibili, select **NVA Protocol** and the bundled **MPV Renderer**. Nirvana 0.39 includes DASH quality handling, faster local message processing, stale-request protection during video switches, and an independent danmaku channel for bundled MPV. See the [application guide](../README.md) for limits and UI controls.

| Plugin | Version | Platform | File |
| --- | --- | --- | --- |
| Bolan IINA Renderer | 0.33 | darwin | [bolan-iina.py](bolan-iina/bolan-iina.py) |
| IINA Renderer | 0.31 | darwin | [iina.py](iina/iina.py) |
| Live Renderer | 0.4 | win32,darwin,linux | [live.py](live/live.py) |
| NVA Protocol | 0.39 | darwin,win32,linux | [nirvana.py](nirvana/nirvana.py) |
| PIFMRDS Renderer | 0.2 | linux | [pi_fm.py](pi-fm-rds/pi_fm.py) |
| PotPlayer Renderer | 0.4 | win32 | [potplayer.py](potplayer/potplayer.py) |
| PotPlayer Advanced | 0.4 | win32 | [potplayer_advanced.py](potplayer/potplayer_advanced.py) |
| Web Renderer | 0.2 | darwin,linux,win32 | [web.py](web/web.py) |

Original plugin instructions and contributor credits are preserved in each plugin folder and [upstream documentation](docs/upstream/README.md). To install manually for source runs, use **Open Config Directory**, copy the Python file into `renderer/` or `protocol/`, restart, and select it.
