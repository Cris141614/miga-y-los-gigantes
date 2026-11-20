# Arma a Miga completa: texturas, materiales, piezas y esqueleto.
MATS = {}


def materiales():
    return {
        "piel": material("mat_miga_piel", "#E8C9A8", 0.62, tex="tex_miga_piel", brillo=0.35),
        "ojos": material("mat_miga_ojos", "#17141F", 0.38, tex="tex_miga_ojos", brillo=0.30),   # poco brillo: el reflejo va pintado
        "pelo": material("mat_miga_pelo", "#2A3046", 0.46, tex="tex_miga_pelo", brillo=0.5),
        "abrigo": material("mat_miga_abrigo", "#3E7C7B", 0.88, tex="tex_miga_abrigo", normal="tex_miga_abrigo_normal",
                           brillo=0.25, velo=0.3),
        "bufanda": material("mat_miga_bufanda", "#C8553D", 0.92, tex="tex_miga_bufanda", normal="tex_miga_bufanda_normal",
                            brillo=0.2, velo=0.4),
        "detalles": material("mat_miga_detalles", "#F4D9A0", 0.70, tex="tex_miga_detalles", brillo=0.3),
        "vidrio": material("mat_miga_vidrio", "#D8ECEE", 0.05, alfa=0.16, brillo=1.0),
        "chispa": material("mat_miga_chispa", "#E6F28A", 0.40, emision="#E6F28A", fuerza_emision=6.0),
    }


def construir(pintar=True):
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    limpiar()
    if pintar:
        pintar_todo()
    MATS.clear()
    MATS.update(materiales())
    raiz = bpy.data.objects.new("Miga", None)
    raiz.empty_display_size = 0.15
    coleccion().objects.link(raiz)
    partes = [hacer_cuerpo(), hacer_ojos(), hacer_pelo(), hacer_abrigo(), hacer_bufanda()]
    frasco, chispa, G = hacer_frasco()
    esq = hacer_esqueleto(raiz)
    for o in partes + [frasco, chispa]:                                # todo cuelga directo de la raiz: el FBX con
        o.parent = raiz                                                #   Apply Transform descoloca a los nietos
        enlazar(o, esq)
    luz = bpy.data.lights.new("Chispa_Luz", "POINT")                   # solo para ver en Blender; en Unity va una Point Light
    luz.color, luz.energy, luz.shadow_soft_size = lin(hexrgb("#E6F28A")), 1.2, 0.012
    ol = bpy.data.objects.new("Chispa_Luz", luz)
    ol.parent, ol.parent_type, ol.parent_bone = esq, "BONE", "Chispa"  # queda en la punta del hueso: el centro de Chispa
    coleccion().objects.link(ol)
    fallas = revisar()
    if fallas:
        raise RuntimeError("Miga quedo mal enlazada al esqueleto: " + "; ".join(fallas))
    info = {}
    for o in coleccion().objects:
        if o.type == "MESH":
            o.data.calc_loop_triangles()
            info[o.name] = len(o.data.loop_triangles)
    info["TOTAL"] = sum(info.values())
    info["HUESOS"] = len(esq.data.bones)
    return info


def guardar_y_exportar():
    """Guarda miga.blend y exporta mod_miga.fbx (mallas, esqueleto y la raiz) para Unity."""
    reposo()
    blend = os.path.join(DIR_BLEND, "miga.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend, relative_remap=True)
    bpy.ops.file.make_paths_relative()
    os.makedirs(DIR_MOD, exist_ok=True)
    for o in bpy.data.objects:
        o.select_set(False)
    for o in coleccion().objects:
        if o.type in {"MESH", "EMPTY", "ARMATURE"}:
            o.select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["Miga"]
    fbx = os.path.join(DIR_MOD, "mod_miga.fbx")
    bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, object_types={"EMPTY", "MESH", "ARMATURE"},
                             axis_forward="-Z", axis_up="Y", bake_space_transform=True,
                             apply_scale_options="FBX_SCALE_UNITS", use_mesh_modifiers=False, mesh_smooth_type="OFF",
                             add_leaf_bones=False, use_armature_deform_only=True, primary_bone_axis="Y",
                             secondary_bone_axis="X", bake_anim=False, path_mode="AUTO", embed_textures=False)
    for o in bpy.data.objects:
        o.select_set(False)
    bpy.ops.wm.save_mainfile()
    return blend, fbx
