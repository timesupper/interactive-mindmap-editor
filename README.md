# Interactive Mindmap Editor（双兼容 Skill / Codex 插件）

将思维导图能力做成 **Claude Skill 与 Codex 插件双兼容** 的目录，用于创建、修复、导入和导出可编辑的 HTML/XMind 思维导图。

## 功能

- 将文本、Markdown、文章、笔记、章节内容整理成思维导图层级结构（JSON）。
- 生成可编辑的独立 HTML 思维导图（支持双击编辑、右键增删、批注、折叠、拖拽、全屏展示）。
- 将 JSON 或文本导出为 XMind 可打开的 `.xmind` 文件。
- 识别现代 `.xmind` 文件并转换回思维导图 JSON。
- 修复 HTML 思维导图的节点编辑、折叠、布局、重叠和层级操作问题。

## 目录结构（双兼容）

```text
claude-skill-interactive-mindmap/
├── .codex-plugin/
│   └── plugin.json                          # Codex 插件清单
├── SKILL.md                                 # Claude 技能定义（根目录，供 Claude 读取）
├── README.md                                # 本说明
├── install-codex.ps1                        # Codex 一键安装脚本（PowerShell）
└── skills/
    └── interactive-mindmap-editor/
        ├── SKILL.md                         # Codex 技能定义（供 Codex 读取）
        ├── agents/
        │   └── openai.yaml                  # Codex agent 接口描述
        └── scripts/
            ├── text_to_mindmap_data.py      # 文本/Markdown → 思维导图 JSON
            ├── mindmap_data_to_xmind.py     # JSON → .xmind
            ├── text_to_xmind.py             # 文本/Markdown → .xmind
            └── xmind_to_mindmap_data.py     # .xmind → JSON
```

## 在 Claude 中使用

将 `claude-skill-interactive-mindmap` 文件夹放到 Claude 能访问的项目目录中。当你的请求涉及"生成思维导图""把这段文字做成思维导图""导出 XMind""修复思维导图 HTML"等任务时，Claude 会自动读取根目录 `SKILL.md` 并遵循其中的工作流。也可在对话中说"使用 interactive-mindmap-editor 技能"手动加载。

## 在 Codex 中使用

在 Windows 上以管理员身份运行安装脚本：

```powershell
cd claude-skill-interactive-mindmap
.\install-codex.ps1
```

脚本会自动：
1. 复制插件到 `$HOME\plugins\interactive-mindmap-editor`
2. 写入 personal marketplace（UTF-8 无 BOM）
3. 注册并安装到 Codex：`codex plugin marketplace add "$HOME"` + `codex plugin add interactive-mindmap-editor@personal`

验证：

```powershell
codex plugin list
# 应看到 interactive-mindmap-editor@personal
```

## 脚本直接调用

Python 脚本与平台无关，可直接在命令行使用（脚本位于 `skills/interactive-mindmap-editor/scripts/`）：

```bash
# 文本 → 思维导图 JSON
python skills/interactive-mindmap-editor/scripts/text_to_mindmap_data.py input.md -o mindmap-data.json --root-title "主题"

# JSON → XMind
python skills/interactive-mindmap-editor/scripts/mindmap_data_to_xmind.py mindmap-data.json -o output.xmind

# 文本 → XMind
python skills/interactive-mindmap-editor/scripts/text_to_xmind.py input.md -o output.xmind --root-title "主题"

# XMind → JSON
python skills/interactive-mindmap-editor/scripts/xmind_to_mindmap_data.py input.xmind -o mindmap-data.json
```

## 双兼容说明

同一份 `scripts/` 被 Claude 和 Codex 共享，避免重复维护：

- **Claude** 读取根目录 `SKILL.md`（frontmatter 含中文触发词），脚本路径指向 `skills/interactive-mindmap-editor/scripts/`。
- **Codex** 读取 `.codex-plugin/plugin.json` 定位技能目录，再读 `skills/interactive-mindmap-editor/SKILL.md`，脚本路径相对该目录为 `scripts/`。

两个 SKILL.md 的差异：Claude 版 frontmatter 用 `name` + `description`（含中文触发词），并新增「Notes（批注）」章节；Codex 版保留原始 Codex 风格 frontmatter 与工作流说明。

## 参考实现

项目文件夹中的 `00_序言/序言思维导图.html` 是一个完整的可编辑 HTML 思维导图参考实现，包含本技能描述的全部交互能力。
