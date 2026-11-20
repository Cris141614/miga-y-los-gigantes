# Inventario

Control de todo lo que necesita el juego. Estados: `pendiente`, `en proceso`, `listo`, `en el juego`.

## Personajes

| Elemento | Referencia | Modelo | Esqueleto | En Unity | Estado |
|---|---|---|---|---|---|
| Miga | `miga-vistas.png` | `miga.blend` | `Miga_Esqueleto` (humanoide, 37 huesos) | `mod_miga.fbx` | en proceso (falta probarla en Unity y animar) |
| La Costurera | `costurera-vistas.png` | `costurera.blend` | `Costurera_Esqueleto` (genérico, 27 huesos) | `mod_costurera.fbx` | en proceso (falta probarla en Unity y animar) |
| Chispa | — | dentro de `miga.blend` | no aplica | dentro de `mod_miga.fbx` | en proceso |

## Animaciones

| Personaje | Animación | Estado |
|---|---|---|
| Miga | Reposo | pendiente |
| Miga | Caminar | pendiente |
| Miga | Correr | pendiente |
| Miga | Agacharse y caminar agachada | pendiente |
| Miga | Saltar y caer | pendiente |
| Miga | Trepar borde | pendiente |
| Miga | Empujar y jalar | pendiente |
| Miga | Tapar el frasco | pendiente |
| La Costurera | Coser | pendiente |
| La Costurera | Girar la cabeza | pendiente |
| La Costurera | Tirar del hilo | pendiente |
| La Costurera | Clavar los dedos | pendiente |
| La Costurera | Perseguir | pendiente |

## Escenario del Nivel 1

| Elemento | Zona | Estado |
|---|---|---|
| Nivel en bloques grises con profundidad (`esc_nivel1_taller`) | 1 a 6 | listo |
| Costurero con tapa | 1 | pendiente |
| Mesa de corte | 2 | pendiente |
| Regla de madera | 2 | pendiente |
| Máquina de coser con pedal | 3 | pendiente |
| Armario de retazos | 4 | pendiente |
| Tijeras grandes | 5 | pendiente |
| Pared con zócalo roto | 6 | pendiente |

## Objetos

| Elemento | Estado |
|---|---|
| Carretes de hilo | pendiente |
| Botones | pendiente |
| Alfileres | pendiente |
| Dedal | pendiente |
| Telas | pendiente |
| Muñecos remendados | pendiente |
| Hilo rojo | pendiente |

## Sonido

| Archivo | Tipo | Estado |
|---|---|---|
| `sfx_miga_pasos` | Efecto | pendiente |
| `sfx_miga_salto` | Efecto | pendiente |
| `sfx_frasco_tapar` | Efecto | pendiente |
| `sfx_hilo_tension` | Efecto | pendiente |
| `sfx_tijeras_corte` | Efecto | pendiente |
| `sfx_agujas_madera` | Efecto | pendiente |
| `sfx_maquina_coser` | Efecto en bucle | pendiente |
| `sfx_costurera_tarareo` | Efecto | pendiente |
| `amb_taller` | Ambiente | pendiente |
| `mus_taller_tension` | Música | pendiente |
| `mus_taller_persecucion` | Música | pendiente |

## Scripts

| Sistema | Estado |
|---|---|
| Movimiento de Miga | en proceso (cápsula lista, falta animar) |
| Cámara lateral | listo (bloques grises) |
| Luz del frasco | pendiente |
| Ruido | pendiente |
| Estados de La Costurera | pendiente |
| Hilo rojo | pendiente |
| Escondites | pendiente |
| Puntos de control | pendiente |
