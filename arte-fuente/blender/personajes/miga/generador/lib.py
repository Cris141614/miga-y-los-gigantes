# Utilidades para construir a Miga por codigo dentro de Blender.
# Convenciones: 1 unidad = 1 metro, Miga mide 1.0 de alto, mira hacia -Y, piso en z = 0.
import bpy, bmesh, math, os
import numpy as np
from mathutils import Vector, Matrix

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, *([".."] * 5)))
DIR_TEX = os.path.join(RAIZ, "juego", "Assets", "_Proyecto", "Art", "Texturas")
DIR_MOD = os.path.join(RAIZ, "juego", "Assets", "_Proyecto", "Art", "Modelos")
DIR_BLEND = os.path.join(RAIZ, "arte-fuente", "blender", "personajes", "miga")
DIR_REF = os.path.join(RAIZ, "docs", "Referencias", "Personajes")
COL = "Miga"
MAX_HUESOS = 4                                # huesos por vertice: el limite por defecto de Unity


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def lin(c):
    return tuple((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


# ----------------------------------------------------------------------------- escena
def coleccion(nombre=COL):
    c = bpy.data.collections.get(nombre)
    if not c:
        c = bpy.data.collections.new(nombre)
        bpy.context.scene.collection.children.link(c)
    return c


def limpiar(nombre=COL):
    c = bpy.data.collections.get(nombre)
    if c:
        for o in list(c.objects):
            bpy.data.objects.remove(o, do_unlink=True)
    for datos in (bpy.data.meshes, bpy.data.armatures, bpy.data.lights):
        for d in list(datos):
            if d.users == 0:
                datos.remove(d)


# ----------------------------------------------------------------------------- mallas
def _peso(pesos, k, p):
    """Pesos de un vertice: dict fijo, lista con un dict por anillo, o funcion del punto."""
    if pesos is None or isinstance(pesos, dict):
        return pesos
    if isinstance(pesos, (list, tuple)):
        return pesos[k]
    return pesos(Vector(p))


def limpiar_pesos(w):
    """Deja como mucho MAX_HUESOS huesos por vertice y hace que sumen 1."""
    w = sorted(((x, h) for h, x in w.items() if x > 0.004), reverse=True)[:MAX_HUESOS]
    total = sum(x for x, _ in w)
    return {h: x / total for x, h in w}


class Malla:
    """Acumula vertices, caras, UV y pesos; al final crea el objeto."""

    def __init__(self, pesos=None):
        self.v, self.f, self.uv, self.m = [], [], [], []
        self.w, self.alt = [], []   # por vertice: pesos {hueso: peso} y posicion alternativa (para formas)
        self.pesos = pesos          # pesos de las piezas que no digan otra cosa
        self.fijas = {}             # cara -> centro: su normal debe apuntar hacia afuera de ese punto

    def loft(self, anillos, vs=None, rect=(0, 1, 0, 1), cerrado=True, tapa0=False, tapa1=False,
             mat=0, girar=False, us=None, uvfun=None, fuera=None, pesos=None, alt=None):
        """Une anillos consecutivos (listas de puntos del mismo largo) con quads."""
        n, K = len(anillos[0]), len(anillos)
        base, cara0 = len(self.v), len(self.f)
        pesos = self.pesos if pesos is None else pesos
        for k, r in enumerate(anillos):
            for i, p in enumerate(r):
                self.v.append((p[0], p[1], p[2]))
                self.w.append(_peso(pesos, k, p))
                self.alt.append(tuple(alt[k][i]) if alt else None)
        if vs is None:
            d = [0.0]
            for k in range(1, K):
                a, b = anillos[k - 1], anillos[k]
                d.append(d[-1] + sum((Vector(a[i]) - Vector(b[i])).length for i in range(n)) / n)
            L = d[-1] or 1.0
            vs = [x / L for x in d]
        m = n if cerrado else n - 1
        if us is None:
            us = [i / m for i in range(m + 1)]
        U0, U1, V0, V1 = rect

        def uv(i, k):
            if uvfun:
                return uvfun(anillos[k][i % n])
            u, v = us[i], vs[k]
            if girar:
                u, v = v, u
            return (U0 + (U1 - U0) * u, V0 + (V1 - V0) * v)

        for k in range(K - 1):
            for i in range(m):
                j = (i + 1) % n
                self.f.append((base + k * n + i, base + k * n + j, base + (k + 1) * n + j, base + (k + 1) * n + i))
                self.uv.append((uv(i, k), uv(i + 1, k), uv(i + 1, k + 1), uv(i, k + 1)))
                self.m.append(mat)
        for k, tapa in ((0, tapa0), (K - 1, tapa1)):
            if not tapa:
                continue
            c = sum((Vector(p) for p in anillos[k]), Vector()) / n
            ci = len(self.v)
            self.v.append(tuple(c))
            self.w.append(_peso(pesos, k, c))
            self.alt.append(tuple(sum((Vector(p) for p in alt[k]), Vector()) / n) if alt else None)
            cuv = uvfun(c) if uvfun else None
            for i in range(m):
                j = (i + 1) % n
                self.f.append((ci, base + k * n + i, base + k * n + j))
                a, b = uv(i, k), uv(i + 1, k)
                self.uv.append((cuv or ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), a, b))
                self.m.append(mat)
        if fuera is not None:
            for i in range(cara0, len(self.f)):
                self.fijas[i] = Vector(fuera)
        return self

    def objeto(self, nombre, mats, suave=True, orientar="auto", centro=None, padre=None):
        me = bpy.data.meshes.new(nombre)
        me.from_pydata(self.v, [], self.f)
        me.update()
        capa = me.uv_layers.new(name="UVMap")
        plano = [c for cara in self.uv for esquina in cara for c in esquina]
        capa.data.foreach_set("uv", plano)
        me.polygons.foreach_set("material_index", self.m)
        for mt in mats:
            me.materials.append(mt)
        bm = bmesh.new()
        bm.from_mesh(me)
        bm.faces.ensure_lookup_table()
        bm.verts.ensure_lookup_table()
        if any(self.w):                                                # pesos: van en la capa de deformacion
            if not all(self.w):
                raise ValueError(nombre + ": hay vertices sin pesos")
            pesos = [limpiar_pesos(w) for w in self.w]
            huesos = sorted({h for w in pesos for h in w})
            indice = {h: i for i, h in enumerate(huesos)}
            cd = bm.verts.layers.deform.verify()
            for v, w in zip(bm.verts, pesos):
                for h, x in w.items():
                    v[cd][indice[h]] = x
        else:
            huesos = []
        if any(a is not None for a in self.alt):                       # posicion alternativa, para una forma
            ca = bm.verts.layers.float_vector.new("alt")
            for v, a in zip(bm.verts, self.alt):
                v[ca] = a if a is not None else v.co
        fijas = set()
        for i, c in self.fijas.items():
            f = bm.faces[i]
            fijas.add(f)
            if (f.calc_center_median() - c).dot(f.normal) < 0:
                f.normal_flip()
        bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-6)
        libres = [f for f in bm.faces if f.is_valid and f not in fijas]
        if orientar == "auto" and libres:
            bmesh.ops.recalc_face_normals(bm, faces=libres)
        bm.to_mesh(me)
        bm.free()
        me.polygons.foreach_set("use_smooth", [suave] * len(me.polygons))
        me.update()
        ob = bpy.data.objects.new(nombre, me)
        for h in huesos:
            ob.vertex_groups.new(name=h)
        coleccion().objects.link(ob)
        if padre:
            ob.parent = padre
        return ob


def forma(ob, nombre):
    """Convierte la posicion alternativa de los vertices en una forma (shape key) y borra el atributo."""
    at = ob.data.attributes["alt"]
    co = [tuple(d.vector) for d in at.data]
    ob.data.attributes.remove(at)
    if not ob.data.shape_keys:
        ob.shape_key_add(name="Basis")
    sk = ob.shape_key_add(name=nombre)
    sk.value = 0.0
    for i, c in enumerate(co):
        sk.data[i].co = c
    return sk


def limita(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def suaviza(t):
    t = limita(t)
    return t * t * (3 - 2 * t)


def anillo(c, X, Y, rx, ry, n, fase=0.0):
    """n puntos en una elipse centrada en c, sobre los ejes X e Y."""
    c, X, Y = Vector(c), Vector(X), Vector(Y)
    return [c + X * (rx * math.cos(fase + 2 * math.pi * i / n)) + Y * (ry * math.sin(fase + 2 * math.pi * i / n))
            for i in range(n)]


def marcos(camino, arriba=(0, 0, 1)):
    """Tangente, lateral y normal a lo largo de un camino de puntos (transporte paralelo)."""
    P = [Vector(p) for p in camino]
    T = []
    for i in range(len(P)):
        a, b = P[max(i - 1, 0)], P[min(i + 1, len(P) - 1)]
        T.append((b - a).normalized())
    N = Vector(arriba)
    out = []
    for t in T:
        N = (N - t * N.dot(t))
        if N.length < 1e-6:
            N = t.orthogonal()
        N.normalize()
        B = t.cross(N).normalized()
        out.append((t, B, N))
    return out


def tubo(camino, radios, n=10, arriba=(0, 0, 1)):
    """Anillos elipticos a lo largo de un camino. radios: lista de (lateral, normal)."""
    fr = marcos(camino, arriba)
    return [anillo(camino[i], fr[i][1], fr[i][2], radios[i][0], radios[i][1], n) for i in range(len(camino))]


def elipsoide(m, c, X, Y, Z, n=16, k=10, **kw):
    """Elipsoide de centro c y semiejes vectoriales X, Y, Z (polos sobre Z)."""
    c, X, Y, Z = Vector(c), Vector(X), Vector(Y), Vector(Z)
    an = []
    for j in range(1, k):
        ph = math.pi * j / k
        an.append([c + Z * math.cos(ph) + (X * math.cos(2 * math.pi * i / n) + Y * math.sin(2 * math.pi * i / n)) * math.sin(ph)
                   for i in range(n)])
    return m.loft(an, tapa0=True, tapa1=True, **kw)


def bez2(a, b, c, t):
    a, b, c = Vector(a), Vector(b), Vector(c)
    return a * (1 - t) ** 2 + b * (2 * t * (1 - t)) + c * t * t


def bez3(a, b, c, d, t):
    a, b, c, d = Vector(a), Vector(b), Vector(c), Vector(d)
    s = 1 - t
    return a * s ** 3 + b * (3 * s * s * t) + c * (3 * s * t * t) + d * t ** 3


def curva(claves, x):
    """Interpolacion cubica suave por claves [(x, (valores...)), ...] ordenadas por x."""
    xs = [k[0] for k in claves]
    x = min(max(x, xs[0]), xs[-1])
    i = max(0, min(len(xs) - 2, int(np.searchsorted(xs, x, side="right") - 1)))
    h = xs[i + 1] - xs[i]
    t = (x - xs[i]) / h

    def pend(j):
        a, b = max(j - 1, 0), min(j + 1, len(xs) - 1)
        return [(claves[b][1][q] - claves[a][1][q]) / (xs[b] - xs[a]) for q in range(len(claves[0][1]))]

    m0, m1 = pend(i), pend(i + 1)
    h00, h10, h01, h11 = 2 * t ** 3 - 3 * t * t + 1, t ** 3 - 2 * t * t + t, -2 * t ** 3 + 3 * t * t, t ** 3 - t * t
    return [h00 * claves[i][1][q] + h10 * h * m0[q] + h01 * claves[i + 1][1][q] + h11 * h * m1[q]
            for q in range(len(claves[0][1]))]


# ----------------------------------------------------------------------------- materiales
def imagen(nombre, nocolor=False):
    ruta = os.path.join(DIR_TEX, nombre + ".png")
    img = bpy.data.images.get(nombre)
    if img is None:
        img = bpy.data.images.load(ruta)
        img.name = nombre
    img.colorspace_settings.name = "Non-Color" if nocolor else "sRGB"
    return img


def material(nombre, color="#FFFFFF", rugosidad=0.7, tex=None, normal=None, fuerza_normal=1.0,
             emision=None, fuerza_emision=0.0, alfa=1.0, brillo=0.5, velo=0.0):
    mat = bpy.data.materials.get(nombre) or bpy.data.materials.new(nombre)
    try:
        mat.use_nodes = True
    except Exception:
        pass
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    out.location, b.location = (300, 0), (0, 0)
    nt.links.new(b.outputs["BSDF"], out.inputs["Surface"])
    b.inputs["Base Color"].default_value = (*lin(hexrgb(color)), 1)
    b.inputs["Roughness"].default_value = rugosidad
    b.inputs["Specular IOR Level"].default_value = brillo
    if velo:
        b.inputs["Sheen Weight"].default_value = velo
    if tex:
        t = nt.nodes.new("ShaderNodeTexImage")
        t.image = imagen(tex)
        t.location = (-350, 100)
        nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
        b.inputs["Base Color"].default_value = (1, 1, 1, 1)      # el color lo da la textura
    if normal:
        t = nt.nodes.new("ShaderNodeTexImage")
        t.image = imagen(normal, nocolor=True)
        t.location = (-600, -250)
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nm.location = (-250, -250)
        nm.inputs["Strength"].default_value = fuerza_normal
        nt.links.new(t.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    if emision:
        b.inputs["Emission Color"].default_value = (*lin(hexrgb(emision)), 1)
        b.inputs["Emission Strength"].default_value = fuerza_emision
    if alfa < 1.0:
        b.inputs["Alpha"].default_value = alfa
        try:
            mat.surface_render_method = "BLENDED"
        except Exception:
            pass
    mat.use_backface_culling = True
    mat.diffuse_color = (*lin(hexrgb(color)), alfa)
    return mat


# ----------------------------------------------------------------------------- pintura
def lienzo(w, h, color):
    a = np.empty((h, w, 3), np.float32)
    a[:] = hexrgb(color) if isinstance(color, str) else color
    u = (np.arange(w) + 0.5) / w
    v = (np.arange(h) + 0.5) / h
    U, V = np.meshgrid(u, v)  # fila 0 = abajo (v = 0), igual que Blender
    return a, U.astype(np.float32), V.astype(np.float32)


def mezcla(a, color, alfa):
    c = np.array(hexrgb(color) if isinstance(color, str) else color, np.float32)
    al = np.clip(alfa, 0, 1)[..., None]
    a *= (1 - al)
    a += c * al


def sd_elipse(X, Y, cx, cy, rx, ry, rot=0.0):
    dx, dy = X - cx, Y - cy
    if rot:
        c, s = math.cos(rot), math.sin(rot)
        dx, dy = dx * c + dy * s, -dx * s + dy * c
    return (np.sqrt((dx / rx) ** 2 + (dy / ry) ** 2) - 1) * min(rx, ry)


def sd_capsula(X, Y, ax, ay, bx, by, r):
    pax, pay, bax, bay = X - ax, Y - ay, bx - ax, by - ay
    h = np.clip((pax * bax + pay * bay) / (bax * bax + bay * bay + 1e-12), 0, 1)
    return np.hypot(pax - bax * h, pay - bay * h) - r


def sd_caja(X, Y, cx, cy, hx, hy, r=0.0):
    dx, dy = np.abs(X - cx) - hx + r, np.abs(Y - cy) - hy + r
    return np.hypot(np.maximum(dx, 0), np.maximum(dy, 0)) + np.minimum(np.maximum(dx, dy), 0) - r


def lleno(sd, px):
    """Relleno con borde antialias; px = tamano de un pixel en las unidades de sd."""
    return np.clip(0.5 - sd / px, 0, 1)


def difuso(sd, ancho):
    t = np.clip(-sd / ancho, 0, 1)
    return t * t * (3 - 2 * t)


def ruido(h, w, sigma, semilla=0, sx=None):
    """Ruido suave periodico en [-1, 1]; sigma en pixeles (sx para estirarlo en x)."""
    rng = np.random.default_rng(semilla)
    F = np.fft.rfft2(rng.standard_normal((h, w)))
    fy = np.fft.fftfreq(h)[:, None]
    fx = np.fft.rfftfreq(w)[None, :]
    F *= np.exp(-2 * (math.pi ** 2) * ((fy * sigma) ** 2 + (fx * (sx or sigma)) ** 2))
    r = np.fft.irfft2(F, s=(h, w))
    r -= r.mean()
    r /= (np.abs(r).max() + 1e-9)
    return r.astype(np.float32)


def normal_de_altura(alt, fuerza):
    dx = (np.roll(alt, -1, 1) - np.roll(alt, 1, 1)) * 0.5 * fuerza
    dy = (np.roll(alt, -1, 0) - np.roll(alt, 1, 0)) * 0.5 * fuerza
    n = np.dstack((-dx, -dy, np.ones_like(alt)))
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    return (n * 0.5 + 0.5).astype(np.float32)


def guardar(a, nombre, nocolor=False):
    h, w, _ = a.shape
    img = bpy.data.images.get(nombre)
    if img:
        bpy.data.images.remove(img)
    img = bpy.data.images.new(nombre, w, h, alpha=False)
    img.colorspace_settings.name = "Non-Color" if nocolor else "sRGB"
    rgba = np.ones((h, w, 4), np.float32)
    rgba[..., :3] = np.clip(a, 0, 1)
    img.pixels.foreach_set(rgba.ravel())
    os.makedirs(DIR_TEX, exist_ok=True)
    img.filepath_raw = os.path.join(DIR_TEX, nombre + ".png")
    img.file_format = "PNG"
    img.save()
    bpy.data.images.remove(img)
    return imagen(nombre, nocolor)
