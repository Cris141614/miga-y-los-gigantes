# Generador de La Costurera

Scripts de Python que construyen el modelo de La Costurera, sus texturas, sus materiales y su esqueleto dentro de Blender.

Para regenerarlo, con `costurera.blend` abierto, en la pestaña **Scripting** de Blender:

```python
import bpy, os
G = bpy.path.abspath("//generador")
ns = {"__name__": "costurera", "__file__": os.path.join(G, "lib.py")}
for f in ("lib.py", "texturas.py", "modelo.py", "esqueleto.py", "construir.py", "vista.py"):
    exec(compile(open(os.path.join(G, f), encoding="utf-8").read(), f, "exec"), ns)
ns["construir"](pintar=True)      # borra la coleccion Costurera y la crea de nuevo
ns["guardar_y_exportar"]()        # guarda costurera.blend y exporta mod_costurera.fbx
```

Cuidado: `construir` borra todo lo que haya en la colección `Costurera`. Si retocaste el modelo a mano o ya lo animaste, no lo corras.

Para probar los pesos: `ns["posar"]("clavar")` (también `"alerta"` e `"inclinada"`) y `ns["reposo"]()` para volver.

| Archivo | Qué hace |
|---|---|
| `lib.py` | Mallas por anillos, materiales y pintura con numpy (copia de la de Miga) |
| `texturas.py` | Pinta las texturas `tex_costurera_*.png` y define las zonas UV |
| `modelo.py` | Todas las piezas, con las medidas tomadas de la hoja de vistas |
| `esqueleto.py` | Huesos, pesos de cada pieza y la armadura `Costurera_Esqueleto` |
| `construir.py` | Une todo, enlaza las mallas al esqueleto, guarda el `.blend` y exporta el FBX |
| `vista.py` | Luces, cámara, poses de prueba y renders de revisión |
