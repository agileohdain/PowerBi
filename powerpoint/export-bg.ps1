<#
.SYNOPSIS
  Exporte la diapo 1 d'un .pptx en PNG haute resolution (fond d'image pour
  la maquette HTML). Optionnel : recolore les 3 formes natives avant l'export.

  Note : l'export SVG n'est pas supporte par l'automatisation COM de PowerPoint
  sur la plupart des versions. Le PNG 2x (3840x2160) est net, leger (couleurs
  plates) et universellement compatible (HTML + Power BI Desktop).

.USAGE
  # Export simple (l'utilisateur a deja personnalise le pptx) :
  ./export-bg.ps1 -Path "clients/acme/fond.pptx" -Output "clients/acme/bg.png"

  # Recolorer depuis le template puis exporter (veloh = theme sombre) :
  ./export-bg.ps1 -Template -Output "clients/veloh/bg.png" `
                  -Primary E0BE7E -Surface 1E293B -Canvas 0F172A

  # Resolution personnalisee (defaut 3840x2160 = 2x le canevas 1920x1080) :
  ./export-bg.ps1 -Path fond.pptx -Output bg.png -Width 1920 -Height 1080
#>
[CmdletBinding(DefaultParameterSetName = 'Direct')]
param(
    [Parameter(ParameterSetName = 'Direct', Mandatory)]
    [string]$Path,                        # chemin du .pptx personnalise

    [Parameter(ParameterSetName = 'Recolor', Mandatory)]
    [switch]$Template,                    # utiliser powerpoint/Maquette Power BI.pptx

    [Parameter(Mandatory)]
    [string]$Output,                      # chemin de sortie (.png)

    # Recoloration optionnelle (hex sans #) - n'importe quel sous-ensemble
    [string]$Primary,                     # forme "Banniere"
    [string]$Surface,                     # forme "Zone logo"
    [string]$Canvas,                      # forme "Fond canevas"

    [int]$Width = 3840,                   # largeur export (defaut 2x)
    [int]$Height = 2160                   # hauteur export (defaut 2x)
)

$ErrorActionPreference = 'Stop'

# --- Resolution du fichier d'entree ---
if ($PSCmdlet.ParameterSetName -eq 'Recolor') {
    $pptxPath = Join-Path $PSScriptRoot "Maquette Power BI.pptx"
} else {
    $pptxPath = $Path
    if (-not [System.IO.Path]::IsPathRooted($pptxPath)) {
        $pptxPath = Join-Path (Get-Location) $pptxPath
    }
}
if (-not (Test-Path -LiteralPath $pptxPath)) { throw "Fichier introuvable: $pptxPath" }
$pptxPath = (Resolve-Path -LiteralPath $pptxPath).Path

# --- Resolution du chemin de sortie (force .png) ---
if (-not [System.IO.Path]::IsPathRooted($Output)) {
    $Output = Join-Path (Get-Location) $Output
}
if ([System.IO.Path]::GetExtension($Output).ToLowerInvariant() -ne '.png') {
    $newOut = [System.IO.Path]::ChangeExtension($Output, '.png')
    if ($Output -ne $newOut) {
        Write-Warning "SVG non supporte par COM ; sortie forcee en PNG : $newOut"
        $Output = $newOut
    }
}
$outDir = Split-Path -Parent $Output
if (-not (Test-Path -LiteralPath $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }

Write-Host "Source : $pptxPath"
Write-Host "Sortie : $Output ($Width x $Height)"

# --- Recoloration (RGB hex -> OLE color BGR attendu par PowerPoint) ---
function ConvertTo-OleColor([string]$hex) {
    $rgb = [System.Convert]::ToInt32($hex, 16)
    $r = ($rgb -shr 16) -band 0xFF
    $g = ($rgb -shr 8) -band 0xFF
    $b = $rgb -band 0xFF
    return ($b -shl 16) -bor ($g -shl 8) -bor $r
}

$ppa = New-Object -ComObject PowerPoint.Application
try { $ppa.Visible = $true } catch {}
try {
    $pres = $ppa.Presentations.Open($pptxPath, $true, $false, $false)
    $slide = $pres.Slides.Item(1)

    # Recoloration des 3 formes natives (par nom)
    $recolors = @{
        'Banniere'     = $Primary
        'Zone logo'    = $Surface
        'Fond canevas' = $Canvas
    }
    if ($Primary -or $Surface -or $Canvas) {
        foreach ($kv in $recolors.GetEnumerator()) {
            if (-not $kv.Value) { continue }
            $shape = $null
            foreach ($sh in $slide.Shapes) {
                if ($sh.Name -eq $kv.Key) { $shape = $sh; break }
            }
            if ($null -ne $shape) {
                $shape.Fill.ForeColor.RGB = (ConvertTo-OleColor $kv.Value)
                Write-Host "Recolorage '$($kv.Key)' -> #$($kv.Value)"
            } else {
                Write-Warning "Forme '$($kv.Key)' introuvable - recolorage ignore"
            }
        }
    }

    # Export PNG
    $slide.Export($Output, "PNG", $Width, $Height)
    $pres.Close()
} finally {
    $ppa.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppa) | Out-Null
}

if (Test-Path -LiteralPath $Output) {
    Write-Host ("Termine : {0} ({1} octets)" -f $Output, (Get-Item -LiteralPath $Output).Length)
} else {
    throw "Echec de l'export : fichier non cree."
}
