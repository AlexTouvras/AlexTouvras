# One command in your own PowerShell: .\run issues.csv
# Does not install a runtime, a package, or a server.
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Rest
)

$ErrorActionPreference = "Stop"
$Page = "https://htmlpreview.github.io/?https://github.com/AlexTouvras/AlexTouvras/blob/cursor/delivery-signal-mvp-b09f/docs/index.html"
$Base = "https://raw.githubusercontent.com/AlexTouvras/AlexTouvras/cursor/delivery-signal-mvp-b09f/delivery-signal"

$Root = $PSScriptRoot
if (-not $Root -or -not (Test-Path (Join-Path $Root "pipeline.py"))) {
    $Root = Join-Path $env:TEMP "delivery-signal"
    New-Item -ItemType Directory -Force -Path $Root | Out-Null
    Invoke-WebRequest "$Base/pipeline.py" -OutFile (Join-Path $Root "pipeline.py")
    Invoke-WebRequest "$Base/extract.py" -OutFile (Join-Path $Root "extract.py")
}

$Python = $null
$Prefix = @()
foreach ($Name in @("python3", "python", "py")) {
    $Command = Get-Command $Name -ErrorAction SilentlyContinue
    if ($Command) {
        $Python = $Command.Source
        if ($Name -eq "py") { $Prefix = @("-3") }
        break
    }
}

if (-not $Python) {
    Write-Error "Python is not on this machine. Open the page and choose the CSV: $Page"
    exit 1
}

& $Python @Prefix (Join-Path $Root "pipeline.py") @Rest
exit $LASTEXITCODE
