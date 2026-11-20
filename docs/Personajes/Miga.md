# Miga

![[miga-vistas.png]]

## Quién es
Una niña del tamaño de una taza, perdida en la Casa Grande. Curiosa, terca y callada. Tiene miedo, pero sigue avanzando.

## Apariencia
- Cabeza grande, piernas delgadas.
- Pelo oscuro con flequillo de lado y dos moños despeinados con ligas rojas.
- Abrigo verde azulado que le queda enorme, con botones, un bolsillo y un parche cosido a mano.
- Bufanda roja con dos puntas: una corta al frente y una larga por la espalda.
- Mangas largas con el puño doblado.
- Calcetines blancos con rayas rojas, botas gastadas y una curita en la rodilla.
- Frasco de vidrio con tapa y asa, con [[Chispa]] dentro.

## Paleta
| Uso | Color |
|---|---|
| Abrigo | `#3E7C7B` |
| Sombra del abrigo | `#356B6A` |
| Bufanda | `#C8553D` |
| Pelo | `#2A3046` |
| Piel | `#E8C9A8` |
| Luz del frasco | `#E6F28A` |
| Botones y detalles | `#F4D9A0` |

## Qué puede hacer
Caminar, correr, agacharse, saltar, trepar, empujar y jalar objetos, tapar el frasco con la bufanda. Ver [[Mecanicas]].

## Notas de modelado
- Modelo estilizado de pocos polígonos; la silueta manda.
- Piezas separadas: cuerpo, abrigo, bufanda, frasco.
- La punta larga de la bufanda lleva huesos propios para moverse al correr.
- Frasco con material emisivo y una luz puntual adentro.
- Esqueleto humanoide para reutilizar animaciones.
- Solo necesita parpadeo; no habla.
- En Unity, Miga mide 1 unidad de alto y el mundo se construye gigante. Ver [[Pipeline]].

## Modelo 3D
![[miga-modelo-retrato.png]]

![[miga-modelo-vistas.png]]

- Mide 1 unidad hasta la coronilla (1.05 con los mechones), mira hacia `-Y` en Blender y tiene el origen en el piso.
- Unos 31 100 triángulos y 37 huesos, en pose en A (brazos a 34° de la vertical).
- Piezas, todas hijas del objeto vacío `Miga` y enlazadas a `Miga_Esqueleto`:

| Objeto | Qué incluye | Materiales |
|---|---|---|
| `Miga_Cuerpo` | Cabeza, orejas, nariz, cuello, torso con camiseta y short, brazos, manos con dedos, piernas, calcetines, botas con cordones, curita | `mat_miga_piel`, `mat_miga_detalles` |
| `Miga_Ojos` | Globos, párpados y pestañas. Tiene la forma `Parpadeo` (0 abierto, 1 cerrado) | `mat_miga_ojos`, `mat_miga_pelo`, `mat_miga_piel` |
| `Miga_Pelo` | Casco, flequillo, capas de mechones atrás, moños y ligas | `mat_miga_pelo`, `mat_miga_detalles` |
| `Miga_Abrigo` | Abrigo con forro, mangas con pliegues, bolsillo, parches, botones y cinta en la espalda | `mat_miga_abrigo`, `mat_miga_detalles` |
| `Miga_Bufanda` | Dos vueltas, nudo, punta corta y punta larga con flecos | `mat_miga_bufanda` |
| `Miga_Frasco` | Vidrio, tapa y asa | `mat_miga_vidrio`, `mat_miga_detalles` |
| `Miga_Chispa` | Luciérnaga con el abdomen emisivo | `mat_miga_chispa`, `mat_miga_detalles` |
| `Miga_Esqueleto` | Armadura con los 37 huesos | — |

- Texturas (`tex_miga_*.png`): piel con la cara pintada, ojos, pelo, abrigo y bufanda con mapa de normales, y un atlas de detalles (calcetines, botas, cordones, botones, ligas, curita, tapa, parches, camiseta y short).
- Ojos: grandes y oscuros como en la hoja de vistas, sin blanco, con un tono violeta apagado abajo y un solo reflejo pintado; material de poco brillo (`mat_miga_ojos`, rugosidad 0.38). Los párpados abiertos casi no tapan el ojo; el de arriba lleva la línea de pestañas y baja con `Parpadeo`.
- El cuerpo bajo el abrigo lleva camiseta y short. La mano derecha va cerrada sobre el asa del frasco; la izquierda, relajada.

### Esqueleto
![[miga-modelo-poses.png]]

- Los huesos del cuerpo usan los nombres de Unity Humanoid, para que Unity los asigne solo:

| Zona | Huesos |
|---|---|
| Tronco | `Hips`, `Spine`, `Chest`, `Neck`, `Head` |
| Brazos | `LeftShoulder`, `LeftUpperArm`, `LeftLowerArm`, `LeftHand` y los `Right...` |
| Piernas | `LeftUpperLeg`, `LeftLowerLeg`, `LeftFoot`, `LeftToes` y los `Right...` |

- Huesos extra, fuera del humanoide: se mueven a mano, por script o con física.

| Hueso | Para qué |
|---|---|
| `Bufanda_01` a `Bufanda_05` | Punta larga de la bufanda, cuelga de `Chest` |
| `BufandaFrente_01` a `BufandaFrente_03` | Punta corta del frente |
| `Mono.L`, `Mono.R` | Que los moños reboten |
| `Dedos.L`, `Dedos.R`, `Pulgar.L`, `Pulgar.R` | Abrir y cerrar cada mano (los cuatro dedos van juntos) |
| `Frasco` | Hijo de `RightHand`: el frasco cuelga y se balancea desde el puño |
| `Chispa` | Hijo de `Frasco`: mueve la luciérnaga dentro del frasco |

- Cada vértice sigue como mucho a 4 huesos, el límite por defecto de Unity.
- La falda del abrigo sigue en parte a los muslos, para que las piernas no la atraviesen al caminar.
- `Left` es su izquierda (`+X` en Blender).

### En Unity
1. Abrir el proyecto: `mod_miga.fbx` y las texturas se importan solos.
2. En el FBX, pestaña **Materials**: `Extract Materials` hacia `Assets/_Proyecto/Art/Materiales/`.
3. En `tex_miga_abrigo_normal` y `tex_miga_bufanda_normal`: `Texture Type = Normal map`.
4. `mat_miga_vidrio`: `Surface Type = Transparent`. `mat_miga_chispa`: activar `Emission`.
5. En el FBX, pestaña **Rig**: `Animation Type = Humanoid`, `Avatar Definition = Create From This Model`, **Apply**.
6. **Configure...**: revisar que los huesos salgan en verde y, como el modelo está en pose en A, usar `Pose > Enforce T-Pose` antes de **Done**.
7. Poner una `Point Light` color `#E6F28A` como hija del hueso `Chispa` (no del objeto `Miga_Chispa`, que ya no se mueve solo).
8. El parpadeo está en `Miga_Ojos > Skinned Mesh Renderer > BlendShapes > Parpadeo` (0 a 100).
9. `Miga_Esqueleto` llega con rotación `X = -90`: es normal en un FBX de Blender, no hay que corregirla.

### Decisiones
- 2026-11-16: el modelo base se genera por código (`generador/`). Si se retoca a mano en Blender, no volver a correr el generador: reconstruye todo desde cero.
- 2026-11-16: todas las piezas cuelgan directo de `Miga`. Con `Apply Transform`, el FBX descoloca los objetos anidados.
- 2026-11-16: las texturas viven en `juego/Assets/_Proyecto/Art/Texturas/` y el `.blend` las usa desde ahí, para no tener dos copias.
- 2026-11-16: ojos normales y mate en lugar de los ojos brillantes de la primera versión.
- 2026-11-17: se descartan los ojos normales (blanco e iris café): le daban cara de cansada. Vuelven los ojos oscuros de la primera versión, con menos brillo, un solo reflejo y los párpados para parpadear. Los scripts de la versión anterior quedan en `_respaldo-v2/`.
- 2026-11-17: `miga.blend` lleva las tres vistas de referencia en la colección `Referencias` (se ven con las teclas 1, Ctrl+3 y Ctrl+1). Las proporciones cuadran con la hoja; la diferencia es la pose en A de los brazos.
- 2026-11-16: el esqueleto y los pesos también salen del generador (`esqueleto.py`). Animar encima está bien; volver a correr `construir` borra lo animado.
- 2026-11-16: las mallas no son hijas del esqueleto: se deforman por el modificador `Esqueleto`, para mantener todo colgando directo de `Miga`.
- 2026-11-16: el frasco y Chispa van enlazados a un hueso cada uno, no como objetos hijos de la mano.
- 2026-11-16: sin huesos por dedo ni en los ojos. La mano se abre y cierra con `Dedos` y `Pulgar`; si hace falta más, se agregan después.
- Pendiente: comprobar en Unity que el avatar humanoide se arma bien, y hacer las animaciones (ver [[Inventario]]).

## Archivos
- Referencia: `docs/Referencias/Personajes/miga-vistas.png` y `.svg`
- Renders del modelo: `docs/Referencias/Personajes/miga-modelo-retrato.png`, `miga-modelo-vistas.png` y `miga-modelo-poses.png`
- Modelo: `arte-fuente/blender/personajes/miga/miga.blend`
- Recortes de referencia: `arte-fuente/blender/personajes/miga/referencias/`
- Generador: `arte-fuente/blender/personajes/miga/generador/`
- En el juego: `juego/Assets/_Proyecto/Art/Modelos/mod_miga.fbx` y `juego/Assets/_Proyecto/Art/Texturas/tex_miga_*.png`
