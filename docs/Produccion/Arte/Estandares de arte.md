# Estándares de arte

Los números que todo asset tiene que cumplir. Las etapas están en [[Pipeline de arte]]; la escala y el export FBX, en [[Pipeline]].

## Escala
- 1 unidad = 1 metro, en Blender y en Unity.
- Miga mide 1 m. La Costurera, 17 m. El mundo está a la escala de los Guardadores.
- Piso del asset en el origen, escala y rotación aplicadas (`Ctrl+A`) antes de exportar.

## Límites por tipo

| Tipo | Triángulos | Texturas | Materiales |
|---|---|---|---|
| Miga | hasta 50 000 | 2048 px por material | hasta 6 |
| Guardador | hasta 80 000 | 4096 px en cara y cuerpo, 2048 px el resto | hasta 6 |
| Objeto grande o pieza de escenario | hasta 15 000 | 2048 px | hasta 3 |
| Objeto pequeño | hasta 2 000 | 512 a 1024 px, en un atlas compartido | 1 |

- Las texturas son cuadradas y en potencia de 2 (512, 1024, 2048, 4096). Nunca más de 4096.
- La prueba `EstandaresDeArtePruebas` usa 50 000 para `mod_miga`, 80 000 para `mod_costurera` y 15 000 para cualquier otro modelo. Un Guardador nuevo se agrega a la lista `Limites` de la prueba.

## Mapas para URP Lit

| Mapa | Nombre | En el material de Unity | Cómo sale de Blender |
|---|---|---|---|
| Color base | `tex_miga_abrigo.png` (sin sufijo) | Base Map | Pintado, o bake `Diffuse` solo con `Color` |
| Normales | `tex_miga_abrigo_normal.png` | Normal Map; textura con `Texture Type = Normal map` | Bake `Normal`, espacio `Tangent`, `+X +Y +Z` (OpenGL, el que usa Unity) |
| Oclusión | `tex_miga_abrigo_ao.png` | Occlusion Map; textura con `sRGB` apagado | Bake `Ambient Occlusion` |
| Metal y suavidad | `tex_tijeras_hoja_metal.png` | Metallic Map; `Source = Metallic Alpha`, `sRGB` apagado | Canal R = metal, canal A = 1 − rugosidad |

- Un material que no es metálico (tela, piel, madera, papel) no lleva `_metal`: `Metallic` en 0 y `Smoothness` con el deslizador.
- El color base va sin luces ni sombras pintadas: la luz la pone Unity.
- Mapas de normales, oclusión y metal se guardan desde Blender como `Non-Color`.

## Densidad de texel
- Igual en todo el asset: con la textura de cuadros (`UV Grid`), los cuadros miden lo mismo en todas las piezas. Cara y manos de personajes pueden llevar el doble.
- Entre assets: un objeto se tiene que ver igual de nítido que Miga a la distancia normal de la cámara lateral. Se revisa en Unity con la textura de cuadros, al lado de Miga.

## Archivos

| Qué | Carpeta | Nombre |
|---|---|---|
| Hojas de referencia | `docs/Referencias/Personajes/` o `docs/Referencias/Escenarios/` | `<asset>-vistas.png`, `<asset>-detalles.png` |
| Esculpido, bajo y bake | `arte-fuente/blender/<personajes, escenarios u objetos>/<asset>/` | `<asset>-esculpido.blend` |
| Bajo con rig y animaciones | la misma carpeta | `<asset>.blend` |
| Texturas | `juego/Assets/_Proyecto/Art/Texturas/` | `tex_<asset>_<pieza>[_mapa].png` |
| Modelo | `juego/Assets/_Proyecto/Art/Modelos/` | `mod_<asset>.fbx` |
| Animaciones | `juego/Assets/_Proyecto/Art/Animaciones/` | `anim_<asset>_<accion>.fbx` |
| Materiales | `juego/Assets/_Proyecto/Art/Materiales/` | `mat_<asset>_<pieza>.mat` |
| Prefab | `juego/Assets/_Proyecto/Prefabs/` | `pf_<asset>.prefab` |

- Nombres en minúsculas, sin tildes ni espacios, como dice [[Convenciones]].
- Dentro del `.blend`: objetos `<asset>_<pieza>` (`miga_abrigo`) y colecciones `Referencias`, `Blockout`, `Alto`, `Bajo`, `Rig`.
- El `-esculpido.blend` puede pesar cientos de MB y pasa por Git LFS, cuya cuota gratis es limitada. Guardarlo con `Compress` (en `File > Save As`) y subirlo solo cuando la etapa esté aprobada, no en cada guardado.
