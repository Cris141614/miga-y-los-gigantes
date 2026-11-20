using UnityEngine;

namespace Miga.Juego
{
    /// <summary>
    /// Algo que Miga puede agarrar para empujar o jalar, como el carrete del costurero (docs/Juego/Mecanicas.md).
    /// Se desliza por el piso sin física: no rueda ni se vuelca, y se detiene justo al tocar otra cosa.
    /// </summary>
    [RequireComponent(typeof(BoxCollider))]
    public class Empujable : MonoBehaviour
    {
        [Tooltip("1 = ligero. Más bajo, más pesado: Miga lo mueve más lento")]
        [Range(0.2f, 1f)]
        public float ligereza = 1f;

        const float Margen = 0.02f;   // la caja se achica un poco al barrer, para no rozar el piso ni las paredes de al lado
        BoxCollider caja;

        void Awake() => caja = GetComponent<BoxCollider>();

        // shortcut: no cae si se empuja fuera de un borde; agregarle gravedad cuando un nivel lo necesite
        /// <summary>Lo mueve por el piso hasta donde pueda sin chocar. Devuelve cuánto se movió.</summary>
        public Vector3 Mover(Vector3 paso, Collider ignorar)
        {
            float largo = paso.magnitude;
            if (largo < 0.0001f)
                return Vector3.zero;
            var dir = paso / largo;
            var centro = transform.TransformPoint(caja.center);
            var medio = Vector3.Scale(caja.size, transform.lossyScale) * 0.5f - Vector3.one * Margen;
            foreach (var golpe in Physics.BoxCastAll(centro, medio, dir, transform.rotation, largo + Margen,
                                                     ~0, QueryTriggerInteraction.Ignore))
                if (golpe.collider != caja && golpe.collider != ignorar)
                    largo = Mathf.Min(largo, Mathf.Max(0f, golpe.distance - Margen));

            var movido = dir * largo;
            transform.position += movido;
            Physics.SyncTransforms();   // para que Miga y los rayos lo vean donde quedó en este mismo frame
            return movido;
        }
    }
}
