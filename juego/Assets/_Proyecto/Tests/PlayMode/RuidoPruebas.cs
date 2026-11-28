using System.Collections;
using System.Collections.Generic;
using Miga.Juego;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace Miga.Pruebas
{
    // Sistema de ruido (#11): los niveles de la tabla de Mecanicas.md y la máquina de coser que los tapa.
    public class RuidoPruebas
    {
        readonly List<GameObject> creados = new List<GameObject>();
        readonly List<NivelRuido> oidos = new List<NivelRuido>();

        void Oir(Vector3 donde, NivelRuido nivel) => oidos.Add(nivel);

        [SetUp]
        public void Escuchar() => Ruido.Sono += Oir;

        [TearDown]
        public void Limpiar()
        {
            Ruido.Sono -= Oir;
            oidos.Clear();
            foreach (var o in creados)
                Object.Destroy(o);
            creados.Clear();
        }

        // Miga parada sobre un piso grande. Espera a que toque el piso y olvida el ruido de esa caída.
        IEnumerator CrearMiga(System.Action<ControlMiga> listo)
        {
            var piso = GameObject.CreatePrimitive(PrimitiveType.Cube);
            piso.transform.position = new Vector3(0f, -0.5f, 0f);
            piso.transform.localScale = new Vector3(30f, 1f, 30f);
            creados.Add(piso);
            var go = new GameObject("Miga");
            creados.Add(go);
            go.transform.position = new Vector3(0f, 0.05f, 0f);
            go.AddComponent<CharacterController>();
            var miga = go.AddComponent<ControlMiga>();
            miga.AjustarCapsula();
            go.AddComponent<RuidoMiga>();
            yield return new WaitForSeconds(0.3f);
            oidos.Clear();
            listo(miga);
        }

        [UnityTest]
        public IEnumerator CaminarHaceRuidoBajo()
        {
            ControlMiga miga = null;
            yield return CrearMiga(m => miga = m);
            miga.entrada.mover = Vector2.right;

            yield return new WaitForSeconds(1f);

            Assert.That(oidos, Has.Member(NivelRuido.Bajo));
            Assert.That(oidos, Has.No.Member(NivelRuido.Medio));
        }

        [UnityTest]
        public IEnumerator AgachadaNoHaceRuido()
        {
            ControlMiga miga = null;
            yield return CrearMiga(m => miga = m);
            miga.entrada = new ControlMiga.Entrada { mover = Vector2.right, agachar = true };

            yield return new WaitForSeconds(1f);

            Assert.That(miga.transform.position.x, Is.GreaterThan(0.3f), "Tiene que haber avanzado");
            Assert.That(oidos, Is.Empty);
        }

        [UnityTest]
        public IEnumerator CorrerYSaltarHacenRuidoMedio()
        {
            ControlMiga miga = null;
            yield return CrearMiga(m => miga = m);
            miga.entrada = new ControlMiga.Entrada { mover = Vector2.right, correr = true };
            yield return new WaitForSeconds(0.5f);
            Assert.That(oidos, Has.Member(NivelRuido.Medio));

            miga.entrada = default;
            yield return new WaitForSeconds(0.5f);
            oidos.Clear();
            miga.Saltar();
            yield return new WaitForSeconds(1f);
            Assert.That(oidos, Has.Exactly(2).EqualTo(NivelRuido.Medio), "Uno al saltar y otro al caer");
        }

        [UnityTest]
        public IEnumerator LaMaquinaEncendidaTapaBajoYMedio()
        {
            var maquina = new GameObject("Maquina").AddComponent<MaquinaDeCoser>();
            creados.Add(maquina.gameObject);
            yield return null;

            Ruido.Hacer(Vector3.zero, NivelRuido.Bajo);
            Ruido.Hacer(Vector3.zero, NivelRuido.Medio);
            Ruido.Hacer(Vector3.zero, NivelRuido.Alto);
            Assert.That(oidos, Is.EqualTo(new[] { NivelRuido.Alto }));

            maquina.enabled = false;   // apagada
            oidos.Clear();
            Ruido.Hacer(Vector3.zero, NivelRuido.Bajo);
            Assert.That(oidos, Is.EqualTo(new[] { NivelRuido.Bajo }));
        }
    }
}
