# Interactive Mindmap Editor（四环境兼容 Skill / 插件）

将思维导图能力做成 **Claude Desktop、Claude Code（CLI）、Codex Desktop、Codex CLI 四环境兼容** 的工具包，用于创建、修复、导入和导出可编辑的 HTML/XMind/Markdown 思维导图，并提供基于 Markdown 的 `Markmap` 兼容互通能力。

## 功能

- 将文本、Markdown、文章、笔记、章节内容整理成思维导图层级结构（JSON）。
- 生成可编辑的独立 HTML 思维导图（支持双击编辑、右键增删、批注、折叠、拖拽、全屏展示）。
- Markdown 提纲与思维导图 JSON 双向转换。
- Markmap Markdown 与思维导图 JSON 双向转换。
- 将 JSON 或文本导出为 XMind 可打开的 `.xmind` 文件。
- 识别现代 `.xmind` 文件并转换回思维导图 JSON。
- 修复 HTML 思维导图的节点编辑、折叠、布局、重叠和层级操作问题。

## 目录结构

```text
claude-skill-interactive-mindmap/
├── .codex-plugin/
│   └── plugin.json                          # Codex 插件清单
├── SKILL.md                                 # Claude Skill 入口（Claude Code / Claude Desktop）
├── CLAUDE.md                                # Claude Code 项目记忆入口（仓库内工作时读取）
├── README.md                                # 本说明
├── USAGE.md                                 # 详细安装与使用说明
├── CHANGELOG.md                             # 版本记录
├── SKILL_CONSTRAINTS.md                     # Skill 功能、性能和验收约束
├── install-codex.ps1                        # Codex 一键安装脚本（PowerShell）
├── SKILL_CONSTRAINTS.md                     # Skill 功能、性能和验收约束
├── templates/
│   └── interactive-mindmap.html              # 可生成的离线 Markmap HTML 模板
├── runtime/
│   ├── markmap-preview.js                    # Markmap 渲染与回退运行时
│   ├── markmap-preview.css                   # Markmap 预览样式
│   └── markmap-assets.js                     # 固定版本的内嵌离线依赖
└── skills/
    └── interactive-mindmap-editor/
        ├── SKILL.md                         # Codex 技能定义（供 Codex 读取）
        ├── agents/
        │   └── openai.yaml                  # Codex agent 接口描述
        └── scripts/
            ├── text_to_mindmap_data.py      # 文本/Markdown → 思维导图 JSON
            ├── markdown_to_mindmap_data.py  # Markdown 提纲 → 思维导图 JSON
            ├── mindmap_data_to_markdown.py  # 思维导图 JSON → Markdown 提纲
            ├── markmap_markdown_to_mindmap_data.py # Markmap Markdown → 思维导图 JSON
            ├── mindmap_data_to_markmap_markdown.py # 思维导图 JSON → Markmap Markdown
            ├── render_markmap_html.py       # JSON → 独立离线 Markmap HTML
            ├── mindmap_data_to_xmind.py     # JSON → .xmind
            ├── text_to_xmind.py             # 文本/Markdown → .xmind
            └── xmind_to_mindmap_data.py     # .xmind → JSON
```

各环境入口：

- **Claude Code（CLI）**：把整个文件夹放到 `~/.claude/skills/`（个人级）或 `<项目>/.claude/skills/`（项目级），读取根目录 `SKILL.md`。
- **Claude Desktop（桌面版）**：Settings → Features → Skills，上传本文件夹的 `.zip`。
- **Codex（CLI 与桌面版）**：读取 `.codex-plugin/plugin.json` 定位技能，再读 `skills/interactive-mindmap-editor/SKILL.md`。桌面版与 CLI 共享 `~/.codex/` 配置，装一次两边可用。

## 快速安装

### Claude Code（CLI）

```powershell
# 个人级（所有项目可用）
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git "$HOME\.claude\skills\interactive-mindmap-editor"

# 或项目级（仅当前项目）
cd "E:\路径\to\你的项目"
New-Item -ItemType Directory -Force ".\.claude\skills" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git ".\.claude\skills\interactive-mindmap-editor"
```

安装后新开 Claude Code 会话即可，请求"生成思维导图"等任务会自动匹配。

### Claude Desktop（桌面版）

将整个 `claude-skill-interactive-mindmap` 文件夹打包为 `.zip`，在 Claude 桌面版 **设置 → 功能 → 技能** 中上传。桌面版脚本运行在受限沙箱，涉及 Python 转换的操作建议在 CLI 完成。

### Codex（CLI 与桌面版）

```powershell
New-Item -ItemType Directory -Force "$HOME\plugins" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git "$HOME\plugins\interactive-mindmap-editor"
cd "$HOME\plugins\interactive-mindmap-editor"
.\install-codex.ps1
```

如果目录已经存在，不要再次执行 `git clone`。直接更新并安装：

```powershell
cd "$HOME\plugins\interactive-mindmap-editor"
git pull origin master
.\install-codex.ps1
```

`install-codex.ps1` 使用 ASCII 注释和提示，兼容 Windows PowerShell 5.1 与 PowerShell 7。PowerShell 5.1 若遇到执行策略限制，可在当前窗口执行 `Set-ExecutionPolicy -Scope Process Bypass` 后重试。

验证：

```powershell
codex plugin list
# 应看到 interactive-mindmap-editor@personal
```

## 脚本直接调用

Python 脚本与平台无关，可直接在命令行使用（位于 `skills/interactive-mindmap-editor/scripts/`）：

```bash
python skills/interactive-mindmap-editor/scripts/text_to_mindmap_data.py input.md -o mindmap-data.json --root-title "主题"
python skills/interactive-mindmap-editor/scripts/mindmap_data_to_xmind.py mindmap-data.json -o output.xmind
python skills/interactive-mindmap-editor/scripts/xmind_to_mindmap_data.py input.xmind -o mindmap-data.json
python skills/interactive-mindmap-editor/scripts/mindmap_data_to_markmap_markdown.py mindmap-data.json -o markmap.md
python skills/interactive-mindmap-editor/scripts/markmap_markdown_to_mindmap_data.py markmap.md -o mindmap-data.json
```

## Markmap 集成策略

- 当前交互式 HTML 编辑器仍然是主编辑器。
- `Markmap` 作为 Markdown 提纲的快速预览和互通层使用，不替代现有编辑、拖拽、自由标题、折叠持久化和 XMind 能力。
- 当前仓库已完成第一阶段：补齐 `mindmap JSON <-> Markmap Markdown` 的转换入口。
- 当前仓库已提供可复用的 HTML Markmap 运行时、离线依赖资产和 HTML 模板：优先使用内嵌渲染引擎，失败时回退本地树形预览。
- `render_markmap_html.py` 可将思维导图 JSON 生成独立、可双击打开的 Markmap HTML。
- 规划文档见 [docs/markmap-plan.md](docs/markmap-plan.md)。

## 双兼容说明

功能边界、性能要求和执行前后检查清单见 [SKILL_CONSTRAINTS.md](SKILL_CONSTRAINTS.md)。

同一份 `scripts/` 被 Claude 和 Codex 共享，避免重复维护：

- **Claude Code** 读取根目录 `SKILL.md`（frontmatter 含中英文触发词），脚本路径使用 `${CLAUDE_SKILL_DIR}/scripts/` 定位，任何安装位置都可靠。
- **Claude Desktop** 上传同一份 `SKILL.md` 与 `scripts/`，但运行在沙箱中。
- **Codex** 读取 `.codex-plugin/plugin.json` 定位技能目录，再读 `skills/interactive-mindmap-editor/SKILL.md`，脚本路径相对该目录为 `scripts/`。

两个 SKILL.md 的差异：Claude 版 frontmatter 用 `name` + `description`（含中英文触发词），脚本路径用 `${CLAUDE_SKILL_DIR}`；Codex 版保留 Codex 风格 frontmatter 与相对路径 `scripts/`。

## 最新 HTML 行为

生成或修复独立 HTML 时，保留 `全部自动编号`、`重编全部编号`、`取消全部编号` 三个全局右键菜单项，并持久化编号启用状态。编号开启后，新增、删除、排序、改挂父节点、自由标题分离以及 JSON/Markdown 导入后自动重编。Markmap 预览显示相同编号，但内部使用标准 `-` Markdown 列表；初始化前校验 SVG 尺寸，关闭或重建时清理异步任务，避免 Chrome/Edge 的 `translate(NaN,NaN)` 错误。

## 详细文档

- [USAGE.md](USAGE.md)：四个环境的详细安装、验证、更新与常见问题。
- [CHANGELOG.md](CHANGELOG.md)：版本迭代记录。
- [docs/markmap-plan.md](docs/markmap-plan.md)：Markmap 分阶段集成方案。

## 参考实现

项目文件夹中的 `00_序言/序言思维导图.html` 是一个完整的可编辑 HTML 思维导图参考实现，包含本技能描述的全部交互能力。


