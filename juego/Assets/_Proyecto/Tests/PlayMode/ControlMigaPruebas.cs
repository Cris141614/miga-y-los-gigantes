using System.Collections;
using System.Collections.Generic;
using Miga.Juego;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace Miga.Pruebas
{
    // Movimiento de Miga sin teclado: cada prueba llena la entrada como lo haría EntradaMiga.
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

        // Un piso con la cara de arriba en y = 0 y Miga parada encima, en x = 0.
        ControlMiga CrearMiga()
        {
            Cubo(new Vector3(0f, -0.5f, 0f), new Vector3(30f, 1f, 4f));
            var go = new GameObject("Miga");
            creados.Add(go);
            go.transform.position = new Vector3(0f, 0.05f, 0f);
            go.AddComponent<CharacterController>();
            var miga = go.AddComponent<ControlMiga>();
            miga.AjustarCapsula();
            return miga;
        }

        [UnityTest]
        public IEnumerator CaminaDeLadoSinSalirseDeSuCarril()
        {
            var miga = CrearMiga();
            miga.entrada.mover = 1f;

            yield return new WaitForSeconds(1f);

            Assert.That(miga.transform.position.x, Is.InRange(1f, 2f));
            Assert.That(miga.transform.position.z, Is.EqualTo(0f).Within(0.001f));
            Assert.That(miga.Corriendo, Is.False);
        }

        [UnityTest]
        public IEnumerator CorrerEsMasRapidoYSeNota()
        {
            var miga = CrearMiga();
            miga.entrada = new ControlMiga.Entrada { mover = 1f, correr = true };

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
            miga.entrada.mover = 1f;
            yield return new WaitForSeconds(0.8f);   // camina hasta la pared

            miga.Saltar();
            yield return new WaitForSeconds(1f);

            Assert.That(miga.transform.position.y, Is.EqualTo(0.8f).Within(0.08f));
            Assert.That(miga.transform.position.x, Is.GreaterThan(1f));
        }

        [UnityTest]
        public IEnumerator NoTrepaUnaParedMasAltaQueSuAlcance()
        {
            var miga = CrearMiga();
            Cubo(new Vector3(3f, 0.8f, 0f), new Vector3(4f, 1.6f, 4f));   // pared de 1.6 m
            miga.entrada.mover = 1f;
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
    }
}
