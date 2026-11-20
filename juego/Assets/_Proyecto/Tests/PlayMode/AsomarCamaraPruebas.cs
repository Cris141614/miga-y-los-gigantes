using System.Collections;
using Miga.Juego;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace Miga.Pruebas
{
    public class AsomarCamaraPruebas
    {
        GameObject camara;

        [TearDown]
        public void Limpiar() => Object.Destroy(camara);

        static float Inclinacion(Transform t) => Mathf.DeltaAngle(0f, t.eulerAngles.x);   // negativa = mira hacia arriba

        [UnityTest]
        public IEnumerator SeAsomaHaciaArribaYVuelveAlSoltar()
        {
            camara = new GameObject("Camara");
            camara.transform.rotation = Quaternion.Euler(-6f, 0f, 0f);   // como Camara_Miga
            var asomar = camara.AddComponent<AsomarCamara>();
            asomar.usarControles = false;

            asomar.mirar = Vector2.up;
            yield return new WaitForSeconds(1f);
            Assert.That(Inclinacion(camara.transform), Is.EqualTo(-6f - asomar.arribaAbajo).Within(1f));

            asomar.mirar = Vector2.zero;
            yield return new WaitForSeconds(1.5f);
            Assert.That(Inclinacion(camara.transform), Is.EqualTo(-6f).Within(0.5f));
        }
    }
}
