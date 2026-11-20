# La Costurera

![[costurera-vistas.png]]

## Quién es
Una [[Guardadores|Guardadora]] que colecciona cosas rotas para remendarlas, quieran o no. Para ella Miga es una muñeca descosida.

## Apariencia
- Gigante delgada y encorvada, con brazos que casi llegan al piso.
- Cada dedo es una aguja.
- Cara tapada por una tela cosida, atada por detrás, con dos botones distintos por ojos y la boca remendada con hilo rojo.
- Moño apretado lleno de alfileres.
- Cinta métrica colgada del cuello y tijeras colgando del cinto.
- Vestido de retazos; por la espalda va cerrado con cruces de hilo rojo.

## Paleta
| Uso | Color |
|---|---|
| Vestido | `#4F4059` |
| Sombra del vestido | `#43364C` |
| Piel | `#B9B6A4` |
| Tela de la cara | `#D9D0BC` |
| Hilo | `#C8553D` |
| Agujas y tijeras | `#C5CAD6` |
| Pelo | `#6B6775` |

## Cómo percibe
- **Casi no ve.** Solo distingue la luz de [[Chispa]] a corta distancia.
- **Oye** golpes, carreras y objetos que caen.
- **Siente el hilo rojo** que la une a la bufanda de Miga: cada tirón le dice hacia dónde.

## Comportamiento (estados)
| Estado | Qué hace | Cómo se sale |
|---|---|---|
| Cosiendo | Trabaja de espaldas, ignora todo | Ruido fuerte o tirón del hilo |
| Alerta | Gira la cabeza hacia el último ruido o tirón | Silencio por unos segundos |
| Tirar del hilo | Jala el hilo y arrastra a Miga hacia ella | Miga se agarra de algo o el hilo se engancha |
| Búsqueda | Clava los dedos en la zona, un golpe a la vez | No encuentra nada |
| Persecución | Solo al final, cuando Miga corta el hilo | Miga escapa por el zócalo |

Cada golpe de la búsqueda se anuncia: levanta la mano, pausa, y clava.

## Sonidos
Máquina de coser lejana, tijeras, agujas contra madera, un tarareo sin melodía, el hilo al tensarse.

## Notas de modelado
- La joroba y el cuello hacia adelante definen la silueta: revisar siempre la vista de lado.
- Manos como piezas separadas, con un hueso por aguja.
- La tela de la cara es una malla aparte, para poder moverla un poco al respirar.
- El vestido no necesita piernas debajo.

## Modelo 3D
![[costurera-modelo-retrato.png]]

![[costurera-modelo-vistas.png]]

- Mide 17 unidades hasta la punta del moño (17.75 con los alfileres), mira hacia `-Y` en Blender y tiene el origen en el piso.
- Unos 18 300 triángulos y 27 huesos. Las proporciones salen medidas de la hoja de vistas.
- Piezas, todas hijas del objeto vacío `Costurera` y enlazadas a `Costurera_Esqueleto`:

| Objeto | Qué incluye | Materiales |
|---|---|---|
| `Costurera_Cuerpo` | Cabeza, orejas, cuello hacia adelante y antebrazos | `mat_costurera_piel` |
| `Costurera_Cara` | Tela de la cara con la boca remendada, los dos botones y las tiras atadas por detrás | `mat_costurera_cara`, `mat_costurera_detalles` |
| `Costurera_Pelo` | Casco tirante, moño enrollado y 8 alfileres | `mat_costurera_pelo`, `mat_costurera_metal`, `mat_costurera_detalles` |
| `Costurera_Vestido` | Vestido de retazos con joroba, mangas, cuello, cinturón, 9 parches y las cruces rojas de la espalda | `mat_costurera_vestido`, `mat_costurera_detalles` |
| `Costurera_Accesorios` | Cinta métrica al cuello y tijeras colgando del cinto | `mat_costurera_detalles`, `mat_costurera_metal` |
| `Costurera_Mano_D`, `Costurera_Mano_I` | Mano y cuatro agujas por dedos | `mat_costurera_piel`, `mat_costurera_metal` |
| `Costurera_Esqueleto` | Armadura con los 27 huesos | — |

- Texturas (`tex_costurera_*.png`): tela de la cara, pelo, vestido con mapa de normales y un atlas de detalles (botones, cinta métrica, parches, hilo, cinturón, alfileres).

### Esqueleto
![[costurera-modelo-esqueleto.png]]

- No tiene piernas, así que en Unity va como rig **Generic** (el Humanoid las exige). Sus animaciones son solo de ella.
- La cadena del cuerpo nace en el piso: la base del vestido no se despega y todo lo de arriba se dobla sobre ella.

| Zona | Huesos | Para qué |
|---|---|---|
| Vestido | `Falda_01`, `Falda_02` | Mecer la falda; `Falda_01` es la raíz |
| Tronco | `Hips`, `Spine`, `Chest` | Encorvarse: la joroba se dobla con `Spine` y `Chest` |
| Cuello | `Neck`, `Neck_02` | Cuello largo hacia adelante, en dos tramos para que gire suave |
| Cabeza | `Head` | Girar la cabeza (estado Alerta) |
| Cara | `Cara` | Hija de `Head`: mueve la tela de la cara al respirar |
| Moño | `Mono` | Hijo de `Head`: que el moño y los alfileres reboten |
| Brazos | `LeftShoulder`, `LeftUpperArm`, `LeftLowerArm`, `LeftHand` y los `Right...` | El codo queda a media manga |
| Agujas | `Aguja_1.L` a `Aguja_4.L` y las `.R` | Un hueso por aguja, de afuera hacia adentro: abrir y cerrar la mano |
| Tijeras | `Tijeras` | Hijo de `Hips`: las tijeras cuelgan del cinto y se balancean |

- Cada vértice sigue como mucho a 4 huesos, el límite por defecto de Unity.
- La axila del vestido sigue a medias al brazo, para que no se rompa al levantarlo.
- `Left` es su izquierda (`+X` en Blender).
- Poses de prueba en `generador/vista.py`: `posar("alerta")`, `posar("inclinada")`, `posar("clavar")` y `reposo()`.

### En Unity
1. Abrir el proyecto: `mod_costurera.fbx` y las texturas se importan solos.
2. En el FBX, pestaña **Materials**: `Extract Materials` hacia `Assets/_Proyecto/Art/Materiales/`.
3. En `tex_costurera_vestido_normal`: `Texture Type = Normal map`.
4. `mat_costurera_metal`: revisar que `Metallic` esté en 1 y `Smoothness` cerca de 0.7.
5. En el FBX, pestaña **Rig**: `Animation Type = Generic`, `Avatar Definition = Create From This Model`, `Root node = None`, **Apply**.
6. `Costurera_Esqueleto` llega con rotación `X = -90`: es normal en un FBX de Blender, no hay que corregirla.

### Decisiones
- 2026-11-16: el modelo base se genera por código (`generador/`). Si se retoca a mano en Blender, no volver a correr el generador.
- 2026-11-16: la tela de la cara y las manos son mallas aparte, como piden las notas de modelado.
- 2026-11-16: el generador usa su propia copia de `lib.py`, para no depender del de Miga mientras se trabaja en su esqueleto.
- 2026-11-17: esqueleto de 27 huesos con rig Generic, porque no tiene piernas. Los brazos y el tronco usan igual los nombres de Unity, para leerlos como los de Miga.
- 2026-11-17: el esqueleto y los pesos salen del generador (`esqueleto.py`). Animar encima está bien; volver a correr `construir` borra lo animado.
- 2026-11-17: las mallas no son hijas del esqueleto: se deforman por el modificador `Esqueleto`, igual que en Miga.
- Pendiente: probarla en Unity, animaciones de sus estados (ver [[Inventario]]), y más resolución en la tela del vestido para verla desde la altura de Miga.

## Archivos
- Referencia: `docs/Referencias/Personajes/costurera-vistas.png` y `.svg`
- Renders del modelo: `docs/Referencias/Personajes/costurera-modelo-retrato.png`, `costurera-modelo-vistas.png` y `costurera-modelo-esqueleto.png`
- Modelo: `arte-fuente/blender/personajes/costurera/costurera.blend`
- Recortes de referencia: `arte-fuente/blender/personajes/costurera/referencias/`
- Generador: `arte-fuente/blender/personajes/costurera/generador/`
- En el juego: `juego/Assets/_Proyecto/Art/Modelos/mod_costurera.fbx` y `juego/Assets/_Proyecto/Art/Texturas/tex_costurera_*.png`
