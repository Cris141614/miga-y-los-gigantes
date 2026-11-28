using UnityEngine;

namespace Miga.Juego
{
    /// <summary>
    /// Mientras este componente está activo, la máquina está encendida y tapa los ruidos bajos y medios.
    /// Para apagarla, se desactiva el componente (lo hará La Costurera al dejar de coser).
    /// </summary>
    public class MaquinaDeCoser : MonoBehaviour
    {
        void OnEnable() => Ruido.Maquina(true);
        void OnDisable() => Ruido.Maquina(false);
    }
}
