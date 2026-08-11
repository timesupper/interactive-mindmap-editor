# Interactive Mindmap Editor 使用说明

## 插件功能

`interactive-mindmap-editor` 是一个 Codex 插件，用于创建、修复和扩展可编辑的 HTML 思维导图。

主要能力：

- 将文本、Markdown、文章、笔记、章节内容整理成思维导图层级结构。
- 生成适用于交互式 HTML 思维导图的数据。
- 修复 HTML 思维导图的节点编辑、折叠、布局和层级操作问题。
- 支持标题/副标题两行编辑。
- 支持节点长文本按字符宽度换行。
- 支持各级节点继续新增、编辑、删除子节点。
- 修复点击标题误触发展开/折叠的问题，只在右侧箭头区域触发折叠。
- 修复编辑节点时遮挡其他节点的问题。

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
│           └── text_to_xmind.py
├── README.md
└── USAGE.md
```

## 在 PowerShell 中安装

以下命令假设你要从 GitHub 安装到当前 Windows 用户的本地插件目录。

### 1. 克隆插件仓库

```powershell
New-Item -ItemType Directory -Force "$HOME\plugins" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git "$HOME\plugins\interactive-mindmap-editor"
```

### 2. 创建或更新个人 marketplace

如果 `$HOME\.agents\plugins\marketplace.json` 不存在，先创建它：

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\plugins" | Out-Null
@'
{
  "name": "personal",
  "interface": {
    "displayName": "Personal"
  },
  "plugins": []
}
'@ | Set-Content "$HOME\.agents\plugins\marketplace.json" -Encoding UTF8
```

然后加入插件条目：

```powershell
$marketplacePath = "$HOME\.agents\plugins\marketplace.json"
$marketplace = Get-Content $marketplacePath -Raw | ConvertFrom-Json

$entry = [pscustomobject]@{
  name = "interactive-mindmap-editor"
  source = [pscustomobject]@{
    source = "local"
    path = "./plugins/interactive-mindmap-editor"
  }
  policy = [pscustomobject]@{
    installation = "AVAILABLE"
    authentication = "ON_INSTALL"
  }
  category = "Productivity"
}

$marketplace.plugins = @($marketplace.plugins | Where-Object { $_.name -ne "interactive-mindmap-editor" })
$marketplace.plugins += $entry
$marketplace | ConvertTo-Json -Depth 10 | Set-Content $marketplacePath -Encoding UTF8
```

### 3. 安装插件

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

## 导出为 XMind 文件

第一阶段支持生成现代 `.xmind` 文件。输出文件是 XMind 可识别的 zip 包，内部包含：

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

### 当前阶段的映射规则

- `title` 会变成 XMind 主题标题。
- `sub` 和 `note` 会写入 XMind 主题备注。
- `children` 会变成 XMind 子主题。
- 第一阶段优先保证层级和文本可打开。
- 样式、图标、颜色、折叠状态、旧版 XMind 8 XML 兼容放到后续阶段。

## 更新插件

如果本地插件已有旧版本：

```powershell
cd "$HOME\plugins\interactive-mindmap-editor"
git pull
codex plugin add interactive-mindmap-editor@personal
```

更新后同样建议新开一个 Codex 任务。
