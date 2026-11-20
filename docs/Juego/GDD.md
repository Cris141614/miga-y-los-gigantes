# Documento de diseño (GDD)

## Concepto
Juego 3D de suspenso con cámara lateral. Una niña pequeña cruza los cuartos de una casa de gigantes. Sin diálogo y sin texto.
Referencia: *Little Nightmares*. La cámara mira de lado, pero Miga también se mueve en profundidad, en un mundo lineal pero semiabierto. El rumbo completo está en [[Vision]].

## Pilares
1. **Soy pequeña.** Todo lo cotidiano es enorme y peligroso.
2. **La luz me ayuda y me delata.**
3. **Se entiende sin palabras.**

## Alcance de la primera versión
Fase 1 de la [[Vision]]: una rebanada jugable de unos 10 minutos, las 6 zonas de [[Nivel 1 - El Taller]] con [[La Costurera]], con movimiento en profundidad.
No se empieza otro nivel hasta que este se pueda jugar de principio a fin.

## Cámara
- Lateral fija, con Cinemachine.
- Baja, a la altura de Miga, para que todo se vea grande.
- Se aleja en los momentos en que aparece un Guardador completo.

### Cómo está hecha
- Cinemachine. `Camara_Miga` sigue a Miga a 7 m, a la altura de su pecho y un poco inclinada hacia arriba (FOV 40), con un seguimiento suave.
- Las cámaras abiertas se activan con una `ZonaDeCamara` (`Scripts/Camara/`): una caja que, mientras Miga está dentro, enciende otra cámara. Cinemachine hace la transición en 2 s.
- En el [[Nivel 1 - El Taller]] hay dos: al cruzar la regla (se ve a La Costurera completa por primera vez) y en la huida (la cámara se aleja y deja espacio detrás de Miga).
- La herramienta `Miga > Construir Nivel 1 en bloques grises` las arma junto con el nivel.
- `AsomarCamara` deja asomar la cámara que sigue a Miga (18° arriba y abajo, 12° a los lados) y al soltar vuelve sola. No gira libre, para no romper el encuadre de lado.

## Controles
| Acción | Teclado | Mando |
|---|---|---|
| Moverse (A/D a los lados, W/S hacia el fondo y hacia la cámara) | WASD | Stick izquierdo |
| Correr | Shift | Gatillo derecho |
| Agacharse | Ctrl | B |
| Saltar y trepar | Espacio | A |
| Agarrar y empujar | E (mantener) | X (mantener) |
| Tapar el frasco | Q (mantener) | Gatillo izquierdo |
| Asomar la cámara | Flechas | Stick derecho |

## Reglas
- No hay barra de vida. Si un Guardador atrapa a Miga, se vuelve al último punto de control.
- Los puntos de control son automáticos, uno por zona.
- No hay inventario ni interfaz en pantalla.

## Plataforma
PC primero. Proyecto de Unity con plantilla 3D (URP).

## Relacionado
[[Mecanicas]] · [[Lore]] · [[Pipeline]]
