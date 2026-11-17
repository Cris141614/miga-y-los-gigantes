# Convenciones

## Nombres de archivos
- Minúsculas, sin tildes, sin espacios, con guiones: `costurera-mano.fbx`.
- Prefijo por tipo dentro de Unity:

| Tipo | Prefijo | Ejemplo |
|---|---|---|
| Modelo | `mod_` | `mod_miga.fbx` |
| Textura | `tex_` | `tex_miga_abrigo.png` |
| Material | `mat_` | `mat_miga_abrigo.mat` |
| Animación | `anim_` | `anim_miga_correr.fbx` |
| Prefab | `pf_` | `pf_costurera.prefab` |
| Efecto de sonido | `sfx_` | `sfx_tijeras_corte.wav` |
| Música | `mus_` | `mus_taller_tension.ogg` |
| Ambiente | `amb_` | `amb_taller.ogg` |
| Escena | `esc_` | `esc_nivel1_taller.unity` |

Las notas de esta bóveda son la excepción: llevan nombre legible.

## Scripts
- C#, una clase por archivo, nombre de clase igual al del archivo.
- Carpetas por sistema: `Jugador/`, `Criaturas/`, `Sistemas/`, `Camara/`, `UI/`.

## Git
- Ramas: `main` (estable), `develop` (trabajo), y una rama por issue con tipo y número: `feat/13-hilo-rojo`.
- Commits con Conventional Commits, en imperativo y minúscula: `feat:`, `fix:`, `art:`, `docs:`, `build:`, `ci:`, `chore:`, `refactor:`, `perf:`, `test:`.
- El título del PR sigue el mismo formato: con squash se convierte en el commit de `develop`.
- El paso a paso completo está en [[Flujo de trabajo]].
- Un commit por cambio con sentido; nunca subir la carpeta `Library/`.

## Bóveda
- Una nota por tema. Enlazar con doble corchete en vez de repetir.
- Las decisiones se escriben en la nota del tema, con fecha.
