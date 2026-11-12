# Miga y los Gigantes

Juego 3D de suspenso con cámara lateral, y el canal de video que sale de él. Una niña del tamaño de una taza cruza una casa hecha para gigantes.

## Estructura

| Carpeta | Qué contiene |
|---|---|
| `docs/` | Bóveda de Obsidian: historia, personajes, niveles, producción, canal y referencias |
| `arte-fuente/` | Archivos de Blender y texturas originales. Unity no lee esta carpeta |
| `audio-fuente/` | Grabaciones y proyectos de audio originales |
| `juego/` | Proyecto de Unity (se crea en el paso 1) |
| `canal/` | Marca, episodios y miniaturas del canal |
| `_plantilla-unity/` | Carpetas y `.gitignore` para copiar dentro de `juego/` |

## Primeros pasos

1. **Unity.** En Unity Hub, crear un proyecto nuevo con la plantilla 3D (URP), nombre `juego`, ubicado en esta carpeta.
2. **Plantilla.** Copiar todo el contenido de `_plantilla-unity/` dentro de `juego/` (incluido el `.gitignore`, que es un archivo oculto) y borrar `_plantilla-unity/`.
3. **GitHub.** Crear un repositorio vacío llamado `miga-y-los-gigantes` (sin README ni .gitignore) y ejecutar en esta carpeta:

   ```bash
   git init -b main
   git lfs install
   git add .
   git commit -m "chore: estructura inicial del proyecto"
   git remote add origin https://github.com/USUARIO/miga-y-los-gigantes.git
   git push -u origin main
   git switch -c develop
   git push -u origin develop
   ```

4. **Obsidian.** Abrir la carpeta `docs/` como bóveda y empezar por `00-Inicio`.
5. **Blender.** Guardar los modelos en `arte-fuente/blender/` y cargar las hojas de `docs/Referencias/Personajes/`.

## Notas
- Git LFS es necesario: los modelos, texturas y audio están configurados en `.gitattributes`. El almacenamiento gratuito de LFS en GitHub es limitado.
- Las reglas de nombres, ramas y commits están en `docs/Produccion/Convenciones.md`.
