using UnityEngine;

namespace Miga.Juego
{
    /// <summary>
    /// La luz de Chispa dentro del frasco: alumbra un radio corto alrededor de Miga y se apaga mientras lo tapa con la
    /// bufanda (ControlMiga.Tapando). Ver docs/Juego/Mecanicas.md.
    /// </summary>
    [RequireComponent(typeof(ControlMiga))]
    public class LuzChispa : MonoBehaviour
    {
        [Tooltip("Hasta dónde alumbra, en metros. Corto: solo alrededor de Miga")]
        public float radio = 2.5f;
        public float intensidad = 2f;
        public Color color = new Color(1f, 0.85f, 0.45f);   // amarillo cálido de luciérnaga
        [Tooltip("Segundos en apagarse al tapar el frasco, y en volver a prenderse al destaparlo")]
        public float tiempoTapar = 0.15f;
        [Tooltip("Dónde va el frasco, medido desde los pies de Miga y mirando hacia donde ella mira")]
        public Vector3 posicionFrasco = new Vector3(0.15f, 0.45f, 0.1f);

        /// <summary>La luz que crea al empezar, hija del modelo para que gire con Miga.</summary>
        public Light Luz { get; private set; }
        /// <summary>Para los Guardadores: true mientras alumbra, aunque sea un poco.</summary>
        public bool Encendida => Luz.intensity > 0f;

        ControlMiga control;

        void Awake()
        {
            control = GetComponent<ControlMiga>();
            var go = new GameObject("Luz_Chispa");
            go.transform.SetParent(control.modelo ? control.modelo : transform, false);
            go.transform.localPosition = posicionFrasco;
            Luz = go.AddComponent<Light>();
            Luz.type = LightType.Point;
            Luz.range = radio;
            Luz.color = color;
            Luz.intensity = intensidad;
            Luz.shadows = LightShadows.None;   // va dentro del modelo: con sombras, el cuerpo de Miga taparía su propia luz
        }

        void Update()
        {
            float meta = control.Tapando ? 0f : intensidad;
            Luz.intensity = Mathf.MoveTowards(Luz.intensity, meta, intensidad / Mathf.Max(tiempoTapar, 0.01f) * Time.deltaTime);
            Luz.range = radio;   // se puede ajustar en el Inspector mientras se juega
        }
    }
}
