using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

namespace Miga.Herramientas
{
    /// <summary>
    /// Arma la escena del Nivel 1 en bloques grises con el plano de docs/Niveles/Nivel 1 - El Taller.md.
    /// Se corre una vez desde el menú Miga; después la escena se ajusta a mano en Unity.
    /// </summary>
    public static class ConstruirNivel1
    {
        const string Escena = "Assets/_Proyecto/Scenes/Niveles/esc_nivel1_taller.unity";
        const string PrefabMiga = "Assets/_Proyecto/Prefabs/Personajes/pf_miga.prefab";
        const string CarpetaMateriales = "Assets/_Proyecto/Art/Materiales/Grises";
        static readonly Vector3 InicioMiga = new Vector3(2.8f, 12.75f, 0f);

        enum Tipo { Estructura, Paso, Obstaculo, Peligro, Escondite, Mecanismo, Fondo, Limite }

        // Mismos colores que la leyenda del plano (docs/Referencias/Escenarios/nivel1-plano.png)
        // Limite no se ve: es una pared invisible.
        static readonly string[] Colores = { "#8A8F9C", "#5B9BD5", "#E0A040", "#D9534F", "#6BAF6B", "#A070C8", "#D5D8DE", "#000000" };

        static readonly string[] Zonas =
        {
            "General", "Zona 1 - El costurero", "Zona 2 - La mesa de corte", "Zona 3 - La maquina de coser",
            "Zona 4 - El armario de retazos", "Zona 5 - Las tijeras", "Zona 6 - La huida",
        };

        readonly struct Bloque
        {
            public readonly int zona;
            public readonly string nombre;
            public readonly float x0, x1, y0, y1;
            public readonly Tipo tipo;

            public Bloque(int zona, string nombre, float x0, float x1, float y0, float y1, Tipo tipo)
            {
                this.zona = zona;
                this.nombre = nombre;
                this.x0 = x0;
                this.x1 = x1;
                this.y0 = y0;
                this.y1 = y1;
                this.tipo = tipo;
            }
        }

        // Vista de lado: x avanza el nivel, y es la altura (en metros, Miga = 1). El carril de Miga es z = 0.
        static readonly Bloque[] Plano =
        {
            new Bloque(0, "Piso", -5f, 137f, -1f, 0f, Tipo.Estructura),
            new Bloque(0, "Limite_Inicio", -0.5f, 0f, 0f, 30f, Tipo.Limite),   // no deja caer de la mesa por la izquierda
            new Bloque(0, "Limite_Final", 137f, 137.5f, 0f, 30f, Tipo.Limite),  // ni seguir de largo al final
            new Bloque(1, "MesaCorte", 0f, 30f, 12.15f, 12.75f, Tipo.Estructura),
            new Bloque(1, "MesaCorte_Pata_A", 0f, 1.2f, 0f, 12.15f, Tipo.Estructura),
            new Bloque(1, "MesaCorte_Pata_B", 28.8f, 30f, 0f, 12.15f, Tipo.Estructura),
            new Bloque(1, "Costurero_Pared_A", 2f, 2.3f, 12.75f, 15.3f, Tipo.Estructura),
            new Bloque(1, "Costurero_Pared_B", 6.8f, 7.1f, 12.75f, 15.3f, Tipo.Estructura),
            new Bloque(1, "Costurero_Tapa", 2f, 5.6f, 15.3f, 15.5f, Tipo.Mecanismo),
            new Bloque(1, "Carrete_1", 5.2f, 6f, 12.75f, 13.6f, Tipo.Paso),
            new Bloque(1, "Carretes_2", 6f, 6.8f, 12.75f, 14.45f, Tipo.Paso),
            new Bloque(2, "Tela_1", 9f, 12f, 12.75f, 13.35f, Tipo.Obstaculo),
            new Bloque(2, "Alfiler_1", 14f, 14.2f, 12.75f, 12.92f, Tipo.Peligro),
            new Bloque(2, "Alfiler_2", 15.5f, 15.7f, 12.75f, 12.92f, Tipo.Peligro),
            new Bloque(2, "RolloTela", 18f, 19f, 12.75f, 13.75f, Tipo.Paso),
            new Bloque(2, "Telas_Escondite", 23f, 26f, 12.75f, 13.95f, Tipo.Escondite),
            new Bloque(2, "Regla_Puente", 29f, 34.5f, 12.75f, 12.92f, Tipo.Paso),
            new Bloque(3, "MesaMaquina", 33.5f, 58.5f, 12.15f, 12.75f, Tipo.Estructura),
            new Bloque(3, "MesaMaquina_Pata_A", 33.5f, 34.7f, 0f, 12.15f, Tipo.Estructura),
            new Bloque(3, "Pedal", 35.5f, 37f, 12.75f, 13.15f, Tipo.Mecanismo),
            new Bloque(3, "Maquina_Base", 38f, 42f, 12.75f, 13.6f, Tipo.Paso),
            new Bloque(3, "Maquina_Aguja", 39.9f, 40.1f, 14.95f, 16.5f, Tipo.Peligro),
            new Bloque(3, "Maquina_Cabezal", 38f, 42f, 16.5f, 18.5f, Tipo.Estructura),
            new Bloque(3, "Cajon_1", 58.5f, 60f, 9.7f, 10f, Tipo.Paso),
            new Bloque(3, "Cajon_2", 58.5f, 61.5f, 7.2f, 7.5f, Tipo.Paso),
            new Bloque(3, "Cajon_3", 58.5f, 63f, 4.7f, 5f, Tipo.Paso),
            new Bloque(3, "Cajon_4", 58.5f, 64.5f, 2.2f, 2.5f, Tipo.Paso),
            new Bloque(3, "Cajonera", 56f, 58.5f, 0f, 12.15f, Tipo.Estructura),
            new Bloque(3, "Costurera_Silueta", 47f, 51f, 0f, 22f, Tipo.Fondo),
            new Bloque(4, "Armario_Lado_A", 70f, 70.4f, 1.2f, 24f, Tipo.Estructura),
            new Bloque(4, "Armario_Repisa", 70f, 87f, 6.8f, 7.2f, Tipo.Estructura),
            new Bloque(4, "Armario_Lado_B", 86.6f, 87f, 1.2f, 24f, Tipo.Estructura),
            new Bloque(4, "Retazos_1", 73f, 75f, 0f, 1.2f, Tipo.Escondite),
            new Bloque(4, "Retazos_2", 79f, 81.5f, 0f, 1.2f, Tipo.Escondite),
            new Bloque(4, "Munecos_1", 76f, 77.5f, 0f, 5f, Tipo.Fondo),
            new Bloque(4, "Munecos_2", 83f, 84.5f, 0f, 5f, Tipo.Fondo),
            new Bloque(5, "Torre_1", 88f, 90f, 0f, 1f, Tipo.Paso),
            new Bloque(5, "Torre_2", 90f, 91.5f, 0f, 2f, Tipo.Paso),
            new Bloque(5, "Torre_3", 91.5f, 93f, 0f, 3f, Tipo.Paso),
            new Bloque(5, "Torre_4", 93f, 94.5f, 0f, 4f, Tipo.Paso),
            new Bloque(5, "Torre_Cima", 94.5f, 97f, 0f, 5f, Tipo.Paso),
            new Bloque(5, "Tijeras", 95.8f, 98.5f, 5f, 5.4f, Tipo.Mecanismo),   // deja 1.3 m libres en la cima para pararse
            new Bloque(6, "Dedal", 102f, 102.6f, 0f, 0.34f, Tipo.Obstaculo),
            new Bloque(6, "Carrete_Huida", 106f, 106.8f, 0f, 0.85f, Tipo.Paso),
            new Bloque(6, "Mesita_Agacharse", 111f, 114f, 0.75f, 2f, Tipo.Obstaculo),
            new Bloque(6, "Botones", 118f, 118.6f, 0f, 0.25f, Tipo.Obstaculo),
            new Bloque(6, "Carrete_Tumbado", 123f, 124f, 0f, 1f, Tipo.Paso),
            new Bloque(6, "Pared_Zocalo_Roto", 132f, 133f, 0.9f, 24f, Tipo.Estructura),
            new Bloque(6, "Salida", 134f, 136f, 0f, 0.1f, Tipo.Mecanismo),
        };

        [MenuItem("Miga/Construir Nivel 1 en bloques grises")]
        static void Construir()
        {
            if (AssetDatabase.LoadAssetAtPath<SceneAsset>(Escena) != null &&
                !EditorUtility.DisplayDialog("Nivel 1", "La escena esc_nivel1_taller ya existe. Se va a reemplazar, " +
                                             "con todo lo que hayas movido a mano.", "Reemplazar", "Cancelar"))
                return;
            if (!EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())
                return;

            var escena = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
            var padres = new Transform[Zonas.Length];
            for (int i = 0; i < Zonas.Length; i++)
                padres[i] = new GameObject(Zonas[i]).transform;

            foreach (var b in Plano)
            {
                // Profundidad: lo del camino es angosto, los muebles más anchos y el fondo queda detrás del carril
                float z = 0f, fondo = b.tipo == Tipo.Estructura ? 6f : 4f;
                if (b.tipo == Tipo.Fondo)
                    (z, fondo) = b.nombre.StartsWith("Costurera") ? (6f, 4f) : (2.2f, 1.6f);
                if (b.nombre == "Piso")
                    fondo = 20f;

                var cubo = GameObject.CreatePrimitive(PrimitiveType.Cube);
                cubo.name = b.nombre;
                cubo.transform.SetParent(padres[b.zona], false);
                cubo.transform.position = new Vector3((b.x0 + b.x1) / 2f, (b.y0 + b.y1) / 2f, z);
                cubo.transform.localScale = new Vector3(b.x1 - b.x0, b.y1 - b.y0, fondo);
                if (b.tipo == Tipo.Limite)
                    Object.DestroyImmediate(cubo.GetComponent<MeshRenderer>());
                else
                    cubo.GetComponent<Renderer>().sharedMaterial = Material(b.tipo);
                cubo.isStatic = b.tipo != Tipo.Mecanismo;   // los mecanismos se van a mover en otras issues
            }

            var prefab = AssetDatabase.LoadAssetAtPath<GameObject>(PrefabMiga);
            if (prefab == null)
            {
                Debug.LogError("No se encontro " + PrefabMiga);
                return;
            }
            var miga = (GameObject)PrefabUtility.InstantiatePrefab(prefab);
            miga.transform.position = InicioMiga;

            var camara = Camera.main.transform;   // provisional: la cámara de verdad es la #9
            camara.SetParent(miga.transform, false);
            camara.localPosition = new Vector3(0f, 1f, -6f);
            camara.localRotation = Quaternion.identity;

            EditorSceneManager.SaveScene(escena, Escena);
            Debug.Log("Nivel 1 construido: " + Escena);
        }

        // Un material de color por tipo de bloque, en Art/Materiales/Grises. Si ya existe, se reutiliza.
        static Material Material(Tipo tipo)
        {
            string ruta = $"{CarpetaMateriales}/mat_gris_{tipo.ToString().ToLowerInvariant()}.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(ruta);
            if (mat != null)
                return mat;
            if (!AssetDatabase.IsValidFolder(CarpetaMateriales))
                AssetDatabase.CreateFolder("Assets/_Proyecto/Art/Materiales", "Grises");
            mat = new Material(Shader.Find("Universal Render Pipeline/Lit"));
            ColorUtility.TryParseHtmlString(Colores[(int)tipo], out var color);
            mat.SetColor("_BaseColor", color);
            AssetDatabase.CreateAsset(mat, ruta);
            return mat;
        }
    }
}
