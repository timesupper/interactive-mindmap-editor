# =============================================================
#  interactive-mindmap-editor 安装脚本（Codex）
#
#  用途: 把当前双兼容技能目录安装为 Codex 插件，
#        注册 personal marketplace 并安装到 Codex。
#  运行: 右键该文件 -> 使用 PowerShell 运行
#        或在 PowerShell 中执行:  .\install-codex.ps1
#  说明: 本脚本假定已安装 codex CLI（https://github.com/openai/codex）
# =============================================================

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$PLUGIN_NAME = 'interactive-mindmap-editor'
$PLUGINS_DIR = Join-Path $HOME 'plugins'
$PLUGIN_DEST = Join-Path $PLUGINS_DIR $PLUGIN_NAME
$MARKETPLACE_DIR = Join-Path $HOME '.agents\plugins'
$MARKETPLACE_FILE = Join-Path $MARKETPLACE_DIR 'marketplace.json'
$SOURCE_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

function Write-Step([string]$title) {
    Write-Host ''
    Write-Host ('=' * 60) -ForegroundColor DarkCyan
    Write-Host ('  ' + $title) -ForegroundColor Cyan
    Write-Host ('=' * 60) -ForegroundColor DarkCyan
}
function Write-Ok([string]$msg)  { Write-Host ('[OK]   ' + $msg) -ForegroundColor Green }
function Write-Warn([string]$msg){ Write-Host ('[!]    ' + $msg) -ForegroundColor Yellow }
function Write-Fail([string]$msg){ Write-Host ('[FAIL] ' + $msg) -ForegroundColor Red }
function Write-Info([string]$msg){ Write-Host ('[·]    ' + $msg) -ForegroundColor Gray }

# 检测 codex CLI
function Test-CodexCli {
    $cmd = Get-Command codex -ErrorAction SilentlyContinue
    return [bool]$cmd
}

Write-Host ''
Write-Host '  Interactive Mindmap Editor - Codex 安装脚本' -ForegroundColor White
Write-Host '  运行时间: ' (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') -ForegroundColor Gray

# -------------------------------------------------------------
# 0. 预检
# -------------------------------------------------------------
Write-Step '预检'

if (-not (Test-CodexCli)) {
    Write-Warn '未检测到 codex 命令。请先安装 Codex CLI：'
    Write-Warn '  npm install -g @openai/codex'
    Write-Warn '或参考 https://github.com/openai/codex 的安装说明。'
    $continue = Read-Host '是否继续（仅安装文件到 plugins 目录，跳过 codex 命令）？ [y/N]'
    if ($continue -notmatch '^[yY]') { exit 1 }
}

# -------------------------------------------------------------
# 1. 复制插件文件到 plugins 目录
# -------------------------------------------------------------
Write-Step '复制插件文件'

New-Item -ItemType Directory -Force -Path $PLUGINS_DIR | Out-Null
if (Test-Path $PLUGIN_DEST) {
    Write-Warn "目标目录已存在: $PLUGIN_DEST"
    $answer = Read-Host '是否覆盖？ [y/N]'
    if ($answer -notmatch '^[yY]') {
        Write-Fail '已取消安装'
        exit 1
    }
    Remove-Item -Recurse -Force $PLUGIN_DEST
}

# 复制源码目录（排除 .git 和 __pycache__）
Write-Info "源目录: $SOURCE_DIR"
Write-Info "目标目录: $PLUGIN_DEST"
robocopy $SOURCE_DIR $PLUGIN_DEST /E /XD .git __pycache__ /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) {
    Write-Fail "复制失败 (robocopy exit $LASTEXITCODE)"
    exit 1
}
Write-Ok "插件已复制到 $PLUGIN_DEST"

# -------------------------------------------------------------
# 2. 创建或更新 personal marketplace
# -------------------------------------------------------------
Write-Step '注册 marketplace'

New-Item -ItemType Directory -Force -Path $MARKETPLACE_DIR | Out-Null

$marketplace = [ordered]@{
    name = 'personal'
    interface = [ordered]@{
        displayName = 'Personal'
    }
    plugins = @(
        [ordered]@{
            name = $PLUGIN_NAME
            source = [ordered]@{
                source = 'local'
                path = "./plugins/$PLUGIN_NAME"
            }
            policy = [ordered]@{
                installation = 'AVAILABLE'
                authentication = 'ON_INSTALL'
            }
            category = 'Productivity'
        }
    )
}

$json = $marketplace | ConvertTo-Json -Depth 10
# 必须写 UTF-8 无 BOM，否则部分 Codex 版本无法解析
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($MARKETPLACE_FILE, $json, $utf8NoBom)
Write-Ok "marketplace 已写入: $MARKETPLACE_FILE"

# -------------------------------------------------------------
# 3. 注册 marketplace 到 codex
# -------------------------------------------------------------
if (Test-CodexCli) {
    Write-Step '注册并安装到 Codex'
    Write-Info 'codex plugin marketplace add "$HOME" ...'
    codex plugin marketplace add "$HOME"
    Write-Info 'codex plugin add ...'
    codex plugin add "${PLUGIN_NAME}@personal"
    Write-Ok 'Codex 插件安装完成'
} else {
    Write-Warn '跳过 codex 注册/安装（未检测到 codex 命令）'
    Write-Warn '安装 codex 后请手动执行:'
    Write-Warn "  codex plugin marketplace add `"$HOME`""
    Write-Warn "  codex plugin add ${PLUGIN_NAME}@personal"
}

# -------------------------------------------------------------
# 4. 完成
# -------------------------------------------------------------
Write-Step '完成'
Write-Ok "插件目录: $PLUGIN_DEST"
Write-Ok 'Codex 桌面版与 CLI 共享 ~/.codex 配置，安装一次两边都可用。'
Write-Ok '建议新开一个 Codex 任务（CLI 或桌面版），让插件和 Skill 被重新加载。'
Write-Host ''
Write-Host '验证: codex plugin list' -ForegroundColor Gray
Write-Host '     应能看到 interactive-mindmap-editor@personal' -ForegroundColor Gray
Write-Host ''
Write-Host '故障排查:' -ForegroundColor Yellow
Write-Host '  - 若报 "plugin was not found in marketplace personal"，确认 marketplace.json 是 UTF-8 无 BOM。' -ForegroundColor Gray
Write-Host '  - 若 codex plugin list 看不到插件，尝试: codex plugin add interactive-mindmap-editor@personal' -ForegroundColor Gray
Write-Host '  - 本地插件发现问题可参考 Codex GitHub issue #26037（Windows 上 0.130 曾有运行时发现 bug）。' -ForegroundColor Gray
Write-Host ''
