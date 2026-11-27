# Etapa 4 - Retopologia y UVs

Parte de [[Pipeline de arte]]. El modelo bajo es el que entra al juego: tiene que verse como el alto, deformarse bien y estar dentro de su límite.

- **Entra:** el esculpido de [[Etapa 3 - Esculpido]] aprobado. Un objeto pequeño entra directo desde [[Etapa 2 - Blockout]].
- **Sale:** la colección `Bajo` en `<asset>-esculpido.blend`, con UVs.

## Cómo
1. En `<asset>-esculpido.blend`, crear el bajo encima del alto:
   - snapping a `Face Project` y el overlay `Retopology`, o
   - un modificador `Shrinkwrap` apuntando al alto.

   En objetos rígidos (sin rig) se puede partir de un `Remesh` y limpiarlo a mano.
2. Marcar costuras de UV (`Mark Seam`) en zonas que no se ven: debajo de los brazos, por dentro, en los bordes de la ropa.
3. `Unwrap`, revisar con la textura de cuadros y acomodar las islas con `Pack Islands`, dejando margen.

## Lista para aprobar
- [ ] Los triángulos están dentro del límite de [[Estandares de arte]].
- [ ] Desde la cámara del juego la silueta del bajo es igual a la del alto; los detalles finos los pondrá el mapa de normales.
- [ ] Personajes:
  - casi todo cuadriláteros, sin n-gons;
  - 3 loops en hombros, codos, muñecas, cadera y rodillas;
  - loops alrededor de ojos y boca.
- [ ] Sin vértices sueltos, caras duplicadas ni normales al revés: `Mesh > Clean Up`, y el overlay `Face Orientation` todo en azul.
- [ ] UVs:
  - sin islas encimadas, salvo piezas espejadas a propósito y desplazadas fuera del cuadro;
  - sin estiramiento en la textura de cuadros;
  - costuras escondidas;
  - margen de al menos 8 px a 2048 o 16 px a 4096;
  - densidad de texel pareja.
- [ ] Bordes duros (`Mark Sharp`) solo donde también hay costura de UV.
