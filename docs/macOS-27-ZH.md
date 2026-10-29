# macOS 27 适配修订版

本分支修复了可由代码和协议测试确认的兼容性问题。**尚未在 macOS 27 实机上验收，也未提供已经构建好的 DMG。**

## 修改内容

- 应用包加入 `NSLocalNetworkUsageDescription`，关闭会干扰 Cocoa 事件循环的 argv emulation。
- 局域网授权期间组播加入失败时重试，授权后可以恢复设备发现。
- mpv 0.38 及以上使用新的 `loadfile` 参数位置；保留对旧 mpv 的支持。启动时探测版本，IPC 同时观察版本属性。
- 每个视频可以携带独立的 Referer、User-Agent、DASH 音轨选项，切换普通视频时不继承上一个视频的选项。
- Finder 启动时可以找到 Apple Silicon 和 Intel Homebrew 的 mpv。
- 构建流程分别使用原生 arm64 / x86_64，捆绑 mpv 的动态库，并生成按架构命名的 DMG。现代构建包最低系统版本设为 macOS 15；这不改变 Python 源码包的最低版本声明。

## 在 Mac 上构建

以下命令在本仓库目录运行，使用原生终端，不要通过 Rosetta 运行：

```sh
xcode-select --install  # 已安装命令行开发工具则跳过
brew install python@3.12 mpv dylibbundler create-dmg gettext
"$(brew --prefix python@3.12)/bin/python3.12" -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/darwin.txt
python -m pip install 'setuptools<81' 'py2app>=0.28.8,<0.29' pytest
export PATH="$(brew --prefix gettext)/bin:$PATH"
python -m pytest tests -q
PYTHON=python bash tools/build_macos.sh
```

输出为 `Macast-MacOS-v0.7-arm64.dmg` 或 `Macast-MacOS-v0.7-x86_64.dmg`，版本号以 `macast/.version` 为准。构建脚本需要干净的 build/dist 目录，已有目录时会停止并提示。Intel 构建用于支持 Intel 的 macOS 版本，并不表示 macOS 27 支持所有 Intel 机型。

应用进行本地 ad-hoc 签名，尚未 Apple 公证；正式分发还需要 Developer ID 签名、公证和票据装订。本地签名不能保证跨机器升级时稳定保留局域网授权身份。不要关闭 SIP 或全局禁用 Gatekeeper。

也可将代码推送到自己的 GitHub 仓库，从 Actions 手动运行 Build Macast。arm64 / x86_64 构建使用 macOS 15 runner；构建成功也不能代替 macOS 27 实机投屏测试。此交付没有触发远程构建或发布。

## 安装 B 站插件

1. 将配套 `Macast-plugins/nirvana/nirvana.py` 放入 Macast 配置目录下的 `protocol` 文件夹。可从菜单 Open Config Directory 打开目录。
2. 重启，协议选择 NVA Protocol，播放器先选择内置 MPV。
3. 将手机和 Mac 接入同一局域网，允许 Macast 的局域网访问；在系统防火墙中允许 Macast 的传入连接。
4. B 站投屏列表中选择“我的小电视”。

插件的 DASH 音轨选项需要配套的新版内置 MPV 播放器。IINA、PotPlayer 等第三方播放器没有随本次交付做完整适配验收。

## 验证记录（2026-10-22）

在 Windows / Python 3.12.14 环境下执行了两仓库的 26 项测试：覆盖旧版/新版 mpv 命令、版本事件、授权后组播重试、B 站可选响应字段、DASH 音轨与清晰度选择、第三方播放器启动保留、空地址保护、布尔弹幕开关、签名编码、分包/粘包、同文件描述符重连、心跳退出，以及 CherryPy/cheroot 真实 TCP 的 NVA 握手与连接转交。

Windows 测试仅替代未能编译安装的 netifaces 接口枚举模块；未模拟 CherryPy、cheroot、TCP socket 或 NVA 握手。没有验证真实网卡枚举、macOS 的组播与权限系统。使用 CherryPy 18.10.0 / cheroot 11.1.2。

另对 B 站匿名公开视频播放接口做了真实请求，得到 HTTP 200、业务码 0；通过修复后的插件解析出 720P 媒体地址，CDN 对单字节 Range 请求返回 HTTP 206。未使用个人账号，也未验证需要登录/会员/地域授权的视频。构建 shell 脚本通过语法检查，工作流通过 YAML 解析。macOS 构建脚本尚未运行。

## Mac 实机验收

- 从 Finder 启动应用，检查菜单栏图标、MPV 启动和本机架构。
- 首次允许局域网访问后，在手机中发现设备；拒绝后在系统设置中允许，再检查发现是否恢复。
- B 站普通视频能正常出声、拖动、暂停/恢复、切清晰度；弹幕可关闭。
- 播放直播、番剧、切换分 P，并在手机断网/恢复网络后重新连接。
- 切换到普通 DLNA 视频，检查没有残留的 B 站音轨和请求头。

多段 `durl` 视频暂时明确报错，避免只播放第一段。DASH Dolby/FLAC 特殊音轨、DRM、账号权限变化以及手机新版客户端未公开的协议变更不在已验证范围内。

## 参考

- Apple 局域网隐私说明：https://developer.apple.com/documentation/technotes/tn3179-understanding-local-network-privacy
- mpv loadfile 参数变化：https://mpv.io/manual/stable/#command-interface-loadfile
- py2app GUI argv emulation 注意事项：https://py2app.readthedocs.io/en/latest/options.html
