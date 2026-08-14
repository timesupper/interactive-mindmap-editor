# Interactive Mindmap Editor 使用说明

`interactive-mindmap-editor` 是一个 **Claude Desktop / Claude Code（CLI）/ Codex Desktop / Codex CLI 四环境兼容** 的工具包，用于创建、修复、导入和导出可编辑的 HTML、Markdown、XMind 思维导图，并提供 `Markmap` 兼容互通能力。

## 功能

- 将文本、Markdown、文章、笔记、章节内容整理成思维导图层级结构（JSON）。
- 生成可编辑的独立 HTML 思维导图（支持双击编辑、右键增删、批注、折叠、拖拽、全屏展示）。
- 支持 Markdown 提纲与思维导图 JSON 双向转换。
- 支持 Markmap Markdown 与思维导图 JSON 双向转换。
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
├── README.md                                # 总览
├── USAGE.md                                 # 本说明
├── CHANGELOG.md                             # 版本记录
├── SKILL_CONSTRAINTS.md                     # Skill 功能、性能和验收约束
├── install-codex.ps1                        # Codex 一键安装脚本（PowerShell）
├── SKILL_CONSTRAINTS.md                     # Skill 功能、性能和验收约束
├── templates/
│   └── interactive-mindmap.html              # 独立 Markmap HTML 模板
├── runtime/
│   ├── markmap-preview.js                    # Markmap 渲染和回退运行时
│   ├── markmap-preview.css                   # Markmap 预览样式
│   └── markmap-assets.js                     # 离线依赖资产
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

## 安装到 Claude Code（CLI）

### 方式一：个人级安装（所有项目可用）

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git "$HOME\.claude\skills\interactive-mindmap-editor"
```

> 注意：Claude Code 要求技能文件夹名称与 `SKILL.md` 的 `name` 字段一致，即 `interactive-mindmap-editor`。安装后需新开一个 Claude Code 会话，技能元数据在启动时加载。`/skills` 可列出已加载技能。

### 方式二：项目级安装（仅当前项目可用）

```powershell
cd "E:\路径\to\你的项目"
New-Item -ItemType Directory -Force ".\.claude\skills" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git ".\.claude\skills\interactive-mindmap-editor"
```

### 更新 Claude 技能

```powershell
cd "$HOME\.claude\skills\interactive-mindmap-editor"
git pull
```

## 安装到 Claude Desktop（桌面版）

Claude 桌面版 **不读取本地技能文件夹**，需要通过应用内设置上传技能的 `.zip` 压缩包：

1. 将 `claude-skill-interactive-mindmap` 整个文件夹打包为 `.zip`（压缩包内第一层就是 `SKILL.md` 所在位置）。
2. 打开 Claude 桌面版 → **设置（Settings）→ 功能（Features）→ 技能（Skills）**。
3. 点击 **添加技能（Add Skill）**，选择该 `.zip` 文件上传。

注意：桌面版技能运行在受限沙箱中，脚本（Python 转换）可能无法安装依赖或访问本地 Python。最稳妥的做法是让桌面版只做**文本 → 思维导图 JSON 或 HTML 生成**，涉及 Python 脚本转换时建议在 Claude Code / Codex CLI 中完成。

## 安装到 Codex（CLI 与桌面版共用）

Codex 桌面版与 CLI 共享同一套 `~/.codex/` 配置，因此安装一次两边都可用。

### 方式一：一键安装脚本

```powershell
cd claude-skill-interactive-mindmap
.\install-codex.ps1
```

脚本会自动：
1. 复制插件到 `$HOME\plugins\interactive-mindmap-editor`
2. 写入 personal marketplace（UTF-8 无 BOM）
3. 注册并安装到 Codex：`codex plugin marketplace add "$HOME"` + `codex plugin add interactive-mindmap-editor@personal`

### 方式二：从 GitHub 安装

```powershell
New-Item -ItemType Directory -Force "$HOME\plugins" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git "$HOME\plugins\interactive-mindmap-editor"
cd "$HOME\plugins\interactive-mindmap-editor"
.\install-codex.ps1
```

如果 `$HOME\plugins\interactive-mindmap-editor` 已经存在，重复执行 `git clone` 会出现 `destination path already exists`。此时直接更新：

```powershell
cd "$HOME\plugins\interactive-mindmap-editor"
git pull origin master
.\install-codex.ps1
```

安装脚本兼容 Windows PowerShell 5.1 和 PowerShell 7，并使用 ASCII 提示文本避免旧版 PowerShell 按系统编码读取脚本时出现字符串终止符错误。

### 方式三：手动安装（脚本不可用时）

如果安装脚本无法运行（如 PowerShell 执行策略限制），可手动创建 personal marketplace：

```powershell
New-Item -ItemType Directory -Force "$HOME\plugins" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git "$HOME\plugins\interactive-mindmap-editor"

New-Item -ItemType Directory -Force "$HOME\.agents\plugins" | Out-Null
$marketplacePath = "$HOME\.agents\plugins\marketplace.json"

$marketplace = [ordered]@{
  name = "personal"
  interface = [ordered]@{ displayName = "Personal" }
  plugins = @(
    [ordered]@{
      name = "interactive-mindmap-editor"
      source = [ordered]@{
        source = "local"
        path = "./plugins/interactive-mindmap-editor"
      }
      policy = [ordered]@{
        installation = "AVAILABLE"
        authentication = "ON_INSTALL"
      }
      category = "Productivity"
    }
  )
}

$json = $marketplace | ConvertTo-Json -Depth 10
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($marketplacePath, $json, $utf8NoBom)

codex plugin marketplace add "$HOME"
codex plugin add interactive-mindmap-editor@personal
```

注意：`marketplace.json` 中 `path: "./plugins/interactive-mindmap-editor"` 是相对 `codex plugin marketplace add` 注册的根目录（这里是 `$HOME`）解析的，因此指向 `$HOME\plugins\interactive-mindmap-editor`，与克隆位置一致。

### 验证

```powershell
codex plugin list
# 应看到 interactive-mindmap-editor@personal
```

安装后新开一个 Codex 会话（CLI 或桌面版均可），插件技能即可用。可用 `@interactive-mindmap-editor` 显式调用。

也可以新开 Codex 或 Claude 任务后输入类似请求测试：

```text
把下面这段文本生成可编辑 HTML 思维导图
```

```text
修复这个 HTML 思维导图的双击编辑和节点折叠问题
```

```text
生成一个带全屏展示按钮的可编辑 HTML 思维导图
```

生成的 HTML 应包含"全屏展示"按键。点击后，页面内容进入全屏并铺满显示屏；鼠标移动到页面顶部时，会出现 `X` 退出按键，点击后退出全屏模式。

生成的 HTML 中，工具栏的"展开"和"折叠"按键应采用分层行为：

- 点击"展开"：展开当前可见节点的下一层。
- 点击"折叠"：折叠当前最深可见的一层。
- 长按"展开"：全部展开。
- 长按"折叠"：全部折叠。

生成的 HTML 如果包含较多工具按钮，应采用紧凑工具菜单：

- 圆形菜单按钮放在右下角缩放 `+` 按钮之上。
- 点击菜单按钮展开或折叠次要工具按钮。
- 次要工具按钮包括 `展开`、`折叠`、`导入 Markdown`、`导出 Markdown`、`XMind`、`全屏展示`、`适配`。
- 缩放 `+`、缩放 `-`、重置视图应保持常驻显示。
- 点击画布空白区域后，菜单应自动收起。

## 脚本直接调用（不依赖任何 Agent）

Python 脚本与平台无关，可直接在命令行使用：

```bash
# 文本/Markdown → 思维导图 JSON
python skills/interactive-mindmap-editor/scripts/text_to_mindmap_data.py input.md -o mindmap-data.json --root-title "主题"

# Markdown 提纲 → 思维导图 JSON
python skills/interactive-mindmap-editor/scripts/markdown_to_mindmap_data.py input.md -o mindmap-data.json --root-title "主题"

# 思维导图 JSON → Markdown 提纲
python skills/interactive-mindmap-editor/scripts/mindmap_data_to_markdown.py mindmap-data.json -o outline.md

# 思维导图 JSON → Markmap Markdown
python skills/interactive-mindmap-editor/scripts/mindmap_data_to_markmap_markdown.py mindmap-data.json -o markmap.md

# Markmap Markdown → 思维导图 JSON
python skills/interactive-mindmap-editor/scripts/markmap_markdown_to_mindmap_data.py markmap.md -o mindmap-data.json

# JSON → XMind
python skills/interactive-mindmap-editor/scripts/mindmap_data_to_xmind.py mindmap-data.json -o output.xmind

# 文本 → XMind
python skills/interactive-mindmap-editor/scripts/text_to_xmind.py input.md -o output.xmind --root-title "主题"

# XMind → JSON
python skills/interactive-mindmap-editor/scripts/xmind_to_mindmap_data.py input.xmind -o mindmap-data.json

# Markmap Markdown ↔ 思维导图 JSON
python skills/interactive-mindmap-editor/scripts/markmap_markdown_to_mindmap_data.py markmap.md -o mindmap-data.json
python skills/interactive-mindmap-editor/scripts/mindmap_data_to_markmap_markdown.py mindmap-data.json -o markmap.md

# 生成可双击打开的离线 Markmap HTML
python skills/interactive-mindmap-editor/scripts/render_markmap_html.py mindmap-data.json \
  --template templates/interactive-mindmap.html \
  --runtime runtime/markmap-preview.js \
  --assets runtime/markmap-assets.js \
  --styles runtime/markmap-preview.css \
  -o output/markmap.html
```

## 更新插件

Codex 更新：

```powershell
cd "$HOME\plugins\interactive-mindmap-editor"
git pull
.\install-codex.ps1
```

Claude Code 个人技能更新：

```powershell
cd "$HOME\.claude\skills\interactive-mindmap-editor"
git pull
```

更新后建议新开一个任务让技能重新加载。

## Markmap 使用方式

`Markmap` 在本插件中的定位是 Markdown 互通与预览层，不是主编辑器。

推荐流程：

1. 用 Markdown 提纲或章节文本生成思维导图 JSON。
2. 在交互式 HTML 中完成编辑、拖拽、折叠和自由标题处理。
3. 需要 `Markmap` 预览或共享时，将当前 JSON 导出为 `markmap.md`。
4. 如果已有 `Markmap`/Markdown 提纲文件，可反向导入为当前插件的思维导图 JSON。

HTML 预览模式建议：

- 优先使用 HTML 内嵌的离线 `markmap` 渲染引擎展示 Markdown。
- 如果内嵌依赖缺失或加载失败，则自动回退为本地树形预览。
- 预览面板可采用悬停菜单：将 `刷新`、`导出 Markdown`、`全屏/退出全屏`、`适应`、`放大`、`缩小`、`折叠/展开` 收纳到单一菜单按钮下。
- `折叠/展开` 可采用三级交互：单击折叠一级，双击恢复一级，长按在全部折叠和全部展开之间切换。`Markmap` 预览重新打开时应恢复上次退出时的预览页状态与折叠层级。

限制说明：

- `Markmap` 转换默认保留层级、标题、副标题、批注文本。
- `Markmap` 不负责恢复自由标题坐标、折叠状态、缩放位置和其他编辑器专属状态。
- `freeNodes` 会作为 `## 自由标题` 段落导出，导回时按普通层级节点处理。

设计方案文档见 [docs/markmap-plan.md](docs/markmap-plan.md)。

## 项目迁移方式

- **Codex**：一台机器装一次，所有 Codex 任务都能用。换设备时在新设备上执行安装命令。若项目需要锁定版本，可把本仓库 clone 进项目，并让 Codex 直接使用该本地路径下的脚本。
- **Claude（个人级）**：`~/.claude/skills/` 安装一次，所有项目可用。
- **Claude（项目级）**：`<项目>/.claude/skills/` 内携带一份固定版本，随项目走。
- **思维导图产物**：`.html`、`.json`、`.md`、`.xmind` 文件是项目产物，随项目目录移动即可，插件/Skill 是工具。

## 常见问题

**Claude Code 里脚本找不到？**
技能引用脚本统一使用 `${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/...`，该变量会展开为技能所在目录，无论技能装在个人级还是项目级。不要用 `scripts/...` 这种相对路径（工作目录是项目根，不是技能目录）。

**Codex 报 `plugin was not found in marketplace personal`？**
检查 `$HOME\.agents\plugins\marketplace.json` 是否为 UTF-8 无 BOM，并确认 `codex plugin marketplace list` 里有 `personal`。

**Windows 上 Codex 装了插件但运行时发现不了？**
Codex CLI 0.130 曾有本地插件发现 bug（GitHub issue #26037）。请升级到 0.137+，或改用项目级 `.agents/plugins/marketplace.json` + 仓库内 `plugins/` 目录的方式。

**桌面版与 CLI 技能不互通？**
Claude 桌面版与 Claude Code CLI 的技能互不同步：桌面版通过上传 `.zip` 安装，CLI 通过 `~/.claude/skills/` 安装，两者相互独立。Codex 桌面版与 CLI 则共享 `~/.codex/`，装一次两边可用。

## 全局编号与 Markmap 兼容

在根节点、任意节点或画布空白处右键，可使用 `全部自动编号`、`重编全部编号`、`取消全部编号`。编号状态会保存到 HTML；编号开启后，新增、删除、拖动换序、改变父子关系、转为自由标题以及导入 JSON/Markdown 都会自动重编。Markmap 使用标准 Markdown 无序列表作为内部输入；关闭预览时清理动画和异步任务，避免 Edge 的 `translate(NaN,NaN)` 错误。

## 参考实现

项目文件夹中的 `00_序言/序言思维导图.html` 是一个完整的可编辑 HTML 思维导图参考实现，包含本技能描述的全部交互能力。


