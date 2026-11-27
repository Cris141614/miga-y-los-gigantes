# Esqueleto de La Costurera: nombres de huesos, pesos de cada pieza y la armadura.
# No tiene piernas, asi que en Unity va como rig Generic. La cadena del cuerpo nace en el piso:
# la base del vestido no se despega y todo lo de arriba se dobla sobre ella.
# Los nombres del tronco y los brazos siguen los de Unity; los extra van en espanol.
ESQ = "Costurera_Esqueleto"
Z_F2, Z_HIPS, Z_SPINE, Z_CHEST = 3.3, 6.6, 9.8, 11.0     # alturas donde empieza cada hueso del tronco
Z_NECK, Z_NECK2, Z_HEAD = 12.05, 12.72, 13.38
I_HOMBRO, I_CODO = 3, 15                                 # puntos de brazo_pts donde estan el hombro y el codo
_BRAZOS = {}


def hum(lado, hueso):
    """Nombre de un hueso con lado, al estilo de Unity: x > 0 es su izquierda."""
    return ("Left" if lado > 0 else "Right") + hueso


def ext(lado, hueso):
    return hueso + (".L" if lado > 0 else ".R")


# ----------------------------------------------------------------------------- pesos
def banda(x, c, a):
    """0 por debajo de c - a, 1 por encima de c + a, suave en medio."""
    return suaviza((x - c + a) / (2 * a))


def cadena(nombres, f):
    """Reparte el peso a lo largo de una cadena de huesos; f[i] = cuanto pasa del hueso i al i + 1."""
    w, resto = {}, 1.0
    for i, h in enumerate(nombres):
        pasa = f[i] if i < len(f) else 0.0
        w[h] = w.get(h, 0.0) + resto * (1 - pasa)
        resto *= pasa
    return w


def mezcla_w(a, b, t):
    out = {h: x * (1 - t) for h, x in a.items()}
    for h, x in b.items():
        out[h] = out.get(h, 0.0) + x * t
    return out


def w_tronco(p):
    """Falda, cadera, columna y pecho segun la altura."""
    z = p[2]
    return cadena(("Falda_01", "Falda_02", "Hips", "Spine", "Chest"),
                  (banda(z, Z_F2, 1.0), banda(z, Z_HIPS, 1.0), banda(z, Z_SPINE, 0.6), banda(z, Z_CHEST, 0.45)))


def w_cuello(p):
    z = p[2]
    return cadena(("Chest", "Neck", "Neck_02", "Head"), (banda(z, Z_NECK, 0.2), banda(z, Z_NECK2, 0.25), banda(z, Z_HEAD, 0.2)))


def brazo_linea(lado):
    """Eje del brazo del hombro a la mano: puntos, radio de la manga y distancia recorrida."""
    if lado not in _BRAZOS:
        pts = brazo_pts(lado)
        P, R = [p for p, _ in pts], [r for _, r in pts]
        K = mano_centro(lado)
        P += [P[-1].lerp(K, 0.5), K]
        R += [0.17, 0.17]
        L = [0.0]
        for i in range(1, len(P)):
            L.append(L[-1] + (P[i] - P[i - 1]).length)
        _BRAZOS[lado] = (P, R, L)
    return _BRAZOS[lado]


def brazo_cerca(lado, p):
    """Distancia al eje del brazo, cuanto se ha recorrido hasta ahi y el radio de la manga en ese punto."""
    P, R, L = brazo_linea(lado)
    mejor = (1e9, 0.0, 0.0)
    for i in range(len(P) - 1):
        ab = P[i + 1] - P[i]
        t = limita((p - P[i]).dot(ab) / ab.length_squared)
        d = (p - (P[i] + ab * t)).length
        if d < mejor[0]:
            mejor = (d, L[i] + (L[i + 1] - L[i]) * t, R[i] + (R[i + 1] - R[i]) * t)
    return mejor


def w_brazo(lado, s):
    L = brazo_linea(lado)[2]
    return cadena((hum(lado, "Shoulder"), hum(lado, "UpperArm"), hum(lado, "LowerArm")),
                  (banda(s, L[I_HOMBRO], 0.5), banda(s, L[I_CODO], 0.7)))


def w_manga(lado):
    """Manga: nace pegada al tronco y enseguida sigue al brazo."""
    def w(p):
        d, s, r = brazo_cerca(lado, p)
        return mezcla_w(w_tronco(p), w_brazo(lado, s), suaviza((s - 0.15) / 1.1))
    return w


def w_vestido(p):
    """Vestido: sigue al tronco; la axila sigue a medias al brazo para que no se rompa al levantarlo."""
    w = w_tronco(p)
    if p.z > 8.5 and abs(p.x) > 1e-6:
        lado = 1 if p.x > 0 else -1
        d, s, r = brazo_cerca(lado, p)
        t = 0.5 * (1 - suaviza((d - r) / 0.35)) * suaviza((s - 0.15) / 1.1)
        if t > 0:
            w = mezcla_w(w, w_brazo(lado, s), t)
    return w


# ----------------------------------------------------------------------------- huesos
def centro_ve(z):
    return Vector((0, curva(CLAVES_VE, z)[2], z))


def cuello_pt(z):
    return Vector((0, -0.74 - 0.47 * (z - 11.9) / 1.5, z))


def huesos():
    """Lista de (nombre, cabeza, cola, padre, conectado, hacia donde mira su eje Z)."""
    H = []

    def h(nombre, cabeza, cola, padre=None, conectado=False, frente=(0, -1, 0)):
        H.append((nombre, Vector(cabeza), Vector(cola), padre, conectado, Vector(frente)))

    h("Falda_01", centro_ve(0.0), centro_ve(Z_F2))
    h("Falda_02", centro_ve(Z_F2), centro_ve(Z_HIPS), "Falda_01", True)
    h("Hips", centro_ve(Z_HIPS), centro_ve(Z_SPINE), "Falda_02", True)
    h("Spine", centro_ve(Z_SPINE), centro_ve(Z_CHEST), "Hips", True)
    h("Chest", centro_ve(Z_CHEST), cuello_pt(Z_NECK), "Spine", True)
    h("Neck", cuello_pt(Z_NECK), cuello_pt(Z_NECK2), "Chest", True)
    h("Neck_02", cuello_pt(Z_NECK2), cuello_pt(Z_HEAD), "Neck", True)
    h("Head", cuello_pt(Z_HEAD), (0, -1.50, 15.85), "Neck_02", True)
    h("Cara", HC, HC + Vector((0, -HRY, 0)), "Head", frente=(0, 0, 1))       # la tela de la cara: para que respire
    h("Mono", (0, -1.05, 15.55), (0, -0.72, 16.90), "Head")
    for lado in (1, -1):
        P = brazo_linea(lado)[0]
        K = mano_centro(lado)
        h(hum(lado, "Shoulder"), (lado * 0.30, -0.50, 11.55), P[I_HOMBRO], "Chest")
        h(hum(lado, "UpperArm"), P[I_HOMBRO], P[I_CODO], hum(lado, "Shoulder"), True)
        h(hum(lado, "LowerArm"), P[I_CODO], K, hum(lado, "UpperArm"), True)
        h(hum(lado, "Hand"), K, K + Vector((0, 0, -0.33)), hum(lado, "LowerArm"), True)
        for j, (base, punta) in enumerate(agujas(lado)):                      # un hueso por aguja
            h(ext(lado, "Aguja_%d" % (j + 1)), base, punta, hum(lado, "Hand"))
    h("Tijeras", *tijeras_eje(), "Hips")
    return H


def hacer_esqueleto(raiz):
    arm = bpy.data.armatures.new(ESQ)
    ob = bpy.data.objects.new(ESQ, arm)
    coleccion().objects.link(ob)
    ob.parent = raiz
    ob.show_in_front = True
    arm.display_type = "STICK"
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.mode_set(mode="EDIT")
    for nombre, cabeza, cola, padre, conectado, frente in huesos():
        b = arm.edit_bones.new(nombre)
        b.head, b.tail = cabeza, cola
        b.align_roll(frente)
        if padre:
            b.parent = arm.edit_bones[padre]
            b.use_connect = conectado
    bpy.ops.object.mode_set(mode="OBJECT")
    return ob


def enlazar(ob, esq):
    """La malla se deforma con el esqueleto por sus grupos de vertices (uno por hueso)."""
    ob.modifiers.new("Esqueleto", "ARMATURE").object = esq


def revisar():
    """Autocomprobacion del enlace: devuelve la lista de problemas (vacia si todo esta bien)."""
    nombres = {b.name for b in bpy.data.objects[ESQ].data.bones}
    fallas = []
    for o in coleccion().objects:
        if o.type != "MESH":
            continue
        sobran = {g.name for g in o.vertex_groups} - nombres
        if sobran:
            fallas.append("%s: grupos sin hueso %s" % (o.name, sorted(sobran)))
        if not any(md.type == "ARMATURE" and md.object for md in o.modifiers):
            fallas.append("%s: sin modificador de esqueleto" % o.name)
        for v in o.data.vertices:
            if not v.groups or len(v.groups) > MAX_HUESOS or abs(sum(g.weight for g in v.groups) - 1) > 1e-3:
                fallas.append("%s: vertice %d con pesos invalidos" % (o.name, v.index))
                break
    return fallas
