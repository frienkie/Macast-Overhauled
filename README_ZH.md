# Macast-Overhauled · macOS 插件集成版

[English](README.md) | [构建指南](BUILDING.md) | [开源许可](THIRD_PARTY_NOTICES.md)

想把手机里的视频投到 Mac 上看？Macast 就是一个常驻菜单栏的接收器，视频、音乐和图片都能投。（音乐和图片的投屏实现仅基于标准 DLNA。）

这个版本从 [xfangfang 的 Macast](https://github.com/xfangfang/Macast) 出发。原版仓库[最后一次提交停在 2022 年](https://github.com/xfangfang/Macast/commits/main/)，[v0.7 仍是最新正式版](https://github.com/xfangfang/Macast/releases)；macOS 却已经经过几次大版本更新，B 站手机端投屏协议也有所变化，于是有了这份修补版。它把哔哩哔哩投屏、内置 MPV 和 [ModernZ](https://github.com/Samillion/ModernZ) 控制界面整合在一起，安装后就能用，不用再手动找播放器和插件。

这是独立维护的衍生版本。安装到 Mac 后，应用仍叫 **Macast.app**。

## 功能

- **手机投屏**：支持标准 DLNA，以及通过 NVA 协议连接的哔哩哔哩投屏。
- **内置播放器**：MPV 与所需动态库随 App 提供，运行无需 Homebrew。
- **清晰度切换**：支持从投屏端切换接口提供的 DASH 清晰度，并匹配音轨。
- **独立弹幕开关**：播放器中分别控制弹幕和普通字幕，手机弹幕开关同步生效。
- **自动缩放界面**：控件根据显示器 DPI、窗口大小和全屏状态调整尺寸，也可手动放大。
- **轻量控制界面**：采用 ModernZ 蓝色主题，不增加缩略图进程、视频滤镜或画质增强处理。
- **插件自动安装**：8 个配套插件随 App 一起安装。以后覆盖安装新版时，自己改过的插件也会保留。

## 安装

### 系统要求

- Apple Silicon Mac（M 系列芯片）。当前提供 `arm64` 安装包。
- macOS 15 或更新版本（安装包声明的最低版本；公开安装包在 macOS 15 上构建）。
- 手机与 Mac 连接同一局域网，且网络允许设备互相访问。

### 安装步骤

1. 从 [Releases 下载 **Macast-MacOS-v0.8-arm64.dmg**](https://github.com/frienkie/Macast-Overhauled/releases/latest/download/Macast-MacOS-v0.8-arm64.dmg)。
2. 打开 DMG，将 **Macast.app** 拖入 **Applications（应用程序）**。
3. 从“应用程序”打开 Macast，菜单栏出现图标即表示应用已启动。
4. 首次使用时允许 Macast 访问局域网。

当前安装包使用本地 ad-hoc 签名，未经过 Apple 公证。如果系统拦截启动，可在系统提供的“隐私与安全性”选项中确认允许；无需关闭 SIP 或全局禁用 Gatekeeper。

### 如何获取新版

由于本人不喜欢工具类应用的联网更新功能，这个修补版不会自动联网检查 Macast 的更新，也不会弹出上游版本提示。需要升级时，从本项目获取新的 DMG，像首次安装一样拖入“应用程序”覆盖即可。随 App 附带、未经修改的插件会在下次启动时更新；你自己修改的插件会保留。

## 使用方法

### 哔哩哔哩投屏

1. 点击 Macast 菜单栏图标，在设置中选择 **NVA Protocol** 和 **MPV Renderer**。
2. 在手机哔哩哔哩客户端中打开视频，点击投屏按钮。
3. 从设备列表选择 **我的小电视**。
4. 使用手机控制播放、暂停、进度与可用清晰度，也可在 Mac 播放器中操作。

可选清晰度由视频、接口返回结果和账号权限决定；某一清晰度没有出现时，本应用无法额外解锁。

### 普通 DLNA 投屏

在 Macast 中选择 DLNA 协议，然后在支持 DLNA 的手机应用中搜索并选择 Macast 设备。设备名以 Macast 的当前设置为准。

### 播放器操作

播放器和设置界面使用英语，视频标题、字幕正文和弹幕保留原语言。将鼠标移到播放器下方可显示控制栏。

| 控件 | 功能 |
| --- | --- |
| 播放 / 暂停按钮 | 控制当前视频 |
| 进度条 | 跳转播放位置 |
| 音量按钮 | 调整音量或静音 |
| **Subtitles** 字幕图标 | 选择普通字幕轨；选择 **Off** 关闭字幕 |
| **Danmaku** 气泡图标 | 单独开启或关闭弹幕；有弹幕可用时显示 |
| 全屏按钮 | 切换全屏显示 |

弹幕和字幕使用独立开关。关闭字幕不会关闭弹幕；手机上的弹幕开关也会同步到播放器。若视频没有提供普通字幕，字幕按钮可能不可用。此界面及弹幕分离功能适用于内置 **MPV Renderer**。

### 大屏幕和高 DPI 显示器

打开 Macast 设置中的 **Player UI Size**：

| 选项 | 效果 |
| --- | --- |
| **Automatic (DPI)** | 随显示器 DPI、窗口大小和全屏状态自动缩放 |
| **Automatic + 25%** | 在自动缩放基础上放大 25% |
| **Automatic + 50%** | 在自动缩放基础上放大 50% |

设置即时生效，无需重启播放器。

## 插件与其他播放器

首次启动时，插件自动安装到当前用户的配置目录。升级后，未经修改的内置插件会自动更新，替换前保留备份；自定义修改不会被覆盖。菜单仅显示兼容当前系统的插件。

| 插件 | 平台 | 用途 |
| --- | --- | --- |
| Nirvana / NVA Protocol | macOS、Linux、Windows | 哔哩哔哩投屏协议 |
| IINA | macOS | 使用外部 IINA 播放器 |
| Bolan IINA | macOS | 支持请求头的 IINA 扩展 |
| Live | macOS、Linux、Windows | 直播源播放器 |
| WebBrowser | macOS、Linux、Windows | 在浏览器中打开媒体 |
| PotPlayer | Windows | 使用外部 PotPlayer |
| PotPlayer Advanced | Windows | PotPlayer 扩展控制 |
| PI-FM-RDS | Raspberry Pi / Linux | FM 音频输出 |

使用 IINA、PotPlayer 等插件前，需另外安装对应应用。外部播放器的界面和字幕行为由其自身管理。插件源码和版本见 [Macast-plugins](Macast-plugins/)。

## 常见问题

### 手机搜不到设备？

确认两台设备处于同一局域网；检查 macOS 是否允许 Macast 访问局域网，以及防火墙是否允许传入连接。访客网络、无线客户端隔离和部分 VPN 可能阻止发现设备。B 站投屏还需确认选中了 **NVA Protocol**。

### 选了设备，却没有打开播放器？

确认播放器选中 **MPV Renderer**。如果使用 IINA 等插件，检查对应播放器是否已经安装。重新选择视频发起投屏，并检查 **Open Config Directory** 中的日志。

### 1080P 怎么选不了？

先确认手机端该视频和账号具备相应清晰度权限。实际可选画质受接口返回结果影响；网络错误、媒体地址失效或客户端协议变化也可能影响播放。

### 切换视频为什么要等一会儿？

切换时播放器会清除旧画面并加载新视频。清晰度与播放地址获取、网络传输、解码准备和缓冲均需要时间；无法保证零等待。若等待异常，可通过配置目录中的 `latency.log` 查看各阶段耗时。

### 如何修改配置或反馈问题

菜单 **Open Config Directory** 可打开：

```text
~/Library/Application Support/Macast
```

其中 `renderer/` 保存播放器插件，`protocol/` 保存协议插件。反馈问题时，请提供 macOS 版本、Mac 芯片、所用协议和播放器、手机客户端版本、复现步骤及相关日志。分享日志前移除账号信息、令牌和完整媒体地址。请说明使用的是本衍生版本，便于与上游版本区分。

## 使用前知道这些就好

- 当前安装包为 macOS arm64；插件包含其他平台支持，不代表 DMG 能在其他平台运行。
- 多段 `durl` 视频暂不支持；DRM、特殊音轨及部分客户端协议组合可能无法播放。
- 新版客户端或服务接口变化可能影响投屏。账号和内容访问权限由媒体服务决定。

## 从源码构建

参阅 [BUILDING.md](BUILDING.md)。保留 `Macast/` 和 `Macast-plugins/` 插件目录，使用原生架构构建。DMG 中附有双语说明、许可证及 `Macast-Local-Source.tar.gz` 本地修改源码快照。

## 开源项目与致谢

本项目使用或衍生自以下开源项目，原作者署名和许可予以保留：

| 项目 | 在本项目中的用途 | 许可 |
| --- | --- | --- |
| [Macast — xfangfang](https://github.com/xfangfang/Macast) | 菜单栏应用、DLNA 与播放器框架，本项目的基础 | [GPL v3](LICENSE) |
| [Macast-plugins — xfangfang 及贡献者](https://github.com/xfangfang/Macast-plugins) | NVA、IINA 等插件基础 | [MIT](Macast-plugins/LICENSE) |
| [mpv](https://github.com/mpv-player/mpv) | 内置视频播放器 | 按构建配置适用 GPL/LGPL，见随包原始许可 |
| [ModernZ — Samillion](https://github.com/Samillion/ModernZ) | 播放器控制界面，本项目增加 DPI 缩放与独立弹幕按钮 | [LGPL v2.1](mpv_ui/LICENSE.ModernZ) |
| [FFmpeg](https://ffmpeg.org/) / [libass](https://github.com/libass/libass) | 媒体处理与 ASS 字幕、弹幕渲染 | FFmpeg 按构建配置适用 GPL/LGPL；libass 为 ISC |
| [Fluent System Icons — Microsoft](https://github.com/microsoft/fluentui-system-icons) | ModernZ 图标字体来源之一 | MIT |
| [Material Symbols — Google](https://github.com/google/material-design-icons) | ModernZ 图标字体来源之一 | Apache 2.0 |
| [Vue](https://github.com/vuejs/vue) / [Element UI](https://github.com/ElemeFE/element) / [Vue Resource](https://github.com/pagekit/vue-resource) | 高级设置页面、组件、英语语言包及请求处理 | MIT |
| [Python](https://www.python.org/) / [py2app](https://github.com/ronaldoussoren/py2app) | 应用运行时与 macOS 打包 | 见各项目原始许可 |
| [rumps](https://github.com/jaredks/rumps) / [PyObjC](https://github.com/ronaldoussoren/pyobjc) | 菜单栏与 Cocoa 集成 | 见随包原始许可 |
| [CherryPy](https://github.com/cherrypy/cherrypy) / [cheroot](https://github.com/cherrypy/cheroot) | 本地 HTTP 服务 | 见随包原始许可 |
| [Requests](https://github.com/psf/requests) / [lxml](https://github.com/lxml/lxml) / [netifaces](https://github.com/al45tair/netifaces) / [pyperclip](https://github.com/asweigart/pyperclip) | 网络请求、XML、网卡枚举与剪贴板支持 | 见随包原始许可 |

ModernZ 继承了 mpv OSC、maoiscat/mpv-osc-modern、cyl0/ModernX 和 dexeonify/ModernX 的工作，完整上游致谢见 [ModernZ 原始文档](mpv_ui/ModernZ-upstream-README.md)。

Macast 和插件的基础版本见 [SOURCE-REVISIONS.json](SOURCE-REVISIONS.json)；ModernZ 固定版本与修改记录见 [UPSTREAM.json](mpv_ui/UPSTREAM.json)。完整许可、原生动态库与 Python 依赖记录见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 及安装包 `Documentation/licenses/INVENTORY.json`。各组件继续遵守各自许可证。
