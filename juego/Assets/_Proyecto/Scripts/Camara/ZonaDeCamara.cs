using UnityEngine;

namespace Miga.Juego
{
    /// <summary>
    /// Mientras Miga está dentro de esta caja, activa otra cámara de Cinemachine (por ejemplo, una abierta
    /// para ver a un Guardador completo). Cinemachine hace la transición: gana la cámara activada más reciente.
    /// </summary>
    [RequireComponent(typeof(BoxCollider))]
    public class ZonaDeCamara : MonoBehaviour
    {
        [Tooltip("La cámara que se activa mientras Miga está dentro de la zona")]
        public GameObject camara;

        BoxCollider caja;
        ControlMiga miga;
        bool dentro;

        void Reset() => GetComponent<BoxCollider>().isTrigger = true;   // solo marca la zona, no choca

        void Awake()
        {
            caja = GetComponent<BoxCollider>();
            caja.isTrigger = true;   // una zona de cámara nunca debe ser una pared
        }

        // En Start y no en Awake: así también vale si la cámara se asigna justo después de crear la zona
        void Start()
        {
            miga = FindAnyObjectByType<ControlMiga>();
            if (camara)
                camara.SetActive(false);
        }

        // Se compara la posición en vez de usar OnTriggerEnter: al trepar, Miga apaga su cápsula un momento
        // y los eventos de trigger harían parpadear la cámara.
        void Update()
        {
            if (!miga || !camara)
                return;
            bool ahora = caja.bounds.Contains(miga.transform.position + Vector3.up * 0.5f);
            if (ahora != dentro)
                camara.SetActive(dentro = ahora);
        }
    }
}
