using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using NUnit.Framework;
using UnityEditor;
using UnityEngine;

namespace Miga.Pruebas
{
    // Lo que docs/Produccion/Arte/Estandares de arte.md pide y se puede medir sin mirar el modelo.
    // Si un asset no cumple, el PR sale en rojo antes de llegar a develop.
    public class EstandaresDeArtePruebas
    {
        const string Arte = "Assets/_Proyecto/Art/";
        const int LimitePorDefecto = 15000; // objeto grande o pieza de escenario
        const int TexturaMaxima = 4096;

        // Modelos con un limite distinto al de por defecto. Un Guardador nuevo se agrega aqui.
        static readonly Dictionary<string, int> Limites = new Dictionary<string, int>
        {
            { "mod_miga", 50000 },
            { "mod_costurera", 80000 },
        };

        [TestCase("Modelos", "mod_")]
        [TestCase("Texturas", "tex_")]
        [TestCase("Materiales", "mat_")]
        [TestCase("Animaciones", "anim_")]
        public void LosArchivosLlevanSuPrefijo(string carpeta, string prefijo)
        {
            var valido = new Regex("^" + prefijo + "[a-z0-9_-]+$");
            var malos = Archivos(carpeta).Select(r => Path.GetFileName(r))
                .Where(n => !valido.IsMatch(Path.GetFileNameWithoutExtension(n)))
                .ToList();
            Assert.That(malos, Is.Empty, $"En {carpeta} todo empieza con {prefijo}, en minusculas, sin tildes ni espacios");
        }

        [Test]
        public void LosModelosNoPasanSuLimiteDeTriangulos()
        {
            var pasados = new List<string>();
            foreach (var ruta in Archivos("Modelos", "t:Model"))
            {
                string nombre = Path.GetFileNameWithoutExtension(ruta);
                int limite = Limites.TryGetValue(nombre, out int l) ? l : LimitePorDefecto;
                int triangulos = Triangulos(ruta);
                if (triangulos > limite) pasados.Add($"{nombre}: {triangulos} de {limite}");
            }
            Assert.That(pasados, Is.Empty, "Triangulos por encima del limite de Estandares de arte");
        }

        [Test]
        public void LasTexturasNoPasanDe4096()
        {
            var grandes = new List<string>();
            foreach (var ruta in Archivos("Texturas", "t:Texture2D"))
            {
                if (!(AssetImporter.GetAtPath(ruta) is TextureImporter importador)) continue;
                importador.GetSourceTextureWidthAndHeight(out int ancho, out int alto);
                if (ancho > TexturaMaxima || alto > TexturaMaxima) grandes.Add($"{ruta}: {ancho}x{alto}");
            }
            Assert.That(grandes, Is.Empty, $"Ninguna textura pasa de {TexturaMaxima} px");
        }

        [Test]
        public void LosMapasDeNormalesSeImportanComoNormalMap()
        {
            var malos = Archivos("Texturas", "t:Texture2D")
                .Where(r => Path.GetFileNameWithoutExtension(r).EndsWith("_normal"))
                .Where(r => (AssetImporter.GetAtPath(r) as TextureImporter)?.textureType != TextureImporterType.NormalMap)
                .ToList();
            Assert.That(malos, Is.Empty, "Poner Texture Type = Normal map en el import");
        }

        // Archivos (no carpetas) dentro de Art/<carpeta> y sus subcarpetas.
        static List<string> Archivos(string carpeta, string filtro = "")
        {
            return AssetDatabase.FindAssets(filtro, new[] { Arte + carpeta })
                .Select(guid => AssetDatabase.GUIDToAssetPath(guid))
                .Where(ruta => !AssetDatabase.IsValidFolder(ruta))
                .Distinct()
                .ToList();
        }

        // Suma de todas las mallas del FBX. GetIndexCount no necesita Read/Write activo.
        static int Triangulos(string ruta)
        {
            int indices = 0;
            foreach (var malla in AssetDatabase.LoadAllAssetsAtPath(ruta).OfType<Mesh>())
                for (int i = 0; i < malla.subMeshCount; i++)
                    indices += (int)malla.GetIndexCount(i);
            return indices / 3;
        }
    }
}
