using System;
using UnityEngine;

namespace Miga.Juego
{
    public enum NivelRuido { Ninguno, Bajo, Medio, Alto }

    /// <summary>
    /// Los ruidos del nivel. Cualquiera los hace con Hacer; los Guardadores se suscriben a Sono y deciden, según la
    /// distancia, si lo oyeron. Ver la tabla de docs/Juego/Mecanicas.md.
    /// </summary>
    public static class Ruido
    {
        /// <summary>Se oyó un ruido: dónde y qué tan fuerte. Los que tapa la máquina de coser no se avisan.</summary>
        public static event Action<Vector3, NivelRuido> Sono;

        static int maquinasEncendidas;

        /// <summary>Hay una máquina de coser encendida: solo se oyen los ruidos altos.</summary>
        public static bool Tapado => maquinasEncendidas > 0;

        public static void Hacer(Vector3 donde, NivelRuido nivel)
        {
            if (nivel == NivelRuido.Ninguno || (Tapado && nivel < NivelRuido.Alto))
                return;
            Sono?.Invoke(donde, nivel);
        }

        // shortcut: la máquina tapa el ruido en todo el nivel, no solo cerca de ella; cambiarlo si un nivel tiene
        // zonas lejos de la máquina donde sí se deba oír.
        internal static void Maquina(bool encendida) => maquinasEncendidas += encendida ? 1 : -1;
    }
}
