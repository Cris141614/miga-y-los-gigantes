# Arma a La Costurera completa. Usa lib.py (copia de la de Miga), texturas.py, modelo.py y esqueleto.py.
COL = "Costurera"
MATS = {}
DIR_BLEND_C = os.path.join(RAIZ, "arte-fuente", "blender", "personajes", "costurera")


def materiales():
    return {
        "piel": material("mat_costurera_piel", "#B9B6A4", 0.85, brillo=0.25),
        "cara": material("mat_costurera_cara", "#D9D0BC", 0.92, tex="tex_costurera_cara", brillo=0.2, velo=0.3),
        "pelo": material("mat_costurera_pelo", "#6B6775", 0.55, tex="tex_costurera_pelo", brillo=0.45),
        "vestido": material("mat_costurera_vestido", "#4F4059", 0.90, tex="tex_costurera_vestido",
                            normal="tex_costurera_vestido_normal", brillo=0.25, velo=0.3),
        "detalles": material("mat_costurera_detalles", "#D9D0BC", 0.65, tex="tex_costurera_detalles", brillo=0.35),
        "metal": material("mat_costurera_metal", "#C5CAD6", 0.28, brillo=0.6, metal=1.0),
    }


def construir(pintar=True):
    limpiar()
    if pintar:
        pintar_todo()
    MATS.clear()
    MATS.update(materiales())
    raiz = bpy.data.objects.new("Costurera", None)
    raiz.empty_display_size = 2.0
    coleccion().objects.link(raiz)
    partes = [hacer_cuerpo(), hacer_cara(), hacer_pelo(), hacer_vestido(), hacer_accesorios(), hacer_mano(-1), hacer_mano(1)]
    esq = hacer_esqueleto(raiz)
    for o in partes:                                                   # todo cuelga directo de la raiz (ver nota de Miga)
        o.parent = raiz
        enlazar(o, esq)
    fallas = revisar()
    if fallas:
        raise RuntimeError("La Costurera quedo mal enlazada al esqueleto: " + "; ".join(fallas))
    info = {}
    for o in partes:
        o.data.calc_loop_triangles()
        info[o.name] = len(o.data.loop_triangles)
    info["TOTAL"] = sum(info.values())
    info["HUESOS"] = len(esq.data.bones)
    return info


def guardar_y_exportar():
    """Guarda costurera.blend y exporta mod_costurera.fbx (mallas, esqueleto y raiz) para Unity."""
    reposo()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(DIR_BLEND_C, "costurera.blend"), relative_remap=True)
    bpy.ops.file.make_paths_relative()
    os.makedirs(DIR_MOD, exist_ok=True)
    for o in bpy.data.objects:
        o.select_set(False)
    for o in coleccion().objects:
        if o.type in {"MESH", "EMPTY", "ARMATURE"}:
            o.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["Costurera"]
    fbx = os.path.join(DIR_MOD, "mod_costurera.fbx")
    bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, object_types={"EMPTY", "MESH", "ARMATURE"},
                             axis_forward="-Z", axis_up="Y", bake_space_transform=True,
                             apply_scale_options="FBX_SCALE_UNITS", use_mesh_modifiers=False, mesh_smooth_type="OFF",
                             add_leaf_bones=False, use_armature_deform_only=True, primary_bone_axis="Y",
                             secondary_bone_axis="X", bake_anim=False, path_mode="AUTO", embed_textures=False)
    for o in bpy.data.objects:
        o.select_set(False)
    bpy.ops.wm.save_mainfile()
    return fbx
