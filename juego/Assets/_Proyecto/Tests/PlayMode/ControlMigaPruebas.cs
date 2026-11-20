using System.Collections;
using System.Collections.Generic;
using Miga.Juego;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace Miga.Pruebas
{
    // Movimiento de Miga sin teclado: cada prueba llena la entrada como lo haría EntradaMiga.
    // x de la entrada es izquierda-derecha en pantalla; y es hacia el fondo (z del mundo).
    public class ControlMigaPruebas
    {
        readonly List<GameObject> creados = new List<GameObject>();

        [TearDown]
        public void Limpiar()
        {
            foreach (var o in creados)
                Object.Destroy(o);
            creados.Clear();
        }

        GameObject Cubo(Vector3 centro, Vector3 tamano)
        {
            var cubo = GameObject.CreatePrimitive(PrimitiveType.Cube);
            cubo.transform.position = centro;
            cubo.transform.localScale = tamano;
            creados.Add(cubo);
            return cubo;
        }

        // Un piso grande con la cara de arriba en y = 0 y Miga parada encima, en el origen.
        ControlMiga CrearMiga()
        {
            Cubo(new Vector3(0f, -0.5f, 0f), new Vector3(30f, 1f, 30f));
            var go = new GameObject("Miga");
            creados.Add(go);
            go.transform.position = new Vector3(0f, 0.05f, 0f);
            go.AddComponent<CharacterController>();
            var miga = go.AddComponent<ControlMiga>();
            miga.AjustarCapsula();
            return miga;
        }

        [UnityTest]
        public IEnumerator CaminaHaciaLaDerecha()
        {
            var miga = CrearMiga();
            miga.entrada.mover = Vector2.right;

            yield return new WaitForSeconds(1f);

            Assert.That(miga.transform.position.x, Is.InRange(1f, 2f));
            Assert.That(miga.transform.position.z, Is.EqualTo(0f).Within(0.01f));
            Assert.That(miga.Corriendo, Is.False);
        }

        [UnityTest]
        public IEnumerator CaminaHaciaElFondoYGiraHaciaAlla()
        {
            var miga = CrearMiga();
            miga.entrada.mover = Vector2.up;

            yield return new WaitForSeconds(1.5f);   // el giro es lento: le da tiempo de terminarlo

            Assert.That(miga.transform.position.z, Is.InRange(1.5f, 3f));
            Assert.That(miga.transform.position.x, Is.EqualTo(0f).Within(0.01f));
            Assert.That(Vector3.Angle(miga.Mirando, Vector3.forward), Is.LessThan(2f));
        }

        [UnityTest]
        public IEnumerator CorrerEsMasRapidoYSeNota()
        {
            var miga = CrearMiga();
            miga.entrada = new ControlMiga.Entrada { mover = Vector2.right, correr = true };

            yield return new WaitForSeconds(1f);

            Assert.That(miga.transform.position.x, Is.GreaterThan(2.5f));
            Assert.That(miga.Corriendo, Is.True);
        }

        [UnityTest]
        public IEnumerator SaltaYAvisaAlSaltarYAlCaer()
        {
            var miga = CrearMiga();
            yield return new WaitForSeconds(0.3f);   // que primero toque el piso
            int saltos = 0, caidas = 0;
            miga.Salto += () => saltos++;
            miga.Aterrizo += () => caidas++;

            miga.Saltar();
            yield return new WaitForSeconds(0.15f);
            Assert.That(miga.transform.position.y, Is.GreaterThan(0.2f));

            yield return new WaitForSeconds(1f);
            Assert.That(miga.EnElPiso, Is.True);
            Assert.That(saltos, Is.EqualTo(1));
            Assert.That(caidas, Is.EqualTo(1));
        }

        [UnityTest]
        public IEnumerator TrepaUnBordeDeSuAltura()
        {
            var miga = CrearMiga();
            Cubo(new Vector3(3f, 0.4f, 0f), new Vector3(4f, 0.8f, 4f));   // borde de 0.8 m que empieza en x = 1
            miga.entrada.mover = Vector2.right;
            yield return new WaitForSeconds(0.8f);   // camina hasta la pared

            miga.Saltar();
            yield return new WaitForSeconds(1f);

            Assert.That(miga.transform.position.y, Is.EqualTo(0.8f).Within(0.08f));
            Assert.That(miga.transform.position.x, Is.GreaterThan(1f));
        }

        [UnityTest]
        public IEnumerator TrepaUnBordeMirandoHaciaElFondo()
        {
            var miga = CrearMiga();
            Cubo(new Vector3(0f, 0.4f, 3f), new Vector3(4f, 0.8f, 4f));   // borde de 0.8 m que empieza en z = 1
            miga.entrada.mover = Vector2.up;
            yield return new WaitForSeconds(0.8f);

            miga.Saltar();
            yield return new WaitForSeconds(1f);

            Assert.That(miga.transform.position.y, Is.EqualTo(0.8f).Within(0.08f));
            Assert.That(miga.transform.position.z, Is.GreaterThan(1f));
        }

        [UnityTest]
        public IEnumerator NoTrepaUnaParedMasAltaQueSuAlcance()
        {
            var miga = CrearMiga();
            Cubo(new Vector3(3f, 0.8f, 0f), new Vector3(4f, 1.6f, 4f));   // pared de 1.6 m
            miga.entrada.mover = Vector2.right;
            yield return new WaitForSeconds(0.8f);

            miga.Saltar();
            yield return new WaitForSeconds(1f);

            Assert.That(miga.transform.position.y, Is.LessThan(0.1f));
            Assert.That(miga.transform.position.x, Is.LessThan(1f));
        }

        [UnityTest]
        public IEnumerator AgachadaNoSePuedeParaBajoUnTechoBajo()
        {
            var miga = CrearMiga();
            yield return new WaitForSeconds(0.3f);
            miga.entrada.agachar = true;
            yield return null;
            yield return null;
            Assert.That(miga.Agachada, Is.True);

            Cubo(new Vector3(0f, 0.85f, 0f), new Vector3(2f, 0.2f, 4f));   // techo a 0.75 m: cabe agachada (0.6), no parada (1)
            yield return new WaitForFixedUpdate();
            miga.entrada.agachar = false;
            yield return new WaitForSeconds(0.2f);

            Assert.That(miga.Agachada, Is.True);
        }

        // Una caja de 0.8 m que se puede empujar, con la cara de la izquierda en x = 0.5, delante de Miga.
        Empujable Caja()
        {
            var caja = Cubo(new Vector3(0.9f, 0.4f, 0f), new Vector3(0.8f, 0.8f, 0.8f)).AddComponent<Empujable>();
            Physics.SyncTransforms();   // que la física ya la vea en su lugar
            return caja;
        }

        // Si una prueba falla, dice dónde quedó Miga
        static string Donde(ControlMiga miga) =>
            $"Miga quedó en {miga.transform.position}, en el piso: {miga.EnElPiso}, trepando: {miga.Trepando}";

        // Espera a que toque el piso, camina hasta la caja y la agarra.
        IEnumerator Agarrar(ControlMiga miga, Empujable caja)
        {
            yield return new WaitForSeconds(0.3f);
            miga.entrada = new ControlMiga.Entrada { mover = Vector2.right, agarrar = true };
            yield return new WaitForSeconds(0.5f);
            Assert.That(miga.Agarrado, Is.EqualTo(caja), Donde(miga));
            miga.entrada.mover = Vector2.zero;
            yield return null;
        }

        [UnityTest]
        public IEnumerator EmpujaUnaCajaAgarrandola()
        {
            var miga = CrearMiga();
            var caja = Caja();
            yield return Agarrar(miga, caja);

            miga.entrada.mover = Vector2.right;
            yield return new WaitForSeconds(1f);

            Assert.That(miga.Agarrado, Is.EqualTo(caja), Donde(miga));
            Assert.That(caja.transform.position.x, Is.GreaterThan(1.5f));
            Assert.That(caja.transform.position.y, Is.EqualTo(0.4f).Within(0.001f));   // se desliza, no se levanta
            Assert.That(miga.transform.position.x, Is.LessThan(caja.transform.position.x - 0.4f));
        }

        [UnityTest]
        public IEnumerator JalaUnaCajaSinDarseVuelta()
        {
            var miga = CrearMiga();
            var caja = Caja();
            yield return Agarrar(miga, caja);
            float antes = caja.transform.position.x;

            miga.entrada.mover = Vector2.left;
            yield return new WaitForSeconds(1f);

            Assert.That(miga.Agarrado, Is.EqualTo(caja), Donde(miga));
            Assert.That(caja.transform.position.x, Is.LessThan(antes - 0.5f));
            Assert.That(Vector3.Angle(miga.Mirando, Vector3.right), Is.LessThan(1f));
        }

        [UnityTest]
        public IEnumerator NoEmpujaUnaCajaContraLaPared()
        {
            var miga = CrearMiga();
            var caja = Caja();
            Cubo(new Vector3(2.5f, 1f, 0f), new Vector3(1f, 2f, 4f));   // pared con la cara en x = 2
            yield return Agarrar(miga, caja);

            miga.entrada.mover = Vector2.right;
            yield return new WaitForSeconds(2f);

            Assert.That(caja.transform.position.x, Is.EqualTo(1.6f).Within(0.01f));   // tocando la pared, sin meterse
            Assert.That(miga.transform.position.x, Is.LessThan(1.2f));
        }

        [UnityTest]
        public IEnumerator MueveUnaCajaDeLado()
        {
            var miga = CrearMiga();
            var caja = Caja();
            yield return Agarrar(miga, caja);

            miga.entrada.mover = Vector2.up;   // hacia el fondo, de lado respecto a la caja
            yield return new WaitForSeconds(1f);

            Assert.That(miga.Agarrado, Is.EqualTo(caja), Donde(miga));
            Assert.That(caja.transform.position.z, Is.GreaterThan(0.5f));
            Assert.That(miga.transform.position.z, Is.EqualTo(caja.transform.position.z).Within(0.03f));
            Assert.That(Vector3.Angle(miga.Mirando, Vector3.right), Is.LessThan(1f));
        }

        [UnityTest]
        public IEnumerator SiLaCajaChocaDeLadoMigaTambienSeDetiene()
        {
            var miga = CrearMiga();
            var caja = Caja();
            Cubo(new Vector3(1f, 1f, 1.5f), new Vector3(4f, 2f, 1f));   // pared al fondo con la cara en z = 1
            yield return Agarrar(miga, caja);

            miga.entrada.mover = Vector2.up;
            yield return new WaitForSeconds(1.5f);

            Assert.That(caja.transform.position.z, Is.EqualTo(0.6f).Within(0.01f));   // la caja toca la pared
            Assert.That(miga.transform.position.z, Is.EqualTo(0.6f).Within(0.03f), Donde(miga));   // y Miga no se adelanta
            Assert.That(miga.Agarrado, Is.EqualTo(caja), Donde(miga));
        }
    }
}
