# Mecánicas

## Movimiento
Caminar, correr, agacharse, saltar, trepar bordes, empujar y jalar objetos pequeños.
Correr hace ruido. Agacharse no.

### Cómo está hecho
Miga es una cápsula con `CharacterController`. La cámara mira de lado, pero Miga se mueve en las cuatro direcciones: izquierda y derecha en pantalla, y hacia el fondo y hacia la cámara, como en *Little Nightmares* (ver [[Vision]]). Gira suave y algo lento hacia donde camina, como con miedo (media vuelta en unos 0.6 s, frenando al final; campo *Tiempo Giro* = 0.2), y trepa y se agacha mirando en cualquier dirección.

| Valor | Cuánto |
|---|---|
| Caminar / correr / agachada | 1.6 / 3.2 / 0.8 m/s |
| Salto | 0.45 m |
| Trepar | Desde el piso, bordes de 0.3 a 1 m (su altura). Saltando se agarra de bordes de hasta unos 1.45 m. Más alto, no |
| Agachada | 0.6 m de alto; bajo un techo bajo no se puede parar |
| Empujar, jalar y mover de lado | 0.8 m/s con un objeto ligero, en cualquier dirección; más lento si pesa (campo *Ligereza* del objeto) |

- `Scripts/Jugador/ControlMiga.cs` mueve a Miga. Avisa a otros sistemas con `Corriendo`, `Agachada`, `Agarrado` y los eventos `Salto` y `Aterrizo`, que usarán el ruido y el hilo rojo.
- `Scripts/Sistemas/Empujable.cs` marca lo que se puede empujar y jalar. Miga lo agarra si lo tiene de frente, mientras se mantiene el botón, y no se da vuelta mientras lo tiene: lo lleva hacia donde se mueva (adelante lo empuja, atrás lo jala, a los lados lo lleva de lado). El objeto se desliza por el piso y se detiene justo al tocar otra cosa; si choca, Miga también se detiene, y si choca solo de un lado, se desliza a lo largo de la pared. Por ahora no cae si se empuja fuera de un borde.
- `Scripts/Jugador/EntradaMiga.cs` lee teclado y mando con los controles del [[GDD]]. Agacharse se mantiene apretado.
- Todos los valores se ajustan en el Inspector de `pf_miga`. Las pruebas están en `Tests/PlayMode/ControlMigaPruebas.cs`.

## La luz de Chispa
- El frasco ilumina un radio corto alrededor de Miga.
- Con luz se ven los peligros del piso: alfileres, huecos, hilos tensos.
- Los Guardadores ven la luz si está cerca.
- **Tapar el frasco** con la bufanda apaga la luz mientras se mantiene el botón. Miga camina más lento y casi a ciegas.

La decisión constante es: ver por dónde piso, o que no me vean.

### Cómo está hecho
`Scripts/Sistemas/LuzChispa.cs`, en `pf_miga`, crea al empezar una luz puntual (`Luz_Chispa`) a la altura del frasco, hija del modelo para que gire con Miga. No proyecta sombras: va dentro del modelo y el cuerpo de Miga taparía su propia luz.

| Valor | Cuánto |
|---|---|
| Radio | 2.5 m |
| Intensidad | 2 |
| Color | amarillo cálido |
| Apagarse o prenderse | 0.15 s |

- Tapar es la entrada `tapar` de `ControlMiga` (Q o gatillo izquierdo, en `EntradaMiga`). Mientras se mantiene:
  - `Tapando` está en true;
  - Miga camina a 1 m/s (campo *Velocidad Tapada*) y no puede correr;
  - la luz baja a 0.
- `LuzChispa.Encendida` dice si alumbra. La usarán los Guardadores para ver la luz ([[La Costurera]], #12).
- Para que la luz se note, el Nivel 1 está en penumbra: luz direccional en 0.25 y luz ambiente en 0.35. La iluminación final es la issue #28.
- Pruebas: `Tests/PlayMode/LuzChispaPruebas.cs`.
- Pendiente: que la luz tiemble cuando un Guardador está cerca ([[Chispa]]). Necesita a La Costurera (#12).

### Decisiones
- 2026-11-27: con el frasco tapado Miga no puede correr: va casi a ciegas.
- 2026-11-27: la luz no proyecta sombras, para que el modelo de Miga no tape su propia luz.

## El hilo rojo (Nivel 1)
- La bufanda de Miga está unida al carrete de [[La Costurera]].
- Caminar no lo tensa. Correr y saltar sí: ella lo siente y pasa a Alerta.
- Si el hilo se engancha en un objeto, hay que volver a soltarlo o queda corto.
- El objetivo del nivel es llegar a unas tijeras y cortarlo.

## Esconderse
Debajo de telas, dentro de carretes huecos, detrás de objetos. Escondida y con el frasco tapado, Miga no es detectable.

## Ruido
| Fuente | Nivel |
|---|---|
| Caminar agachada | Ninguno |
| Caminar | Bajo |
| Correr, saltar, caer | Medio |
| Tirar un objeto | Alto |

El ruido de la máquina de coser encendida tapa los niveles bajo y medio.

## Orden para programar
1. Movimiento y cámara.
2. Luz del frasco y tapar.
3. Ruido y estados de La Costurera.
4. Hilo rojo.
5. Esconderse y puntos de control.
