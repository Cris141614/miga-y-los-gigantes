# Etapa 1 - Referencias 2D

Parte de [[Pipeline de arte]]. Siempre va primero: nada se modela sin una hoja aprobada.

- **Entra:** la descripción del asset en su nota ([[Miga]], [[La Costurera]], [[Nivel 1 - El Taller]]).
- **Sale:** `<asset>-vistas.png` (y `.svg` si se dibujó en vectores) y `<asset>-detalles.png`, en `docs/Referencias/`.

## Cómo
1. **Silueta.** Probar varias siluetas rellenas de negro y quedarse con la que se reconoce sin ningún detalle.
2. **Hoja de vistas.** Frente, lado y espalda, sin perspectiva, una junto a otra. Líneas guía horizontales que crucen las tres vistas: piso, rodillas, cintura, hombros, barbilla y punta de la cabeza. Los personajes van en la misma pose en A que usará el rig.
3. **Vista 3/4** para entender los volúmenes.
4. **Hoja de detalles.**
   - Piezas sueltas en grande: botones, frasco, costuras, cierres.
   - Qué material es cada parte: tela, piel, metal, madera.
   - Paleta con el código hex de cada color.
5. **Escala.** El asset dibujado al lado de Miga (1 m), con su altura en metros.
6. Enlazar las hojas en la nota del asset con `![[<asset>-vistas.png]]` y cargarlas en Blender como dice [[Pipeline]].

Un objeto pequeño puede tener solo frente, lado y arriba, con su tamaño junto a Miga.

## Lista para aprobar
- [ ] La silueta en negro se reconoce y no se confunde con la de otro personaje u objeto.
- [ ] Las líneas guía coinciden en las tres vistas.
- [ ] Lo que aparece en una vista aparece en las otras: nada sale en el frente y desaparece de lado.
- [ ] Están la vista 3/4, los detalles, los materiales y la paleta.
- [ ] La altura en metros está marcada junto a Miga.
- [ ] Fondo plano, sin sombras proyectadas, para poder cargarla en Blender.
- [ ] La hoja está enlazada en la nota del asset.
