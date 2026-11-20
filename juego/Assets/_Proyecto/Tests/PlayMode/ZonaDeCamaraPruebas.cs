using System.Collections;
using System.Collections.Generic;
using Miga.Juego;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace Miga.Pruebas
{
    public class ZonaDeCamaraPruebas
    {
        readonly List<GameObject> creados = new List<GameObject>();

        [TearDown]
        public void Limpiar()
        {
            foreach (var o in creados)
                Object.Destroy(o);
            creados.Clear();
        }

        [UnityTest]
        public IEnumerator LaCamaraAbiertaSeActivaSoloMientrasMigaEstaDentro()
        {
            var piso = GameObject.CreatePrimitive(PrimitiveType.Cube);
            piso.transform.position = new Vector3(0f, -0.5f, 0f);
            piso.transform.localScale = new Vector3(30f, 1f, 4f);
            creados.Add(piso);

            var go = new GameObject("Miga");
            creados.Add(go);
            go.transform.position = new Vector3(0f, 0.05f, 0f);
            go.AddComponent<CharacterController>();
            var miga = go.AddComponent<ControlMiga>();
            miga.AjustarCapsula();

            var camara = new GameObject("Camara_Abierta");
            creados.Add(camara);
            var zona = new GameObject("Zona");
            creados.Add(zona);
            zona.transform.position = new Vector3(1.5f, 0.5f, 0f);   // de x = 1 a x = 2
            zona.AddComponent<BoxCollider>().size = new Vector3(1f, 2f, 2f);
            zona.AddComponent<ZonaDeCamara>().camara = camara;

            yield return null;
            Assert.That(camara.activeSelf, Is.False, "Afuera de la zona la cámara abierta está apagada");

            miga.entrada.mover = Vector2.right;
            yield return new WaitForSeconds(1f);   // va por x = 1.5
            Assert.That(camara.activeSelf, Is.True, "Dentro de la zona se activa");

            yield return new WaitForSeconds(1f);   // va por x = 3
            Assert.That(camara.activeSelf, Is.False, "Al salir se apaga");
        }
    }
}
