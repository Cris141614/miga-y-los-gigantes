# Etapa 6 - Rig y animacion

Parte de [[Pipeline de arte]]. Solo para lo que se mueve: personajes, Guardadores y objetos con partes móviles.

- **Entra:** el bajo texturizado de [[Etapa 5 - Bake y texturas]], copiado a `<asset>.blend` con `File > Append`.
- **Sale:**
  - el esqueleto y los pesos en `<asset>.blend`;
  - `mod_<asset>.fbx` con esqueleto;
  - una animación por archivo: `anim_<asset>_<accion>.fbx`.

## Cómo
1. Crear el `Armature`.
   - Miga y cualquier personaje con cuerpo humano: los huesos que Unity necesita para `Humanoid` (cadera, columna, pecho, cuello, cabeza, brazos, manos, piernas y pies).
   - Criaturas como La Costurera: `Generic`.
2. Huesos con lado en el nombre: `.L` y `.R`.
3. Pesos: `Ctrl+P > With Automatic Weights`, y después corregir pintando pesos. Al terminar: `Weights > Limit Total` en 4 y `Normalize All`.
4. Las animaciones de la lista de [[Inventario]], cada una en su propia `Action`, y exportarlas a un FBX por animación.

## Lista para aprobar
- [ ] Las poses extremas no rompen la malla: agacharse, brazos arriba, girar la cabeza, trepar. Sin aplastamientos ni piezas que se atraviesan.
- [ ] Máximo 4 huesos por vértice, con pesos normalizados.
- [ ] Miga: en Unity, `Rig > Animation Type = Humanoid > Configure` sin huesos en rojo.
- [ ] Los ciclos (reposo, caminar, correr) cierran sin salto.
- [ ] Al moverse en el juego, los pies no patinan: la velocidad de la animación coincide con la del movimiento.
- [ ] `EscalaDeLosModelosPruebas` sigue en verde.
- [ ] En la issue: clip corto con las poses extremas y los ciclos.
