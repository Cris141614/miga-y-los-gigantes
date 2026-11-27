using System;
using System.Collections;
using UnityEngine;

namespace Miga.Juego
{
    /// <summary>
    /// Mueve a Miga: caminar, correr, agacharse, saltar, trepar bordes y empujar o jalar objetos. La cámara mira de lado, pero Miga
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
            [Tooltip("Mantener para agarrar lo que tiene enfrente y empujarlo o jalarlo")]
            public bool agarrar;
            [Tooltip("Mantener para tapar el frasco de Chispa con la bufanda")]
            public bool tapar;
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

        [Header("Frasco tapado")]
        [Tooltip("Velocidad con el frasco tapado: camina casi a ciegas y no puede correr")]
        public float velocidadTapada = 1f;

        [Header("Empujar y jalar")]
        [Tooltip("Velocidad con un objeto ligero. La multiplica la Ligereza de cada Empujable")]
        public float velocidadEmpujar = 0.8f;

        [Tooltip("El modelo hijo: gira para mirar hacia donde camina")]
        public Transform modelo;

        public Entrada entrada;

        // Para el sistema de ruido y el hilo rojo
        public bool Corriendo { get; private set; }
        public bool Agachada { get; private set; }
        public bool Trepando { get; private set; }
        /// <summary>Tiene el frasco tapado: la luz de Chispa se apaga (ver LuzChispa).</summary>
        public bool Tapando { get; private set; }
        /// <summary>Lo que tiene agarrado para empujar o jalar; null si no tiene nada.</summary>
        public Empujable Agarrado { get; private set; }
        public bool EnElPiso => cc.isGrounded;
        /// <summary>Hacia dónde mira, en el plano del piso (largo 1).</summary>
        public Vector3 Mirando => mirando;
        public event Action Salto;
        public event Action Aterrizo;

        const float AlturaManos = 0.4f;   // agarra lo que tenga enfrente a esta altura

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
            Tapando = entrada.tapar;
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

            if (ActualizarAgarre(enPiso))
            {
                MoverAgarrada(dir, dt);
                return;
            }

            if (camina)   // gira sobre el eje vertical, así nunca se inclina aunque dé media vuelta
            {
                float actual = Mathf.Atan2(mirando.x, mirando.z) * Mathf.Rad2Deg;
                float meta = Mathf.Atan2(dir.x, dir.z) * Mathf.Rad2Deg;
                // Suave al empezar y al terminar el giro, no a velocidad fija
                float nuevo = Mathf.SmoothDampAngle(actual, meta, ref velGiro, tiempoGiro);
                mirando = Quaternion.Euler(0f, nuevo, 0f) * Vector3.forward;
            }
            Corriendo = entrada.correr && !Agachada && !Tapando && camina;
            float maxima = Agachada ? velocidadAgachada : Tapando ? velocidadTapada : Corriendo ? velocidadCorrer : velocidadCaminar;
            vel = Vector3.MoveTowards(vel, dir * maxima, aceleracion * dt);

            bool pidioSalto = Time.time - ultimoSaltoPedido <= memoriaSalto;
            // Con el botón de agarrar apretado no se trepa sola: quiere agarrar, no subirse
            bool empujaEnElAire = !enPiso && camina && !entrada.agarrar && Vector3.Dot(dir.normalized, mirando) > 0.7f;
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

        // Mientras se mantiene el botón, agarra lo que tiene enfrente. Lo suelta al soltar el botón, al agacharse,
        // al caer o si ya no lo tiene enfrente.
        bool ActualizarAgarre(bool enPiso)
        {
            bool pisando = enPiso || Time.time - ultimoEnPiso <= tiempoCoyote;   // tolera que el piso parpadee al chocar
            float alcanceManos = cc.radius + (Agarrado != null ? 0.25f : 0.15f);   // ya agarrado, no lo suelta por un pelo
            if (!entrada.agarrar || !pisando || Agachada || !BuscarEmpujable(alcanceManos, out var objeto, out var eje))
            {
                Agarrado = null;
                return false;
            }
            if (objeto != Agarrado)
            {
                Agarrado = objeto;
                mirando = eje;   // queda de frente a la cara que agarró
                vel = Vector3.zero;
                Corriendo = false;
            }
            return true;
        }

        // Lleva el objeto hacia donde se mueva, sin darse vuelta: adelante lo empuja, atrás lo jala y a los lados
        // lo lleva de lado. Se mueve por partes para que, si uno choca, el otro se deslice a lo largo de la pared.
        void MoverAgarrada(Vector3 dir, float dt)
        {
            velY = -2f;   // pegada al piso
            var paso = dir * (velocidadEmpujar * Agarrado.ligereza * dt);
            float avance = Vector3.Dot(paso, mirando);
            var adelante = mirando * avance;
            MoverJuntos(adelante, avance > 0f);
            MoverJuntos(paso - adelante, false);
            if (modelo)
                modelo.rotation = Quaternion.LookRotation(mirando);
        }

        // Mueve a Miga y al objeto lo mismo. Primero el que va adelante; si el otro no puede seguirlo, lo regresa.
        void MoverJuntos(Vector3 paso, bool primeroElObjeto)
        {
            if (primeroElObjeto)
            {
                var movido = Agarrado.Mover(paso, cc);
                var hecho = MoverMiga(movido);
                Agarrado.Mover(hecho - movido, cc);
            }
            else
            {
                var hecho = MoverMiga(paso);
                var movido = Agarrado.Mover(hecho, cc);
                MoverMiga(movido - hecho);
            }
        }

        // Mueve a Miga pegada al piso. Devuelve cuánto avanzó en la dirección pedida, sin la altura.
        Vector3 MoverMiga(Vector3 paso)
        {
            var antes = transform.position;
            cc.Move(paso + Vector3.up * (velY * Time.deltaTime));
            float largo = paso.magnitude;
            return largo < 0.0001f ? Vector3.zero : paso / largo * Vector3.Dot(transform.position - antes, paso / largo);
        }

        // ¿Tiene enfrente, a la altura de las manos, algo que se pueda empujar? eje: hacia el objeto, de frente a su cara.
        bool BuscarEmpujable(float distancia, out Empujable objeto, out Vector3 eje)
        {
            objeto = null;
            eje = mirando;
            RaycastHit golpe = default;   // lo más cercano que no sea su propia cápsula: el rayo sale de adentro de ella
            foreach (var h in Physics.RaycastAll(transform.position + Vector3.up * AlturaManos, mirando, distancia,
                                                 ~0, QueryTriggerInteraction.Ignore))
                if (h.collider != cc && (golpe.collider == null || h.distance < golpe.distance))
                    golpe = h;
            if (golpe.collider == null)
                return false;
            eje = Vector3.ProjectOnPlane(-golpe.normal, Vector3.up).normalized;
            if (Vector3.Dot(eje, mirando) < 0.5f)
                return false;   // de frente, no de costado
            objeto = golpe.collider.GetComponentInParent<Empujable>();
            return objeto != null;
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
