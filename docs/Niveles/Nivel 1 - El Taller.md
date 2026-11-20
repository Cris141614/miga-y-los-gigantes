# Nivel 1 - El Taller

El cuarto de costura de [[La Costurera]]. Duración objetivo: 5 a 8 minutos.

## Resumen
Miga despierta dentro de un costurero, descubre que está atada por un hilo rojo, cruza el taller sin tensarlo, corta el hilo con unas tijeras y escapa por un zócalo roto.

## Zonas

| # | Zona | Qué pasa | Qué aprende el jugador |
|---|---|---|---|
| 1 | El costurero | Miga despierta entre botones y carretes. Empuja la tapa para salir. | Moverse, empujar, la luz de Chispa |
| 2 | La mesa de corte | Cruza entre telas, alfileres y una regla que sirve de puente. Al correr, el hilo se tensa y La Costurera gira la cabeza. | Saltar, trepar, que correr la delata |
| 3 | La máquina de coser | La aguja sube y baja. Miga pisa el pedal para encenderla: el ruido tapa sus pasos y puede correr. | Usar el ruido a favor, pasar a ritmo |
| 4 | El armario de retazos | A oscuras entre muñecos remendados. La Costurera busca clavando los dedos. | Tapar el frasco, esconderse |
| 5 | Las tijeras | Miga trepa hasta las tijeras y corta el hilo. Silencio. La Costurera se da vuelta. | — |
| 6 | La huida | Persecución hasta el zócalo roto. | Todo junto |

## Plano de bloques grises
![[nivel1-plano.png]]

En metros, a la escala de La Costurera (17 veces Miga). Cada fila tiene la vista de lado arriba y la vista de arriba abajo, con la profundidad. El recorrido **baja**: empieza en la mesa de trabajo (12.75 m) y termina en el piso, metiéndose en la pared. Mide unos 137 m de largo.

### La banda donde camina Miga
Miga va a la izquierda y a la derecha (x), y también hacia el fondo y hacia la cámara (z). Camina dentro de una banda de **6 m de fondo** (z de -3 a 3), seis veces su altura: alcanza para rodear cosas, esconderse detrás y elegir camino sin perder la cámara de lado, que la sigue también en profundidad. Los muebles son más anchos que la banda (las mesas miden 15 m de fondo), así que se ven inmensos aunque Miga nunca llegue a sus bordes.

Paredes invisibles:
- `Limite_Frente` y `Limite_Fondo`: los bordes de la banda en todo el nivel. No se puede caer de la mesa hacia la cámara ni hacia el fondo.
- `Limite_Inicio` y `Limite_Final`: los extremos, en x = 0 y x = 137.
- `Limite_Regla_Frente` y `Limite_Regla_Fondo`: sobre el hueco entre las dos mesas. La regla es la única forma de cruzar y no se puede caer por los lados.
- `Costurero_Pared_Frente`: la pared del costurero que da a la cámara es invisible, como en una casa de muñecas. Se ve a Miga adentro, pero no se sale por ahí. El armario directamente no tiene pared del frente.

| Zona | Dónde | Recorrido y profundidad |
|---|---|---|
| 1 | Costurero de 2.55 m sobre la mesa de corte | Caja de 5 × 3.4 m. Dos carretes (0.85 y 1.7 m), del lado de la cámara, sirven de escalera para salir. La tapa queda medio abierta hasta que se pueda empujar |
| 2 | Mesa de corte, 30 m | Tela (0.6) y alfileres tumbados que tapan parte de la banda: se saltan o se rodean. Después, una fila de rollos de 1.6 m (no se trepa) separa **dos caminos**: por el fondo, agachada bajo una tela colgante; por el frente, junto a un montón de telas para esconderse. Se juntan en la regla, que mide 0.85 m de ancho |
| 3 | Mesa de la máquina | Pedal (3 m de ancho), base de la máquina (0.85) de lado a lado bajo la aguja, y 4 cajones abiertos como escalera hasta el piso. La silueta de La Costurera queda al fondo, fuera de la banda |
| 4 | Armario, 17 m de ancho | Se entra por la rendija de abajo (1.2). Tres montones de retazos (1.2) en zigzag: al frente, al fondo y otra vez al frente. Los muñecos de 5 m quedan más atrás, fuera del camino |
| 5 | Torre junto al armario | 5 escalones de 1 m, de 3 m de fondo, hasta las tijeras, a 5 m |
| 6 | Piso | Dedal (0.34), carrete de pie que tapa la mitad del fondo (0.85), mesita de lado a lado para pasar agachada (0.75), botones (0.25), carrete tumbado de lado a lado (1) y el zócalo roto: un hueco de 1.5 m de ancho y 0.9 de alto en el centro de la pared |

Medidas que respeta todo el plano: Miga trepa hasta 1 m desde el piso y hasta unos 1.45 m saltando; pasa agachada por debajo de 0.75 m. Ver [[Mecanicas]].

La escena `esc_nivel1_taller` se arma desde Unity con el menú `Miga > Construir Nivel 1 en bloques grises` (`Scripts/Editor/ConstruirNivel1.cs`). Volver a correrlo reemplaza la escena: lo que se ajuste a mano después se pierde.

## Ritmo
Calma (1) → tensión baja (2) → respiro con truco (3) → miedo (4) → decisión (5) → carrera (6).

## Momentos que deben quedar
- La primera vez que se ve a La Costurera completa: de espaldas, cosiendo, ocupando toda la pantalla.
- El hilo rojo cruzando el nivel entero desde el principio, sin explicación.
- Los muñecos del armario tienen parches iguales al del abrigo de Miga.
- Al cortar el hilo, la bufanda queda más corta. Ese cambio se conserva.

## Decisiones
- 2026-11-19: el nivel empieza arriba, en la mesa de trabajo, y va bajando hasta el piso. Al revés serían unas 13 trepadas seguidas.
- 2026-11-19: el pedal de la máquina va sobre la mesa, antes de la aguja, para que Miga lo pise y pase con el ruido.
- 2026-11-19: los bloques grises se generan con un script de editor; después se ajustan a mano.
- 2026-11-20: el nivel tiene profundidad. Miga camina en una banda de 6 m de fondo cerrada con paredes invisibles, y las mesas miden 15 m de fondo para que se sientan inmensas.
- 2026-11-20: en la zona 2 el camino se separa en dos (agachada por el fondo o escondida por el frente) y se junta otra vez en la regla.
- 2026-11-20: el costurero y el armario se ven como casa de muñecas: sin pared del frente, para ver a Miga adentro.

## Final del nivel
Miga cae del otro lado de la pared, sola y a oscuras. Chispa vuelve a brillar. A lo lejos se oye otro cuarto.

Este es el final de la rebanada jugable (fase 1). En el capítulo 1 completo el taller tiene más zonas, y antes de escapar Miga derrota a La Costurera, de una forma **por definir**. Ver [[Vision]].

## Qué se necesita construir
La lista completa con estados está en [[Inventario]].

- **Personajes:** Miga, La Costurera, Chispa.
- **Escenario:** costurero, mesa de corte, máquina de coser con pedal, armario, tijeras grandes, zócalo roto.
- **Objetos:** carretes, botones, alfileres, dedal, regla, telas, muñecos remendados.
- **Sonido:** máquina de coser, tijeras, agujas en madera, tarareo, hilo tensándose, pasos de Miga, ambiente del cuarto.

## Orden de trabajo
1. Bloques grises de las 6 zonas, jugable de principio a fin.
2. Movimiento, luz e hilo.
3. La Costurera con sus estados.
4. Modelos finales, uno por zona.
5. Sonido y luz.
