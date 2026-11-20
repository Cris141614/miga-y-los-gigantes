# Texturas de La Costurera, pintadas con numpy. El modelo usa estas mismas zonas UV.
VE_Z1 = 12.15                                 # altura del cuello del vestido (m)
VE_CUERPO = (0.0, 1.0, 0.22, 1.0)             # u = angulo (0 = costado derecho, 0.25 = frente, 0.75 = espalda), v = altura
VE_MANGA_D = (0.0, 0.5, 0.0, 0.2)
VE_MANGA_I = (0.5, 1.0, 0.0, 0.2)
VE_OSCURO = (0.5, 0.224)                      # punto del ruedo, para el interior
CA_ANG, CA_Z0, CA_Z1, CA_R = math.radians(75), 13.28, 15.30, 1.13     # tela de la cara: medio angulo, alturas y radio
DT = dict(BOTON_NEGRO=(0, .25, .75, 1), BOTON_CREMA=(.25, .5, .75, 1), CINTA=(.5, .75, .75, 1), HILO=(.75, 1, .75, 1),
          P_CLARO=(0, .25, .5, .75), P_ROJO=(.25, .5, .5, .75), P_MALVA=(.5, .75, .5, .75), P_OSCURO=(.75, 1, .5, .75),
          CINTURON=(0, .25, .25, .5), TELA=(.25, .5, .25, .5), A_ROJO=(.5, .75, .25, .5), A_CREMA=(.75, 1, .25, .5))


def uv_cara(th, z):
    return (0.5 + th / (2 * CA_ANG) * 0.92, 0.04 + 0.92 * (z - CA_Z0) / (CA_Z1 - CA_Z0))


def dentro(r, m=0.035):
    """Bloque del atlas con margen, para que no se cuele el color del vecino."""
    return (r[0] + m * (r[1] - r[0]), r[1] - m * (r[1] - r[0]), r[2] + m * (r[3] - r[2]), r[3] - m * (r[3] - r[2]))


def bloque(U, V, r):
    bu, bv = (U - r[0]) / (r[1] - r[0]), (V - r[2]) / (r[3] - r[2])
    return bu, bv, ((bu >= 0) & (bu < 1) & (bv >= 0) & (bv < 1)).astype(np.float32)


def trama(U, V, N, p):
    return 0.5 + 0.5 * np.sin(2 * math.pi * U * N / p) * np.sin(2 * math.pi * V * N / p)


def tex_cara():
    N = 1024
    a, U, V = lienzo(N, N, "#D9D0BC")
    S = (U - 0.5) / 0.92 * 2 * CA_ANG * CA_R                    # metros sobre la cara, en horizontal
    Z = CA_Z0 + (V - 0.04) / 0.92 * (CA_Z1 - CA_Z0)
    px = 0.0031
    a *= (0.94 + 0.08 * trama(U, V, N, 9) + 0.04 * ruido(N, N, 50, 21) + 0.02 * ruido(N, N, 1.5, 22))[..., None]
    mezcla(a, "#B5AB95", np.clip((np.abs(S) - 0.85) / 0.6, 0, 1) * 0.55)              # mas oscura hacia los lados
    mezcla(a, "#B5AB95", np.clip((13.75 - Z) / 0.5, 0, 1) * 0.35)
    mezcla(a, "#A2957A", np.clip(ruido(N, N, 35, 23) * 1.4 - 0.35, 0, 1) * 0.32)      # manchas viejas
    for sx, sz, r in ((-0.53, 14.50, 0.46), (0.53, 14.42, 0.38)):
        mezcla(a, "#A99F8A", np.exp(-(((S - sx) / r) ** 2 + ((Z - sz) / r) ** 2) ** 1.2) * 0.55)   # sombra de los botones
    mezcla(a, "#BBB09A", lleno(np.abs(S) - 0.04, px) * ((Z > 13.36) & (Z < 15.22)) * 0.65)       # pliegue de la costura
    mezcla(a, "#C8553D", lleno(np.abs(S) - 0.017, px) * (((Z * 100) % 16) < 9.5) * ((Z > 13.40) & (Z < 15.18)))
    p0, p1, p2 = (-0.58, 13.83), (0.0, 13.43), (0.58, 13.83)                           # boca remendada

    def B(t):
        return [(1 - t) ** 2 * p0[k] + 2 * t * (1 - t) * p1[k] + t * t * p2[k] for k in (0, 1)]

    for i in range(20):
        q0, q1 = B(i / 20), B((i + 1) / 20)
        mezcla(a, "#7E2F22", lleno(sd_capsula(S, Z, q0[0], q0[1], q1[0], q1[1], 0.020), px))
    for t in (0.07, 0.24, 0.41, 0.59, 0.76, 0.93):
        q = B(t)
        mezcla(a, "#C8553D", lleno(sd_capsula(S, Z, q[0] - 0.02, q[1] - 0.12, q[0] + 0.02, q[1] + 0.12, 0.017), px))
    orilla = ((U > 0.046) & (U < 0.085)) | ((U > 0.915) & (U < 0.954))                 # puntadas del borde
    mezcla(a, "#C8553D", orilla * (((Z * 100) % 13) < 3.0) * 1.0)
    mezcla(a, "#C8553D", ((V > 0.046) & (V < 0.080)) * (((S * 100) % 13) < 3.0) * 1.0)
    return guardar(a, "tex_costurera_cara")


def tex_pelo():
    N = 512
    a, U, V = lienzo(N, N, "#6B6775")
    s1, s2 = ruido(N, N, 90, 31, sx=1.6), ruido(N, N, 140, 32, sx=6)
    a *= (1 + 0.20 * (0.6 * s1 + 0.4 * s2))[..., None]
    mezcla(a, "#CFCCD8", np.clip(ruido(N, N, 120, 33, sx=1.0) * 2.2 - 1.25, 0, 1) * 0.6)     # canas
    mezcla(a, "#9F9CB0", np.exp(-((V - 0.4) / 0.09) ** 2) * (0.5 + 0.5 * np.clip(s1 * 1.5 + 0.4, 0, 1)) * 0.35)
    return guardar(a, "tex_costurera_pelo")


def tex_vestido():
    N = 2048
    a, U, V = lienzo(N, N, "#4F4059")
    alt = np.zeros((N, N), np.float32)
    tr = trama(U, V, N, 11)
    # ---- cuerpo: retazos cosidos
    bu, bv, mk = bloque(U, V, VE_CUERPO)
    Z = bv * VE_Z1
    rng = np.random.default_rng(7)
    cols = 12
    w = (U - 0.75) % 1.0                                         # 0 = espalda, 0.5 = frente
    b = np.linspace(0, 1, cols + 1)
    b[1:-1] += rng.uniform(-0.014, 0.014, cols - 1)
    idx = np.clip(np.searchsorted(b, w, side="right") - 1, 0, cols - 1)
    dv = np.minimum(w - b[idx], b[idx + 1] - w) * N              # distancia a la costura vertical (px)
    cortes = np.sort(rng.uniform(1.4, 10.6, (cols, 3)), axis=1).astype(np.float32)
    celda = np.zeros((N, N), np.int64)
    dh = np.full((N, N), 1e9, np.float32)
    for c in range(3):
        cz = cortes[:, c][idx]
        celda += Z > cz
        dh = np.minimum(dh, np.abs(Z - cz) / VE_Z1 * 0.78 * N)
    claros = [hexrgb(h) for h in ("#4F4059", "#554562", "#4B3D56", "#5A4966")]
    oscuros = [hexrgb(h) for h in ("#43364C", "#473A52", "#3F3247", "#4B3D56")]
    tabla = np.zeros((cols, 4, 3), np.float32)
    for i in range(cols):
        centro = (b[i] + b[i + 1]) / 2
        for j in range(4):
            pal = claros if 0.37 < centro < 0.63 else oscuros
            tabla[i, j] = pal[int(rng.integers(0, 4))]
    mezcla(a, (0, 0, 0), mk)
    a += tabla[idx, celda] * mk[..., None]
    a *= (0.90 + 0.12 * tr + 0.04 * ruido(N, N, 1.4, 41) + 0.06 * ruido(N, N, 120, 42))[..., None]
    alt += (tr - 0.5) * 0.5
    canesu = mk * (Z > 11.35)
    mezcla(a, "#43364C", canesu * 0.9)
    ruedo = mk * (Z < 0.38)
    mezcla(a, "#3A2E42", ruedo * 0.95)
    suc = np.clip(ruido(N, N, 30, 43) * 1.5 - 0.2, 0, 1) * np.clip((2.4 - Z) / 2.4, 0, 1) * mk
    mezcla(a, "#5B5148", suc * 0.35)                             # polvo del piso
    for uc in (0.0, 0.5, 1.0):                                   # sombra bajo los brazos
        a *= (1 - mk * 0.22 * np.exp(-(((U - uc) / 0.045) ** 2 + ((Z - 10.3) / 1.3) ** 2)))[..., None]
    a *= (1 - mk * 0.10 * np.exp(-((Z - 9.75) / 0.35) ** 2))[..., None]              # sombra del cinturon
    costura = lleno(np.minimum(dv, dh) - 1.3, 1.0) * mk * (Z < 11.35) * (Z > 0.38)
    mezcla(a, "#2A2132", costura * 0.9)
    alt -= costura * 0.7
    punt = (lleno(np.abs(dv - 6) - 1.6, 1.0) * (((V * N) % 26) < 15) + lleno(np.abs(dh - 6) - 1.6, 1.0) * (((U * N) % 26) < 15))
    punt = np.clip(punt, 0, 1) * mk * (Z < 11.3) * (Z > 0.45) * (((idx + celda) % 3) != 0)
    mezcla(a, "#CFC5B0", punt * 0.75)
    alt += punt * 0.5
    for zc in (11.35, 0.38):                                     # pespunte del canesu y del ruedo
        p = lleno(np.abs((Z - zc) / VE_Z1 * 0.78 * N - (5 if zc < 1 else -5)) - 1.6, 1.0) * (((U * N) % 26) < 15) * mk
        mezcla(a, "#CFC5B0", p * 0.75)
        alt += p * 0.5
    esp = lleno(np.abs((U - 0.75) * N) - 2.2, 1.0) * (((Z * 100) % 37) < 22) * mk * (Z > 0.6) * (Z < 10.95)
    mezcla(a, "#D9D0BC", esp)                                    # cierre de la espalda
    alt += esp * 0.6
    # ---- mangas
    for blo in (VE_MANGA_D, VE_MANGA_I):
        bu, bv, mk = bloque(U, V, blo)
        mezcla(a, "#5C4B6B", mk)
        a *= (1 - mk * (1 - (0.90 + 0.12 * tr + 0.05 * ruido(N, N, 110, 44))))[..., None]
        a *= (1 - mk * 0.18 * np.clip((0.10 - bu) / 0.10, 0, 1))[..., None]
        puno = mk * (bu > 0.93)
        mezcla(a, "#43364C", puno * 0.85)
        p = lleno(np.abs((bu - 0.92) * 0.5 * N) - 1.6, 1.0) * (((V * N) % 26) < 15) * mk
        mezcla(a, "#CFC5B0", p * 0.75)
        alt += p * 0.5 + mk * (tr - 0.5) * 0.0
    guardar(normal_de_altura(alt, 4.5), "tex_costurera_vestido_normal", nocolor=True)
    return guardar(a, "tex_costurera_vestido")


def tex_detalles():
    N = 1024
    a, U, V = lienzo(N, N, "#D9D0BC")
    tr = trama(U, V, N, 8)
    # botones
    for nombre, base in (("BOTON_NEGRO", "#1B1F2B"), ("BOTON_CREMA", "#F4D9A0")):
        bu, bv, mk = bloque(U, V, DT[nombre])
        x, y = (bu - 0.5) * 2, (bv - 0.5) * 2
        r = np.hypot(x, y)
        mezcla(a, base, mk)
        if nombre == "BOTON_NEGRO":
            mezcla(a, "#343A4E", mk * ((r > 0.70) & (r < 0.86)) * 0.9)
            mezcla(a, "#4A5168", mk * np.exp(-(((x + 0.3) / 0.3) ** 2 + ((y - 0.35) / 0.3) ** 2)) * 0.45)
            for hx in (-0.19, 0.19):
                for hy in (-0.19, 0.19):
                    mezcla(a, "#D9D0BC", mk * lleno(sd_elipse(x, y, hx, hy, 0.075, 0.075), 2 / 256))
            for sg in (1, -1):
                mezcla(a, "#C8553D", mk * lleno(sd_capsula(x, y, -0.19, -0.19 * sg, 0.19, 0.19 * sg, 0.04), 2 / 256))
        else:
            mezcla(a, "#3A2E42", mk * ((r > 0.52) & (r < 0.66)) * 0.95)
            mezcla(a, "#FCEBC4", mk * np.exp(-(((x + 0.3) / 0.3) ** 2 + ((y - 0.35) / 0.3) ** 2)) * 0.4)
            mezcla(a, "#C8553D", mk * lleno(sd_capsula(x, y, -0.2, 0.0, 0.2, 0.0, 0.045), 2 / 256))
            for hx in (-0.2, 0.2):
                mezcla(a, "#2A2132", mk * lleno(sd_elipse(x, y, hx, 0, 0.085, 0.085), 2 / 256))
    # cinta metrica: u = ancho, v = medio metro de largo
    bu, bv, mk = bloque(U, V, DT["CINTA"])
    mezcla(a, "#F4D9A0", mk)
    a *= (1 - mk * 0.05 * (1 - tr))[..., None]
    marca = (np.abs(((bv * 10 + 0.5) % 1.0) - 0.5) < 0.09) * (bu < 0.42)
    marca = marca | ((np.abs(bv - 0.5) < 0.012) & (bu < 0.68)) | (bv < 0.014) | (bv > 0.986)
    mezcla(a, "#2A2132", mk * marca * 0.92)
    mezcla(a, "#C8553D", mk * lleno(sd_elipse(bu, bv, 0.82, 0.08, 0.07, 0.035), 1 / 256) * 0.9)
    mezcla(a, "#D9B978", mk * ((bu < 0.05) | (bu > 0.95)) * 0.8)
    # hilo rojo
    bu, bv, mk = bloque(U, V, DT["HILO"])
    mezcla(a, "#C8553D", mk)
    a *= (1 - mk * 0.22 * (0.5 + 0.5 * np.sin(2 * math.pi * (bu * 7 + bv * 16))))[..., None]
    # parches
    for nombre, base, sem in (("P_CLARO", "#5E4D70", 51), ("P_ROJO", "#8E3B2B", 52), ("P_MALVA", "#6A5560", 53), ("P_OSCURO", "#3A2E42", 54)):
        bu, bv, mk = bloque(U, V, DT[nombre])
        mezcla(a, base, mk)
        a *= (1 + mk * (0.14 * (tr - 0.5) + 0.07 * ruido(N, N, 28, sem)))[..., None]
        wp = 256
        sdb = sd_caja(bu * wp, bv * wp, wp / 2, wp / 2, wp / 2 - 30, wp / 2 - 30, 6)
        ang = np.arctan2(bv - 0.5, bu - 0.5)
        mezcla(a, "#D9D0BC", mk * lleno(np.abs(sdb) - 3.6, 1.0) * (((ang * 8.6) % 1.0) < 0.6) * 0.95)
        a *= (1 - mk * 0.16 * (sdb > 0) * np.clip(sdb / 26, 0, 1))[..., None]
    bu, bv, mk = bloque(U, V, DT["CINTURON"])
    mezcla(a, "#221C2B", mk)
    a *= (1 + mk * 0.10 * ruido(N, N, 6, 55))[..., None]
    bu, bv, mk = bloque(U, V, DT["TELA"])
    a *= (1 - mk * 0.10 * (1 - tr))[..., None]
    for nombre, base in (("A_ROJO", "#C8553D"), ("A_CREMA", "#F4D9A0")):
        bu, bv, mk = bloque(U, V, DT[nombre])
        mezcla(a, base, mk)
        mezcla(a, "#FFFFFF", mk * np.exp(-(((bu - 0.35) / 0.18) ** 2 + ((bv - 0.68) / 0.18) ** 2)) * 0.35)
    return guardar(a, "tex_costurera_detalles")


def pintar_todo():
    return [f().name for f in (tex_cara, tex_pelo, tex_vestido, tex_detalles)]
