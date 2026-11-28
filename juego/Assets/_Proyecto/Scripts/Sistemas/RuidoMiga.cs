using UnityEngine;

namespace Miga.Juego
{
    /// <summary>
    /// El ruido que hace Miga: un paso cada tanto mientras camina (bajo; medio si corre; nada si va agachada),
    /// y ruido medio al saltar y al caer.
    /// </summary>
    [RequireComponent(typeof(ControlMiga))]
    public class RuidoMiga : MonoBehaviour
    {
        [Tooltip("Segundos entre pasos al caminar. Corriendo, los pasos van el doble de rápido")]
        public float intervaloPaso = 0.45f;

        /// <summary>Qué tan fuerte suenan sus pasos ahora.</summary>
        public NivelRuido NivelPasos =>
            control.Agachada ? NivelRuido.Ninguno : control.Corriendo ? NivelRuido.Medio : NivelRuido.Bajo;

        const float VelocidadMinima = 0.2f;   // m/s: más despacio que esto ya no cuenta como paso

        ControlMiga control;
        Vector3 antes;
        float hastaPaso;

        void Awake()
        {
            control = GetComponent<ControlMiga>();
            control.Salto += Fuerte;
            control.Aterrizo += Fuerte;
            antes = transform.position;
        }

        void OnDestroy()
        {
            control.Salto -= Fuerte;
            control.Aterrizo -= Fuerte;
        }

        void Fuerte() => Ruido.Hacer(transform.position, NivelRuido.Medio);

        void Update()
        {
            Vector3 avance = transform.position - antes;
            antes = transform.position;
            avance.y = 0f;
            bool camina = control.EnElPiso && !control.Trepando
                && avance.magnitude > VelocidadMinima * Time.deltaTime;
            if (!camina)
            {
                hastaPaso = 0f;   // el primer paso al arrancar suena de una vez
                return;
            }
            hastaPaso -= Time.deltaTime;
            if (hastaPaso > 0f)
                return;
            hastaPaso = control.Corriendo ? intervaloPaso / 2f : intervaloPaso;
            Ruido.Hacer(transform.position, NivelPasos);
        }
    }
}
