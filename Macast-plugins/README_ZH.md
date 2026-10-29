# Macast 插件集成版

[English](README.md) · [应用说明](../README_ZH.md) · [MIT 许可](LICENSE)

本地插件集与修改后的 Macast 应用配套使用。全部 8 个插件已经嵌入 DMG，首次打开 App 自动安装到用户配置目录；受管理且未经修改的版本会自动更新并备份，用户自定义文件会被保留。菜单只显示兼容平台。IINA、PotPlayer 等播放器本体需另外安装。

B 站投屏选择 **NVA Protocol** 和内置 **MPV Renderer**。Nirvana 0.39 包含 DASH 清晰度处理、本机消息延迟优化、切换视频时阻止旧请求回写，以及内置 MPV 独立弹幕通道。使用边界和界面操作见 [应用说明](../README_ZH.md)。

| 插件 | 版本 | 平台 | 文件 |
| --- | --- | --- | --- |
| Bolan IINA Renderer | 0.33 | darwin | [bolan-iina.py](bolan-iina/bolan-iina.py) |
| IINA Renderer | 0.31 | darwin | [iina.py](iina/iina.py) |
| Live Renderer | 0.4 | win32,darwin,linux | [live.py](live/live.py) |
| NVA Protocol | 0.39 | darwin,win32,linux | [nirvana.py](nirvana/nirvana.py) |
| PIFMRDS Renderer | 0.2 | linux | [pi_fm.py](pi-fm-rds/pi_fm.py) |
| PotPlayer Renderer | 0.4 | win32 | [potplayer.py](potplayer/potplayer.py) |
| PotPlayer Advanced | 0.4 | win32 | [potplayer_advanced.py](potplayer/potplayer_advanced.py) |
| Web Renderer | 0.2 | darwin,linux,win32 | [web.py](web/web.py) |

各插件原始说明与贡献者署名保存在对应目录及 [上游文档](docs/upstream/README_ZH.md)。源码运行需要手动安装时，使用 **Open Config Directory** 打开配置目录，将 Python 文件放入 `renderer/` 或 `protocol/`，重启后选择。
