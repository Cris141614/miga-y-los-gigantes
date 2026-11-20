using System;
using System.Collections;
using UnityEngine;

namespace Miga.Juego
{
    /// <summary>
    /// Mueve a Miga: caminar, correr, agacharse, saltar y trepar bordes. La cámara mira de lado, pero Miga
    /// también se mueve en profundidad, como en Little Nightmares (ver docs/Juego/Vision.md).
    /// No lee el teclado: usa <see cref="entrada"/>, que llena EntradaMiga (o una prueba).
    /// </summary>
    [RequireComponent(typeof(CharacterController))]
    public class ControlMiga : MonoBehaviour
    {
        [Serializable]
        public struct Entrada
        {
            [Tooltip("x: izquierda (-1) y derecha (1) en pantalla. y: hacia la cámara (-1) y hacia el fondo (1)")]
            public Vector2 mover;
            public bool correr;
            public bool agachar;
        }

        [Header("Velocidades (m/s)")]
        public float velocidadCaminar = 1.6f;
        public float velocidadCorrer = 3.2f;
        public float velocidadAgachada = 0.8f;
        public float aceleracion = 14f;
        [Tooltip("Segundos que tarda, más o menos, en girar hacia donde camina. Más alto, más lento y pesado")]
        public float tiempoGiro = 0.2f;   // lento y pesado, como con miedo

        [Header("Salto")]
        public float alturaSalto = 0.45f;
        public float gravedad = 20f;
        [Tooltip("Segundos en que todavía puede saltar después de dejar el borde")]
        public float tiempoCoyote = 0.1f;
        [Tooltip("Segundos que se recuerda el botón de saltar si se apretó un poco antes de tocar el piso")]
        public float memoriaSalto = 0.15f;

        [Header("Trepar")]
        [Tooltip("Bordes más bajos que esto se pasan saltando")]
        public float alturaMinimaBorde = 0.3f;
        [Tooltip("Altura máxima del borde, medida desde los pies: la altura de Miga")]
        public float alcance = Escala.AlturaMiga;
        public float duracionTrepar = 0.4f;

        [Header("Agacharse")]
        public float alturaAgachada = 0.6f;

        [Tooltip("El modelo hijo: gira para mirar hacia donde camina")]
        public Transform modelo;

        public Entrada entrada;

        // Para el sistema de ruido y el hilo rojo
        public bool Corriendo { get; private set; }
        public bool Agachada { get; private set; }
        public bool Trepando { get; private set; }
        public bool EnElPiso => cc.isGrounded;
        /// <summary>Hacia dónde mira, en el plano del piso (largo 1).</summary>
        public Vector3 Mirando => mirando;
        public event Action Salto;
        public event Action Aterrizo;

        CharacterController cc;
        Vector3 vel, mirando = Vector3.right;
        float velY, velGiro;
        float ultimoEnPiso = -1f, ultimoSaltoPedido = -1f;
        bool enElAire;

        /// <summary>Pide un salto. Si hay un borde a su alcance enfrente, lo trepa.</summary>
        public void Saltar() => ultimoSaltoPedido = Time.time;

        /// <summary>Cápsula del tamaño de Miga, con el origen en los pies.</summary>
        public void AjustarCapsula()
        {
            var c = GetComponent<CharacterController>();
            c.height = Escala.AlturaMiga;
            c.radius = 0.2f;
            c.center = new Vector3(0f, Escala.AlturaMiga / 2f, 0f);
            c.stepOffset = 0.15f;
            c.skinWidth = 0.02f;
            c.minMoveDistance = 0f;
        }

        void Reset() => AjustarCapsula();   // Unity lo llama al agregar el componente en el editor

        void Awake() => cc = GetComponent<CharacterController>();

        void Update()
        {
            if (Trepando)
                return;

            float dt = Time.deltaTime;
            bool enPiso = cc.isGrounded;
            if (enPiso)
                ultimoEnPiso = Time.time;

            ActualizarAgachada(enPiso);

            // Plano del piso: x es izquierda-derecha en pantalla, z es hacia el fondo
            var dir = new Vector3(entrada.mover.x, 0f, entrada.mover.y);
            dir = dir.magnitude < 0.15f ? Vector3.zero : Vector3.ClampMagnitude(dir, 1f);
            bool camina = dir != Vector3.zero;
            if (camina)   // gira sobre el eje vertical, así nunca se inclina aunque dé media vuelta
            {
                float actual = Mathf.Atan2(mirando.x, mirando.z) * Mathf.Rad2Deg;
                float meta = Mathf.Atan2(dir.x, dir.z) * Mathf.Rad2Deg;
                // Suave al empezar y al terminar el giro, no a velocidad fija
                float nuevo = Mathf.SmoothDampAngle(actual, meta, ref velGiro, tiempoGiro);
                mirando = Quaternion.Euler(0f, nuevo, 0f) * Vector3.forward;
            }
            Corriendo = entrada.correr && !Agachada && camina;
            float maxima = Agachada ? velocidadAgachada : Corriendo ? velocidadCorrer : velocidadCaminar;
            vel = Vector3.MoveTowards(vel, dir * maxima, aceleracion * dt);

            bool pidioSalto = Time.time - ultimoSaltoPedido <= memoriaSalto;
            bool empujaEnElAire = !enPiso && camina && Vector3.Dot(dir.normalized, mirando) > 0.7f;
            if ((pidioSalto || empujaEnElAire) && !Agachada && BuscarBorde(out Vector3 arriba))
            {
                ultimoSaltoPedido = -1f;
                StartCoroutine(Trepar(arriba));
                return;
            }

            if (pidioSalto && !Agachada && Time.time - ultimoEnPiso <= tiempoCoyote)
            {
                velY = Mathf.Sqrt(2f * gravedad * alturaSalto);
                ultimoSaltoPedido = ultimoEnPiso = -1f;
                Salto?.Invoke();
            }
            else if (enPiso && velY < 0f)
            {
                velY = -2f;   // pegada al piso, para que isGrounded no parpadee
            }
            velY -= gravedad * dt;

            var choques = cc.Move((vel + Vector3.up * velY) * dt);
            if ((choques & CollisionFlags.Above) != 0 && velY > 0f)
                velY = 0f;
            bool aterrizo = enElAire && cc.isGrounded;
            enElAire = !cc.isGrounded;
            if (aterrizo)
                Aterrizo?.Invoke();

            if (modelo)
                modelo.rotation = Quaternion.LookRotation(mirando);
        }

        void ActualizarAgachada(bool enPiso)
        {
            bool quiere = entrada.agachar && (enPiso || Agachada);
            if (quiere == Agachada || (!quiere && HayAlgoEn(transform.position, alturaAgachada, Escala.AlturaMiga)))
                return;   // bajo un techo bajo no se puede parar
            Agachada = quiere;
            cc.height = Agachada ? alturaAgachada : Escala.AlturaMiga;
            cc.center = new Vector3(0f, cc.height / 2f, 0f);
        }

        // Busca enfrente, hacia donde mira, un borde entre alturaMinimaBorde y alcance, con lugar para pararse encima.
        bool BuscarBorde(out Vector3 destino)
        {
            destino = default;
            var pies = transform.position;
            if (!Physics.Raycast(pies + Vector3.up * alturaMinimaBorde, mirando, out var pared, cc.radius + 0.25f,
                                 ~0, QueryTriggerInteraction.Ignore))
                return false;
            if (Vector3.Dot(pared.normal, -mirando) < 0.5f)
                return false;   // la pared tiene que estar de frente, no de costado

            // Desde arriba de su alcance, bajar justo detrás de la orilla hasta dar con la parte de arriba
            var detras = pared.point + mirando * (cc.radius + 0.05f);
            var arriba = new Vector3(detras.x, pies.y + alcance + 0.05f, detras.z);
            if (!Physics.Raycast(arriba, Vector3.down, out var tope, alcance + 0.05f - alturaMinimaBorde,
                                 ~0, QueryTriggerInteraction.Ignore))
                return false;   // más alto que su alcance: el rayo empieza dentro de la pared y no la ve

            destino = new Vector3(arriba.x, tope.point.y + 0.01f, arriba.z);
            return !HayAlgoEn(destino, 0.02f, Escala.AlturaMiga);
        }

        IEnumerator Trepar(Vector3 destino)
        {
            Trepando = true;
            Corriendo = false;
            vel = Vector3.zero;
            velY = 0f;
            cc.enabled = false;
            var inicio = transform.position;
            var orilla = new Vector3(inicio.x, destino.y, inicio.z);
            float subir = duracionTrepar * 0.6f, pasar = duracionTrepar - subir;
            for (float t = 0f; t < subir; t += Time.deltaTime)
            {
                transform.position = Vector3.Lerp(inicio, orilla, t / subir);
                yield return null;
            }
            for (float t = 0f; t < pasar; t += Time.deltaTime)
            {
                transform.position = Vector3.Lerp(orilla, destino, t / pasar);
                yield return null;
            }
            transform.position = destino;
            cc.enabled = true;
            enElAire = false;   // queda parada encima: no es una caída
            Trepando = false;
        }

        // ¿Hay algo sólido (que no sea ella) entre esas dos alturas, con el ancho de su cápsula?
        bool HayAlgoEn(Vector3 pies, float desde, float hasta)
        {
            float r = cc.radius * 0.95f;
            var abajo = pies + Vector3.up * (desde + r);
            var arriba = pies + Vector3.up * Mathf.Max(hasta - r, desde + r);
            foreach (var c in Physics.OverlapCapsule(abajo, arriba, r, ~0, QueryTriggerInteraction.Ignore))
                if (c != cc)
                    return true;
            return false;
        }
    }
}
