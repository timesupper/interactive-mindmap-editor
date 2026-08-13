# Interactive Mindmap Editor 使用说明

## 插件功能

`interactive-mindmap-editor` 是一个 Codex / Claude 双兼容工具包，用于创建、修复、导入和导出可编辑的 HTML、Markdown、XMind 思维导图。

主要能力：

- 将文本、Markdown、文章、笔记、章节内容整理成思维导图层级结构。
- 支持作为 Codex personal plugin 使用。
- 支持作为 Claude personal skill 或 project skill 使用。
- 支持直接调用 Python 脚本使用。
- 生成适用于交互式 HTML 思维导图的数据。
- 修复 HTML 思维导图的节点编辑、折叠、布局和层级操作问题。
- 支持标题/副标题两行编辑。
- 支持节点长文本按字符宽度换行。
- 支持各级节点继续新增、编辑、删除子节点。
- 修复点击标题误触发展开/折叠的问题，只在右侧箭头区域触发折叠。
- 修复编辑节点时遮挡其他节点的问题。
- 支持生成带“全屏展示”按键的 HTML，进入全屏后内容铺满屏幕，鼠标指向顶部时显示 `X` 退出按键。
- 支持在 HTML 页面中把次要工具按钮收纳到圆形菜单按钮中，减少右下角按钮占用空间。
- 支持工具栏展开/折叠分层操作：点击一次只展开或折叠一级，长按则全部展开或全部折叠。
- 支持 Markdown 提纲导入为思维导图 JSON，也支持将思维导图 JSON 导出为 Markdown 提纲。
- 支持生成带“导入 Markdown”和“导出 Markdown”按键的 HTML 页面。
- 支持将插件 JSON 或文本导出为 XMind 可打开的 `.xmind` 文件。
- 支持识别现代 `.xmind` 文件，并转换回插件可用的思维导图 JSON。

## 插件目录结构

```text
interactive-mindmap-editor/
├── .codex-plugin/
│   └── plugin.json
├── SKILL.md
├── CLAUDE.md
├── install-codex.ps1
├── skills/
│   └── interactive-mindmap-editor/
│       ├── SKILL.md
│       ├── agents/
│       │   └── openai.yaml
│       └── scripts/
│           ├── markdown_to_mindmap_data.py
│           ├── mindmap_data_to_markdown.py
│           ├── mindmap_data_to_xmind.py
│           ├── text_to_mindmap_data.py
│           ├── text_to_xmind.py
│           └── xmind_to_mindmap_data.py
├── README.md
├── CHANGELOG.md
└── USAGE.md
```

入口说明：

- Codex 使用 `.codex-plugin/plugin.json` 和 `skills/interactive-mindmap-editor/SKILL.md`。
- Claude Skill 使用根目录 `SKILL.md`。
- Claude Code 在本仓库内工作时还会读取 `CLAUDE.md`。
- Codex 和 Claude 共享同一套 `scripts/` 脚本，避免重复维护。

## 在 Codex 中安装

以下命令假设你要从 GitHub 安装到当前 Windows 用户的本地插件目录。

### 方式一：一键安装

```powershell
New-Item -ItemType Directory -Force "$HOME\plugins" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git "$HOME\plugins\interactive-mindmap-editor"
cd "$HOME\plugins\interactive-mindmap-editor"
.\install-codex.ps1
```

### 方式二：手动安装

如果不使用安装脚本，可以手动创建 personal marketplace。

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\plugins" | Out-Null
$marketplacePath = "$HOME\.agents\plugins\marketplace.json"

$marketplace = [ordered]@{
  name = "personal"
  interface = [ordered]@{
    displayName = "Personal"
  }
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
```

注意：`marketplace.json` 必须写成 UTF-8 无 BOM。不要用 `Set-Content -Encoding UTF8` 生成该文件，否则部分 Codex CLI 版本可能报：

```text
plugin `interactive-mindmap-editor` was not found in marketplace `personal`
```

或：

```text
invalid marketplace file: expected value at line 1 column 1
```

### 3. 注册 marketplace

```powershell
codex plugin marketplace add "$HOME"
```

检查是否识别成功：

```powershell
codex plugin marketplace list
codex plugin list
```

`codex plugin list` 中应能看到：

```text
interactive-mindmap-editor@personal
```

安装插件：

```powershell
codex plugin add interactive-mindmap-editor@personal
```

安装完成后，建议新开一个 Codex 任务，让插件和 Skill 被重新加载。

## 在 Claude 中安装

Claude 有两种推荐安装方式。

### 方式一：个人 Skill

适合多个项目共用同一份思维导图能力。

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git "$HOME\.claude\skills\interactive-mindmap-editor"
```

安装后，Claude 可通过该目录根部的 `SKILL.md` 识别此技能。

### 方式二：项目 Skill

适合某个项目需要固定版本，随项目一起迁移。

```powershell
cd "E:\path\to\your\project"
New-Item -ItemType Directory -Force ".\.claude\skills" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git ".\.claude\skills\interactive-mindmap-editor"
```

项目 Skill 的好处是：这个项目带着 `.claude\skills\interactive-mindmap-editor` 迁移到其他机器后，Claude 仍可读取同一份技能说明和脚本。

## Codex 和 Claude 的项目迁移方式

### Codex 项目迁移

Codex 插件更适合“机器级安装”：

- 在每台机器上安装一次插件。
- 不需要把插件复制到每个项目。
- 项目内只需要保留实际产物，例如 `.html`、`.json`、`.md`、`.xmind`。
- 如果某个项目必须锁定插件版本，可以把本仓库复制或克隆到项目内，并在请求中明确让 Codex 使用该路径下的脚本。

换设备时：

```powershell
cd "$HOME\plugins\interactive-mindmap-editor"
git pull
.\install-codex.ps1
```

### Claude 项目迁移

Claude 有两种迁移策略：

- 个人 Skill：每台机器安装一次，多个项目共用。
- 项目 Skill：将本仓库放在项目的 `.claude\skills\interactive-mindmap-editor` 下，随项目一起迁移。

如果你希望项目在任何机器上打开都带着同一版本的能力，使用项目 Skill。

如果你希望所有项目共用最新版，使用个人 Skill。

### 思维导图产物迁移

无论使用 Codex 还是 Claude，项目迁移时都应保留：

- 可编辑 HTML：`*.html`
- 思维导图数据：`*.json`
- Markdown 提纲：`*.md`
- XMind 文件：`*.xmind`

这些是项目产物；插件/Skill 是工具。

## 验证安装

可以用下面的命令查看插件是否已安装：

```powershell
codex plugin list
```

也可以新开 Codex 任务后输入类似请求测试：

```text
把下面这段文本生成可编辑 HTML 思维导图
```

或：

```text
修复这个 HTML 思维导图的双击编辑和节点折叠问题
```

或：

```text
生成一个带全屏展示按钮的可编辑 HTML 思维导图
```

生成的 HTML 应包含“全屏展示”按键。点击后，页面内容进入全屏并铺满显示屏；鼠标移动到页面顶部时，会出现 `X` 退出按键，点击后退出全屏模式。

生成的 HTML 中，工具栏的“展开”和“折叠”按键应采用分层行为：

- 点击“展开”：展开当前可见节点的下一层。
- 点击“折叠”：折叠当前最深可见的一层。
- 长按“展开”：全部展开。
- 长按“折叠”：全部折叠。

生成的 HTML 如果包含较多工具按钮，应采用紧凑工具菜单：

- 圆形菜单按钮放在右下角缩放 `+` 按钮之上。
- 点击菜单按钮展开或折叠次要工具按钮。
- 次要工具按钮包括 `展开`、`折叠`、`导入 Markdown`、`导出 Markdown`、`XMind`、`全屏展示`、`适配`。
- 缩放 `+`、缩放 `-`、重置视图应保持常驻显示。
- 点击画布空白区域后，菜单应自动收起。

## 文本转思维导图脚本

插件包含一个脚本：

```text
skills/interactive-mindmap-editor/scripts/text_to_mindmap_data.py
```

可以将结构化文本或 Markdown 提纲转换成思维导图 JSON：

```powershell
python .\skills\interactive-mindmap-editor\scripts\text_to_mindmap_data.py .\input.md -o .\mindmap-data.json --root-title "主题"
```

生成的 JSON 可用于导入或替换现有 HTML 思维导图中的数据对象。

## Markdown 导入/导出

### Markdown 提纲导入为思维导图 JSON

```powershell
python .\skills\interactive-mindmap-editor\scripts\markdown_to_mindmap_data.py .\input.md -o .\mindmap-data.json --root-title "主题"
```

该脚本会识别 Markdown 标题、项目符号、编号列表和缩进层级，并生成插件 HTML 可用的 `root -> part -> topic -> leaf` JSON。

### 思维导图 JSON 导出为 Markdown 提纲

```powershell
python .\skills\interactive-mindmap-editor\scripts\mindmap_data_to_markdown.py .\mindmap-data.json -o .\outline.md
```

导出的 Markdown 会使用一级标题表示根节点，使用缩进列表表示子节点层级；节点副标题会接在同一行，节点批注会尽量保留为引用块。

### HTML 页面中的 Markdown 按钮

后续由本插件生成或修复的 HTML 页面，如果已经有导入/导出工具栏，应提供：

- `导入 Markdown`：选择 `.md` / `.markdown` / `.txt` 文件后，将 Markdown 提纲转换成当前思维导图。
- `导出 Markdown`：将当前页面中的思维导图导出为 `.md` 文件。

### HTML 导出文件位置

插件后续生成或修复的独立 HTML 页面，应让 JSON、Markdown、XMind 三种导出统一使用系统“另存为”窗口：

- 点击导出后直接打开系统“另存为”窗口，可选择系统“下载”等文件夹。
- 用户在“另存为”窗口确认位置后立即写入文件，不再弹出第二次确认框。
- 用户取消“另存为”窗口时，本次导出结束，不应自动下载到浏览器默认目录。
- 三种格式共用稳定的选择器标识，并在 IndexedDB 中保存上一次成功导出的文件句柄。
- 再次导出或重新打开 HTML 后导出时，应把该文件句柄作为 `startIn`，默认回到上次保存文件所在目录。
- 导出成功后显示页面内提示，内容包含文件名，3 秒后自动消失。
- 本地 `file://` 页面优先使用 `showSaveFilePicker`，不要使用 `showDirectoryPicker` 选择系统下载目录。

## XMind 文件支持

插件支持生成现代 `.xmind` 文件。输出文件是 XMind 可识别的 zip 包，内部包含：

```text
content.json
metadata.json
manifest.json
```

### JSON 导出为 XMind

如果已经有插件生成的思维导图 JSON：

```powershell
python .\skills\interactive-mindmap-editor\scripts\mindmap_data_to_xmind.py .\mindmap-data.json -o .\output.xmind
```

### 文本或 Markdown 直接导出为 XMind

```powershell
python .\skills\interactive-mindmap-editor\scripts\text_to_xmind.py .\input.md -o .\output.xmind --root-title "主题"
```

### XMind 导入为插件 JSON

第二阶段支持识别 `.xmind` 文件，并转换成插件 HTML 可导入的 JSON：

```powershell
python .\skills\interactive-mindmap-editor\scripts\xmind_to_mindmap_data.py .\input.xmind -o .\mindmap-data.json
```

该导入器优先识别现代 XMind 文件中的 `content.json`，同时对旧版 XMind 包中的 `content.xml` 做基础兼容。

### 当前映射规则

- `title` 会变成 XMind 主题标题。
- `sub` 和 `note` 会写入 XMind 主题备注。
- `children` 会变成 XMind 子主题。
- 导入 `.xmind` 时，XMind 主题标题会变成插件 `title`。
- 导入 `.xmind` 时，XMind 备注会变成插件 `sub`。
- 导入 `.xmind` 时，XMind 子主题会变成插件 `children`。
- 当前阶段优先保证层级和文本可双向转换。
- 样式、图标、颜色、折叠状态等高级 XMind 元数据暂不做完整还原。

## 更新插件

如果本地插件已有旧版本：

```powershell
cd "$HOME\plugins\interactive-mindmap-editor"
git pull
codex plugin add interactive-mindmap-editor@personal
```

更新后同样建议新开一个 Codex 任务。

## 版本迭代说明

完整版本记录见 [CHANGELOG.md](CHANGELOG.md)。
