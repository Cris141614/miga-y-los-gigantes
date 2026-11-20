using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace Miga.Pruebas
{
    // Prueba de ejemplo en Play Mode: la fisica del proyecto deja un objeto apoyado en el piso.
    // Las pruebas del movimiento de Miga (#7) van en esta misma carpeta.
    public class FisicaPruebas
    {
        GameObject piso, caja;

        [TearDown]
        public void Limpiar()
        {
            Object.Destroy(piso);
            Object.Destroy(caja);
        }

        [UnityTest]
        public IEnumerator UnaCajaCaeYQuedaSobreElPiso()
        {
            piso = GameObject.CreatePrimitive(PrimitiveType.Cube);
            piso.transform.localScale = new Vector3(10f, 1f, 10f);       // su cara de arriba queda en y = 0.5
            caja = GameObject.CreatePrimitive(PrimitiveType.Cube);
            caja.transform.position = new Vector3(0f, 3f, 0f);
            caja.AddComponent<Rigidbody>();

            yield return new WaitForSeconds(2f);

            Assert.That(caja.transform.position.y, Is.EqualTo(1f).Within(0.05f));   // piso (0.5) + media caja (0.5)
        }
    }
}
