# Etapa 2 - Blockout

Parte de [[Pipeline de arte]]. Aquí se decide si el asset funciona en el juego antes de gastar horas en detalle.

- **Entra:** la hoja de [[Etapa 1 - Referencias 2D]] aprobada, cargada en la colección `Referencias` del `<asset>.blend`.
- **Sale:** la colección `Blockout` en `<asset>.blend` y un `mod_<asset>.fbx` gris de prueba, colocado en el nivel.

## Cómo
1. Armar el asset con formas simples (cubos, cilindros, esferas) siguiendo las vistas. Una pieza por parte: cabeza, torso, abrigo, tapa, patas.
2. Piso en el origen, 1 unidad = 1 m, escala aplicada.
3. Exportar el FBX con los ajustes de [[Pipeline]] y ponerlo en el nivel al lado de Miga.
4. Mirarlo con la cámara lateral del juego, a la distancia normal, y sacar una captura.

## Lista para aprobar
- [ ] Coincide con las tres vistas; la altura no se aleja más de un 2 % de la hoja.
- [ ] En el nivel tiene el tamaño correcto al lado de Miga.
- [ ] La silueta se entiende desde la cámara lateral.
- [ ] Personajes: hombros, codos, cadera y rodillas están donde dice la hoja, en pose en A.
- [ ] Escenario: Miga puede pasar, trepar o esconderse donde lo pide [[Nivel 1 - El Taller]]. Las medidas de juego mandan sobre el detalle.
- [ ] La captura desde la cámara del juego está en la issue.
