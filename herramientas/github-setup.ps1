# Configura GitHub para Miga y los Gigantes: ajustes del repo, labels, milestones,
# proyecto, issues iniciales y protección de main y develop.
#
# Requisitos (una sola vez):
#   winget install --id GitHub.cli
#   gh auth login
#   gh auth refresh -s project
#
# Ejecutar desde la raíz del proyecto:
#   powershell -ExecutionPolicy Bypass -File .\herramientas\github-setup.ps1
#
# Se puede repetir: labels, milestones y proyecto se actualizan, y las issues
# solo se crean si el repositorio todavía no tiene ninguna.
# Guardado en UTF-8 con BOM a propósito: Windows PowerShell 5.1 lee mal las tildes sin BOM.

$Repo     = 'Cris141614/miga-y-los-gigantes'
$Owner    = 'Cris141614'
$Proyecto = 'Miga y los Gigantes'

Set-Location (Split-Path $PSScriptRoot -Parent)

function Fallar($msg) { Write-Host "ERROR: $msg" -ForegroundColor Red; exit 1 }
function Revisar($paso) { if ($LASTEXITCODE -ne 0) { Fallar "falló el paso: $paso" } }
function Paso($msg) { Write-Host "`n== $msg" -ForegroundColor Cyan }

Paso 'Revisando GitHub CLI'
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { Fallar 'instala GitHub CLI: winget install --id GitHub.cli' }
gh auth status; Revisar 'no hay sesión. Ejecuta: gh auth login'
gh project list --owner $Owner --limit 1 | Out-Null
Revisar 'falta el permiso de proyectos. Ejecuta: gh auth refresh -s project'

# ---------------------------------------------------------------------------
Paso 'Ajustes del repositorio'
# develop por defecto: así "Closes #n" cierra la issue al fusionar el PR en develop
gh repo edit $Repo --default-branch develop --enable-squash-merge --enable-merge-commit --enable-rebase-merge=false --delete-branch-on-merge
Revisar 'gh repo edit'
gh api -X PATCH "repos/$Repo" -f 'squash_merge_commit_title=PR_TITLE' -f 'squash_merge_commit_message=PR_BODY' | Out-Null
Revisar 'mensaje de squash'

# ---------------------------------------------------------------------------
Paso 'Labels'
$labels = @(
    # Tipo: igual que el prefijo del commit
    @('feat',            '1D76DB', 'Funcionalidad nueva del juego'),
    @('fix',             'D73A4A', 'Corrección de un error'),
    @('art',             '8E44AD', 'Modelos, texturas, animaciones y audio'),
    @('docs',            '0075CA', 'Documentación y bóveda'),
    @('build',           '5319E7', 'Paquetes, dependencias y sistema de build'),
    @('ci',              '0E8A16', 'GitHub Actions y automatización'),
    @('chore',           'BFD4F2', 'Mantenimiento'),
    @('refactor',        'FBCA04', 'Reorganizar código sin cambiar lo que hace'),
    @('perf',            'F9A825', 'Rendimiento'),
    @('test',            'C2E0C6', 'Pruebas'),
    # Área del proyecto
    @('area:jugador',    'C5DEF5', 'Miga: movimiento y acciones'),
    @('area:camara',     'C5DEF5', 'Cámara'),
    @('area:criaturas',  'C5DEF5', 'Guardadores: La Costurera y otros'),
    @('area:sistemas',   'C5DEF5', 'Luz, ruido, hilo, escondites, puntos de control'),
    @('area:nivel',      'C5DEF5', 'Escenas y diseño de niveles'),
    @('area:arte',       'C5DEF5', 'Blender, texturas y materiales'),
    @('area:audio',      'C5DEF5', 'Efectos, ambiente y música'),
    @('area:canal',      'C5DEF5', 'Canal de YouTube y TikTok'),
    @('area:infra',      'C5DEF5', 'Repositorio, CI, Sentry, herramientas'),
    # Prioridad y estado
    @('prioridad:alta',  'B60205', 'Bloquea la versión actual'),
    @('prioridad:media', 'D93F0B', 'Importante, no bloquea'),
    @('prioridad:baja',  'FEF2C0', 'Cuando haya tiempo'),
    @('bloqueado',       '000000', 'Espera otra issue o una decisión'),
    @('descartado',      'CFD3D7', 'No se hará o está duplicada')
)
foreach ($l in $labels) {
    gh label create $l[0] --repo $Repo --color $l[1] --description $l[2] --force | Out-Null
    Revisar "label $($l[0])"
}
# Las de GitHub por defecto se reemplazan por las de arriba
foreach ($d in 'bug', 'enhancement', 'documentation', 'duplicate', 'good first issue', 'help wanted', 'invalid', 'question', 'wontfix') {
    gh label delete $d --repo $Repo --yes 2>$null | Out-Null
}

# ---------------------------------------------------------------------------
Paso 'Milestones'
$milestones = [ordered]@{
    'Puesta en marcha'           = 'Repositorio, CI, Sentry, GitGuardian y Blender listos para trabajar'
    'v0.1.0 - Bloques grises'    = 'Nivel 1 jugable de principio a fin con cubos y Miga como cápsula'
    'v0.2.0 - Mecánicas'         = 'Luz, ruido, La Costurera, hilo rojo, escondites y puntos de control'
    'v0.3.0 - Arte'              = 'Modelos y animaciones finales, una zona a la vez'
    'v0.4.0 - Sonido y luz'      = 'Efectos, ambiente, música e iluminación final'
    'Canal'                      = 'Episodios y devlogs'
}
$existentes = gh api "repos/$Repo/milestones?state=all&per_page=100" --jq '.[].title'
Revisar 'leer milestones'
foreach ($t in $milestones.Keys) {
    if ($existentes -notcontains $t) {
        gh api "repos/$Repo/milestones" -f "title=$t" -f "description=$($milestones[$t])" | Out-Null
        Revisar "milestone $t"
    }
}

# ---------------------------------------------------------------------------
Paso 'Proyecto'
$lista = (gh project list --owner $Owner --format json) -join "`n" | ConvertFrom-Json
$p = $lista.projects | Where-Object { $_.title -eq $Proyecto }
if ($p) { $num = $p.number } else {
    $num = gh project create --owner $Owner --title $Proyecto --format json --jq '.number'
    Revisar 'crear proyecto'
}
gh project link $num --owner $Owner --repo 'miga-y-los-gigantes' 2>$null | Out-Null

# ---------------------------------------------------------------------------
Paso 'Issues'
$hay = gh issue list --repo $Repo --state all --limit 1 --json number --jq 'length'
Revisar 'leer issues'
if ($hay -ne '0') {
    Write-Host 'El repositorio ya tiene issues: no se crean otra vez.' -ForegroundColor Yellow
} else {
    $tmp  = Join-Path $env:TEMP 'miga-issue.md'
    $utf8 = New-Object System.Text.UTF8Encoding $false

    function Issue($titulo, $labels, $milestone, $que, $nota, [string[]]$criterios) {
        $cuerpo = "## Qué hay que hacer`n$que`n`n## Nota de la bóveda`n``$nota```n`n## Criterios de aceptación`n"
        $cuerpo += ($criterios | ForEach-Object { "- [ ] $_" }) -join "`n"
        [IO.File]::WriteAllText($tmp, $cuerpo, $utf8)
        $url = gh issue create --repo $Repo --title $titulo --label $labels --milestone $milestone --project $Proyecto --body-file $tmp
        Revisar "issue: $titulo"
        Write-Host "  $url  $titulo"
    }

    $m = 'Puesta en marcha'
    Issue 'Configurar CI, plantillas y protección de ramas' 'ci,area:infra,prioridad:alta' $m `
        'Subir los workflows de GitHub Actions, las plantillas de issues y PR, Dependabot y la nota del flujo de trabajo.' `
        'docs/Produccion/Flujo de trabajo.md' `
        @('Los PR validan el título con Conventional Commits', 'Plantillas de issue y PR disponibles en GitHub', 'La nota Flujo de trabajo está enlazada en la bóveda')
    Issue 'Integrar Sentry para reportar errores' 'build,area:infra,prioridad:alta' $m `
        'Agregar el SDK de Sentry para Unity y conectarlo a un proyecto de Sentry.' `
        'docs/Produccion/Flujo de trabajo.md' `
        @('El paquete io.sentry.unity está en Packages/manifest.json', 'El DSN está configurado con Tools > Sentry', 'Un error de prueba aparece en Sentry', 'El token de Sentry no está en el repositorio')
    Issue 'Activar GitGuardian en el repositorio' 'chore,area:infra' $m `
        'Instalar la app de GitGuardian en GitHub para detectar contraseñas y tokens subidos por error.' `
        'docs/Produccion/Flujo de trabajo.md' `
        @('La app de GitGuardian tiene acceso al repositorio', 'Los PR muestran el check de GitGuardian')
    Issue 'Configurar la licencia de Unity para GitHub Actions' 'ci,area:infra' $m `
        'Agregar los secretos de Unity para que el workflow pueda compilar, probar y hacer builds.' `
        'docs/Produccion/Flujo de trabajo.md' `
        @('Existen los secretos UNITY_LICENSE, UNITY_EMAIL y UNITY_PASSWORD', 'El workflow Unity pasa en un PR que toca juego/')
    Issue 'Cargar las hojas de vistas en Blender' 'art,area:arte' $m `
        'Preparar los archivos de Blender de Miga y La Costurera con sus hojas de referencia.' `
        'docs/Produccion/Pipeline.md' `
        @('miga.blend y costurera.blend en arte-fuente/blender/personajes/', 'Referencias de frente, lado y espalda alineadas con el origen')

    $m = 'v0.1.0 - Bloques grises'
    Issue 'Escena del Nivel 1 con las 6 zonas en bloques grises' 'feat,area:nivel,prioridad:alta' $m `
        'Construir el taller completo con cubos, a la escala de Miga, para probar recorrido y ritmo.' `
        'docs/Niveles/Nivel 1 - El Taller.md' `
        @('Escena esc_nivel1_taller en Assets/_Proyecto/Scenes/Niveles/', 'Las 6 zonas existen en orden', 'Se puede recorrer de principio a fin')
    Issue 'Movimiento de Miga como cápsula' 'feat,area:jugador,prioridad:alta' $m `
        'Caminar, correr, agacharse, saltar y trepar bordes con el Input System y los controles del GDD.' `
        'docs/Juego/Mecanicas.md' `
        @('Teclado y mando funcionan según la tabla de controles del GDD', 'Trepa bordes a la altura de Miga', 'Correr y saltar quedan expuestos para el sistema de ruido')
    Issue 'Empujar y jalar objetos pequeños' 'feat,area:jugador' $m `
        'Agarrar con E o X y mover objetos como la tapa del costurero.' `
        'docs/Juego/Mecanicas.md' `
        @('Miga empuja y jala manteniendo el botón', 'Sirve para abrir el costurero de la zona 1')
    Issue 'Cámara lateral con Cinemachine' 'feat,area:camara,prioridad:alta' $m `
        'Cámara lateral fija y baja, a la altura de Miga.' `
        'docs/Juego/GDD.md' `
        @('Paquete Cinemachine instalado', 'La cámara sigue a Miga de lado', 'Se puede alejar en un punto marcado de la escena')

    $m = 'v0.2.0 - Mecánicas'
    Issue 'Luz de Chispa y tapar el frasco' 'feat,area:sistemas' $m `
        'El frasco ilumina alrededor de Miga y se apaga al taparlo con la bufanda.' `
        'docs/Juego/Mecanicas.md' `
        @('Radio corto de luz que muestra peligros del piso', 'Q o gatillo izquierdo tapa el frasco mientras se mantiene', 'Con el frasco tapado Miga camina más lento')
    Issue 'Sistema de ruido' 'feat,area:sistemas' $m `
        'Cada acción de Miga produce un nivel de ruido que pueden oír los Guardadores.' `
        'docs/Juego/Mecanicas.md' `
        @('Niveles ninguno, bajo, medio y alto según la tabla', 'La máquina de coser encendida tapa los niveles bajo y medio')
    Issue 'La Costurera con estados como caja gris' 'feat,area:criaturas' $m `
        'Comportamiento de La Costurera con estados, antes de tener el modelo.' `
        'docs/Personajes/La Costurera.md' `
        @('Estados definidos según la nota del personaje', 'Reacciona a la luz, al ruido y al hilo', 'Si atrapa a Miga, vuelve al último punto de control')
    Issue 'Hilo rojo entre la bufanda y el carrete' 'feat,area:sistemas' $m `
        'El hilo une a Miga con La Costurera: correr y saltar lo tensan.' `
        'docs/Juego/Mecanicas.md' `
        @('El hilo cruza el nivel desde el inicio', 'Correr y saltar lo tensan y alertan a La Costurera', 'Se puede enganchar y soltar', 'Se corta con las tijeras y la bufanda queda más corta')
    Issue 'Escondites y puntos de control' 'feat,area:sistemas' $m `
        'Esconderse debajo de telas, en carretes o detrás de objetos, y volver al último punto de control al ser atrapada.' `
        'docs/Juego/Mecanicas.md' `
        @('Escondida y con el frasco tapado, Miga no es detectable', 'Un punto de control automático por zona')

    $m = 'v0.3.0 - Arte'
    Issue 'Modelo y esqueleto de Miga' 'art,area:arte' $m 'Modelar, texturizar y riggear a Miga en Blender y llevarla a Unity.' 'docs/Personajes/Miga.md' `
        @('mod_miga.fbx en Assets/_Proyecto/Art/Modelos/', 'Fiel a la hoja de vistas', 'Registrado en Inventario')
    Issue 'Animaciones de Miga' 'art,area:arte' $m 'Todas las animaciones de Miga de la tabla del Inventario.' 'docs/Produccion/Inventario.md' `
        @('Reposo, caminar, correr, agacharse, saltar, trepar, empujar y tapar el frasco', 'Conectadas al movimiento')
    Issue 'Modelo de La Costurera' 'art,area:arte' $m 'Modelar, texturizar y riggear a La Costurera.' 'docs/Personajes/La Costurera.md' `
        @('mod_costurera.fbx en Assets/_Proyecto/Art/Modelos/', 'Fiel a la hoja de vistas', 'Registrado en Inventario')
    Issue 'Animaciones de La Costurera' 'art,area:arte' $m 'Animaciones de La Costurera de la tabla del Inventario.' 'docs/Produccion/Inventario.md' `
        @('Coser, girar la cabeza, tirar del hilo, clavar los dedos y perseguir', 'Conectadas a sus estados')
    $zonas = @('1: el costurero', '2: la mesa de corte', '3: la máquina de coser', '4: el armario de retazos', '5: las tijeras', '6: la huida')
    foreach ($z in $zonas) {
        Issue "Escenario de la zona $z" 'art,area:nivel' $m "Reemplazar los bloques grises de la zona $z por los modelos finales." 'docs/Niveles/Nivel 1 - El Taller.md' `
            @('Modelos finales en su lugar', 'La zona se sigue jugando igual', 'Elementos registrados en Inventario')
    }
    Issue 'Objetos pequeños del taller' 'art,area:arte' $m 'Carretes, botones, alfileres, dedal, telas y muñecos remendados.' 'docs/Produccion/Inventario.md' `
        @('Cada objeto como prefab en Prefabs/Objetos/', 'Registrados en Inventario')

    $m = 'v0.4.0 - Sonido y luz'
    Issue 'Efectos de sonido del Nivel 1' 'art,area:audio' $m 'Pasos, salto, frasco, hilo, tijeras, agujas, máquina de coser y tarareo.' 'docs/Produccion/Inventario.md' `
        @('Todos los sfx_ de la tabla de sonido en el juego', 'Volumen equilibrado')
    Issue 'Ambiente y música del taller' 'art,area:audio' $m 'Ambiente del cuarto y música de tensión y persecución.' 'docs/Produccion/Inventario.md' `
        @('amb_taller, mus_taller_tension y mus_taller_persecucion en el juego', 'La música cambia en la persecución')
    Issue 'Iluminación final del Nivel 1' 'art,area:nivel' $m 'Luz final de las 6 zonas, cuidando que Chispa siga siendo la luz principal.' 'docs/Niveles/Nivel 1 - El Taller.md' `
        @('Las 6 zonas iluminadas', 'Rendimiento estable en PC')

    $m = 'Canal'
    Issue 'Episodio 0: presentación de Miga' 'area:canal' $m 'Primer video del canal presentando a Miga.' 'docs/Canal/Episodios.md' `
        @('Guion en la bóveda', 'Video publicado en YouTube y TikTok')
    Issue 'Primer devlog' 'area:canal' $m 'Video corto de cómo se hizo una parte del juego.' 'docs/Canal/Canal.md' `
        @('Guion en la bóveda', 'Video publicado')

    Remove-Item $tmp -ErrorAction SilentlyContinue
}

# ---------------------------------------------------------------------------
Paso 'Protección de main y develop'
$reglas = gh api "repos/$Repo/rulesets" --jq '.[].name' 2>$null
if ($reglas -notcontains 'ramas-protegidas') {
    gh api -X POST "repos/$Repo/rulesets" --input 'herramientas\github\ramas-protegidas.json' | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'AVISO: no se pudieron proteger las ramas. GitHub no lo permite en repos privados con cuenta gratis.' -ForegroundColor Yellow
    }
}

Write-Host "`nListo. Proyecto: https://github.com/users/$Owner/projects/$num" -ForegroundColor Green
