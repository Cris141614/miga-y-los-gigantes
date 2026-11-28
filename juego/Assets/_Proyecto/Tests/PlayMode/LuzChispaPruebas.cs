using System.Collections;
using System.Collections.Generic;
using Miga.Juego;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace Miga.Pruebas
{
    // La luz de Chispa y tapar el frasco (#10). La entrada se llena a mano, como en ControlMigaPruebas.
    public class LuzChispaPruebas
    {
        readonly List<GameObject> creados = new List<GameObject>();

        [TearDown]
        public void Limpiar()
        {
            foreach (var o in creados)
                Object.Destroy(o);
            creados.Clear();
        }

        // Miga parada en el origen sobre un piso grande, con su luz.
        LuzChispa CrearMiga()
        {
            var piso = GameObject.CreatePrimitive(PrimitiveType.Cube);
            piso.transform.position = new Vector3(0f, -0.5f, 0f);
            piso.transform.localScale = new Vector3(30f, 1f, 30f);
            creados.Add(piso);
            var go = new GameObject("Miga");
            creados.Add(go);
            go.transform.position = new Vector3(0f, 0.05f, 0f);
            go.AddComponent<CharacterController>();
            go.AddComponent<ControlMiga>().AjustarCapsula();
            return go.AddComponent<LuzChispa>();
        }

        [UnityTest]
        public IEnumerator AlumbraUnRadioCortoAlrededorDeMiga()
        {
            var chispa = CrearMiga();
            yield return null;

            Assert.That(chispa.Encendida, Is.True);
            Assert.That(chispa.Luz.type, Is.EqualTo(LightType.Point));
            Assert.That(chispa.Luz.range, Is.InRange(1f, 4f), "Radio corto: unos pasos alrededor de Miga");
            Assert.That(Vector3.Distance(chispa.Luz.transform.position, chispa.transform.position), Is.LessThan(1f));
        }

        [UnityTest]
        public IEnumerator TaparApagaLaLuzYDestaparLaPrende()
        {
            var chispa = CrearMiga();
            var miga = chispa.GetComponent<ControlMiga>();

            miga.entrada.tapar = true;
            yield return new WaitForSeconds(0.3f);
            Assert.That(miga.Tapando, Is.True);
            Assert.That(chispa.Encendida, Is.False);

            miga.entrada.tapar = false;
            yield return new WaitForSeconds(0.3f);
            Assert.That(chispa.Encendida, Is.True);
            Assert.That(chispa.Luz.intensity, Is.EqualTo(chispa.intensidad).Within(0.01f));
        }

        [UnityTest]
        public IEnumerator ConElFrascoTapadoCaminaMasLentoYNoCorre()
        {
            var miga = CrearMiga().GetComponent<ControlMiga>();
            miga.entrada = new ControlMiga.Entrada { mover = Vector2.right, correr = true, tapar = true };

            yield return new WaitForSeconds(1f);

            Assert.That(miga.Corriendo, Is.False);
            // Caminando normal avanza más de 1.4 m en un segundo; tapada, alrededor de 1 m
            Assert.That(miga.transform.position.x, Is.InRange(0.7f, 1.1f));
        }
    }
}
