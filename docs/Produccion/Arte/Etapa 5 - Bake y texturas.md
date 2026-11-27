# Etapa 5 - Bake y texturas

Parte de [[Pipeline de arte]]. Se pasa el detalle del alto al bajo y se pinta el color.

- **Entra:** el alto y el bajo aprobados, en `<asset>-esculpido.blend`.
- **Herramienta:** Blender con Cycles.
- **Sale:** `tex_<asset>_<pieza>[_mapa].png` en `juego/Assets/_Proyecto/Art/Texturas/`. El `.blend` las usa desde ahí, para no tener dos copias.

## Cómo
1. Motor de render en Cycles.
2. Por cada mapa, crear una imagen vacía del tamaño que pide [[Estandares de arte]]. Ponerla en un nodo `Image Texture` dentro del material del bajo: seleccionado y sin conectar.
3. Seleccionar el alto, después el bajo (el bajo queda activo). En `Bake`, activar `Selected to Active` y ajustar `Extrusion` o una `Cage` hasta que cubra el alto sin cruzarse.
4. Hornear los mapas:
   - **Normal:** espacio `Tangent`, `+X +Y +Z`.
   - **Ambient Occlusion.**
5. Color base:
   - pintado en `Texture Paint` sobre el bajo, o
   - con materiales de nodos horneados con `Diffuse`, dejando activo solo `Color`.
6. Guardar los PNG en la carpeta de Texturas. Normales, oclusión y metal se guardan como `Non-Color`.

## Lista para aprobar
- [ ] El mapa de normales no tiene ondas, bordes cortados ni manchas donde el rayo no llegó. Se revisa aplicado al bajo, con luz rasante.
- [ ] Las costuras de UV no se notan.
- [ ] El color base no tiene luces ni sombras pintadas.
- [ ] Los colores son los de la paleta de la hoja de detalles.
- [ ] Mapas, tamaños y nombres según [[Estandares de arte]].
- [ ] En la issue: captura en Unity con la luz del nivel.
