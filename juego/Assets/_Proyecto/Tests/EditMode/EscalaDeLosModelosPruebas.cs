using Miga.Juego;
using NUnit.Framework;
using UnityEditor;
using UnityEngine;

namespace Miga.Pruebas
{
    // Los personajes tienen que llegar a Unity con la escala del Pipeline y los pies en el origen.
    // Si un FBX se exporta con otra escala, esta prueba falla antes de que se note en el nivel.
    public class EscalaDeLosModelosPruebas
    {
        const string Carpeta = "Assets/_Proyecto/Art/Modelos/";

        [TestCase("mod_miga.fbx", Escala.AlturaMiga, Escala.AlturaMiga * 1.15f)]               // 1.05 con los mechones
        [TestCase("mod_costurera.fbx", Escala.AlturaCosturera, Escala.AlturaCosturera * 1.09f)] // 17.75 con los alfileres
        public void ElModeloMideLoQueDiceElPipeline(string archivo, float alto, float maximo)
        {
            var modelo = AssetDatabase.LoadAssetAtPath<GameObject>(Carpeta + archivo);
            Assert.That(modelo, Is.Not.Null, "No se encontro " + Carpeta + archivo);

            var copia = Object.Instantiate(modelo);
            try
            {
                MedirAlto(copia, out float piso, out float arriba);
                Assert.That(piso, Is.EqualTo(0f).Within(alto * 0.03f), "Los pies tienen que quedar en el origen");
                Assert.That(arriba - piso, Is.InRange(alto * 0.95f, maximo), "Alto del modelo");
            }
            finally
            {
                Object.DestroyImmediate(copia);
            }
        }

        // Altura mas baja y mas alta de todas las mallas, en su pose y con todas sus transformaciones.
        static void MedirAlto(GameObject raiz, out float piso, out float arriba)
        {
            var mallas = raiz.GetComponentsInChildren<SkinnedMeshRenderer>();
            Assert.That(mallas, Is.Not.Empty, "El modelo no tiene mallas con esqueleto");

            piso = float.MaxValue;
            arriba = float.MinValue;
            var horneada = new Mesh();
            foreach (var malla in mallas)
            {
                malla.BakeMesh(horneada, true);
                var aMundo = malla.transform.localToWorldMatrix;
                foreach (var v in horneada.vertices)
                {
                    float y = aMundo.MultiplyPoint3x4(v).y;
                    piso = Mathf.Min(piso, y);
                    arriba = Mathf.Max(arriba, y);
                }
            }
            Object.DestroyImmediate(horneada);
        }
    }
}
