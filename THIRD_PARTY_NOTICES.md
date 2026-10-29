# Licenses and attribution / 许可与署名

This is a modified distribution of Macast, not a new license grant for every bundled component. Original copyright and license notices are preserved. The original license texts govern; the Chinese descriptions below are explanatory and are not replacement license translations.

本项目是 Macast 的修改发行版，各组件继续遵循原有许可，不统一改为某一许可证。原始版权声明与许可正文予以保留；本页中文仅作说明，不替代许可原文。

| Component / 组件 | Source and license / 来源与许可 | Local record / 本地记录 |
| --- | --- | --- |
| Macast | [xfangfang/Macast](https://github.com/xfangfang/Macast), GNU GPL v3 | [Original license](LICENSE), [base revision](SOURCE-REVISIONS.json) |
| Macast plugins | [xfangfang/Macast-plugins](https://github.com/xfangfang/Macast-plugins), MIT | [Original license](Macast-plugins/LICENSE); individual source headers and plugin READMEs retain contributor credits |
| ModernZ 0.3.3 | [Samillion/ModernZ](https://github.com/Samillion/ModernZ), LGPL v2.1; derived from mpv OSC and ModernX forks | [License](mpv_ui/LICENSE.ModernZ), [upstream credits](mpv_ui/ModernZ-upstream-README.md), [revision and changes](mpv_ui/UPSTREAM.json) |
| ModernZ icon font | Microsoft Fluent System Icons (MIT); Google Material Symbols (Apache 2.0), credited by ModernZ | Original icon license texts under `Macast/licenses/icons/` |
| MPV 0.41.0 and linked native libraries | Homebrew builds; each project retains its own terms, including GPL/LGPL and permissive licenses | Generated `licenses/native/` contains original notices, formulae, receipts and dependency inventory |
| Python and Python packages | Python Software Foundation license and individual package licenses | Generated `licenses/python/` contains packaged distribution metadata and original license files |
| Vue 2.6.14 | [vuejs/vue](https://github.com/vuejs/vue/tree/v2.6.14), MIT | [License](licenses/frontend/Vue-2.6.14.txt) |
| Element UI 2.15.7, English locale and icon assets | [ElemeFE/element](https://github.com/ElemeFE/element/tree/v2.15.7), MIT | [License](licenses/frontend/Element-UI-2.15.7.txt) |
| Vue Resource 1.5.3 | [pagekit/vue-resource](https://github.com/pagekit/vue-resource/tree/1.5.3), MIT | [License](licenses/frontend/Vue-Resource-1.5.3.txt) |

## Packaged records / 安装包中的记录

`Macast.app/Contents/Resources/distribution/` and the DMG's `Documentation/` folder contain these notices, bilingual READMEs, and the generated license inventory. The DMG also contains `Macast-Local-Source.tar.gz`: local application/plugin source, UI assets, build scripts and provenance, excluding user configuration, logs, caches, and build outputs. It does not contain complete third-party dependency source trees. Native dependency records include the Homebrew formulae and upstream source locations; Python records include package metadata and source/project links.

`Macast.app/Contents/Resources/distribution/` 和 DMG 中的 `Documentation/` 保存本页、双语说明及构建时生成的许可清单。DMG 中的 `Macast-Local-Source.tar.gz` 保存本地应用、插件、UI 资源、构建脚本和来源记录，不包含用户配置、日志、缓存与编译产物；它也不包含第三方依赖的完整源码。原生依赖记录附有 Homebrew 配方和上游源码位置；Python 依赖记录附有包元数据及项目链接。

The local changes cover macOS startup/network handling, MPV command compatibility, bundled plugin management, Bilibili playback and switching, English UI, DPI scaling, and independent danmaku controls. Existing authorship is retained. Before publishing binaries to others, accompany them with the corresponding source and build materials required by each applicable license; this inventory is not a claim that upstream links alone fulfill source distribution requirements.

本地修改包括 macOS 启动与网络处理、MPV 命令兼容、内置插件管理、B 站播放与切换、英语界面、DPI 缩放和独立弹幕控件。原作者署名保留。向他人公开分发二进制时，仍应按各许可证附带所需的对应源码和构建材料；本清单不表示仅提供上游链接就已满足源码分发要求。
