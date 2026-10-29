# Build / 构建

[English README](README.md) · [中文说明](README_ZH.md)

Build natively on macOS with Xcode Command Line Tools. The GitHub repository includes the companion plugins in `Macast-plugins/`. A local two-folder checkout with the directories side by side also works. The current local package uses Python 3.12, MPV 0.41.0 and arm64. Intel output must be built separately on a compatible Intel environment.

在 macOS 原生终端构建，安装 Xcode Command Line Tools，GitHub 仓库已经包含 `Macast-plugins/` 子目录；本地将两个源码目录并排放置也可构建。当前安装包使用 Python 3.12、MPV 0.41.0 和 arm64；Intel 安装包需在兼容的 Intel 环境独立构建。

```sh
cd Macast-Overhauled
brew install python@3.12 mpv dylibbundler create-dmg gettext
"$(brew --prefix python@3.12)/bin/python3.12" -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/darwin.txt
python -m pip install 'setuptools<81' 'py2app>=0.28.8,<0.29'
export PATH="$(brew --prefix gettext)/bin:$PATH"
PYTHON=python bash tools/build_macos.sh
```

Move existing `build/` and `dist/` directories aside before rebuilding. The script generates bundled plugins, builds the App, bundles MPV and libraries, prepares distribution documentation/licenses and a local source archive, then signs and creates the DMG. Build logs and machine-local backups are not source inputs. `build-requirements.lock.txt` records the Python environment used locally; future Homebrew versions can change native dependency versions.

重新构建前先移走已有的 `build/` 和 `dist/`。脚本依次生成内置插件、构建 App、收集 MPV 和动态库、整理文档与许可及本地源码压缩包，再签名并生成 DMG。构建日志和本机备份不属于源码输入；`build-requirements.lock.txt` 记录本机构建的 Python 环境，未来 Homebrew 版本可能改变原生依赖版本。

`tools/prepare_distribution.py` can also refresh documentation and license records for an existing `dist/Macast.app`. Run it **before signing**. The final DMG is `Macast-MacOS-v<version>-<architecture>.dmg`. Local ad-hoc signing is used; Developer ID signing and notarization are separate release steps.

已有 App 可用 `tools/prepare_distribution.py` 更新文档与许可，必须在签名前执行。最终输出为 `Macast-MacOS-v<版本>-<架构>.dmg`。本地使用 ad-hoc 签名；Developer ID 签名和 Apple 公证属于独立发布步骤。

Playback validation is performed by the user. Optional existing regression checks can be run with `python -m pytest tests ../Macast-plugins/tests -q` after installing pytest; they do not verify actual phone casting.

实际播放由使用者验收。需要回归检查时，可安装 pytest 后运行 `python -m pytest tests ../Macast-plugins/tests -q`，该检查不能替代手机投屏测试。
