# Esqueleto de Miga: nombres de huesos, pesos de cada pieza y la armadura.
# Los huesos del cuerpo llevan los nombres de Unity Humanoid para que Unity los reconozca solo.
# Los extra (bufanda, monos, dedos, frasco y Chispa) van en espanol y Unity los deja como huesos adicionales.
ESQ = "Miga_Esqueleto"
Z_HIPS, Z_SPINE, Z_CHEST, Z_NECK, Z_HEAD, Z_TOP = 0.335, 0.405, 0.490, 0.625, 0.672, 0.990
Z_CADERA, Z_RODILLA, Z_TOBILLO = 0.325, 0.172, 0.056
L_CODO, L_MUNECA = 0.150, 0.292               # distancia del hombro al codo y a la muneca, a lo largo del brazo


def hum(lado, hueso):
    """Nombre de un hueso humanoide: x > 0 es su izquierda."""
    return ("Left" if lado > 0 else "Right") + hueso


def ext(lado, hueso):
    """Nombre de un hueso extra con lado."""
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


def w_tronco(p, tope=None):
    """Hips, Spine, Chest, Neck y Head segun la altura."""
    z = p[2] if tope is None else min(p[2], tope)
    return cadena(("Hips", "Spine", "Chest", "Neck", "Head"),
                  (banda(z, Z_SPINE, 0.035), banda(z, Z_CHEST, 0.035), banda(z, Z_NECK + 0.004, 0.018), banda(z, Z_HEAD, 0.012)))


def w_brazo(lado, tope=None):
    """Hombro, brazo, antebrazo y mano segun la distancia a lo largo del brazo."""
    S, d, X, Y = brazo(lado)

    def w(p):
        s = (Vector(p) - S).dot(d)
        if tope is not None:
            s = min(s, tope)
        return cadena((hum(lado, "Shoulder"), hum(lado, "UpperArm"), hum(lado, "LowerArm"), hum(lado, "Hand")),
                      (banda(s, 0.012, 0.030), banda(s, L_CODO, 0.028), banda(s, L_MUNECA, 0.013)))
    return w


def w_pierna(lado):
    """Cadera, muslo, pierna, pie y dedos del pie segun la altura (y lo adelante que este, en la bota)."""
    C, punta, costado = bota_ejes(lado)

    def w(p):
        p = Vector(p)
        ww = cadena(("Hips", hum(lado, "UpperLeg"), hum(lado, "LowerLeg"), hum(lado, "Foot")),
                    (1 - banda(p.z, Z_CADERA + 0.004, 0.022), 1 - banda(p.z, Z_RODILLA, 0.022),
                     1 - banda(p.z, Z_TOBILLO + 0.004, 0.018)))
        t = banda((p - C).dot(punta), 0.046, 0.012) * (1 - banda(p.z, 0.052, 0.010))
        ww[hum(lado, "Toes")] = ww[hum(lado, "Foot")] * t
        ww[hum(lado, "Foot")] *= 1 - t
        return ww
    return w


def w_abrigo(p):
    """Abrigo: sigue al tronco; la falda sigue en parte a los muslos y los hombros a las claviculas."""
    p = Vector(p)
    w = w_tronco(p, tope=0.60)
    f = 0.55 * suaviza((Z_HIPS - p.z) / 0.15)
    if f > 0:
        izq = suaviza((p.x + 0.05) / 0.10)
        w = {h: x * (1 - f) for h, x in w.items()}
        w["LeftUpperLeg"], w["RightUpperLeg"] = f * izq, f * (1 - izq)
    for lado in (1, -1):
        g = 0.5 * suaviza(1 - (p - brazo(lado)[0]).length / 0.09)
        if g > 0:
            w = {h: x * (1 - g) for h, x in w.items()}
            w[hum(lado, "Shoulder")] = g
    return w


def w_cola(nombre, n, largo):
    """Punta de la bufanda: Chest arriba y luego nombre_01..n hacia abajo."""
    def w(p):
        t = BUF_Z - p[2]
        return cadena(["Chest"] + ["%s_%02d" % (nombre, k + 1) for k in range(n)],
                      [banda(t, 0.012, 0.016)] + [banda(t, largo * k / n, 0.016) for k in range(1, n)])
    return w


# ----------------------------------------------------------------------------- huesos
def chispa_centro():
    jx, jy, zt = frasco_eje()
    return Vector((jx, jy, zt - 0.126))


def huesos():
    """Lista de (nombre, cabeza, cola, padre, conectado, hacia donde mira su eje Z)."""
    H = []

    def h(nombre, cabeza, cola, padre=None, conectado=False, frente=(0, -1, 0)):
        H.append((nombre, Vector(cabeza), Vector(cola), padre, conectado, Vector(frente)))

    h("Hips", (0, CY, Z_HIPS), (0, CY, Z_SPINE))
    h("Spine", (0, CY, Z_SPINE), (0, CY, Z_CHEST), "Hips", True)
    h("Chest", (0, CY, Z_CHEST), (0, CY + 0.004, Z_NECK), "Spine", True)
    h("Neck", (0, CY + 0.004, Z_NECK), (0, CY + 0.006, Z_HEAD), "Chest", True)
    h("Head", (0, CY + 0.006, Z_HEAD), (0, CY + 0.006, Z_TOP), "Neck", True)
    for lado in (1, -1):
        S, d, X, Y = brazo(lado)
        W, f, t, n = mano_marco(lado)
        h(hum(lado, "Shoulder"), (lado * 0.026, CY, 0.600), S, "Chest")
        h(hum(lado, "UpperArm"), S, S + d * L_CODO, hum(lado, "Shoulder"), True)
        h(hum(lado, "LowerArm"), S + d * L_CODO, W, hum(lado, "UpperArm"), True)
        h(hum(lado, "Hand"), W, W + f * 0.0395, hum(lado, "LowerArm"), True, frente=-n)
        dedos, pulgar = mano_huesos(lado)
        h(ext(lado, "Dedos"), *dedos, hum(lado, "Hand"), frente=-n)
        h(ext(lado, "Pulgar"), *pulgar, hum(lado, "Hand"), frente=-n)
        C, punta, costado = bota_ejes(lado)
        rodilla, tobillo = C + Vector((0, -0.003, Z_RODILLA)), C + Vector((0, 0.003, Z_TOBILLO))
        h(hum(lado, "UpperLeg"), C + Vector((0, 0, Z_CADERA)), rodilla, "Hips")
        h(hum(lado, "LowerLeg"), rodilla, tobillo, hum(lado, "UpperLeg"), True)
        h(hum(lado, "Foot"), tobillo, C + punta * 0.046 + Vector((0, 0, 0.014)), hum(lado, "LowerLeg"), True, frente=(0, 0, 1))
        h(hum(lado, "Toes"), C + punta * 0.046 + Vector((0, 0, 0.014)), C + punta * 0.079 + Vector((0, 0, 0.014)),
          hum(lado, "Foot"), True, frente=(0, 0, 1))
        B, dm, Xm, Ym = mono(lado)
        h(ext(lado, "Mono"), B - dm * 0.045, B + dm * 0.050, "Head", frente=(0, -1, 0))
    for nombre, n, largo, centro, frente in (("Bufanda", 5, BUF_COLA, bufanda_cola, (0, 1, 0)),
                                             ("BufandaFrente", 3, BUF_FRENTE, bufanda_frente, (0, -1, 0))):
        for k in range(n):
            a, b = centro(BUF_Z - largo * k / n, k / n), centro(BUF_Z - largo * (k + 1) / n, (k + 1) / n)
            h("%s_%02d" % (nombre, k + 1), a, b, "%s_%02d" % (nombre, k) if k else "Chest", k > 0, frente=frente)
    Q, G = agarre(-1), chispa_centro()
    h("Frasco", Q, Q - Vector((0, 0, 0.171)), "RightHand")
    h("Chispa", G - Vector((0, 0, 0.014)), G, "Frasco")
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
