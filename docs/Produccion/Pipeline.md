# Pipeline

Cómo pasa algo de idea a estar dentro del juego.

## Flujo
1. **Referencia** en `docs/Referencias/` (hoja de vistas en PNG y SVG).
2. **Modelo** en Blender, en `arte-fuente/blender/`.
3. **Exportar** a FBX hacia `juego/Assets/_Proyecto/Art/Modelos/`.
4. **Prefab** en Unity, en `Assets/_Proyecto/Prefabs/`.
5. **Registrar** en [[Inventario]].

## Usar las hojas de vistas en Blender
- `miga.blend` y `costurera.blend` ya traen las tres vistas en la colección `Referencias`, con el piso en el origen y a la escala del juego. Se ven en vista ortográfica: frente con `1`, lado con `Ctrl+3`, espalda con `Ctrl+1`.
- Para cargarlas en otro personaje: recortar sus vistas en `arte-fuente/blender/personajes/<personaje>/referencias/` (`<personaje>-frente.png`, `-lado.png`, `-espalda.png`), agregar sus medidas a `HOJAS` en `arte-fuente/blender/referencias.py` y, con su `.blend` abierto, correr en la pestaña Scripting: `exec(open(bpy.path.abspath("//../../referencias.py"), encoding="utf-8").read()); cargar("<personaje>")`.
- A mano: `Add > Image > Reference`, una por vista.
- Como dibujo 2D editable: `File > Import > Scalable Vector Graphics (.svg)`. Las formas entran como curvas.
- Alinear siempre la línea de piso con el origen.

## Escala
- **Miga mide 1 unidad (1 metro) en Unity.** El mundo se construye a la escala de los Guardadores, unas 17 veces más grande.
- La Costurera mide unas 17 unidades.
- En Blender: 1 unidad = 1 metro, igual que Unity.

## Exportar FBX desde Blender
- Aplicar escala y rotación antes de exportar (`Ctrl+A`).
- `Forward: -Z`, `Up: Y`, con `Apply Transform` activo.
- Un FBX por personaje u objeto. Las animaciones van en FBX aparte.

## Audio
- Originales y proyectos de edición en `audio-fuente/`.
- Al juego solo entra el archivo final: `.wav` para efectos, `.ogg` para música y ambiente.

## Qué va en Git y qué no
- Sí: todo el repo, incluida esta bóveda.
- Archivos pesados (modelos, texturas, audio) pasan por Git LFS; ya está configurado en `.gitattributes`.
- No: las carpetas `Library/`, `Temp/` y `Logs/` de Unity; ya están en el `.gitignore`.

## Videos del canal
Se graban dentro de Unity, con las mismas escenas del juego. Ver [[Canal]].
