# =============================================================
#  interactive-mindmap-editor installer (Codex)
#
#  Purpose: install this dual-compatible skill as a Codex plugin.
#  Run: .\install-codex.ps1
#  Requires: Codex CLI (https://github.com/openai/codex)
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
function Write-Info([string]$msg){ Write-Host ('[i]    ' + $msg) -ForegroundColor Gray }

# Check for the Codex CLI.
function Test-CodexCli {
    $cmd = Get-Command codex -ErrorAction SilentlyContinue
    return [bool]$cmd
}

Write-Host ''
Write-Host '  Interactive Mindmap Editor - Codex installer' -ForegroundColor White
Write-Host '  Run time: ' (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') -ForegroundColor Gray

# -------------------------------------------------------------
# 0. Preflight
# -------------------------------------------------------------
Write-Step 'Preflight'

if (-not (Test-CodexCli)) {
    Write-Warn 'Codex CLI was not found. Install it first:'
    Write-Warn '  npm install -g @openai/codex'
    Write-Warn 'See https://github.com/openai/codex for installation instructions.'
    $continue = Read-Host 'Continue without Codex CLI? [y/N]'
    if ($continue -notmatch '^[yY]') { exit 1 }
}

# -------------------------------------------------------------
# 1. Copy plugin files to the plugins directory.
# -------------------------------------------------------------
Write-Step 'Copy plugin files'

New-Item -ItemType Directory -Force -Path $PLUGINS_DIR | Out-Null
if (Test-Path $PLUGIN_DEST) {
    Write-Warn "Destination already exists: $PLUGIN_DEST"
    $answer = Read-Host 'Overwrite it? [y/N]'
    if ($answer -notmatch '^[yY]') {
        Write-Fail 'Installation cancelled'
        exit 1
    }
    Remove-Item -Recurse -Force $PLUGIN_DEST
}

# Copy source files, excluding .git and __pycache__.
Write-Info "Source: $SOURCE_DIR"
Write-Info "Destination: $PLUGIN_DEST"
robocopy $SOURCE_DIR $PLUGIN_DEST /E /XD .git __pycache__ /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) {
    Write-Fail "Copy failed (robocopy exit $LASTEXITCODE)"
    exit 1
}
Write-Ok "Plugin copied to $PLUGIN_DEST"

# -------------------------------------------------------------
# 2. Create or update the personal marketplace.
# -------------------------------------------------------------
Write-Step 'Register marketplace'

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
# Write UTF-8 without a BOM for compatibility with older Codex versions.
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($MARKETPLACE_FILE, $json, $utf8NoBom)
Write-Ok "Marketplace written to: $MARKETPLACE_FILE"

# -------------------------------------------------------------
# 3. Register the marketplace with Codex.
# -------------------------------------------------------------
if (Test-CodexCli) {
    Write-Step 'Register and install in Codex'
    Write-Info 'codex plugin marketplace add "$HOME" ...'
    codex plugin marketplace add "$HOME"
    Write-Info 'codex plugin add ...'
    codex plugin add "${PLUGIN_NAME}@personal"
    Write-Ok 'Codex plugin installation complete'
} else {
    Write-Warn 'Skipped Codex registration because Codex CLI was not found.'
    Write-Warn 'After installing Codex, run:'
    Write-Warn "  codex plugin marketplace add `"$HOME`""
    Write-Warn "  codex plugin add ${PLUGIN_NAME}@personal"
}

# -------------------------------------------------------------
# 4. Complete.
# -------------------------------------------------------------
Write-Step 'Complete'
Write-Ok "Plugin directory: $PLUGIN_DEST"
Write-Ok 'Codex Desktop and CLI share the same plugin configuration.'
Write-Ok 'Start a new Codex task so the plugin and skill are reloaded.'
Write-Host ''
Write-Host 'Verify: codex plugin list' -ForegroundColor Gray
Write-Host '       interactive-mindmap-editor@personal should be listed' -ForegroundColor Gray
Write-Host ''
Write-Host 'Troubleshooting:' -ForegroundColor Yellow
Write-Host '  - If marketplace personal is not found, check marketplace.json encoding.' -ForegroundColor Gray
Write-Host '  - If the plugin is missing, run: codex plugin add interactive-mindmap-editor@personal' -ForegroundColor Gray
Write-Host '  - For local plugin discovery issues, update Codex CLI to a current version.' -ForegroundColor Gray
Write-Host ''
