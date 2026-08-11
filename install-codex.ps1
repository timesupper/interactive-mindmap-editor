# Install interactive-mindmap-editor as a Codex personal plugin.

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$PluginName = 'interactive-mindmap-editor'
$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PluginsDir = Join-Path $HOME 'plugins'
$PluginDest = Join-Path $PluginsDir $PluginName
$MarketplaceDir = Join-Path $HOME '.agents\plugins'
$MarketplaceFile = Join-Path $MarketplaceDir 'marketplace.json'

function Write-Step([string]$Message) {
  Write-Host ''
  Write-Host "== $Message ==" -ForegroundColor Cyan
}

function Test-CodexCli {
  return [bool](Get-Command codex -ErrorAction SilentlyContinue)
}

Write-Step 'Copy plugin files'
New-Item -ItemType Directory -Force -Path $PluginsDir | Out-Null

if ((Resolve-Path -LiteralPath $SourceDir).Path -ne (Resolve-Path -LiteralPath $PluginDest -ErrorAction SilentlyContinue).Path) {
  if (Test-Path -LiteralPath $PluginDest) {
    $answer = Read-Host "Target exists: $PluginDest. Overwrite it? [y/N]"
    if ($answer -notmatch '^[yY]') {
      throw 'Install canceled.'
    }
    Remove-Item -LiteralPath $PluginDest -Recurse -Force
  }
  robocopy $SourceDir $PluginDest /E /XD .git __pycache__ /XF *.pyc /NFL /NDL /NJH /NJS /NP | Out-Null
  if ($LASTEXITCODE -ge 8) {
    throw "robocopy failed with exit code $LASTEXITCODE"
  }
} else {
  Write-Host "Source already equals plugin destination: $PluginDest"
}

Write-Step 'Write personal marketplace'
New-Item -ItemType Directory -Force -Path $MarketplaceDir | Out-Null
$marketplace = [ordered]@{
  name = 'personal'
  interface = [ordered]@{
    displayName = 'Personal'
  }
  plugins = @(
    [ordered]@{
      name = $PluginName
      source = [ordered]@{
        source = 'local'
        path = "./plugins/$PluginName"
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
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($MarketplaceFile, $json, $utf8NoBom)
Write-Host "Marketplace written: $MarketplaceFile"

if (Test-CodexCli) {
  Write-Step 'Register and install in Codex'
  codex plugin marketplace add "$HOME"
  codex plugin add "${PluginName}@personal"
  Write-Host 'Codex plugin installed. Open a new Codex task to reload skills.' -ForegroundColor Green
} else {
  Write-Step 'Manual Codex commands'
  Write-Host 'Codex CLI was not found. After installing Codex, run:'
  Write-Host 'codex plugin marketplace add "$HOME"'
  Write-Host "codex plugin add ${PluginName}@personal"
}
