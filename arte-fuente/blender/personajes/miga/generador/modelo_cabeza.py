# Cabeza, cara, ojos con parpados y pelo de Miga.
HC = Vector((0.0, 0.0, 0.815))               # centro de la cabeza
AX, AY, AZ, AZB = 0.166, 0.158, 0.172, 0.167  # semiejes; AZB = mitad de abajo
# Orilla de cada parpado (1 = borde de arriba del ojo, -1 = borde de abajo). Abiertos casi no tapan: ojo grande y redondo.
PARPADO_ABIERTO, PARPADO_CERRADO = 0.84, -0.58
PARPADO_BAJO, PARPADO_BAJO_CERRADO = -0.90, -0.62


def cab_pt(th, ph, off=0.0):
    """Punto de la cabeza. th: angulo alrededor (0 = frente, + hacia su izquierda); ph: 0 arriba, pi abajo."""
    c, s = math.cos(ph), max(math.sin(ph), 0.0)
    s2, zz = (s ** 0.85, AZB * c) if c < 0 else (s, AZ * c)
    w = 1 + 0.06 * math.exp(-((ph - 2.0) / 0.5) ** 2)                 # mejillas mas anchas
    p = Vector((AX * w * s2 * math.sin(th), -AY * s2 * math.cos(th), zz))
    if off:
        p += Vector((p.x / AX ** 2, p.y / AY ** 2, p.z / AZ ** 2)).normalized() * off
    return HC + p


def cab_normal(p):
    d = Vector(p) - HC
    return Vector((d.x / AX ** 2, d.y / AY ** 2, d.z / AZ ** 2)).normalized()


def phi_de_z(z):
    d = z - HC.z
    return math.acos(limita(d / (AZ if d >= 0 else AZB), -1.0, 1.0))


def cab_en(th_grados, z, off=0.0):
    return cab_pt(math.radians(th_grados), phi_de_z(z), off)


def uv_cara(p):
    return (0.5 + p[0] / CARA_M, 0.5 + (p[2] - CARA_Z) / CARA_M)


def uv_lisa(p):
    return PIEL_LISA


def marco_cara(th_grados, z):
    """Punto sobre la cara y sus ejes: derecha (hacia +X), arriba y normal."""
    P = cab_en(th_grados, z)
    N = cab_normal(P)
    R = Vector((0, 0, 1)).cross(N).normalized()
    return P, R, N.cross(R).normalized(), N


def hacer_cabeza(m):
    """Cabeza, nariz y orejas. Usa los pesos por defecto de la malla (Head)."""
    n, k = 44, 26
    an = [[cab_pt(-math.pi + 2 * math.pi * i / n, math.pi * j / k) for i in range(n)] for j in range(1, k)]
    m.loft(an, tapa0=True, tapa1=True, uvfun=uv_cara)
    P, R, U, N = marco_cara(0, 0.729)                                  # nariz
    elipsoide(m, P - N * 0.0040, R * 0.0088, U * 0.0078, N * 0.0088, n=12, k=8, uvfun=uv_cara)
    for lado in (-1, 1):                                               # orejas
        P = cab_en(lado * 88, 0.776)
        N = cab_normal(P)
        elipsoide(m, P + N * 0.010, Vector((0, 0.017, 0)), Vector((0, 0, 0.028)), N * 0.026, n=12, k=8, uvfun=uv_lisa)


def hacer_ojos():
    """Globos, parpados y pestanas. La forma Parpadeo baja el parpado de arriba hasta cerrar el ojo."""
    m = Malla(pesos={"Head": 1.0})
    nA = 14
    As = [-0.985 + 1.97 * i / nA for i in range(nA + 1)]
    for lado in (-1, 1):
        P, R, U, N = marco_cara(lado * OJO_TH, OJO_Z)
        c = P - N * 0.0036
        atras = c - N * 0.05

        def domo(a, b, sep=0.0, c=c, R=R, U=U, N=N):
            """Punto sobre el globo (a y b van de -1 a 1), separado sep hacia afuera."""
            return c + R * (OJO_RX * a) + U * (OJO_RZ * b) + N * (OJO_RN * math.sqrt(max(1 - a * a - b * b, 0.0)) + sep)

        elipsoide(m, c, R * OJO_RX, U * OJO_RZ, N * OJO_RN, n=24, k=10,
                  uvfun=lambda p, c=c, R=R, U=U: (0.5 + (Vector(p) - c).dot(R) / (2 * OJO_RX) * 0.94,
                                                  0.5 + (Vector(p) - c).dot(U) / (2 * OJO_RZ) * 0.94))

        def filas(signo, orilla, ts, sep=0.0011):
            """Filas del parpado: de su nacimiento (t = 0) al comienzo de la orilla (t = 1); t = 2 es la orilla."""
            out = []
            for t in ts:
                fila = []
                for a in As:
                    raiz = math.sqrt(1 - a * a)
                    fin = (orilla + signo * 0.075) * raiz              # la orilla mide siempre lo mismo
                    if t < 0:                                          # fila escondida dentro de la cabeza
                        fila.append(domo(a * 1.05, signo * raiz * 1.05, -0.0015))
                    elif t > 1:
                        fila.append(domo(a, orilla * raiz, sep))
                    else:
                        fila.append(domo(a, signo * raiz + (fin - signo * raiz) * t, sep))
                out.append(fila)
            return out

        for signo, abierto, cerrado, mat_orilla, tono in ((1, PARPADO_ABIERTO, PARPADO_CERRADO, 1, PIEL_PARPADO),
                                                          (-1, PARPADO_BAJO, PARPADO_BAJO_CERRADO, 2, PIEL_PARPADO_BAJO)):
            piel = (-1,) + tuple((k / 7) ** 2 for k in range(8))       # filas juntas cerca del borde: ahi el globo curva mas
            m.loft(filas(signo, abierto, piel), cerrado=False, uvfun=lambda p, tono=tono: tono, mat=2, fuera=atras,
                   alt=filas(signo, cerrado, piel))
            # orilla: linea de pestanas arriba, piel abajo; la ultima fila dobla hacia el ojo
            ori = filas(signo, abierto, (1.0, 2)) + filas(signo, abierto, (2,), sep=0.0002)
            ori_c = filas(signo, cerrado, (1.0, 2)) + filas(signo, cerrado, (2,), sep=0.0002)
            if mat_orilla == 1:
                m.loft(ori, cerrado=False, mat=1, rect=(0.1, 0.2, 0.6, 0.9), fuera=atras, alt=ori_c)
            else:
                m.loft(ori, cerrado=False, uvfun=lambda p, tono=tono: tono, mat=2, fuera=atras, alt=ori_c)

        radios = [(0.0030, 0.0030), (0.0024, 0.0024), (0.0015, 0.0015), (0.0005, 0.0005)]
        for a0, largo, sube in ((0.80, 0.016, 0.007), (0.58, 0.010, 0.010)):          # pestanas de la esquina de afuera
            def camino(orilla, a0=a0, largo=largo, sube=sube):
                p0 = domo(lado * a0, orilla * math.sqrt(1 - a0 * a0), 0.0013)
                p1 = p0 + R * (lado * largo) + U * sube - N * 0.004
                return [p0.lerp(p1, t) + U * (0.003 * math.sin(math.pi * t)) for t in (0, 0.33, 0.66, 1.0)]

            m.loft(tubo(camino(PARPADO_ABIERTO), radios, n=6, arriba=N), tapa0=True, tapa1=True, mat=1,
                   rect=(0.1, 0.2, 0.6, 0.9), alt=tubo(camino(PARPADO_CERRADO), radios, n=6, arriba=N))
    ob = m.objeto("Miga_Ojos", [MATS["ojos"], MATS["pelo"], MATS["piel"]])
    forma(ob, "Parpadeo")
    return ob


def linea_pelo(th):
    """Altura del borde del pelo segun el angulo en grados (0 = frente)."""
    a = abs(th)
    f = 0.875 + (0.826 - 0.875) * (th - 30) / 28 if th >= 30 else 0.875 + (0.810 - 0.875) * (30 - th) / 88
    lados = 0.676 - 0.020 * suaviza((a - 68) / 112)
    t = suaviza((a - 51) / 11)
    return f * (1 - t) + lados * t


def casco_off(th, z):
    """Separacion del casco de pelo sobre la cabeza en un angulo (grados) y una altura."""
    atras = (1 - math.cos(math.radians(th))) / 2
    fin = phi_de_z(linea_pelo(th))
    t = limita((phi_de_z(z) - 0.03) / (fin - 0.03)) ** (1 / 0.92)
    return 0.0175 + 0.004 * atras + 0.012 * atras * t ** 1.6


def mechon(m, claves, ancho, grosor, off=0.019, levanta=0.010, n=8, K=12, u_esc=0.55, sobre_casco=False):
    """Mechon en punta sobre la cabeza. claves: 3 puntos (angulo en grados, z) de una curva."""
    cam, an = [], []
    for j in range(K + 1):
        t = j / K
        th = (1 - t) ** 2 * claves[0][0] + 2 * t * (1 - t) * claves[1][0] + t * t * claves[2][0]
        z = (1 - t) ** 2 * claves[0][1] + 2 * t * (1 - t) * claves[1][1] + t * t * claves[2][1]
        if sobre_casco:                                                # pegado al casco, no a la cabeza
            sep = casco_off((th + 180) % 360 - 180, z) * (0.55 + 0.45 * suaviza(t / 0.15)) + off * suaviza(t / 0.15)
        else:
            sep = off * (0.30 + 0.70 * suaviza(t / 0.22))
        cam.append(cab_en(th, z, sep + levanta * math.sin(math.pi * t) ** 1.2))
    for j in range(K + 1):
        t = j / K
        T = (cam[min(j + 1, K)] - cam[max(j - 1, 0)]).normalized()
        N = cab_normal(cam[j])
        B = T.cross(N).normalized()
        N = B.cross(T).normalized()
        w = max(ancho * (1 - t) ** 0.6 * (0.78 + 0.22 * math.sin(math.pi * min(t / 0.55, 1.0))), 0.0009)
        g = max(grosor * math.sin(math.pi * (0.12 + 0.88 * t) ** 0.8) ** 0.7 * (1 - t) ** 0.25, 0.0008)
        an.append([cam[j] + B * (w * math.cos(2 * math.pi * i / n))
                   + N * (g * math.sin(2 * math.pi * i / n) * (1.0 if math.sin(2 * math.pi * i / n) > 0 else 0.45))
                   for i in range(n)])
    m.loft(an, vs=[j / K for j in range(K + 1)], us=[u_esc * i / n for i in range(n + 1)], tapa0=True, tapa1=True)


def rizo(m, puntos, r0=0.0048, K=10, **kw):
    cam = [bez3(*puntos, j / K) for j in range(K + 1)]
    m.loft(tubo(cam, [(r0 * (1 - 0.8 * j / K),) * 2 for j in range(K + 1)], n=6),
           us=[0.15 * i / 6 for i in range(7)], tapa0=True, tapa1=True, **kw)


def espiral(m, B, X, Y, d, lado, R=0.0575, vueltas=1.6, ancho=0.019, grosor=0.0085, K=34, n=8, **kw):
    """Mechon enrollado alrededor del mono, de la base a la punta."""
    cam, nor = [], []
    for j in range(K + 1):
        t = j / K
        ang, lat = lado * 2 * math.pi * vueltas * t + 1.0, -0.50 + 1.85 * t
        N = ((X * math.cos(ang) + Y * math.sin(ang)) * math.cos(lat) + d * math.sin(lat)).normalized()
        cam.append(B + N * (R * (1 - 0.05 * t)))
        nor.append(N)
    an = []
    for j in range(K + 1):
        t = j / K
        T = (cam[min(j + 1, K)] - cam[max(j - 1, 0)]).normalized()
        Bv = T.cross(nor[j]).normalized()
        w = max(ancho * (1 - 0.80 * t) * suaviza(t / 0.10 + 0.25), 0.0012)
        g = max(grosor * (1 - 0.65 * t), 0.001)
        an.append([cam[j] + Bv * (w * math.cos(2 * math.pi * i / n))
                   + nor[j] * (g * math.sin(2 * math.pi * i / n) * (1.0 if math.sin(2 * math.pi * i / n) > 0 else 0.3))
                   for i in range(n)])
    m.loft(an, vs=[0.08 + 0.62 * j / K for j in range(K + 1)], us=[0.4 * i / n for i in range(n + 1)], tapa0=True,
           tapa1=True, **kw)


def mono(lado):
    """Centro del mono y sus ejes: d apunta hacia afuera de la cabeza."""
    B = Vector((lado * 0.141, 0.022, 0.966))
    d = (B - (HC + Vector((0, 0, 0.04)))).normalized()
    X = d.cross(Vector((0, 1, 0))).normalized()
    return B, d, X, d.cross(X).normalized()


def hacer_pelo():
    m = Malla(pesos={"Head": 1.0})
    # casco: cubre la cabeza hasta la linea del pelo y se dobla hacia la piel en el borde
    n, K = 72, 14
    an = []
    for j in range(K + 3):
        fila = []
        for i in range(n):
            th = -180 + 360 * i / n
            atras = (1 - math.cos(math.radians(th))) / 2
            ph_fin = phi_de_z(linea_pelo(th))
            t = min(j / K, 1.0)
            off = 0.0175 + 0.004 * atras + 0.012 * atras * t ** 1.6
            if j == K + 1:
                off *= 0.5
            elif j == K + 2:
                off = 0.0005
            fila.append(cab_pt(math.radians(th), 0.03 + (ph_fin - 0.03) * t ** 0.92 + (0.012 if j > K else 0), off))
        an.append(fila)
    m.loft(an, vs=[0.9 * min(j / K, 1.0) for j in range(K + 3)], us=[3 * i / n for i in range(n + 1)], tapa0=True)
    # flequillo de lado: nace en la raya (a su izquierda) y barre hacia su derecha
    for claves, ancho in (
            (((26, 0.966), (-28, 0.958), (-63, 0.802)), 0.050),
            (((27, 0.953), (-16, 0.938), (-45, 0.806)), 0.048),
            (((28, 0.939), (-4, 0.918), (-26, 0.817)), 0.046),
            (((29, 0.924), (10, 0.902), (-6, 0.834)), 0.042),
            (((30, 0.908), (22, 0.890), (13, 0.851)), 0.034),
            (((33, 0.948), (52, 0.928), (62, 0.823)), 0.044),
            (((32, 0.918), (44, 0.897), (45, 0.846)), 0.032)):
        mechon(m, claves, ancho, 0.015)
    for lado in (-1, 1):                                               # mechones largos delante de las orejas
        mechon(m, ((lado * 60, 0.900), (lado * 66, 0.780), (lado * 51, 0.664)), 0.041, 0.013, off=0.016, levanta=0.005,
               n=10, K=14)
    # capas de atras y de los lados: mechones en punta que rompen el borde liso del casco
    for q in range(12):
        th = 76 + 208 * q / 11                                         # de su izquierda, por la nuca, a su derecha
        corto = q % 2                                                  # alterna una capa larga y una corta
        desv = 9 * math.sin(q * 1.7 + 0.5)
        z0 = 0.955 - 0.045 * corto - 0.02 * math.sin(q * 1.3) ** 2
        z1 = linea_pelo((th + desv + 180) % 360 - 180) + (0.012 if corto else -0.006 - 0.016 * math.sin(q * 2.1) ** 2)
        mechon(m, ((th - desv * 0.4, z0), (th + desv * 0.3, 0.800), (th + desv, z1)), 0.045 - 0.007 * corto, 0.0065,
               off=0.0045 - 0.002 * corto, levanta=0.002, n=8, K=10, sobre_casco=True)
    # monos, mechones sueltos y ligas
    for lado in (-1, 1):
        wm = {ext(lado, "Mono"): 1.0}
        B, d, X, Y = mono(lado)
        elipsoide(m, B, X * 0.057, Y * 0.057, d * 0.052, n=22, k=12, girar=True, rect=(0, 2.0, 0.05, 0.75), pesos=wm)
        espiral(m, B, X, Y, d, lado, pesos=wm)
        p0 = B + d * 0.048
        rizo(m, (p0, p0 + Vector((lado * 0.004, 0, 0.040)), p0 + Vector((lado * 0.036, 0, 0.058)),
                 p0 + Vector((lado * 0.044, 0, 0.034))), pesos=wm)
        p0 = B + d * 0.040 + Vector((-lado * 0.022, -0.012, 0.010))
        rizo(m, (p0, p0 + Vector((-lado * 0.012, -0.010, 0.030)), p0 + Vector((-lado * 0.034, -0.014, 0.034)),
                 p0 + Vector((-lado * 0.036, -0.012, 0.016))), r0=0.0040, pesos=wm)
        C = B - d * 0.026                                              # liga roja en la base del mono
        N = 20
        an = [anillo(C + (X * math.cos(2 * math.pi * i / N) + Y * math.sin(2 * math.pi * i / N)) * 0.053,
                     X * math.cos(2 * math.pi * i / N) + Y * math.sin(2 * math.pi * i / N), d, 0.0105, 0.0105, 8)
              for i in range(N + 1)]
        m.loft(an, vs=[i / N for i in range(N + 1)], rect=DT_LIGA, girar=True, mat=1)
    p0 = Vector((0.012, -0.012, 0.992))                                # mechon suelto de arriba
    rizo(m, (p0, p0 + Vector((-0.006, 0, 0.046)), p0 + Vector((0.034, 0, 0.066)), p0 + Vector((0.046, 0, 0.040))), r0=0.0052)
    return m.objeto("Miga_Pelo", [MATS["pelo"], MATS["detalles"]])
