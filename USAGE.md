# Interactive Mindmap Editor 使用说明

## 插件功能

`interactive-mindmap-editor` 是一个 Codex 插件，用于创建、修复、导入和导出可编辑的 HTML/XMind 思维导图。

主要能力：

- 将文本、Markdown、文章、笔记、章节内容整理成思维导图层级结构。
- 生成适用于交互式 HTML 思维导图的数据。
- 修复 HTML 思维导图的节点编辑、折叠、布局和层级操作问题。
- 支持标题/副标题两行编辑。
- 支持节点长文本按字符宽度换行。
- 支持各级节点继续新增、编辑、删除子节点。
- 修复点击标题误触发展开/折叠的问题，只在右侧箭头区域触发折叠。
- 修复编辑节点时遮挡其他节点的问题。
- 支持生成带“全屏展示”按键的 HTML，进入全屏后内容铺满屏幕，鼠标指向顶部时显示 `X` 退出按键。
- 支持工具栏展开/折叠分层操作：点击一次只展开或折叠一级，长按则全部展开或全部折叠。
- 支持将插件 JSON 或文本导出为 XMind 可打开的 `.xmind` 文件。
- 支持识别现代 `.xmind` 文件，并转换回插件可用的思维导图 JSON。

## 插件目录结构

```text
interactive-mindmap-editor/
├── .codex-plugin/
│   └── plugin.json
├── skills/
│   └── interactive-mindmap-editor/
│       ├── SKILL.md
│       ├── agents/
│       │   └── openai.yaml
│       └── scripts/
│           ├── mindmap_data_to_xmind.py
│           ├── text_to_mindmap_data.py
│           ├── text_to_xmind.py
│           └── xmind_to_mindmap_data.py
├── README.md
├── CHANGELOG.md
└── USAGE.md
```

## 在新系统的 PowerShell 中安装

以下命令假设你要从 GitHub 安装到当前 Windows 用户的本地插件目录。

### 1. 克隆插件仓库

```powershell
New-Item -ItemType Directory -Force "$HOME\plugins" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git "$HOME\plugins\interactive-mindmap-editor"
```

### 2. 创建或更新个人 marketplace

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

### 4. 安装插件

```powershell
codex plugin add interactive-mindmap-editor@personal
```

安装完成后，建议新开一个 Codex 任务，让插件和 Skill 被重新加载。

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
