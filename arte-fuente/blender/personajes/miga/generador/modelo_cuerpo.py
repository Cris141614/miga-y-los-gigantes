# Cuerpo, manos, piernas, botas, abrigo, bufanda, frasco y Chispa.
CY = 0.004                                    # centro del cuerpo en y
AB_Z0, AB_Z1 = 0.175, 0.668                   # ruedo y cuello del abrigo
CLAVES_AB = [                                 # z: (radio en x, radio en y)
    (0.175, (0.206, 0.127)), (0.220, (0.198, 0.124)), (0.300, (0.184, 0.118)), (0.400, (0.166, 0.110)),
    (0.480, (0.151, 0.102)), (0.560, (0.136, 0.092)), (0.618, (0.117, 0.082)), (0.650, (0.082, 0.066)),
    (0.668, (0.040, 0.040))]
CLAVES_TORSO = [                              # el cuerpo que va debajo del abrigo, z: (radio en x, radio en y)
    (0.300, (0.058, 0.044)), (0.335, (0.076, 0.056)), (0.380, (0.072, 0.053)), (0.430, (0.064, 0.049)),
    (0.500, (0.068, 0.050)), (0.560, (0.076, 0.050)), (0.598, (0.082, 0.046)), (0.622, (0.062, 0.042)),
    (0.640, (0.036, 0.034))]
BRAZO_ANG = 34                                # grados desde la vertical (pose en A)
PIERNA_X = 0.048
BOTA_GIRO = 9                                 # grados que las puntas de las botas miran hacia adentro
RADIO_AGARRE = 0.0076                         # radio con que los dedos rodean el asa del frasco


def ab_radios(th, z):
    rx, ry = curva(CLAVES_AB, z)
    amp = 0.030 * limita((0.47 - z) / 0.30) ** 1.5                     # vuelo: ondas hacia el ruedo
    k = 1 + amp * math.cos(7 * th + 0.6) + 0.4 * amp * math.cos(3 * th + 2.0)
    return rx * k, ry * k


def ab_pt(th, z, off=0.0):
    """Punto del abrigo. th en radianes (0 = frente, + hacia su izquierda)."""
    rx, ry = ab_radios(th, z)
    return Vector(((rx + off) * math.sin(th), CY - (ry + off) * math.cos(th), z))


def ab_marco(th, z, off=0.0):
    """Punto sobre el abrigo y sus ejes: lateral, arriba y normal hacia afuera."""
    e = 0.002
    P = ab_pt(th, z, off)
    R = (ab_pt(th + e, z, off) - ab_pt(th - e, z, off)).normalized()
    U = (ab_pt(th, z + e, off) - ab_pt(th, z - e, off)).normalized()
    N = R.cross(U).normalized()
    if N.dot(Vector((math.sin(th), -math.cos(th), 0))) < 0:
        N = -N
    return P, R, U, N


def th_de_x(x, z):
    """Angulo del frente del abrigo donde la coordenada x vale lo pedido."""
    th = 0.0
    for _ in range(6):
        th = math.asin(limita(x / ab_radios(th, z)[0], -1, 1))
    return th


def torso_pt(th, z, off=0.0):
    rx, ry = curva(CLAVES_TORSO, z)
    return Vector(((rx + off) * math.sin(th), CY - (ry + off) * math.cos(th), z))


def lamina(m, th_c, z_c, ancho, alto, giro, off_c, off_b, rect, mat, nx=6, nz=6, pelo=0.008):
    """Parche, bolsillo o cinta: rejilla pegada al abrigo, abombada al centro."""
    r = ab_radios(th_c, z_c)[0]
    cg, sg = math.cos(math.radians(giro)), math.sin(math.radians(giro))
    filas = []
    for j in range(nz + 1):
        fila = []
        for i in range(nx + 1):
            a, b = ancho * (i / nx - 0.5), alto * (j / nz - 0.5)
            borde = min(i, nx - i) * ancho / nx, min(j, nz - j) * alto / nz
            off = off_b + (off_c - off_b) * suaviza(min(borde) / pelo)
            fila.append(ab_pt(th_c + (a * cg - b * sg) / r, z_c + a * sg + b * cg, off))
        filas.append(fila)
    m.loft(filas, vs=[j / nz for j in range(nz + 1)], us=[i / nx for i in range(nx + 1)], cerrado=False,
           rect=rect, mat=mat, fuera=(0, CY, z_c))


def boton(m, th, z):
    P, R, U, N = ab_marco(th, z)
    uvb = lambda p: ((DT_BOTON[0] + DT_BOTON[1]) / 2 + (Vector(p) - P).dot(R) / 0.0135 * 0.118,
                     (DT_BOTON[2] + DT_BOTON[3]) / 2 + (Vector(p) - P).dot(U) / 0.0135 * 0.118)
    m.loft([anillo(P + N * h, R, U, r, r, 14) for r, h in ((0.0112, 0.0062), (0.0135, 0.0046), (0.0138, 0.0))],
           uvfun=uvb, tapa0=True, mat=1)


def hacer_abrigo():
    m = Malla(pesos=w_abrigo)
    n = 56
    ths = [-math.pi + 2 * math.pi * i / n for i in range(n)]
    zs = [0.668, 0.662, 0.652, 0.640, 0.625, 0.605, 0.580, 0.550, 0.515, 0.480, 0.440, 0.400, 0.360, 0.320,
          0.280, 0.245, 0.212, 0.190, 0.175]
    m.loft([[ab_pt(t, z) for t in ths] for z in zs] + [[ab_pt(t, 0.1715, -0.003) for t in ths]],
           vs=[(z - AB_Z0) / (AB_Z1 - AB_Z0) for z in zs] + [0.0], rect=AB_CUERPO, tapa0=True)
    forro = lambda p: ((AB_FORRO[0] + AB_FORRO[1]) / 2, (AB_FORRO[2] + AB_FORRO[3]) / 2)
    m.loft([[ab_pt(t, 0.1715, -0.003) for t in ths]] + [[ab_pt(t, z, -0.007) for t in ths]
                                                       for z in (0.176, 0.21, 0.30, 0.40, 0.50, 0.60)],
           uvfun=forro, tapa1=True)
    # mangas, con pliegues a la altura del codo
    for lado, blo in ((-1, AB_MANGA_D), (1, AB_MANGA_I)):
        S, d, X, Y = brazo(lado)
        wm = w_brazo(lado, tope=0.272)                                 # el puno no sigue a la mano
        est = [(0.0, 0.058), (0.035, 0.062), (0.085, 0.058), (0.122, 0.0550), (0.138, 0.0578), (0.153, 0.0540),
               (0.168, 0.0568), (0.184, 0.0535), (0.210, 0.053), (0.256, 0.054), (0.262, 0.0605), (0.300, 0.0615),
               (0.306, 0.0585)]
        L = est[-1][0]
        m.loft([anillo(S + d * s, X, Y, r, r * 0.90, 18) for s, r in est], vs=[s / L for s, _ in est], rect=blo,
               girar=True, tapa0=True, pesos=wm)
        m.loft([anillo(S + d * s, X, Y, r, r * 0.90, 18) for s, r in ((0.306, 0.0585), (0.304, 0.052), (0.275, 0.050))],
               uvfun=forro, tapa1=True, pesos=wm)
    # bolsillo (a su derecha) y parches
    z_b = 0.327
    lamina(m, th_de_x(-0.112, z_b), z_b, 0.078, 0.088, 0, 0.0065, 0.0008, AB_BOLSILLO, 0, nx=7, nz=7)
    lamina(m, th_de_x(0.104, 0.300), 0.300, 0.058, 0.056, -9, 0.0045, 0.0008, DT_PARCHE_A, 1)
    lamina(m, math.radians(127), 0.468, 0.052, 0.050, 6, 0.0045, 0.0008, DT_PARCHE_B, 1)
    # cinta de la espalda con un boton en cada punta
    lamina(m, math.pi, 0.405, 0.176, 0.030, 0, 0.0048, 0.0010, AB_CINTA, 0, nx=16, nz=3, pelo=0.006)
    for z in (0.505, 0.413, 0.320):                                    # botones del frente
        boton(m, 0.0, z)
    for lado in (-1, 1):
        boton(m, math.pi + lado * 0.43, 0.405)
    return m.objeto("Miga_Abrigo", [MATS["abrigo"], MATS["detalles"]])


def brazo(lado):
    """Hombro, direccion del brazo y dos ejes perpendiculares."""
    a = math.radians(BRAZO_ANG)
    S = Vector((lado * 0.100, CY, 0.612))
    d = Vector((lado * math.sin(a), -0.07, -math.cos(a))).normalized()
    X = d.cross(Vector((0, 1, 0))).normalized()
    return S, d, X, d.cross(X).normalized()


def mano_marco(lado):
    """Muneca y ejes de la mano: hacia los dedos, hacia el pulgar y hacia donde mira la palma."""
    S, d, X, Y = brazo(lado)
    W = S + d * L_MUNECA
    if lado < 0:                                                       # mano del frasco: cuelga casi vertical,
        f = (Vector((0, 0, -1)) * 0.6 + d * 0.4).normalized()          #   con la palma hacia atras
        n = Vector((0, 1, 0))
    else:                                                              # mano libre: relajada, palma hacia el cuerpo
        f, n = d, Vector((-lado, 0, 0))
    n = (n - f * n.dot(f)).normalized()
    return W, f, (f.cross(n) if lado < 0 else n.cross(f)).normalized(), n


def agarre(lado=-1):
    """Punto del puno por donde pasa el asa del frasco."""
    W, f, t, n = mano_marco(lado)
    return W + f * 0.0400 + n * (RADIO_AGARRE - 0.001)


def mano_dedos(lado):
    """Dedos como (base, largo, radio, angulo que se cierra). El primero es el indice."""
    W, f, t, n = mano_marco(lado)
    out = []
    for q, (u, largo, r) in enumerate(((0.0138, 0.0235, 0.0050), (0.0047, 0.0265, 0.0052), (-0.0045, 0.0250, 0.0050),
                                       (-0.0132, 0.0195, 0.0045))):
        if lado < 0:                                                   # puno: todos rodean el asa
            base, ang = W + f * 0.0400 + t * u - n * 0.001, largo / RADIO_AGARRE
        else:                                                          # relajada: nudillos en arco
            base = W + f * (0.0405 - 0.0055 * (u / 0.0138) ** 2) + t * u - n * 0.001
            ang = math.radians(52) * (1 + 0.12 * q)
        out.append((base, largo, r, ang))
    return out


def mano_pulgar(lado):
    """Base del pulgar y sus direcciones al nacer y en la punta."""
    W, f, t, n = mano_marco(lado)
    d1 = f * 0.55 + n * 0.80 - t * 0.25 if lado < 0 else f * 0.85 + t * 0.35 + n * 0.40
    return W + f * 0.0150 + t * 0.0175 + n * 0.0035, (f * 0.62 + t * 0.70 + n * 0.30).normalized(), d1.normalized()


def mano_huesos(lado):
    """Cabeza y cola de los huesos Dedos y Pulgar."""
    W, f, t, n = mano_marco(lado)
    a = mano_dedos(lado)[1][3] * 0.2
    nudillos = W + f * 0.0395 - n * 0.001
    bp, d0, d1 = mano_pulgar(lado)
    return (nudillos, nudillos + (f * math.cos(a) + n * math.sin(a)) * 0.022), (bp, bp + d0 * 0.020)


def hacer_mano(m, lado):
    """Palma, cuatro dedos y pulgar. La mano del frasco va cerrada sobre el asa."""
    W, f, t, n = mano_marco(lado)
    mano, dedos, pulgar = {hum(lado, "Hand"): 1.0}, {ext(lado, "Dedos"): 1.0}, {ext(lado, "Pulgar"): 1.0}
    elipsoide(m, W + f * 0.0240, t * 0.0200, n * 0.0105, f * 0.0215, n=14, k=8, uvfun=uv_lisa, pesos=mano)
    escala = (1.0, 1.0, 1.0, 0.99, 0.96, 0.92, 0.86, 0.74, 0.42)

    def dedo(cam, r, hueso):
        """Tubo que nace dentro de la palma: los dos primeros anillos siguen a la mano."""
        mitad = {hum(lado, "Hand"): 0.5, **{h: 0.5 for h in hueso}}
        m.loft(tubo(cam, [(r * e, r * e) for e in escala], n=8, arriba=n), uvfun=uv_lisa, tapa0=True, tapa1=True,
               pesos=[mano, mitad] + [hueso] * 7)

    K = 6
    for base, largo, r, ang in mano_dedos(lado):
        cam, p, dr = [base - f * 0.004, base], base, f
        for j in range(1, K + 1):
            a = ang * (j - 0.5) / K
            dr = f * math.cos(a) + n * math.sin(a)
            p = p + dr * (largo / K)
            cam.append(p)
        dedo(cam + [p + dr * (r * 0.55)], r, dedos)
    bp, d0, d1 = mano_pulgar(lado)
    cam, p, dr = [bp - d0 * 0.004, bp], bp, d0
    for j in range(1, K + 1):
        dr = d0.lerp(d1, (j - 0.5) / K).normalized()
        p = p + dr * (0.022 / K)
        cam.append(p)
    dedo(cam + [p + dr * 0.0032], 0.0058, pulgar)


def hacer_cuerpo():
    m = Malla(pesos={"Head": 1.0})
    hacer_cabeza(m)
    m.pesos = None
    cuello = ((0.612, 0.0340), (0.640, 0.0315), (0.665, 0.0300), (0.700, 0.0300))
    m.loft([anillo((0, CY + 0.002, z), (1, 0, 0), (0, 1, 0), r, r * 0.94, 16) for z, r in cuello], uvfun=uv_lisa,
           pesos=w_tronco)
    # torso con camiseta y short: va escondido bajo el abrigo
    n = 24
    ths = [-math.pi + 2 * math.pi * i / n for i in range(n)]
    zs = (0.300, 0.318, 0.335, 0.360, 0.395, 0.430, 0.465, 0.500, 0.535, 0.565, 0.598, 0.616, 0.630, 0.640)
    m.loft([[torso_pt(t, z) for t in ths] for z in zs], vs=[(z - 0.30) / 0.34 for z in zs], rect=DT_CAMISETA, mat=1,
           tapa0=True, tapa1=True, pesos=w_tronco)
    m.loft([[torso_pt(t, z, 0.0005 if z > 0.37 else 0.0035) for t in ths] for z in (0.372, 0.360, 0.335, 0.312, 0.297)],
           rect=DT_SHORT, mat=1, tapa1=True, pesos=w_tronco)
    for lado in (-1, 1):
        S, d, X, Y = brazo(lado)                                       # brazo, dentro de la manga
        est = ((-0.022, 0.0200), (0.0, 0.0245), (0.030, 0.0255), (0.090, 0.0245), (L_CODO, 0.0225), (0.200, 0.0215),
               (0.262, 0.0185), (L_MUNECA + 0.006, 0.0170))
        m.loft([anillo(S + d * s, X, Y, r, r * 0.94, 12) for s, r in est], uvfun=uv_lisa, tapa0=True, pesos=w_brazo(lado))
        hacer_mano(m, lado)
        x, wp = lado * PIERNA_X, w_pierna(lado)                        # pierna
        eje = lambda z, r, dy=0.0, n=14, x=x: anillo((x, CY + dy, z), (1, 0, 0), (0, 1, 0), r, r, n)
        m.loft([eje(z, r) for z, r in ((0.338, 0.0290), (0.300, 0.0298), (0.264, 0.0290), (0.262, 0.0262))],
               rect=DT_SHORT, mat=1, pesos=wp)
        pierna = ((0.275, 0.0262, 0.0), (0.240, 0.0250, 0.0), (0.205, 0.0234, 0.0), (0.182, 0.0224, -0.0010),
                  (0.168, 0.0228, -0.0022), (0.152, 0.0214, -0.0008), (0.128, 0.0196, 0.0))
        m.loft([eje(z, r, dy) for z, r, dy in pierna], uvfun=uv_lisa, pesos=wp)
        calc = ((0.1385, 0.0185), (0.1400, 0.0226), (0.1340, 0.0240), (0.1270, 0.0236), (0.1235, 0.0220),
                (0.100, 0.0216), (0.075, 0.0214), (0.050, 0.0214))
        m.loft([eje(z, r) for z, r in calc], vs=[(z - 0.045) / 0.095 for z, _ in calc], rect=DT_CALCETIN, mat=1, pesos=wp)
        bota(m, lado)
    # curita bajo la rodilla izquierda
    x = PIERNA_X
    filas = [[Vector((x + 0.0236 * math.sin(a), CY - 0.0015 - 0.0236 * math.cos(a), z + 0.010 * a)) for a in
              [math.radians(-62 + 124 * i / 8) for i in range(9)]] for z in (0.148, 0.156, 0.164)]
    m.loft(filas, vs=[0.30, 0.5, 0.70], us=[0.08 + 0.84 * i / 8 for i in range(9)], cerrado=False, rect=DT_CURITA, mat=1,
           fuera=(x, CY, 0.156), pesos=w_pierna(1))
    return m.objeto("Miga_Cuerpo", [MATS["piel"], MATS["detalles"]])


BOTA_NIV = [(0.0000, 0.0, 0.90), (0.0045, 0.0, 1.00), (0.0160, 0.0, 1.00), (0.0195, 0.0, 0.962), (0.0300, 0.0, 0.955),
            (0.0390, 0.10, 0.945), (0.0470, 0.34, 0.95), (0.0550, 0.64, 0.97), (0.0630, 0.88, 1.0), (0.0740, 1.0, 1.0),
            (0.0880, 1.0, 1.05)]                                       # z, mezcla planta -> cana, escala


def bota_ejes(lado):
    """Centro de la bota y sus direcciones hacia la punta y hacia el lado."""
    g = math.radians(-lado * BOTA_GIRO)
    return Vector((lado * PIERNA_X, CY, 0)), Vector((math.sin(g), -math.cos(g), 0)), Vector((math.cos(g), math.sin(g), 0))


def bota(m, lado):
    C, punta, costado = bota_ejes(lado)
    wp = w_pierna(lado)
    n = 22

    def punto(a, t, esc, z):
        px, py = 0.0375 * esc * math.sin(a), 0.012 + (0.054 + 0.011 * math.cos(a)) * esc * math.cos(a)    # planta
        cx, cy = 0.0275 * esc * math.sin(a), -0.004 + 0.0275 * esc * math.cos(a)                           # cana
        return C + costado * (px + (cx - px) * t) + punta * (py + (cy - py) * t) + Vector((0, 0, z))

    ang = [-math.pi + 2 * math.pi * i / n for i in range(n)]
    m.loft([[punto(a, t, e, z) for a in ang] for z, t, e in BOTA_NIV], vs=[z / 0.090 for z, _, _ in BOTA_NIV],
           rect=DT_BOTA, tapa0=True, mat=1, pesos=wp)
    oscuro = lambda p: (DT_BOTA[0] + 0.1, DT_BOTA[2] + 0.04)
    m.loft([[punto(a, 1.0, e, z) for a in ang] for z, e in ((0.0880, 1.05), (0.0885, 0.93), (0.0740, 0.86))],
           uvfun=oscuro, tapa1=True, mat=1, pesos=wp)
    # cordones cruzados sobre el empeine y un lazo arriba
    zs, ts, es = zip(*BOTA_NIV)
    sobre = lambda a, z: punto(a, float(np.interp(z, zs, ts)), float(np.interp(z, zs, es)) * 1.045, z)
    niveles, A = (0.049, 0.060, 0.071, 0.081), 0.52
    for z0, z1 in zip(niveles, niveles[1:]):
        for sg in (-1, 1):
            cam = [sobre(sg * A * (1 - 2 * u), z0 + (z1 - z0) * u) for u in (0, 0.2, 0.4, 0.6, 0.8, 1.0)]
            m.loft(tubo(cam, [(0.0021, 0.0021)] * 6, n=6), rect=DT_CORDON, tapa0=True, tapa1=True, mat=1, pesos=wp)
    P = sobre(0.0, 0.0835) + punta * 0.001
    elipsoide(m, P, costado * 0.0034, Vector((0, 0, 0.0030)), punta * 0.0026, n=8, k=6, rect=DT_CORDON, mat=1, pesos=wp)
    for sg in (-1, 1):
        elipsoide(m, P + costado * (sg * 0.0085) - Vector((0, 0, 0.0030)), (costado * sg + Vector((0, 0, -0.45))) * 0.0080,
                  (Vector((0, 0, 1)) + costado * (sg * 0.45)) * 0.0036, punta * 0.0020, n=10, k=6, rect=DT_CORDON,
                  mat=1, pesos=wp)


def hacer_bufanda():
    m = Malla(pesos={"Chest": 1.0})
    N_ = 44

    def vuelta(Rx, Ry, z0, caida, rr, rv, fase, cuello):
        an = []
        for i in range(N_ + 1):
            a = -math.pi + 2 * math.pi * i / N_
            rad = Vector((math.sin(a), -math.cos(a), 0))
            c = Vector((Rx * math.sin(a), CY - Ry * math.cos(a), z0 - caida * math.cos(a)))
            g = 1 + 0.07 * math.sin(3 * a + fase) + 0.04 * math.sin(7 * a + 2 * fase)
            an.append(anillo(c, rad, (0, 0, 1), rr * g, rv * g, 12))
        m.loft(an, vs=[1.125 * i / N_ for i in range(N_ + 1)], rect=(BU_CUELLO[0], BU_CUELLO[0] + 20 / 48, 0, 1),
               pesos={"Chest": 1 - cuello, "Neck": cuello})

    vuelta(0.098, 0.084, 0.613, 0.010, 0.034, 0.035, 0.4, 0.0)
    vuelta(0.080, 0.070, 0.652, 0.008, 0.029, 0.029, 2.1, 0.4)
    # nudo
    K = Vector((0.064, -0.099, 0.600))
    elipsoide(m, K, Vector((0.034, 0.009, 0.004)), Vector((0.003, 0, -0.026)), Vector((-0.006, 0.023, 0)), n=14, k=10,
              rect=(BU_CUELLO[0], BU_CUELLO[0] + 14 / 48, 0.2, 0.2 + 10 / 64))

    def punta(cam, anchos, arriba, flecos, pesos):
        L = [0.0]
        for i in range(1, len(cam)):
            L.append(L[-1] + (cam[i] - cam[i - 1]).length)
        m.loft(tubo(cam, [(w, 0.0075) for w in anchos], n=12, arriba=arriba), vs=[(L[-1] - s) / BU_M for s in L],
               rect=(BU_PUNTAS[0], BU_PUNTAS[1], 0, 1), tapa0=True, tapa1=True, pesos=pesos)
        fr = marcos(cam, arriba)[-1]
        for j in range(flecos):                                       # flecos
            b = cam[-1] + fr[1] * (anchos[-1] * 0.86 * (2 * j / (flecos - 1) - 1))
            lf = 0.026 + 0.006 * math.sin(j * 2.3)
            c2 = [b + Vector((0, 0, 0.004)), b - Vector((0.001 * math.sin(j * 1.7), 0, lf * 0.5)), b - Vector((0, 0, lf))]
            m.loft(tubo(c2, [(0.0042, 0.0036), (0.0040, 0.0034), (0.0022, 0.0020)], n=6, arriba=arriba),
                   vs=[0.5, 0.52, 0.55], rect=(BU_CUELLO[0], BU_CUELLO[0] + 3 / 48, 0, 1), tapa1=True, pesos=pesos)

    # punta corta al frente: cuelga del nudo siguiendo el abrigo
    cam, anchos = [], []
    for i in range(11):
        t = i / 10
        cam.append(bufanda_frente(BUF_Z - BUF_FRENTE * t, t))
        anchos.append(0.017 + 0.010 * suaviza(t / 0.25))
    punta(cam, anchos, (0, -1, 0), 5, w_cola("BufandaFrente", 3, BUF_FRENTE))
    # punta larga por la espalda
    cam, anchos = [Vector((0.004, CY + 0.100, 0.612))], [0.034]
    for i in range(1, 17):
        t = i / 16
        cam.append(bufanda_cola(BUF_Z - BUF_COLA * t, t))
        anchos.append(0.036 + 0.010 * suaviza(t / 0.3))
    punta(cam, anchos, (0, 1, 0), 8, w_cola("Bufanda", 5, BUF_COLA))
    return m.objeto("Miga_Bufanda", [MATS["bufanda"]])


BUF_Z, BUF_FRENTE, BUF_COLA = 0.598, 0.198, 0.323   # altura donde nacen las puntas y cuanto cuelga cada una


def bufanda_frente(z, t):
    """Centro de la punta corta a una altura (t: 0 en el nudo, 1 en el extremo)."""
    return ab_pt(th_de_x(0.066 + 0.007 * math.sin(2.6 * t), z), z, 0.013 + 0.004 * math.sin(math.pi * t))


def bufanda_cola(z, t):
    """Centro de la punta larga de la espalda a una altura."""
    return ab_pt(math.pi, z, 0.016 + 0.006 * math.sin(math.pi * t)) + Vector((0.006 * math.sin(3.0 * t), 0, 0))


def frasco_eje():
    """Eje del frasco (x, y) y altura del punto mas alto del asa, que pasa por el puno."""
    Q = agarre(-1)
    return Q.x, Q.y, Q.z


def hacer_frasco():
    jx, jy, zt = frasco_eje()
    m = Malla(pesos={"Frasco": 1.0})
    aro = lambda r, z, n=24: anillo((jx, jy, z), (1, 0, 0), (0, 1, 0), r, r, n)
    z0 = zt - 0.052                                                    # borde de arriba de la tapa
    perfil = ((0.0300, -0.016), (0.0312, -0.024), (0.0400, -0.033), (0.0450, -0.045), (0.0455, -0.100), (0.0435, -0.111),
              (0.0360, -0.1175), (0.0150, -0.1190))
    m.loft([aro(r, z0 + dz) for r, dz in perfil], tapa0=True, tapa1=True, rect=(0.05, 0.95, 0.05, 0.95))
    tapa = ((0.0290, 0.0), (0.0340, -0.0025), (0.0345, -0.0165), (0.0320, -0.0180))
    m.loft([aro(r, z0 + dz) for r, dz in tapa], vs=[0.04, 0.2, 0.85, 0.96], rect=DT_TAPA,
           tapa0=True, tapa1=True, mat=1)
    cam = [Vector((jx + 0.0365 * math.cos(a), jy, z0 - 0.008 + 0.060 * math.sin(a))) for a in
           [math.pi * i / 16 for i in range(17)]]
    m.loft(tubo(cam, [(0.0026, 0.0026)] * 17, n=6, arriba=(0, 1, 0)), rect=DT_ALAMBRE, tapa0=True, tapa1=True, mat=1)
    for sg in (-1, 1):                                                 # orejas donde el asa se engancha a la tapa
        elipsoide(m, (jx + sg * 0.0358, jy, z0 - 0.0085), Vector((0.0034, 0, 0)), Vector((0, 0.0052, 0)),
                  Vector((0, 0, 0.0062)), n=8, k=6, rect=DT_ALAMBRE, mat=1)
    ob = m.objeto("Miga_Frasco", [MATS["vidrio"], MATS["detalles"]])
    # Chispa: abdomen que brilla, cuerpo y alas
    c = Malla(pesos={"Chispa": 1.0})
    G = chispa_centro()
    elipsoide(c, G, Vector((0.0105, 0, 0)), Vector((0, 0.0105, 0)), Vector((0, 0, 0.0125)), n=14, k=10)
    elipsoide(c, G + Vector((0, 0.002, 0.016)), Vector((0.0062, 0, 0)), Vector((0, 0.0062, 0)), Vector((0, 0, 0.0085)),
              n=10, k=8, rect=DT_BICHO, mat=1)
    for lado in (-1, 1):
        elipsoide(c, G + Vector((lado * 0.010, 0.006, 0.014)), Vector((0.0085, 0, lado * 0.004)), Vector((0, 0.0012, 0)),
                  Vector((-lado * 0.002, 0, 0.0042)), n=10, k=6, rect=DT_ALA, mat=1)
    ch = c.objeto("Miga_Chispa", [MATS["chispa"], MATS["detalles"]])
    return ob, ch, G
