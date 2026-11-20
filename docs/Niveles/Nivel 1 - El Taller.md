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

Vista de lado, en metros, a la escala de La Costurera (17 veces Miga). El recorrido **baja**: empieza en la mesa de trabajo (12.75 m) y termina en el piso, metiéndose en la pared. Mide unos 137 m.

| Zona | Dónde | Recorrido |
|---|---|---|
| 1 | Costurero de 2.55 m sobre la mesa de corte | Dos carretes de 0.85 m y la pared de la caja. La tapa queda medio abierta hasta que se pueda empujar |
| 2 | Mesa de corte, 30 m | Tela (0.6), alfileres tumbados (0.17), rollo de tela (1), montón de telas (1.2, salto con agarre) y la regla de 5 m como puente |
| 3 | Mesa de la máquina | Pedal sobre la mesa, base de la máquina (0.85) bajo la aguja, y 4 cajones abiertos como escalera hasta el piso |
| 4 | Armario, 17 m de ancho | Se entra por la rendija de abajo (1.2). Compartimento de 6.8 m de alto, con retazos (1.2) y muñecos de 5 m al fondo |
| 5 | Torre junto al armario | 5 escalones de 1 m hasta las tijeras, a 5 m |
| 6 | Piso | Dedal (0.34), carretes (0.85 y 1), botones (0.25), mesita para pasar agachada (0.75) y el zócalo roto (0.9, agachada) |

Dos paredes invisibles (`Limite_Inicio` en x = 0 y `Limite_Final` en x = 137) cierran el nivel: no se puede caer de la mesa por la izquierda ni seguir de largo al final.

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
