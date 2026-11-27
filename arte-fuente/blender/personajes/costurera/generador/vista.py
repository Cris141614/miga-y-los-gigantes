# Luces, camara, poses de prueba y renders de revision de La Costurera. Nada de esto se exporta a Unity.
from mathutils import Matrix
DIR_VISTAS = os.path.join(AQUI, "_vistas")
ESC = 17.0                                    # todo va 17 veces mas lejos y mas grande que con Miga
VISTAS = {"frente": (0, -1, 0.0), "tres_cuartos": (-0.62, -1, 0.22), "lado": (-1, 0, 0.0), "espalda": (0, 1, 0.0),
          "tres_cuartos_izq": (0.7, -1, 0.25), "espalda_3_4": (0.7, 1, 0.3)}
# Poses para probar los pesos: (hueso, eje del mundo, grados). Los padres van antes que los hijos.
# Girar en +X inclina hacia adelante; en -X levanta un brazo hacia el frente.
POSES = {
    "alerta": [("Neck", "Z", 20), ("Neck_02", "Z", 25), ("Head", "Z", 30), ("Head", "X", -8), ("Mono", "X", -6)],
    "inclinada": [("Falda_02", "X", 6), ("Hips", "X", 10), ("Spine", "X", 14), ("Chest", "X", 12), ("Neck", "X", -12),
                  ("Head", "X", -14), ("LeftUpperArm", "X", -40), ("RightUpperArm", "X", -40), ("Tijeras", "X", -30)],
    "clavar": [("Hips", "X", 6), ("Spine", "X", 8), ("Chest", "Z", -14), ("RightShoulder", "X", -30), ("RightUpperArm", "X", -70),
               ("RightLowerArm", "X", -45), ("RightHand", "X", 35), ("Aguja_1.R", "Y", 12), ("Aguja_4.R", "Y", -12),
               ("LeftUpperArm", "Y", -14), ("Head", "Z", -18)],
}


def girar(hueso, eje, grados):
    """Gira un hueso de la pose alrededor de un eje del mundo que pasa por su cabeza."""
    pb = bpy.data.objects[ESQ].pose.bones[hueso]
    bpy.context.view_layer.update()
    M = pb.matrix.copy()
    T = Matrix.Translation(M.to_translation())
    pb.matrix = T @ Matrix.Rotation(math.radians(grados), 4, eje) @ T.inverted() @ M
    bpy.context.view_layer.update()


def reposo():
    """Quita cualquier pose."""
    esq = bpy.data.objects.get(ESQ)
    if esq:
        for pb in esq.pose.bones:
            pb.matrix_basis = Matrix.Identity(4)
    bpy.context.view_layer.update()


def posar(nombre):
    reposo()
    for hueso, eje, grados in POSES[nombre]:
        girar(hueso, eje, grados)


def preparar_vista(muestras=48):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.view_settings.view_transform = "Standard"
    try:
        sc.eevee.taa_render_samples = muestras
    except Exception:
        pass
    w = sc.world or bpy.data.worlds.new("Mundo")
    sc.world = w
    try:
        w.use_nodes = True
    except Exception:
        pass
    bg = w.node_tree.nodes.get("Background")
    bg.inputs[0].default_value = (*lin(hexrgb("#1A2030")), 1)
    bg.inputs[1].default_value = 1.0
    limpiar("Costurera_Vista")
    c = coleccion("Costurera_Vista")

    def luz(nombre, pos, energia, tam, color):
        l = bpy.data.lights.new(nombre, "AREA")
        l.energy, l.size, l.color = energia * ESC * ESC, tam * ESC, lin(hexrgb(color))
        o = bpy.data.objects.new(nombre, l)
        o.location = Vector(pos) * ESC
        o.rotation_euler = (Vector((0, 0, 0.55 * ESC)) - o.location).to_track_quat("-Z", "Y").to_euler()
        c.objects.link(o)

    luz("Vista_Principal", (-1.3, -2.0, 2.0), 150, 1.6, "#FFF4E6")
    luz("Vista_Relleno", (1.9, -1.4, 0.9), 45, 2.0, "#DCE6FF")
    luz("Vista_Contra", (0.9, 2.0, 1.7), 110, 1.2, "#BFD0FF")
    cam = bpy.data.objects.new("Vista_Camara", bpy.data.cameras.new("Vista_Camara"))
    cam.data.type, cam.data.clip_end = "ORTHO", 2000
    c.objects.link(cam)
    sc.camera = cam
    me = bpy.data.meshes.new("Vista_Piso")
    me.from_pydata([(-600, -600, 0), (600, -600, 0), (600, 600, 0), (-600, 600, 0)], [], [(0, 1, 2, 3)])
    me.materials.append(material("mat_vista_piso", "#232A3C", 0.9))
    c.objects.link(bpy.data.objects.new("Vista_Piso", me))
    return cam


def render(nombre, vistas=("frente", "tres_cuartos", "lado", "espalda"), res=(400, 540), centro=(0, -0.3, 8.9), escala=20.0,
           persp=False):
    """Renderiza varias vistas y las junta en una hoja PNG dentro de _vistas."""
    sc = bpy.context.scene
    cam = bpy.data.objects.get("Vista_Camara") or preparar_vista()
    sc.camera = cam
    os.makedirs(DIR_VISTAS, exist_ok=True)
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = res[0], res[1], 100
    sc.render.image_settings.file_format = "PNG"
    hoja = np.zeros((res[1], res[0] * len(vistas), 4), np.float32)
    for i, v in enumerate(vistas):
        d = Vector(VISTAS[v] if isinstance(v, str) else v).normalized()
        cam.location = Vector(centro) + d * 4 * ESC
        cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
        if persp:
            cam.data.type, cam.data.lens = "PERSP", 36 * 4 * ESC / escala
        else:
            cam.data.type, cam.data.ortho_scale = "ORTHO", escala
        ruta = os.path.join(DIR_VISTAS, "_tmp.png")
        sc.render.filepath = ruta
        bpy.ops.render.render(write_still=True)
        img = bpy.data.images.load(ruta)
        buf = np.empty(res[0] * res[1] * 4, np.float32)
        img.pixels.foreach_get(buf)
        hoja[:, i * res[0]:(i + 1) * res[0]] = buf.reshape(res[1], res[0], 4)
        bpy.data.images.remove(img)
    out = bpy.data.images.new("_hoja", hoja.shape[1], hoja.shape[0], alpha=False)
    out.pixels.foreach_set(hoja.ravel())
    out.filepath_raw = os.path.join(DIR_VISTAS, nombre + ".png")
    out.file_format = "PNG"
    out.save()
    bpy.data.images.remove(out)
    return os.path.join(DIR_VISTAS, nombre + ".png")
