# Documento de diseño (GDD)

## Concepto
Juego 3D de suspenso con cámara lateral. Una niña diminuta cruza los cuartos de una casa de gigantes. Sin diálogo y sin texto.

## Pilares
1. **Soy pequeña.** Todo lo cotidiano es enorme y peligroso.
2. **La luz me ayuda y me delata.**
3. **Se entiende sin palabras.**

## Alcance de la primera versión
Un solo nivel jugable de 5 a 8 minutos: [[Nivel 1 - El Taller]], con [[La Costurera]].
No se empieza otro nivel hasta que este se pueda jugar de principio a fin.

## Cámara
- Lateral fija, con Cinemachine.
- Baja, a la altura de Miga, para que todo se vea grande.
- Se aleja en los momentos en que aparece un Guardador completo.

## Controles
| Acción | Teclado | Mando |
|---|---|---|
| Moverse | A / D | Stick izquierdo |
| Correr | Shift | Gatillo derecho |
| Agacharse | Ctrl | B |
| Saltar y trepar | Espacio | A |
| Agarrar y empujar | E (mantener) | X (mantener) |
| Tapar el frasco | Q (mantener) | Gatillo izquierdo |

## Reglas
- No hay barra de vida. Si un Guardador atrapa a Miga, se vuelve al último punto de control.
- Los puntos de control son automáticos, uno por zona.
- No hay inventario ni interfaz en pantalla.

## Plataforma
PC primero. Proyecto de Unity con plantilla 3D (URP).

## Relacionado
[[Mecanicas]] · [[Lore]] · [[Pipeline]]
