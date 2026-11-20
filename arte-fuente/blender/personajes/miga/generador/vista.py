# Luces, camara, poses de prueba y renders de revision. Nada de esto se exporta a Unity.
DIR_VISTAS = os.path.join(AQUI, "_vistas")
VISTAS = {"frente": (0, -1, 0.0), "tres_cuartos": (-0.62, -1, 0.22), "lado": (-1, 0, 0.0), "espalda": (0, 1, 0.0),
          "tres_cuartos_izq": (0.7, -1, 0.25), "espalda_3_4": (0.7, 1, 0.3), "arriba": (0, -0.55, 1)}
# Poses para probar los pesos: (hueso, eje del mundo, grados). Los padres van antes que los hijos.
POSES = {
    "T": [("LeftUpperArm", "Y", -56), ("RightUpperArm", "Y", 56)],
    "caminar": [("Spine", "X", -5), ("Head", "Z", 18), ("LeftUpperLeg", "X", -30), ("LeftLowerLeg", "X", 22),
                ("RightUpperLeg", "X", 24), ("RightLowerLeg", "X", 30), ("LeftUpperArm", "X", 28), ("LeftLowerArm", "X", -30),
                ("RightUpperArm", "X", -22), ("RightLowerArm", "X", -20), ("Bufanda_02", "X", -14), ("Bufanda_04", "X", -16),
                ("Mono.L", "Y", 8), ("Mono.R", "Y", 8)],
    "trepar": [("Spine", "X", -8), ("Head", "X", -12), ("LeftUpperArm", "X", -115), ("LeftLowerArm", "X", -20),
               ("RightUpperArm", "X", -35), ("RightUpperLeg", "X", -62), ("RightLowerLeg", "X", 70),
               ("BufandaFrente_02", "X", 14), ("Bufanda_03", "X", -12)],
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
    """Quita cualquier pose y abre los ojos."""
    esq = bpy.data.objects.get(ESQ)
    if esq:
        for pb in esq.pose.bones:
            pb.matrix_basis = Matrix.Identity(4)
    ojos = bpy.data.objects.get("Miga_Ojos")
    if ojos and ojos.data.shape_keys:
        ojos.data.shape_keys.key_blocks["Parpadeo"].value = 0.0
    bpy.context.view_layer.update()


def posar(nombre, parpadeo=0.0):
    reposo()
    for hueso, eje, grados in POSES[nombre]:
        girar(hueso, eje, grados)
    bpy.data.objects["Miga_Ojos"].data.shape_keys.key_blocks["Parpadeo"].value = parpadeo


def preparar_vista(muestras=48):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.view_settings.view_transform = "Standard"
    sc.render.film_transparent = False
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
    limpiar("Miga_Vista")
    c = coleccion("Miga_Vista")

    def luz(nombre, pos, energia, tam, color="#FFFFFF"):
        l = bpy.data.lights.new(nombre, "AREA")
        l.energy, l.size, l.color = energia, tam, lin(hexrgb(color))
        o = bpy.data.objects.new(nombre, l)
        o.location = pos
        o.rotation_euler = (Vector((0, 0, 0.55)) - Vector(pos)).to_track_quat("-Z", "Y").to_euler()
        c.objects.link(o)

    luz("Vista_Principal", (-1.3, -2.0, 2.0), 150, 1.6, "#FFF4E6")
    luz("Vista_Relleno", (1.9, -1.4, 0.9), 45, 2.0, "#DCE6FF")
    luz("Vista_Contra", (0.9, 2.0, 1.7), 110, 1.2, "#BFD0FF")
    cam = bpy.data.objects.new("Vista_Camara", bpy.data.cameras.new("Vista_Camara"))
    cam.data.type = "ORTHO"
    c.objects.link(cam)
    sc.camera = cam
    me = bpy.data.meshes.new("Vista_Piso")
    me.from_pydata([(-40, -40, 0), (40, -40, 0), (40, 40, 0), (-40, 40, 0)], [], [(0, 1, 2, 3)])
    piso = bpy.data.objects.new("Vista_Piso", me)
    me.materials.append(material("mat_vista_piso", "#232A3C", 0.9))
    c.objects.link(piso)
    return cam


def render(nombre, vistas=("frente", "tres_cuartos", "lado", "espalda"), res=(400, 540), centro=(0, 0, 0.53), escala=1.22,
           persp=False, muestras=48):
    """Renderiza varias vistas y las junta en una sola hoja PNG dentro de _vistas."""
    sc = bpy.context.scene
    cam = bpy.data.objects.get("Vista_Camara") or preparar_vista(muestras)
    sc.camera = cam
    sc.eevee.taa_render_samples = muestras
    os.makedirs(DIR_VISTAS, exist_ok=True)
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = res[0], res[1], 100
    sc.render.image_settings.file_format = "PNG"
    hoja = np.zeros((res[1], res[0] * len(vistas), 4), np.float32)
    for i, v in enumerate(vistas):
        d = Vector(VISTAS[v] if isinstance(v, str) else v).normalized()
        cam.location = Vector(centro) + d * 4
        cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
        if persp:
            cam.data.type, cam.data.lens = "PERSP", 36 * 4 / escala
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
