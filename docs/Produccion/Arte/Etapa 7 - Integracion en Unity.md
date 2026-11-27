# Etapa 7 - Integracion en Unity

Parte de [[Pipeline de arte]]. El asset entra al juego y se prueba donde se va a usar.

- **Entra:** FBX y texturas aprobados.
- **Sale:** `pf_<asset>.prefab` colocado en el nivel. En [[Inventario]] queda `en el juego`.

## Cómo
1. Exportar el FBX con los ajustes de [[Pipeline]]: `Apply Transform`, `Forward: -Z`, `Up: Y`.
2. En el import del FBX:
   - `Rig`: Humanoid, Generic o None según el asset;
   - materiales `mat_<asset>_<pieza>` con el shader URP Lit.
3. En el import de las texturas:
   - las `_normal` con `Texture Type = Normal map`;
   - las `_ao` y `_metal` con `sRGB` apagado.
4. Prefab `pf_<asset>` con colliders simples (cápsula, cajas). Nunca un `Mesh Collider` sobre el modelo detallado.
5. Ponerlo en el nivel y probarlo con Miga.
6. `Window > General > Test Runner`: correr EditMode y PlayMode.

## Lista para aprobar
- [ ] `EstandaresDeArtePruebas` y `EscalaDeLosModelosPruebas` en verde.
- [ ] La consola no muestra errores ni avisos del import.
- [ ] Se ve bien con la luz del nivel y desde la cámara lateral.
- [ ] Miga choca, se esconde o trepa donde debe.
- [ ] [[Inventario]] actualizado, y el PR cierra la issue con `Closes #`.
- [ ] En la issue: captura o clip del asset en el nivel.
