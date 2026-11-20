# La Costurera: 17 m de alto, mira hacia -Y, piso en z = 0. Medidas tomadas de costurera-vistas.png.
HC = Vector((0.0, -1.64, 14.55))              # centro de la cabeza (adelantada: va encorvada)
HRX, HRY, HRZ = 1.12, 1.16, 1.30
CLAVES_VE = [                                 # vestido, z: (radio en x, radio en y, centro en y)
    (0.0, (3.30, 2.40, -0.045)), (0.5, (3.36, 2.39, -0.05)), (1.0, (3.37, 2.305, -0.065)), (2.0, (3.20, 2.22, -0.09)),
    (3.0, (3.01, 2.13, -0.09)), (4.0, (2.88, 2.065, -0.085)), (5.0, (2.73, 2.025, -0.075)), (6.0, (2.58, 1.98, -0.04)),
    (7.0, (2.40, 1.925, -0.005)), (8.0, (2.22, 1.835, 0.015)), (9.0, (2.00, 1.67, 0.03)), (9.5, (1.89, 1.535, 0.015)),
    (10.0, (1.80, 1.465, 0.005)), (10.5, (1.70, 1.345, -0.055)), (11.0, (1.56, 1.21, -0.14)), (11.5, (1.36, 1.03, -0.28)),
    (11.8, (1.12, 0.875, -0.405)), (12.0, (0.78, 0.795, -0.505)), (12.15, (0.40, 0.40, -0.80))]
BRAZO = [                                     # brazo izquierdo (+X): (x, y, z, radio de la manga); el derecho es su espejo
    (0.45, -0.50, 11.55, 0.36), (1.45, -0.32, 11.0, 0.44), (2.15, -0.55, 10.0, 0.40), (2.73, -0.95, 9.0, 0.37),
    (3.12, -1.34, 8.0, 0.35), (3.38, -1.58, 7.0, 0.34), (3.52, -1.75, 6.0, 0.33), (3.55, -1.86, 5.0, 0.33),
    (3.52, -1.92, 4.45, 0.345)]
CLAVES_PELO = [(0, (15.12,)), (40, (15.02,)), (65, (14.85,)), (80, (14.55,)), (100, (14.0,)), (130, (13.75,)), (180, (13.70,))]


# ----------------------------------------------------------------------------- superficies
def cab(th, ph, off=0.0):
    s, c = max(math.sin(ph), 0.0), math.cos(ph)
    p = Vector((HRX * s * math.sin(th), -HRY * s * math.cos(th), HRZ * c))
    if off:
        p += Vector((p.x / HRX ** 2, p.y / HRY ** 2, p.z / HRZ ** 2)).normalized() * off
    return HC + p


def cab_n(p):
    d = Vector(p) - HC
    return Vector((d.x / HRX ** 2, d.y / HRY ** 2, d.z / HRZ ** 2)).normalized()


def ph_z(z):
    return math.acos(limita((z - HC.z) / HRZ, -1.0, 1.0))


def cab_en(th_grados, z, off=0.0):
    return cab(math.radians(th_grados), ph_z(z), off)


def ve_radios(th, z):
    rx, ry, cy = curva(CLAVES_VE, z)
    amp = 0.045 * limita((6.5 - z) / 6.5) ** 1.4                       # pliegues hacia el ruedo
    k = 1 + amp * math.cos(9 * th + 0.8) + 0.45 * amp * math.cos(4 * th + 2.1)
    return rx * k, ry * k, cy


def ve_pt(th, z, off=0.0):
    """Punto del vestido. th en radianes: 0 = frente, + hacia su izquierda."""
    rx, ry, cy = ve_radios(th, z)
    return Vector(((rx + off) * math.sin(th), cy - (ry + off) * math.cos(th), z))


def ve_marco(th, z, off=0.0):
    e = 0.004
    P = ve_pt(th, z, off)
    R = (ve_pt(th + e, z, off) - ve_pt(th - e, z, off)).normalized()
    U = (ve_pt(th, z + e, off) - ve_pt(th, z - e, off)).normalized()
    N = R.cross(U).normalized()
    if N.dot(Vector((math.sin(th), -math.cos(th), 0))) < 0:
        N = -N
    return P, R, U, N


def th_de_x(x, z, atras=False):
    th = 0.0
    for _ in range(6):
        th = math.asin(limita(x / ve_radios(math.pi - th if atras else th, z)[0], -1, 1))
    return math.pi - th if atras else th


def lamina(m, th_c, z_c, ancho, alto, giro, off_c, off_b, rect, mat, nx=8, nz=8, pelo=0.12):
    """Parche pegado al vestido, abombado al centro."""
    e = 0.004
    r = (ve_pt(th_c + e, z_c) - ve_pt(th_c - e, z_c)).length / (2 * e)
    cg, sg = math.cos(math.radians(giro)), math.sin(math.radians(giro))
    filas = []
    for j in range(nz + 1):
        fila = []
        for i in range(nx + 1):
            a, b = ancho * (i / nx - 0.5), alto * (j / nz - 0.5)
            borde = min(min(i, nx - i) * ancho / nx, min(j, nz - j) * alto / nz)
            fila.append(ve_pt(th_c + (a * cg - b * sg) / r, z_c + a * sg + b * cg, off_b + (off_c - off_b) * suaviza(borde / pelo)))
        filas.append(fila)
    m.loft(filas, vs=[j / nz for j in range(nz + 1)], us=[i / nx for i in range(nx + 1)], cerrado=False, rect=rect, mat=mat,
           fuera=(0, 0, z_c))


def brazo_pts(lado, sub=3):
    claves = [(float(i), c) for i, c in enumerate(BRAZO)]
    out = []
    for j in range((len(BRAZO) - 1) * sub + 1):
        x, y, z, r = curva(claves, j / sub)
        out.append((Vector((lado * x, y, z)), r))
    return out


def mano_centro(lado):
    return Vector((lado * 3.45, -2.0, 2.28))


def agujas(lado):
    """Base y punta de las cuatro agujas de una mano, de afuera hacia adentro."""
    K = mano_centro(lado)
    out = []
    for dx, dy, zt in ((0.68, -0.26, 0.44), (0.21, -0.10, 0.21), (-0.15, 0.06, 0.21), (-0.72, 0.22, 0.44)):
        punta = Vector((K.x + lado * dx, K.y + dy, zt))
        out.append((K + (punta - K).normalized() * 0.16, punta))
    return out


def tijeras_marco():
    """Punto de las tijeras sobre el vestido, sus ejes y el angulo donde cuelgan."""
    th_t = th_de_x(1.17, 7.3)
    return ve_marco(th_t, 7.25, 0.11) + (th_t,)


def tijeras_eje():
    """De donde cuelgan (en el cinto) y su tornillo: el hueso Tijeras va de uno a otro."""
    P, R, U, N, th_t = tijeras_marco()
    return ve_pt(th_t - 0.02, 9.74, 0.07), P + U * (0.45 * 1.25)


# ----------------------------------------------------------------------------- piezas
def hacer_cuerpo():
    m = Malla(pesos={"Head": 1.0})
    n, k = 40, 22
    m.loft([[cab(-math.pi + 2 * math.pi * i / n, math.pi * j / k) for i in range(n)] for j in range(1, k)], tapa0=True, tapa1=True)
    cam = [Vector((0, -0.74 - 0.47 * t, 11.9 + 1.5 * t)) for t in (0, 0.25, 0.5, 0.75, 1)]             # cuello hacia adelante
    m.loft(tubo(cam, [(0.27, 0.29)] * 5, n=16, arriba=(0, -1, 0)), pesos=w_cuello)
    for lado in (-1, 1):
        P = cab_en(lado * 108, 14.3)                                                                   # orejas
        N = cab_n(P)
        elipsoide(m, P + N * 0.02, Vector((0, 0.16, 0)), Vector((0, 0, 0.30)), N * 0.13, n=10, k=6)
        pts = brazo_pts(lado)                                                                          # antebrazos, como palos
        W, K = pts[-1][0], mano_centro(lado)
        m.loft(tubo([pts[-3][0], W, W.lerp(K, 0.5), K], [(0.17, 0.17), (0.17, 0.17), (0.155, 0.155), (0.15, 0.15)], n=10,
                    arriba=(0, -1, 0)), tapa0=True, tapa1=True, pesos={hum(lado, "LowerArm"): 1.0})
    return m.objeto("Costurera_Cuerpo", [MATS["piel"]])


def hacer_mano(lado):
    m = Malla(pesos={hum(lado, "Hand"): 1.0})
    K = mano_centro(lado)
    elipsoide(m, K, Vector((0.27, 0, 0)), Vector((0, 0.27, 0)), Vector((0, 0, 0.29)), n=14, k=10)
    for j, (base, punta) in enumerate(agujas(lado)):                                                   # un dedo = una aguja = un hueso
        cam = [base, base.lerp(punta, 0.06), base.lerp(punta, 0.5), base.lerp(punta, 0.93), punta]
        m.loft(tubo(cam, [(0.085, 0.085), (0.062, 0.062), (0.055, 0.055), (0.026, 0.026), (0.004, 0.004)], n=6, arriba=(0, -1, 0)),
               tapa0=True, tapa1=True, mat=1, pesos={ext(lado, "Aguja_%d" % (j + 1)): 1.0})
    return m.objeto("Costurera_Mano_D" if lado < 0 else "Costurera_Mano_I", [MATS["piel"], MATS["metal"]])


def hacer_cara():
    """Tela de la cara: malla aparte, con sus botones y las tiras que la atan por detras."""
    m = Malla(pesos={"Cara": 1.0})
    nx, nz, z0, z1, thm = 30, 24, 13.30, 15.28, math.radians(72)
    uv = lambda p: uv_cara(math.atan2(p[0] / HRX, -(p[1] - HC.y) / HRY), p[2])
    filas = []
    for j in range(nz + 1):
        z = z0 + (z1 - z0) * j / nz
        fila = []
        for i in range(nx + 1):
            th = -thm + 2 * thm * i / nx
            borde = min(min(i, nx - i) * 2 * thm * CA_R / nx, min(j, nz - j) * (z1 - z0) / nz)
            off = (0.012 + 0.05 * suaviza(borde / 0.12) + 0.11 * math.exp(-((th * CA_R / 0.17) ** 2 + ((z - 14.22) / 0.21) ** 2))
                   + 0.012 * math.sin(7 * z + 3 * th))
            fila.append(cab_en(math.degrees(th), z, off))
        filas.append(fila)
    m.loft(filas, cerrado=False, uvfun=uv, fuera=HC)
    for th, z, r, blo, giro in ((-27, 14.50, 0.30, "BOTON_NEGRO", 12), (27, 14.42, 0.235, "BOTON_CREMA", -20)):   # ojos: dos botones distintos
        P = cab_en(th, z, 0.07)
        N = cab_n(P)
        R = Vector((0, 0, 1)).cross(N).normalized()
        U = N.cross(R)
        g = math.radians(giro)
        R, U = R * math.cos(g) + U * math.sin(g), U * math.cos(g) - R * math.sin(g)
        b = DT[blo]
        uvb = lambda p, P=P, R=R, U=U, r=r, b=b: ((b[0] + b[1]) / 2 + (Vector(p) - P).dot(R) / r * 0.112,
                                                 (b[2] + b[3]) / 2 + (Vector(p) - P).dot(U) / r * 0.112)
        m.loft([anillo(P + N * h, R, U, rr, rr, 20) for rr, h in ((r * 0.84, 0.075), (r, 0.055), (r * 1.02, 0.0))], uvfun=uvb,
               tapa0=True, mat=1)
    tela = dentro(DT["TELA"])
    cam = [cab_en(72 + 216 * i / 24, 14.50 - 0.10 * math.sin(math.pi * i / 24), 0.035 + 0.115 * suaviza(min(i, 24 - i) / 3))
           for i in range(25)]
    m.loft(tubo(cam, [(0.055, 0.016)] * 25, n=8, arriba=cab_n(cam[0])), rect=tela, tapa0=True, tapa1=True, mat=1)
    K = cab_en(180, 14.40, 0.19)                                                                       # nudo y puntas
    elipsoide(m, K, Vector((0.11, 0, 0)), Vector((0, 0.07, 0)), Vector((0, 0, 0.09)), n=10, k=6, rect=tela, mat=1)
    for lado in (-1, 1):
        c2 = [K, K + Vector((lado * 0.13, 0.05, -0.22)), K + Vector((lado * 0.24, 0.02, -0.52))]
        m.loft(tubo(c2, [(0.05, 0.014), (0.05, 0.014), (0.035, 0.012)], n=8, arriba=(0, 1, 0)), rect=tela, tapa0=True, tapa1=True, mat=1)
    return m.objeto("Costurera_Cara", [MATS["cara"], MATS["detalles"]])


def espiral(m, B, X, Y, d, R, vueltas, ancho, grosor, K=44, n=8):
    cam, nor = [], []
    for j in range(K + 1):
        t = j / K
        ang, lat = 2 * math.pi * vueltas * t + 1.0, -0.50 + 1.85 * t
        N = ((X * math.cos(ang) + Y * math.sin(ang)) * math.cos(lat) + d * math.sin(lat)).normalized()
        cam.append(B + N * (R * (1 - 0.05 * t)))
        nor.append(N)
    an = []
    for j in range(K + 1):
        t = j / K
        T = (cam[min(j + 1, K)] - cam[max(j - 1, 0)]).normalized()
        Bv = T.cross(nor[j]).normalized()
        w = max(ancho * (1 - 0.80 * t) * suaviza(t / 0.10 + 0.25), 0.012)
        g = max(grosor * (1 - 0.65 * t), 0.01)
        an.append([cam[j] + Bv * (w * math.cos(2 * math.pi * i / n))
                   + nor[j] * (g * math.sin(2 * math.pi * i / n) * (1.0 if math.sin(2 * math.pi * i / n) > 0 else 0.3))
                   for i in range(n)])
    m.loft(an, vs=[0.08 + 0.62 * j / K for j in range(K + 1)], us=[0.4 * i / n for i in range(n + 1)], tapa0=True, tapa1=True)


def linea_pelo(th_grados):
    return curva(CLAVES_PELO, abs(((th_grados + 180) % 360) - 180))[0]


def hacer_pelo():
    m = Malla(pesos={"Mono": 1.0})                                                                   # mono y alfileres; el casco va con la cabeza
    n, K = 56, 12
    an = []
    for j in range(K + 3):                                                                             # casco tirante
        fila = []
        for i in range(n):
            th = -180 + 360 * i / n
            off = 0.085 if j <= K else (0.045 if j == K + 1 else 0.004)
            fila.append(cab(math.radians(th), 0.03 + (ph_z(linea_pelo(th)) - 0.03) * min(j / K, 1.0) ** 0.95 + (0.01 if j > K else 0), off))
        an.append(fila)
    m.loft(an, vs=[0.9 * min(j / K, 1.0) for j in range(K + 3)], us=[3 * i / n for i in range(n + 1)], tapa0=True, pesos={"Head": 1.0})
    BC = Vector((0, -0.80, 16.2))                                                                      # mono apretado
    d = (BC - (HC + Vector((0, 0.2, 0.6)))).normalized()
    X = d.cross(Vector((0, 1, 0))).normalized()
    Y = d.cross(X).normalized()
    elipsoide(m, BC, X * 0.70, Y * 0.70, d * 0.68, n=24, k=14, girar=True, rect=(0, 2, 0.05, 0.75))
    espiral(m, BC, X, Y, d, 0.705, 2.2, 0.20, 0.085)
    for dx, dy, dz, L, r, blo in ((-0.68, -0.15, 0.71, 1.45, 0.115, "A_ROJO"), (0.10, 0.12, 0.99, 1.47, 0.115, "A_CREMA"),
                                  (0.75, -0.10, 0.65, 1.48, 0.115, "A_ROJO"), (-0.30, -0.75, 0.58, 1.12, 0.085, "A_CREMA"),
                                  (0.45, -0.62, 0.64, 1.18, 0.085, "A_ROJO"), (-0.25, 0.80, 0.55, 1.10, 0.085, "A_ROJO"),
                                  (0.55, 0.62, 0.56, 1.15, 0.085, "A_CREMA"), (-0.86, 0.28, 0.42, 1.08, 0.085, "A_CREMA")):   # alfileres
        v = Vector((dx, dy, dz)).normalized()
        a, b = BC + v * 0.35, BC + v * L
        m.loft(tubo([a, b], [(0.022, 0.022)] * 2, n=6), tapa0=True, tapa1=True, mat=1)
        elipsoide(m, b, Vector((r, 0, 0)), Vector((0, r, 0)), Vector((0, 0, r)), n=10, k=6, rect=dentro(DT[blo], 0.2), mat=2)
    return m.objeto("Costurera_Pelo", [MATS["pelo"], MATS["metal"], MATS["detalles"]])


def hacer_vestido():
    m = Malla(pesos=w_vestido)
    n = 64
    ths = [-math.pi / 2 + 2 * math.pi * i / n for i in range(n)]
    zs = [12.15, 12.08, 11.95, 11.8, 11.6, 11.35, 11.0, 10.6, 10.2, 9.8, 9.4, 9.0, 8.5, 8.0, 7.4, 6.8, 6.2, 5.6, 5.0, 4.4, 3.8,
          3.2, 2.6, 2.0, 1.5, 1.0, 0.6, 0.3, 0.1, 0.02]
    m.loft([[ve_pt(t, z) for t in ths] for z in zs], vs=[z / VE_Z1 for z in zs], rect=VE_CUERPO, tapa0=True)
    oscuro = lambda p: VE_OSCURO
    m.loft([[ve_pt(t, 0.02) for t in ths], [ve_pt(t, 0.0, -0.05) for t in ths], [ve_pt(t, 0.04, -0.14) for t in ths]], uvfun=oscuro,
           tapa1=True)
    for lado, blo in ((-1, VE_MANGA_D), (1, VE_MANGA_I)):                                              # mangas
        pts = brazo_pts(lado)
        cam = [p for p, _ in pts]
        L = [0.0]
        for i in range(1, len(cam)):
            L.append(L[-1] + (cam[i] - cam[i - 1]).length)
        an = tubo(cam, [(r, r * 0.94) for _, r in pts], n=18, arriba=(0, -1, 0))
        m.loft(an, vs=[s / L[-1] for s in L], rect=blo, girar=True, tapa0=True, pesos=w_manga(lado))
        fr = marcos(cam, (0, -1, 0))[-1]
        r = pts[-1][1]
        boca = [anillo(cam[-1] - fr[0] * h, fr[1], fr[2], r * e, r * 0.94 * e, 18) for h, e in ((0.0, 1.0), (0.02, 0.86), (0.45, 0.80))]
        m.loft(boca, uvfun=oscuro, tapa1=True, pesos=w_manga(lado))
    canesu = lambda p: (0.25, VE_CUERPO[2] + (VE_CUERPO[3] - VE_CUERPO[2]) * 11.9 / VE_Z1)
    aro = lambda r, z: anillo((0, -0.80, z), (1, 0, 0), (0, 1, 0), r, r, 24)
    m.loft([aro(0.40, 12.10), aro(0.47, 12.16), aro(0.45, 12.27), aro(0.36, 12.30), aro(0.30, 12.20)], uvfun=canesu)   # cuello
    zb = lambda t: 9.82 - 0.13 * math.cos(t)                                                           # cinturon
    m.loft([[ve_pt(t, zb(t) + dz, off) for t in ths] for dz, off in ((0.11, 0.0), (0.09, 0.05), (-0.09, 0.05), (-0.11, 0.0))],
           rect=dentro(DT["CINTURON"]), mat=1, fuera=(0, 0, 9.8))
    for x, z, an_, al, giro, blo, atras in (                                                           # retazos
            (-0.55, 7.63, 1.32, 1.80, -12, "P_CLARO", False), (-0.57, 5.55, 0.80, 0.95, -8, "P_ROJO", False),
            (1.25, 3.88, 1.60, 2.05, -12, "P_MALVA", False), (-1.72, 2.39, 1.50, 2.05, -8, "P_OSCURO", False),
            (-1.42, 4.49, 1.50, 2.05, 8, "P_CLARO", True), (1.42, 2.39, 1.50, 2.00, 10, "P_MALVA", True)):
        lamina(m, th_de_x(x, z, atras), z, an_, al, giro, 0.05, 0.008, dentro(DT[blo]), 1)
    lamina(m, math.radians(-82), 6.74, 1.30, 1.80, 6, 0.05, 0.008, dentro(DT["P_CLARO"]), 1)
    lamina(m, math.radians(-74), 2.99, 1.40, 2.00, -6, 0.05, 0.008, dentro(DT["P_MALVA"]), 1)
    lamina(m, math.radians(96), 4.6, 1.20, 1.50, -10, 0.05, 0.008, dentro(DT["P_ROJO"]), 1)
    for z in (10.35, 9.33, 8.44, 7.50):                                                                # cruces de hilo rojo en la espalda
        for giro in (45, -45):
            lamina(m, math.pi, z, 0.66, 0.075, giro, 0.04, 0.04, dentro(DT["HILO"], 0.1), 1, nx=4, nz=1)
    return m.objeto("Costurera_Vestido", [MATS["vestido"], MATS["detalles"]])


def hacer_accesorios():
    m = Malla(pesos={"Tijeras": 1.0})                                                                # la cinta sigue al tronco
    # cinta metrica colgada del cuello: baja mas por su derecha que por su izquierda
    pts = []
    for i in range(11):
        z, x = 6.64 + (11.75 - 6.64) * i / 10, -0.44 - 0.12 * i / 10
        pts.append(ve_marco(th_de_x(x, z), z, 0.10))
    N0 = pts[0][3]
    cam = [p[0] for p in pts]
    cam += [Vector(p) for p in ((-0.57, -1.10, 12.02), (-0.50, -0.92, 12.16), (-0.40, -0.74, 12.25), (-0.22, -0.56, 12.29),
                                (0.0, -0.50, 12.30), (0.22, -0.56, 12.29), (0.40, -0.74, 12.25), (0.50, -0.92, 12.16),
                                (0.59, -1.10, 12.02))]
    for i in range(9):
        z, x = 11.75 - (11.75 - 7.82) * i / 8, 0.60 + 0.18 * i / 8
        cam.append(ve_pt(th_de_x(x, z), z, 0.10))
    an = tubo(cam, [(0.085, 0.012)] * len(cam), n=8, arriba=N0)
    cinta = dentro(DT["CINTA"], 0.02)
    us = [(math.cos(2 * math.pi * i / 8) + 1) / 2 for i in range(9)]
    for k in range(len(an) - 1):                                                                       # cada tramo repite las marcas
        m.loft([an[k], an[k + 1]], vs=[0.0, 1.0], us=us, rect=cinta, tapa0=(k == 0), tapa1=(k == len(an) - 2), pesos=w_tronco)
    # tijeras colgando del cinto, a su izquierda
    P, R, U, N, th_t = tijeras_marco()
    Lc = lambda a, b, c=0.0: P + R * (a * 1.25) + U * (b * 1.25) + N * c
    for sg in (-1, 1):
        c = 0.030 * sg
        ojo = [anillo(Lc(sg * 0.20 + 0.165 * math.cos(t), 0.95 + 0.165 * math.sin(t), c), R * math.cos(t) + U * math.sin(t), N, 0.050, 0.034, 6)
               for t in [2 * math.pi * i / 18 for i in range(19)]]
        m.loft(ojo, mat=1)
        m.loft(tubo([Lc(sg * 0.165, 0.80, c), Lc(sg * 0.07, 0.60, c), Lc(0, 0.45, c)], [(0.055, 0.030), (0.072, 0.030), (0.095, 0.030)],
                    n=6, arriba=N), tapa0=True, tapa1=True, mat=1)
        a, b = Lc(0, 0.45, c), Lc(-sg * 0.06, -1.30, c)
        m.loft(tubo([a.lerp(b, t) for t in (0, 0.15, 0.45, 0.75, 0.94, 1.0)],
                    [(0.115, 0.030), (0.115, 0.027), (0.090, 0.022), (0.060, 0.016), (0.024, 0.010), (0.004, 0.004)], n=4, arriba=N),
               tapa0=True, tapa1=True, mat=1)
    m.loft([anillo(Lc(0, 0.45, h), R, U, 0.07, 0.07, 10) for h in (0.075, -0.075)], tapa0=True, tapa1=True, mat=1)
    cuelga = [tijeras_eje()[0], ve_pt(th_t - 0.03, 9.1, 0.10), Lc(-0.20, 1.115, -0.030)]
    m.loft(tubo(cuelga, [(0.014, 0.014)] * 3, n=5, arriba=N), rect=dentro(DT["TELA"]), tapa0=True, tapa1=True)
    return m.objeto("Costurera_Accesorios", [MATS["detalles"], MATS["metal"]])
