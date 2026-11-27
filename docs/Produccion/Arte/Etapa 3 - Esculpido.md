# Etapa 3 - Esculpido

Parte de [[Pipeline de arte]]. El modelo de alta resolución: de aquí salen los detalles que después se hornean en el mapa de normales. Los objetos pequeños se saltan esta etapa.

- **Entra:** el blockout de [[Etapa 2 - Blockout]] aprobado.
- **Herramienta:** Blender, modo Sculpt.
- **Sale:** `<asset>-esculpido.blend` con la colección `Alto`.

## Cómo
1. Copiar el blockout a `<asset>-esculpido.blend`. Unir las piezas que van pegadas y aplicar `Voxel Remesh` (`Ctrl+R` en Sculpt) para tener una malla pareja.
2. **Formas primarias** con poca resolución: volumen, anatomía, caída general de la ropa. Subir la resolución (remesh más fino o modificador `Multiresolution`) solo cuando la forma ya está bien.
3. **Formas secundarias:** pliegues, costuras, parches, bordes de tela.
4. **Formas terciarias:** poros, tejido, rasguños. Pueden ir directo en la textura en vez de esculpirse.
5. Las piezas separadas son objetos con nombre: `miga_abrigo`, `miga_bufanda`, `miga_frasco`.
6. Revisar con MatCap gris y girando la luz, desde las vistas de la hoja y desde la cámara del juego.

## Lista para aprobar
- [ ] Mide lo mismo que el blockout; el piso y la escala no se movieron.
- [ ] La silueta coincide con la hoja desde frente, lado y espalda.
- [ ] Los pliegues tienen lógica: caen por gravedad y salen de los puntos de tensión (hombros, codos, cinturón, costuras).
- [ ] Están los tres niveles de detalle, y el terciario no tapa las formas grandes desde la cámara del juego.
- [ ] La asimetría (parches, arrugas, desgaste) se agregó a propósito, después de terminar la parte simétrica.
- [ ] Sin agujeros, picos ni piezas que se atraviesan.
- [ ] Personajes: misma pose en A que usará el rig.
- [ ] El archivo se puede trabajar: hasta unos 5 millones de caras en total. Si Blender se traba, bajar la resolución de lo que no se ve.
- [ ] En la issue: capturas de frente, lado, espalda y 3/4 en MatCap gris, al lado de la hoja.
