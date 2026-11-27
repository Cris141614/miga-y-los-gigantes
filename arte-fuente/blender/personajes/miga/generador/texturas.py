# Pinta las texturas de Miga con numpy y las guarda en juego/Assets/_Proyecto/Art/Texturas.
# Cada funcion documenta como se usa su espacio UV; el modelo usa las mismas constantes.

# Proyeccion de la cara: u = 0.5 + x / CARA_M, v = 0.5 + (z - CARA_Z) / CARA_M
CARA_M, CARA_Z = 0.40, 0.815
PIEL_LISA = (0.03, 0.03)                     # punto de piel sin pintar (manos, piernas, orejas)
PIEL_PARPADO, PIEL_PARPADO_BAJO = (0.965, 0.035), (0.965, 0.105)   # tono de cada parpado, en una esquina libre
# Ojos: angulo en la cara, altura y semiejes (ancho, alto, fondo). La textura cubre el ovalo completo.
OJO_TH, OJO_Z, OJO_RX, OJO_RZ, OJO_RN = 23.4, 0.766, 0.0325, 0.0395, 0.0072
# Abrigo: cuerpo, mangas, bolsillo, cinta de la espalda y forro (u0, u1, v0, v1)
AB_CUERPO = (0.0, 1.0, 0.36, 1.0)
AB_MANGA_D = (0.0, 0.5, 0.14, 0.34)
AB_MANGA_I = (0.5, 1.0, 0.14, 0.34)
AB_BOLSILLO = (0.02, 0.20, 0.02, 0.115)
AB_CINTA = (0.24, 0.62, 0.025, 0.105)
AB_FORRO = (0.66, 0.98, 0.02, 0.10)
# Bufanda: la textura cubre 0.5 m x 0.5 m
BU_M = 0.5
BU_PUNTAS = (0.0, 0.36)                      # rango de u para las puntas (con rayas crema cerca de v = 0)
BU_CUELLO = (0.44, 0.94)                     # rango de u sin rayas
# Atlas de detalles (u0, u1, v0, v1)
DT_CALCETIN = (0.0, 0.25, 0.5, 1.0)
DT_BOTA = (0.25, 0.75, 0.5, 1.0)
DT_BOTON = (0.75, 1.0, 0.75, 1.0)
DT_LIGA = (0.75, 1.0, 0.5, 0.75)
DT_CURITA = (0.0, 0.25, 0.25, 0.5)
DT_TAPA = (0.25, 0.5, 0.25, 0.5)
DT_ALAMBRE = (0.5, 0.75, 0.25, 0.5)
DT_BICHO = (0.75, 1.0, 0.25, 0.5)
DT_ALA = (0.0, 0.25, 0.0, 0.25)
DT_PARCHE_A = (0.25, 0.5, 0.0, 0.25)
DT_PARCHE_B = (0.5, 0.75, 0.0, 0.25)
DT_CAMISETA = (0.75, 0.875, 0.125, 0.25)     # ropa de abajo del abrigo
DT_SHORT = (0.75, 0.875, 0.0, 0.125)
DT_CORDON = (0.875, 1.0, 0.125, 0.25)        # cordones de las botas


def linea_flequillo(x):
    """Altura aproximada del borde del flequillo segun x (metros)."""
    return np.interp(x, [-0.17, -0.10, 0.0, 0.082, 0.13, 0.17], [0.805, 0.822, 0.847, 0.875, 0.845, 0.822])


def bloque(U, V, r):
    """Coordenadas 0..1 dentro de un bloque y su mascara."""
    bu, bv = (U - r[0]) / (r[1] - r[0]), (V - r[2]) / (r[3] - r[2])
    return bu, bv, ((bu >= 0) & (bu < 1) & (bv >= 0) & (bv < 1)).astype(np.float32)


def tex_piel():
    N = 1024
    a, U, V = lienzo(N, N, "#E8C9A8")
    X, Z, px = (U - 0.5) * CARA_M, CARA_Z + (V - 0.5) * CARA_M, CARA_M / N
    a *= (1 + 0.012 * ruido(N, N, 70, 1))[..., None]
    mezcla(a, "#E4BB98", np.clip((0.79 - Z) / 0.12, 0, 1) * 0.30)                      # mas calida abajo
    s = np.clip((Z - (linea_flequillo(X) - 0.050)) / 0.050, 0, 1)
    mezcla(a, "#CFA381", s * s * (3 - 2 * s) * 0.42)                                   # sombra del flequillo
    for lado in (-1, 1):
        g = np.exp(-(((X - lado * 0.066) / 0.050) ** 2 + ((Z - 0.764) / 0.056) ** 2) ** 1.4)
        mezcla(a, "#D7AD8A", g * 0.30)                                                 # cuenca del ojo
        g = np.exp(-(((X - lado * 0.104) / 0.031) ** 2 + ((Z - 0.716) / 0.0175) ** 2) ** 1.3)
        mezcla(a, "#EE9482", g * 0.55)                                                 # rubor
        for fx, fz in ((0.126, 0.739), (0.111, 0.744), (0.119, 0.731), (0.134, 0.729)):
            mezcla(a, "#B3744C", lleno(sd_elipse(X, Z, lado * fx, fz, 0.0021, 0.0019), px) * 0.70)   # pecas
        # ceja: mas alta por dentro, expresion preocupada
        p0, p1, p2 = (lado * 0.040, 0.823), (lado * 0.066, 0.823), (lado * 0.092, 0.805)
        for i in range(14):
            t0, t1 = i / 14, (i + 1) / 14
            q0 = [(1 - t0) ** 2 * p0[k] + 2 * t0 * (1 - t0) * p1[k] + t0 * t0 * p2[k] for k in (0, 1)]
            q1 = [(1 - t1) ** 2 * p0[k] + 2 * t1 * (1 - t1) * p1[k] + t1 * t1 * p2[k] for k in (0, 1)]
            mezcla(a, "#3A3350", lleno(sd_capsula(X, Z, q0[0], q0[1], q1[0], q1[1], 0.0027 - 0.0015 * t0), px) * 0.85)
    # nariz
    mezcla(a, "#C4906F", np.exp(-((X / 0.010) ** 2 + ((Z - 0.7215) / 0.0038) ** 2)) * 0.45)
    mezcla(a, "#EBB59B", np.exp(-((X / 0.012) ** 2 + ((Z - 0.729) / 0.010) ** 2)) * 0.30)
    # boca: curva hacia abajo
    p0, p1, p2 = (-0.025, 0.6885), (0.0, 0.7005), (0.025, 0.6885)
    for i in range(16):
        t0, t1 = i / 16, (i + 1) / 16
        q0 = [(1 - t0) ** 2 * p0[k] + 2 * t0 * (1 - t0) * p1[k] + t0 * t0 * p2[k] for k in (0, 1)]
        q1 = [(1 - t1) ** 2 * p0[k] + 2 * t1 * (1 - t1) * p1[k] + t1 * t1 * p2[k] for k in (0, 1)]
        r = 0.0015 + 0.0012 * math.sin(math.pi * (t0 + t1) / 2)
        mezcla(a, "#7A3B31", lleno(sd_capsula(X, Z, q0[0], q0[1], q1[0], q1[1], r), px))
    mezcla(a, "#CE9E80", np.exp(-((X / 0.017) ** 2 + ((Z - 0.6815) / 0.0040) ** 2)) * 0.35)   # sombra del labio
    for (pu, pv), color in ((PIEL_PARPADO, "#DBAE90"), (PIEL_PARPADO_BAJO, "#DDB193")):       # parpados: algo mas oscuros
        mezcla(a, color, ((np.abs(U - pu) < 0.035) & (np.abs(V - pv) < 0.035)).astype(np.float32))
    return guardar(a, "tex_miga_piel")


def tex_ojos():
    """Ojo grande y oscuro, como en la hoja de vistas: sin blanco y con un solo reflejo pintado."""
    N = 512
    a, U, V = lienzo(N, N, "#17141F")
    x, y, px = (U - 0.5) * 2, (V - 0.5) * 2, 2 / N
    r = np.hypot(x, y)
    mezcla(a, "#4A3A63", np.clip((0.12 - y) / 0.9, 0, 1) * np.clip(1 - r * r, 0, 1) * 0.70)   # iris violeta apagado, mas claro abajo
    mezcla(a, "#7B699C", difuso(sd_elipse(x, y, 0.0, -0.56, 0.46, 0.20), 0.22) * 0.22)        # luz rebotada, muy suave
    mezcla(a, "#08070C", difuso(sd_elipse(x, y, 0.0, 0.05, 0.36, 0.40), 0.28) * 0.88)         # pupila
    mezcla(a, "#09070E", np.clip((r - 0.76) / 0.2, 0, 1) * 0.75)                              # borde oscuro
    mezcla(a, "#06050A", np.clip((y - 0.40) / 0.45, 0, 1) * 0.55)                             # sombra del parpado
    mezcla(a, "#FFFFFF", lleno(sd_elipse(x, y, 0.30, 0.33, 0.19, 0.165), px))                 # reflejo: uno solo, redondo sobre el ojo
    mezcla(a, "#FFFFFF", lleno(sd_elipse(x, y, -0.33, -0.40, 0.055, 0.050), px) * 0.45)       # chispa de abajo, apenas
    return guardar(a, "tex_miga_ojos")


def tex_pelo():
    N = 512
    a, U, V = lienzo(N, N, "#2A3046")
    s1, s2 = ruido(N, N, 90, 3, sx=1.8), ruido(N, N, 140, 4, sx=7)
    hebra = 0.6 * s1 + 0.4 * s2
    a *= (1 + 0.20 * hebra)[..., None]
    banda = np.exp(-((V - 0.36) / 0.075) ** 2) * (0.45 + 0.55 * np.clip(s1 * 1.6 + 0.4, 0, 1))
    mezcla(a, "#6272A6", banda * 0.50)                                                 # brillo en aro
    a *= (1 - 0.14 * np.clip((V - 0.78) / 0.22, 0, 1))[..., None]                      # puntas mas oscuras
    return guardar(a, "tex_miga_pelo")


def tejido(U, V, N, p=14.0, B=70.0):
    """Espiga (herringbone) en 0..1; p = periodo del hilo y B = ancho de banda, en pixeles."""
    x, y = U * N, V * N
    sg = np.where((np.floor(x / B) % 2) == 0, 1.0, -1.0)
    return 0.5 + 0.5 * np.sin(2 * math.pi * (y + sg * x) / p)


def tex_abrigo():
    N = 2048
    a, U, V = lienzo(N, N, "#3E7C7B")
    px = 1.0 / N
    tj = tejido(U, V, N)
    alt = (tj - 0.5) * 0.5                                                             # mapa de altura para el normal
    a *= (0.94 + 0.10 * tj + 0.035 * ruido(N, N, 1.3, 5) + 0.05 * ruido(N, N, 160, 6))[..., None]

    def puntadas(sd_linea, a_lo_largo, periodo, largo, mask, grosor=2.2):
        """Linea de puntadas: sd_linea = distancia a la linea (px); a_lo_largo = coordenada (px)."""
        m = lleno(np.abs(sd_linea) - grosor, 1.0) * ((a_lo_largo % periodo) < largo) * mask
        mezcla(a, "#79B8B2", m * 0.85)
        return m

    # ---- cuerpo
    bu, bv, mk = bloque(U, V, AB_CUERPO)
    a *= (1 - mk * 0.22 * np.clip((bv - 0.90) / 0.10, 0, 1))[..., None]                # sombra bajo la bufanda
    a *= (1 - mk * 0.10 * np.clip((0.20 - bv) / 0.20, 0, 1))[..., None]                # mas oscuro hacia el ruedo
    for uc in (0.25, 0.75):                                                            # sombra bajo los brazos
        a *= (1 - mk * 0.16 * np.exp(-(((bu - uc) / 0.05) ** 2 + ((bv - 0.80) / 0.14) ** 2)))[..., None]
    suc = np.clip(ruido(N, N, 26, 7) * 1.5 - 0.25, 0, 1) * np.clip((0.22 - bv) / 0.22, 0, 1) * mk
    mezcla(a, "#4F5B4A", suc * 0.30)                                                   # suciedad del ruedo
    ruedo = mk * (bv < 0.040)
    a *= (1 - 0.13 * ruedo)[..., None]
    alt += ruedo * 0.35
    alt += puntadas((bv - 0.052) * 0.64 * N, U * N, 26, 15, mk) * 0.5
    d = (U - 0.5) * N                                                                  # tapeta del frente
    seam = lleno(np.abs(d) - 1.6, 1.0) * mk
    mezcla(a, "#234E4D", seam * 0.9)
    mezcla(a, "#5A9C98", lleno(np.abs(d - 5.5) - 1.2, 1.0) * mk * 0.45)
    alt -= seam * 0.6
    alt += puntadas(d - 22, V * N, 26, 15, mk) * 0.5
    for uc in (0.0, 0.25, 0.75, 1.0):                                                  # costuras laterales y espalda
        s = lleno(np.abs((U - uc) * N) - 1.2, 1.0) * mk
        mezcla(a, "#2C5B5A", s * 0.55)
        alt -= s * 0.4

    # ---- mangas
    for blo in (AB_MANGA_D, AB_MANGA_I):
        bu, bv, mk = bloque(U, V, blo)
        a *= (1 - mk * 0.14 * np.clip((0.12 - bu) / 0.12, 0, 1))[..., None]            # sombra en el hombro
        a *= (1 - mk * 0.08 * np.exp(-((bu - 0.50) / 0.07) ** 2))[..., None]           # arrugas del codo
        puno = mk * (bu > 0.855)
        a *= (1 - 0.20 * puno)[..., None]
        alt += puno * 0.35
        alt += puntadas((bu - 0.875) * 0.5 * N, V * N, 24, 14, mk) * 0.5
        alt += puntadas((bu - 0.985) * 0.5 * N, V * N, 24, 14, mk) * 0.5
        s = lleno(np.abs((bv - 0.5) * 0.2 * N) - 1.2, 1.0) * mk * (bu < 0.855)        # costura de la manga
        mezcla(a, "#2C5B5A", s * 0.5)

    # ---- bolsillo
    bu, bv, mk = bloque(U, V, AB_BOLSILLO)
    w, h = (AB_BOLSILLO[1] - AB_BOLSILLO[0]) * N, (AB_BOLSILLO[3] - AB_BOLSILLO[2]) * N
    a *= (1 - 0.07 * mk)[..., None]
    arriba = mk * (bv > 0.84)
    a *= (1 - 0.12 * arriba)[..., None]
    alt += puntadas((bv - 0.80) * h, bu * w, 22, 13, mk) * 0.5
    sdb = sd_caja(bu * w, bv * h, w / 2, h / 2 + 30, w / 2 - 16, h / 2 + 14, 26)       # borde en U
    alt += puntadas(sdb, (bu * w + bv * h), 22, 13, mk * (bv < 0.80)) * 0.5

    # ---- cinta de la espalda
    bu, bv, mk = bloque(U, V, AB_CINTA)
    w, h = (AB_CINTA[1] - AB_CINTA[0]) * N, (AB_CINTA[3] - AB_CINTA[2]) * N
    a *= (1 - 0.09 * mk)[..., None]
    for linea in (0.16, 0.84):
        alt += puntadas((bv - linea) * h, bu * w, 22, 13, mk) * 0.5

    # ---- forro
    bu, bv, mk = bloque(U, V, (AB_FORRO[0] - 0.02, AB_FORRO[1] + 0.02, AB_FORRO[2] - 0.02, AB_FORRO[3] + 0.02))
    mezcla(a, "#2A5352", mk * 0.92)

    guardar(normal_de_altura(alt.astype(np.float32), 5.0), "tex_miga_abrigo_normal", nocolor=True)
    return guardar(a, "tex_miga_abrigo")


def tex_bufanda():
    N = 1024
    a, U, V = lienzo(N, N, "#C8553D")
    fx, fy = (U * 48) % 1.0, (V * 64) % 1.0
    lin_ = np.where(fx < 0.5, 1 - 2 * fx, 2 * fx - 1)                                  # la V de cada punto
    d = np.abs(fy - lin_)
    d = np.minimum(d, 1 - d)
    h = np.clip(1 - d / 0.42, 0, 1)
    h = h * h * (3 - 2 * h)
    borde_col = np.clip(1 - np.minimum(fx, 1 - fx) / 0.10, 0, 1)                       # surco entre columnas
    h = np.clip(h - 0.7 * borde_col, 0, 1)
    raya = (U < 0.40) & (((V >= 4 / 64) & (V < 6 / 64)) | ((V >= 7 / 64) & (V < 9 / 64)))
    mezcla(a, "#F4D9A0", raya.astype(np.float32))
    a *= (0.70 + 0.36 * h + 0.03 * ruido(N, N, 1.2, 8) + 0.05 * ruido(N, N, 90, 9))[..., None]
    guardar(normal_de_altura(h.astype(np.float32), 4.0), "tex_miga_bufanda_normal", nocolor=True)
    return guardar(a, "tex_miga_bufanda")


def tex_detalles():
    N = 1024
    a, U, V = lienzo(N, N, "#F4D9A0")
    # calcetin
    bu, bv, mk = bloque(U, V, DT_CALCETIN)
    mezcla(a, "#EFE8DC", mk)
    mezcla(a, "#C8553D", mk * (((bv > 0.67) & (bv < 0.80)) | ((bv > 0.36) & (bv < 0.49))))
    a *= (1 - mk * (0.10 * (0.5 - 0.5 * np.cos(2 * math.pi * bu * 14)) + 0.06 * (bv > 0.90)))[..., None]
    # bota
    bu, bv, mk = bloque(U, V, DT_BOTA)
    mezcla(a, "#3B3F5B", mk)
    cuero = ruido(N, N, 5, 10)
    a *= (1 + mk * 0.07 * cuero)[..., None]
    frente = np.exp(-((bu - 0.5) / 0.16) ** 2)
    gast = np.clip(ruido(N, N, 9, 11) * 1.6 + 0.15, 0, 1) * frente * np.exp(-((bv - 0.36) / 0.13) ** 2)
    mezcla(a, "#7C7F9C", mk * gast * 0.55)                                             # punta gastada
    talon = np.clip(ruido(N, N, 7, 12) * 1.5 - 0.1, 0, 1) * (np.exp(-(bu / 0.08) ** 2) + np.exp(-((bu - 1) / 0.08) ** 2))
    mezcla(a, "#6C6F8C", mk * talon * np.exp(-((bv - 0.33) / 0.10) ** 2) * 0.45)
    ray = np.clip(ruido(N, N, 22, 13, sx=0.8) * 3 - 2.3, 0, 1)
    mezcla(a, "#8A8DA8", mk * ray * (bv > 0.24) * 0.5)                                 # rasgunos
    sd_p = sd_elipse(bu, bv, 0.5, 0.20, 0.215, 0.30)                                   # puntera mas clara
    mezcla(a, "#4E5378", mk * lleno(sd_p, 1 / 512) * (bv > 0.235) * 0.80)
    mezcla(a, "#262A44", mk * lleno(np.abs(sd_p) - 0.006, 1 / 512) * (bv > 0.235) * 0.85)
    mezcla(a, "#7C7F9C", mk * gast * 0.40)
    mezcla(a, "#555A7C", mk * ((bv > 0.185) & (bv < 0.235)) * 0.9)                     # vira
    mezcla(a, "#20223A", mk * (bv <= 0.185))                                           # suela
    mezcla(a, "#535878", mk * (bv > 0.93) * 0.8)                                       # borde de arriba
    # boton
    bu, bv, mk = bloque(U, V, DT_BOTON)
    x, y = (bu - 0.5) * 2, (bv - 0.5) * 2
    r = np.hypot(x, y)
    mezcla(a, "#D2AE74", mk * ((r > 0.66) & (r < 0.86)) * 0.75)
    mezcla(a, "#FBE9BF", mk * np.exp(-(((x + 0.25) / 0.3) ** 2 + ((y - 0.3) / 0.3) ** 2)) * 0.35)
    mezcla(a, "#B5503A", mk * lleno(sd_capsula(x, y, -0.2, -0.2, 0.2, 0.2, 0.045), 2 / 256))
    mezcla(a, "#B5503A", mk * lleno(sd_capsula(x, y, -0.2, 0.2, 0.2, -0.2, 0.045), 2 / 256))
    for hx in (-0.2, 0.2):
        for hy in (-0.2, 0.2):
            mezcla(a, "#5E4A2E", mk * lleno(sd_elipse(x, y, hx, hy, 0.085, 0.085), 2 / 256))
    # liga
    bu, bv, mk = bloque(U, V, DT_LIGA)
    mezcla(a, "#C8553D", mk)
    a *= (1 - mk * 0.16 * (0.5 - 0.5 * np.cos(2 * math.pi * bu * 22)))[..., None]
    # curita
    bu, bv, mk = bloque(U, V, DT_CURITA)
    mezcla(a, "#EDC49B", mk)
    w = 256
    pad = lleno(sd_caja(bu * w, bv * w, w / 2, w / 2, 46, 62, 10), 1.0)
    mezcla(a, "#F9E7C8", mk * pad)
    mezcla(a, "#D9AE84", mk * lleno(np.abs(sd_caja(bu * w, bv * w, w / 2, w / 2, 46, 62, 10)) - 1.5, 1.0) * 0.8)
    pts = (((bu * w) % 22 - 11) ** 2 + ((bv * w) % 22 - 11) ** 2) < 7
    mezcla(a, "#D7A982", mk * pts * (1 - pad) * 0.8)
    # tapa, alambre, bicho, ala
    bu, bv, mk = bloque(U, V, DT_TAPA)
    mezcla(a, "#8D92A3", mk)
    a *= (1 + mk * (0.12 * np.sin(2 * math.pi * bv * 7) + 0.05 * ruido(N, N, 40, 14, sx=1.5)))[..., None]
    for blo, colr in ((DT_ALAMBRE, "#70758A"), (DT_BICHO, "#2A2320"), (DT_ALA, "#E2EAEC")):
        mezcla(a, colr, bloque(U, V, blo)[2])
    # parches
    for blo, colr, sem in ((DT_PARCHE_A, "#C9A46C", 15), (DT_PARCHE_B, "#C0996A", 16)):
        bu, bv, mk = bloque(U, V, blo)
        mezcla(a, colr, mk)
        tr = 0.5 + 0.25 * np.sin(2 * math.pi * bu * 26) + 0.25 * np.sin(2 * math.pi * bv * 26)   # arpillera
        a *= (1 + mk * (0.16 * (tr - 0.5) + 0.06 * ruido(N, N, 30, sem)))[..., None]
        w = 256
        sdb = sd_caja(bu * w, bv * w, w / 2, w / 2, w / 2 - 30, w / 2 - 30, 8)
        ang = np.arctan2(bv - 0.5, bu - 0.5)
        dash = lleno(np.abs(sdb) - 4.0, 1.0) * (((ang * 9.5) % 1.0) < 0.62)
        mezcla(a, "#2A2433", mk * dash * 0.95)                                         # puntadas a mano
        a *= (1 - mk * 0.10 * np.clip(sdb / 30 + 1, 0, 1) * (sdb > 0))[..., None]
    # ropa de abajo del abrigo: camiseta de punto y short
    bu, bv, mk = bloque(U, V, DT_CAMISETA)
    mezcla(a, "#EAE2D2", mk)
    a *= (1 - mk * 0.07 * (0.5 - 0.5 * np.cos(2 * math.pi * bu * 18)))[..., None]
    bu, bv, mk = bloque(U, V, DT_SHORT)
    mezcla(a, "#34475A", mk)
    a *= (1 + mk * 0.06 * ruido(N, N, 3, 17))[..., None]
    # cordones: crema con el torcido del hilo
    bu, bv, mk = bloque(U, V, DT_CORDON)
    mezcla(a, "#E6DBC2", mk)
    a *= (1 - mk * 0.14 * (0.5 - 0.5 * np.cos(2 * math.pi * (bu + bv) * 9)))[..., None]
    return guardar(a, "tex_miga_detalles")


def pintar_todo():
    return [f().name for f in (tex_piel, tex_ojos, tex_pelo, tex_abrigo, tex_bufanda, tex_detalles)]
