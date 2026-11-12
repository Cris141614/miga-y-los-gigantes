# Configura Git, Git LFS y GitHub para Miga y los Gigantes.
# Ejecutar DESPUES de crear el proyecto de Unity en la carpeta "juego":
#   powershell -ExecutionPolicy Bypass -File .\configurar.ps1
# Se puede volver a ejecutar sin problema: salta lo que ya esta hecho.
# Solo ASCII a proposito: Windows PowerShell 5.1 lee mal las tildes sin BOM.

Set-Location $PSScriptRoot

function Fallar($msg) { Write-Host "ERROR: $msg" -ForegroundColor Red; exit 1 }
function Revisar($paso) { if ($LASTEXITCODE -ne 0) { Fallar "fallo el paso: $paso" } }
function Paso($msg) { Write-Host "`n== $msg" -ForegroundColor Cyan }

Paso 'Revisando requisitos'
foreach ($cmd in 'git', 'gh') {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) { Fallar "no se encontro '$cmd' en el PATH" }
}
git lfs version; Revisar 'Git LFS no esta instalado (https://git-lfs.com)'
if (-not (git config user.name) -or -not (git config user.email)) {
    Fallar 'falta tu identidad de Git. Ejecuta: git config --global user.name "Tu Nombre"  y  git config --global user.email "tu@correo"'
}
gh auth status
if ($LASTEXITCODE -ne 0) { Fallar 'no has iniciado sesion en GitHub. Ejecuta: gh auth login' }
if (-not (Test-Path 'juego\ProjectSettings\ProjectVersion.txt')) {
    Fallar 'no existe el proyecto de Unity en la carpeta "juego". Crealo primero desde Unity Hub.'
}

if (Test-Path '_plantilla-unity') {
    Paso 'Copiando la plantilla dentro de juego'
    robocopy '_plantilla-unity' 'juego' /E /NFL /NDL /NJH /NJS | Out-Null
    # robocopy: 0-7 es exito, 8 o mas es error
    if ($LASTEXITCODE -ge 8 -or -not (Test-Path 'juego\.gitignore')) { Fallar 'no se pudo copiar la plantilla' }
    Remove-Item '_plantilla-unity' -Recurse -Force
}

Paso 'Preparando el repositorio local'
if (-not (Test-Path '.git')) { git init -b main; Revisar 'git init' }
git lfs install --local; Revisar 'git lfs install'
git add .; Revisar 'git add'
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -m 'chore: estructura inicial del proyecto'; Revisar 'git commit'
}

Paso 'Subiendo a GitHub'
if ((git remote) -notcontains 'origin') {
    gh repo create miga-y-los-gigantes --private --source . --remote origin --push
    Revisar 'gh repo create'
} else {
    git push -u origin main; Revisar 'git push main'
}

Paso 'Creando la rama develop'
if ((git branch --format '%(refname:short)') -notcontains 'develop') { git switch -c develop } else { git switch develop }
Revisar 'git switch develop'
git push -u origin develop; Revisar 'git push develop'

Write-Host "`nListo. Repositorio:" -ForegroundColor Green
gh repo view --json url --jq .url
