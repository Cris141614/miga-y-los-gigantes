# Flujo de trabajo

Cómo pasa un cambio de una idea a una versión publicada. Los nombres y prefijos están en [[Convenciones]]; las tareas viven en GitHub (ver [[Tareas]]).

## Ramas

| Rama | Para qué | Sale de | Entra en |
|---|---|---|---|
| `main` | Solo versiones publicadas, con tag | — | — |
| `develop` | Integrar el trabajo (rama por defecto) | `main` | `main`, al publicar |
| `feat/13-hilo-rojo` | Una sola issue | `develop` | `develop` |
| `hotfix/0.1.1` | Error urgente en una versión publicada | `main` | `main` y `develop` |

`main` y `develop` están protegidas: no aceptan commits directos, todo entra por PR.

## Trabajar una issue

1. En el proyecto de GitHub, mover la issue a **In Progress**.
2. Crear la rama desde `develop` actualizado:
   ```powershell
   git switch develop
   git pull
   git switch -c feat/13-hilo-rojo
   ```
3. Commits pequeños con Conventional Commits.
4. Subir la rama y abrir el PR hacia `develop` con la plantilla, `Closes #13`, labels y milestone.
5. Revisar los checks: **Titulo del PR** (obligatorio), **Unity** (si tocaste `juego/`) y **GitGuardian**.
6. Fusionar con **Squash**: el título del PR queda como el commit en `develop`. La rama se borra y la issue se cierra sola.

## Pruebas automáticas

Usan el Test Framework de Unity (NUnit) y corren solas en cada PR que toca `juego/`.

- **Compilar y probar** es el check que manda: si el proyecto no compila o una prueba falla, sale en rojo.
- **Resultados de pruebas** siempre sale gris (neutral), porque GameCI lo crea así. Solo informa: su título dice cuántas pasaron (`3/3 - Passed`) y dentro está el detalle de cada una.

| Tipo | Carpeta | Para qué | Ejemplo |
|---|---|---|---|
| EditMode | `Assets/_Proyecto/Tests/EditMode/` | Lo que no necesita darle a Play: cálculos, escalas, configuración de assets | `EscalaDeLosModelosPruebas` |
| PlayMode | `Assets/_Proyecto/Tests/PlayMode/` | Lo que necesita frames y física: moverse, saltar, que un Guardador detecte a Miga | `FisicaPruebas` |

- El código del juego va en `Assets/_Proyecto/Scripts/`, dentro del ensamblado `Miga.Juego`. Las pruebas lo pueden usar porque lo referencian.
- Cada mecánica nueva llega con al menos una prueba.
- La clase termina en `Pruebas` y cada prueba dice en su nombre qué comprueba: `UnaCajaCaeYQuedaSobreElPiso`.

### Correrlas en Unity
1. `Window > General > Test Runner`.
2. Pestaña **EditMode** o **PlayMode** > **Run All**.
3. Verde, pasa. Rojo, clic en la prueba para ver qué falló.

### Escribir una prueba
```csharp
[Test]          // se comprueba de una vez
public void MigaMideUnMetro() { Assert.That(Escala.AlturaMiga, Is.EqualTo(1f)); }

[UnityTest]     // solo PlayMode: puede esperar frames o segundos
public IEnumerator MigaCaeAlPiso() { yield return new WaitForSeconds(1f); Assert.That(/* ... */); }
```

## Publicar una versión

Cada milestone es una versión (`v0.1.0 - Bloques grises`). Mientras la versión empiece con `0.` se publica como **pre-release** (beta).

1. Milestone sin issues abiertas y `develop` jugable.
2. PR de `develop` a `main` titulado `chore(release): v0.1.0`, fusionado con **merge commit** (nunca squash).
3. Tag y release desde `main`:
   ```powershell
   git switch main
   git pull
   git tag -a v0.1.0 -m 'Release v0.1.0'
   git push origin v0.1.0
   gh release create v0.1.0 --verify-tag --title 'v0.1.0' --prerelease --generate-notes
   ```
4. GitHub Actions hace el build de Windows y lo adjunta a la release como `.zip`.
5. PR de `main` a `develop` para que las dos ramas compartan el tag.

## Herramientas

| Herramienta | Qué hace | Dónde se configura |
|---|---|---|
| GitHub Actions | Valida títulos de PR, compila y prueba Unity, hace el build de cada release | `.github/workflows/` |
| Sentry | Reporta los errores del juego mientras alguien juega | Proyecto `miga-y-los-gigantes` en la organización `nova-sf` de sentry.io. En Unity: `Tools > Sentry`, opciones en `Assets/Resources/Sentry/` |
| GitGuardian | Avisa si se sube una contraseña o token | App de GitHub instalada en el repo |
| Dependabot | Propone actualizar las acciones de GitHub cada mes | `.github/dependabot.yml` |
| GitHub Projects | Tablero con todas las issues | Proyecto **Miga y los Gigantes** |

### Secretos de GitHub Actions
En el repo: **Settings > Secrets and variables > Actions**.

| Secreto | Valor |
|---|---|
| `UNITY_LICENSE` | Contenido de `C:\ProgramData\Unity\Unity_lic.ulf` |
| `UNITY_EMAIL` | Correo de la cuenta de Unity |
| `UNITY_PASSWORD` | Contraseña de la cuenta de Unity |

El token de Sentry nunca va al repositorio: la carpeta `Assets/Plugins/Sentry/` (donde Unity guarda `SentryCliOptions.asset`) está en el `.gitignore`. El DSN sí se sube: solo dice a dónde mandar los errores.

## Decisiones
- 2026-11-12: las tareas se llevan como issues en GitHub; la bóveda guarda diseño y decisiones.
- 2026-11-12: squash al fusionar en `develop`, merge commit al pasar a `main`.
- 2026-11-12: versiones `0.x` como pre-release hasta que el Nivel 1 esté completo.
- 2026-11-12: CI solo baja de LFS los archivos de `juego/`, para no gastar la cuota gratis.
- 2026-11-16: Sentry captura también los errores del editor (`Capture In Editor`). Los PR de Dependabot necesitan sus propios secretos de Unity (`gh secret set ... --app dependabot`).
- 2026-11-19: el código del juego va en el ensamblado `Miga.Juego` y las pruebas en dos ensamblados aparte, EditMode y PlayMode. La primera prueba real comprueba la escala de los modelos.
- 2026-11-19: el check *Resultados de pruebas* queda neutral aunque todo pase; se juzga por *Compilar y probar*.
