# Carga las hojas de vistas de un personaje como imagenes de referencia, alineadas con el origen.
# Uso, con el .blend del personaje abierto, en la pestana Scripting de Blender:
#   exec(open(bpy.path.abspath("//../../referencias.py"), encoding="utf-8").read()); cargar("miga")
# Frente: tecla 1. Lado: Ctrl+3 (mira de izquierda a derecha). Espalda: Ctrl+1.
# Las imagenes solo se ven en esas vistas ortograficas y no se pueden seleccionar por accidente.
import bpy, math, os

# Medidas de las hojas en docs/Referencias/Personajes (pixeles del recorte de cada vista)
HOJAS = {
    # alto: metros desde el piso hasta la linea "cabeza"; px_alto: pixeles entre esas dos lineas
    "miga": dict(alto=1.0, px_alto=600.0, ancho=600, largo=789, piso=17.5, centro=300.0, distancia=0.6),
    "costurera": dict(alto=17.0, px_alto=1132.0, ancho=840, largo=1373, piso=33.5, centro=420.0, distancia=10.0),
}
# vista: (rotacion en grados, direccion hacia donde se aleja la imagen, detras del personaje)
VISTAS = {
    "frente": ((90, 0, 0), (0, 1, 0)),
    "lado": ((90, 0, -90), (1, 0, 0)),
    "espalda": ((90, 0, 180), (0, -1, 0)),
}


def cargar(personaje):
    h = HOJAS[personaje]
    mpp = h["alto"] / h["px_alto"]
    col = bpy.data.collections.get("Referencias") or bpy.data.collections.new("Referencias")
    if col.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(col)
    for o in list(col.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    if not bpy.data.filepath:
        raise RuntimeError("Guarda primero el .blend en arte-fuente/blender/personajes/<personaje>/")
    carpeta = bpy.path.abspath("//referencias")                      # junto al .blend del personaje
    for vista, (rot, atras) in VISTAS.items():
        ruta = os.path.join(carpeta, f"{personaje}-{vista}.png")
        img = bpy.data.images.load(ruta, check_existing=True)
        ob = bpy.data.objects.new(f"Ref_{personaje}_{vista}", None)
        ob.empty_display_type = "IMAGE"
        ob.data = img
        ob.empty_display_size = max(h["ancho"], h["largo"]) * mpp      # el lado mas largo de la imagen, en metros
        ob.empty_image_offset = (-h["centro"] / h["ancho"], -h["piso"] / h["largo"])   # piso y centro en el origen
        ob.rotation_euler = [math.radians(a) for a in rot]
        ob.location = [c * h["distancia"] for c in atras]
        ob.empty_image_side = "FRONT"                                    # solo se ve desde su lado: frente y espalda no se mezclan
        ob.show_empty_image_only_axis_aligned = True
        ob.show_empty_image_perspective = False
        ob.use_empty_image_alpha = True
        ob.color[3] = 0.55
        ob.hide_select = True
        ob.hide_render = True
        col.objects.link(ob)
    bpy.ops.file.make_paths_relative()
    return [o.name for o in col.objects]
