using Miga.Juego;
using Unity.Cinemachine;
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

        enum Tipo { Estructura, Paso, Obstaculo, Peligro, Escondite, Mecanismo, Fondo, Limite, Empujable }

        // Mismos colores que la leyenda del plano (docs/Referencias/Escenarios/nivel1-plano.png)
        // Limite no se ve: es una pared invisible.
        static readonly string[] Colores = { "#8A8F9C", "#5B9BD5", "#E0A040", "#D9534F", "#6BAF6B", "#A070C8", "#D5D8DE", "#000000", "#2FA4A0" };

        static readonly string[] Zonas =
        {
            "General", "Zona 1 - El costurero", "Zona 2 - La mesa de corte", "Zona 3 - La maquina de coser",
            "Zona 4 - El armario de retazos", "Zona 5 - Las tijeras", "Zona 6 - La huida",
        };

        readonly struct Bloque
        {
            public readonly int zona;
            public readonly string nombre;
            public readonly float x0, x1, y0, y1, z0, z1;
            public readonly Tipo tipo;

            public Bloque(int zona, string nombre, float x0, float x1, float y0, float y1, float z0, float z1, Tipo tipo)
            {
                this.zona = zona;
                this.nombre = nombre;
                this.x0 = x0;
                this.x1 = x1;
                this.y0 = y0;
                this.y1 = y1;
                this.z0 = z0;
                this.z1 = z1;
                this.tipo = tipo;
            }
        }

        // x avanza el nivel, y es la altura y z la profundidad, en metros (Miga = 1). Miga se mueve en la banda
        // de z = -3 a z = 3, cerrada por paredes invisibles. Los frentes del costurero y del armario no se ven,
        // como en una casa de muñecas, para que la cámara vea adentro.
        static readonly Bloque[] Plano =
        {
            new Bloque(0, "Piso", -5f, 140f, -1f, 0f, -20f, 20f, Tipo.Estructura),
            new Bloque(0, "Limite_Inicio", -0.5f, 0f, 0f, 30f, -3.5f, 3.5f, Tipo.Limite),
            new Bloque(0, "Limite_Final", 137f, 137.5f, 0f, 30f, -3.5f, 3.5f, Tipo.Limite),
            new Bloque(0, "Limite_Frente", -0.5f, 137.5f, 0f, 30f, -3.5f, -3f, Tipo.Limite),
            new Bloque(0, "Limite_Fondo", -0.5f, 137.5f, 0f, 30f, 3f, 3.5f, Tipo.Limite),
            new Bloque(1, "MesaCorte", 0f, 30f, 12.15f, 12.75f, -7.5f, 7.5f, Tipo.Estructura),
            new Bloque(1, "MesaCorte_Pata_1", 0f, 1.2f, 0f, 12.15f, -7.5f, -6.3f, Tipo.Estructura),
            new Bloque(1, "MesaCorte_Pata_2", 0f, 1.2f, 0f, 12.15f, 6.3f, 7.5f, Tipo.Estructura),
            new Bloque(1, "MesaCorte_Pata_3", 28.8f, 30f, 0f, 12.15f, -7.5f, -6.3f, Tipo.Estructura),
            new Bloque(1, "MesaCorte_Pata_4", 28.8f, 30f, 0f, 12.15f, 6.3f, 7.5f, Tipo.Estructura),
            new Bloque(1, "Costurero_Pared_A", 2f, 2.3f, 12.75f, 15.3f, -1.7f, 1.7f, Tipo.Estructura),
            new Bloque(1, "Costurero_Pared_B", 6.8f, 7.1f, 12.75f, 15.3f, -1.7f, 1.7f, Tipo.Estructura),
            new Bloque(1, "Costurero_Pared_Fondo", 2f, 7.1f, 12.75f, 15.3f, 1.4f, 1.7f, Tipo.Estructura),
            new Bloque(1, "Costurero_Pared_Frente", 2f, 7.1f, 12.75f, 15.3f, -1.7f, -1.4f, Tipo.Limite),
            new Bloque(1, "Costurero_Tapa", 2f, 5.6f, 15.3f, 15.5f, -1.7f, 1.7f, Tipo.Mecanismo),
            // Suelto: hay que empujarlo hasta la pila para salir (#8)
            new Bloque(1, "Carrete_Empujable", 3.6f, 4.4f, 12.75f, 13.6f, -1.4f, -0.4f, Tipo.Empujable),
            new Bloque(1, "Carretes_2", 6f, 6.8f, 12.75f, 14.45f, -1.4f, -0.4f, Tipo.Paso),
            new Bloque(2, "Tela_1", 9f, 12f, 12.75f, 13.35f, -3f, 0f, Tipo.Obstaculo),
            new Bloque(2, "Alfiler_1", 14f, 14.2f, 12.75f, 12.92f, -2f, 1f, Tipo.Peligro),
            new Bloque(2, "Alfiler_2", 15.5f, 15.7f, 12.75f, 12.92f, -1f, 2.5f, Tipo.Peligro),
            new Bloque(2, "Rollos_Separador", 17f, 27f, 12.75f, 14.35f, -0.5f, 0.5f, Tipo.Estructura),
            new Bloque(2, "Tela_Colgante", 19f, 25f, 13.5f, 15.25f, 0.5f, 3f, Tipo.Obstaculo),
            new Bloque(2, "Telas_Escondite", 23f, 26f, 12.75f, 13.95f, -3f, -1.5f, Tipo.Escondite),
            new Bloque(2, "Regla_Puente", 29f, 34.5f, 12.75f, 12.87f, -0.425f, 0.425f, Tipo.Paso),
            new Bloque(2, "Limite_Regla_Frente", 30f, 33.5f, 12.15f, 16f, -3f, -0.425f, Tipo.Limite),
            new Bloque(2, "Limite_Regla_Fondo", 30f, 33.5f, 12.15f, 16f, 0.425f, 3f, Tipo.Limite),
            new Bloque(3, "MesaMaquina", 33.5f, 58.5f, 12.15f, 12.75f, -7.5f, 7.5f, Tipo.Estructura),
            new Bloque(3, "MesaMaquina_Pata_1", 33.5f, 34.7f, 0f, 12.15f, -7.5f, -6.3f, Tipo.Estructura),
            new Bloque(3, "MesaMaquina_Pata_2", 33.5f, 34.7f, 0f, 12.15f, 6.3f, 7.5f, Tipo.Estructura),
            new Bloque(3, "Pedal", 35.5f, 37f, 12.75f, 13.15f, -1.5f, 1.5f, Tipo.Mecanismo),
            new Bloque(3, "Maquina_Base", 38f, 42f, 12.75f, 13.6f, -3f, 3f, Tipo.Paso),
            new Bloque(3, "Maquina_Aguja", 39.9f, 40.1f, 14.95f, 16.5f, -0.1f, 0.1f, Tipo.Peligro),
            new Bloque(3, "Maquina_Cabezal", 38f, 42f, 16.5f, 18.5f, -3f, 3f, Tipo.Estructura),
            new Bloque(3, "Cajonera", 56f, 58.5f, 0f, 12.15f, -3.5f, 3.5f, Tipo.Estructura),
            new Bloque(3, "Cajon_1", 58.5f, 60f, 9.7f, 10f, -3f, 3f, Tipo.Paso),
            new Bloque(3, "Cajon_2", 58.5f, 61.5f, 7.2f, 7.5f, -3f, 3f, Tipo.Paso),
            new Bloque(3, "Cajon_3", 58.5f, 63f, 4.7f, 5f, -3f, 3f, Tipo.Paso),
            new Bloque(3, "Cajon_4", 58.5f, 64.5f, 2.2f, 2.5f, -3f, 3f, Tipo.Paso),
            new Bloque(3, "Costurera_Silueta", 47f, 51f, 0f, 22f, 8f, 12f, Tipo.Fondo),
            new Bloque(4, "Armario_Lado_A", 70f, 70.4f, 1.2f, 24f, -3.5f, 10f, Tipo.Estructura),
            new Bloque(4, "Armario_Repisa", 70f, 87f, 6.8f, 7.2f, -3.5f, 10f, Tipo.Estructura),
            new Bloque(4, "Armario_Lado_B", 86.6f, 87f, 1.2f, 24f, -3.5f, 10f, Tipo.Estructura),
            new Bloque(4, "Retazos_1", 73f, 75f, 0f, 1.2f, -3f, 0f, Tipo.Escondite),
            new Bloque(4, "Retazos_2", 79f, 81.5f, 0f, 1.2f, 0f, 3f, Tipo.Escondite),
            new Bloque(4, "Retazos_3", 83.5f, 85.5f, 0f, 1.2f, -3f, -1f, Tipo.Escondite),
            new Bloque(4, "Munecos_1", 76f, 77.5f, 0f, 5f, 4f, 5.5f, Tipo.Fondo),
            new Bloque(4, "Munecos_2", 82f, 83.5f, 0f, 5f, 4f, 5.5f, Tipo.Fondo),
            new Bloque(5, "Torre_1", 88f, 90f, 0f, 1f, -1.5f, 1.5f, Tipo.Paso),
            new Bloque(5, "Torre_2", 90f, 91.5f, 0f, 2f, -1.5f, 1.5f, Tipo.Paso),
            new Bloque(5, "Torre_3", 91.5f, 93f, 0f, 3f, -1.5f, 1.5f, Tipo.Paso),
            new Bloque(5, "Torre_4", 93f, 94.5f, 0f, 4f, -1.5f, 1.5f, Tipo.Paso),
            new Bloque(5, "Torre_Cima", 94.5f, 97f, 0f, 5f, -1.5f, 1.5f, Tipo.Paso),
            new Bloque(5, "Tijeras", 95.8f, 98.5f, 5f, 5.4f, -0.5f, 0.5f, Tipo.Mecanismo),
            new Bloque(6, "Dedal", 102f, 102.6f, 0f, 0.34f, -1f, -0.4f, Tipo.Obstaculo),
            new Bloque(6, "Carrete_Huida", 106f, 106.8f, 0f, 0.85f, 0f, 3f, Tipo.Paso),
            new Bloque(6, "Mesita_Agacharse", 111f, 114f, 0.75f, 2f, -3f, 3f, Tipo.Obstaculo),
            new Bloque(6, "Botones", 118f, 118.6f, 0f, 0.25f, -3f, -1.5f, Tipo.Obstaculo),
            new Bloque(6, "Carrete_Tumbado", 123f, 124f, 0f, 1f, -3f, 3f, Tipo.Paso),
            new Bloque(6, "Pared_Zocalo_A", 132f, 133f, 0f, 24f, -3.5f, -0.75f, Tipo.Estructura),
            new Bloque(6, "Pared_Zocalo_B", 132f, 133f, 0f, 24f, 0.75f, 3.5f, Tipo.Estructura),
            new Bloque(6, "Pared_Zocalo_Arriba", 132f, 133f, 0.9f, 24f, -0.75f, 0.75f, Tipo.Estructura),
            new Bloque(6, "Salida", 134f, 136f, 0f, 0.1f, -1f, 1f, Tipo.Mecanismo),
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
                var cubo = GameObject.CreatePrimitive(PrimitiveType.Cube);
                cubo.name = b.nombre;
                cubo.transform.SetParent(padres[b.zona], false);
                cubo.transform.position = new Vector3((b.x0 + b.x1) / 2f, (b.y0 + b.y1) / 2f, (b.z0 + b.z1) / 2f);
                cubo.transform.localScale = new Vector3(b.x1 - b.x0, b.y1 - b.y0, b.z1 - b.z0);
                if (b.tipo == Tipo.Limite)
                    Object.DestroyImmediate(cubo.GetComponent<MeshRenderer>());
                else
                    cubo.GetComponent<Renderer>().sharedMaterial = Material(b.tipo);
                // Lo que se mueve no puede ser estático: los mecanismos (en otras issues) y lo que se empuja
                cubo.isStatic = b.tipo != Tipo.Mecanismo && b.tipo != Tipo.Empujable;
                if (b.tipo == Tipo.Empujable)
                    cubo.AddComponent<Empujable>();
            }

            var prefab = AssetDatabase.LoadAssetAtPath<GameObject>(PrefabMiga);
            if (prefab == null)
            {
                Debug.LogError("No se encontro " + PrefabMiga);
                return;
            }
            var miga = (GameObject)PrefabUtility.InstantiatePrefab(prefab);
            miga.transform.position = InicioMiga;

            ArmarCamaras(miga.transform);

            EditorSceneManager.SaveScene(escena, Escena);
            Debug.Log("Nivel 1 construido: " + Escena);
        }

        // Cámara lateral (#9): una baja que sigue a Miga, y cámaras abiertas que se activan en zonas marcadas.
        static void ArmarCamaras(Transform miga)
        {
            Camera.main.gameObject.AddComponent<CinemachineBrain>();   // mezcla las cámaras en 2 s
            var padre = new GameObject("Camaras").transform;

            // Baja, a la altura de su pecho y un poco inclinada hacia arriba: todo se ve más grande
            var sigue = Camara(padre, "Camara_Miga", miga.position + new Vector3(0f, 0.6f, -7f), -6f, 40f);
            Seguir(sigue, miga, new Vector3(0f, 0.6f, -7f), new Vector3(0.6f, 0.9f, 0f));
            sigue.gameObject.AddComponent<AsomarCamara>();   // joystick derecho o flechas

            // Al cruzar la regla se ve por primera vez a La Costurera completa, sentada a la máquina
            var regla = Camara(padre, "Camara_Abierta_Regla", new Vector3(40f, 11f, -45f), 0f, 40f);
            Zona(padre, "Zona_Camara_Regla", new Vector3(31.75f, 14f, 0f), new Vector3(6.5f, 4f, 7f), regla);

            // En la huida la cámara se aleja y deja a Miga a la derecha, para ver lo que viene detrás
            var huida = Camara(padre, "Camara_Abierta_Huida", miga.position, -3f, 45f);
            Seguir(huida, miga, new Vector3(-5f, 3f, -20f), new Vector3(0.4f, 0.6f, 0f));
            Zona(padre, "Zona_Camara_Huida", new Vector3(115.5f, 3f, 0f), new Vector3(33f, 6f, 7f), huida);
        }

        static CinemachineCamera Camara(Transform padre, string nombre, Vector3 posicion, float inclinacion, float fov)
        {
            var go = new GameObject(nombre);
            go.transform.SetParent(padre, false);
            go.transform.SetPositionAndRotation(posicion, Quaternion.Euler(inclinacion, 0f, 0f));
            var camara = go.AddComponent<CinemachineCamera>();
            camara.Lens.FieldOfView = fov;
            return camara;
        }

        static void Seguir(CinemachineCamera camara, Transform miga, Vector3 distancia, Vector3 suavizado)
        {
            camara.Target.TrackingTarget = miga;
            var seguir = camara.gameObject.AddComponent<CinemachineFollow>();
            seguir.FollowOffset = distancia;
            seguir.TrackerSettings.PositionDamping = suavizado;
        }

        static void Zona(Transform padre, string nombre, Vector3 centro, Vector3 tamano, CinemachineCamera camara)
        {
            var go = new GameObject(nombre);
            go.transform.SetParent(padre, false);
            go.transform.position = centro;
            var caja = go.AddComponent<BoxCollider>();
            caja.isTrigger = true;
            caja.size = tamano;
            go.AddComponent<ZonaDeCamara>().camara = camara.gameObject;
            camara.gameObject.SetActive(false);
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
