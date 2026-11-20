# Generador de Miga

Scripts de Python que construyen el modelo de Miga dentro de Blender: mallas, texturas, materiales, esqueleto y pesos.

Para regenerarlo, con `miga.blend` abierto, en la pestaña **Scripting** de Blender:

```python
import bpy, os
G = bpy.path.abspath("//generador")   # con miga.blend abierto
ns = {"__name__": "miga", "__file__": os.path.join(G, "lib.py")}
for f in ("lib.py", "texturas.py", "modelo_cabeza.py", "modelo_cuerpo.py", "esqueleto.py", "construir.py", "vista.py"):
    exec(compile(open(os.path.join(G, f), encoding="utf-8").read(), f, "exec"), ns)
ns["construir"](pintar=True)      # borra la coleccion Miga y la crea de nuevo
ns["guardar_y_exportar"]()        # guarda miga.blend y exporta mod_miga.fbx
```

Cuidado: `construir` borra todo lo que haya en la colección `Miga`, incluidas las animaciones que cuelguen de `Miga_Esqueleto`. Si retocaste el modelo a mano o ya animaste, no lo corras.

`construir` se revisa solo: si alguna malla queda con vértices sin peso o con grupos que no tienen hueso, falla con un mensaje en vez de dejar el modelo a medias.

| Archivo | Qué hace |
|---|---|
| `lib.py` | Mallas por anillos (con pesos y formas), materiales y pintura con numpy |
| `texturas.py` | Pinta las texturas `tex_miga_*.png` y define las zonas UV |
| `modelo_cabeza.py` | Cabeza, cara, ojos con párpados y pelo |
| `modelo_cuerpo.py` | Cuerpo, manos, piernas, botas, abrigo, bufanda, frasco y Chispa |
| `esqueleto.py` | Huesos, pesos de cada pieza y la armadura |
| `construir.py` | Une todo, guarda el `.blend` y exporta el FBX |
| `vista.py` | Luces, cámara, poses de prueba y renders de revisión |

## Probar el esqueleto

```python
ns["posar"]("caminar")            # tambien "T" y "trepar"; mueve los huesos para ver como deforma
ns["reposo"]()                    # vuelve a la pose en A y abre los ojos
```
