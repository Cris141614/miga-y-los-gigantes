using UnityEngine;
using UnityEngine.InputSystem;

namespace Miga.Juego
{
    /// <summary>
    /// Deja asomar la cámara hacia donde se empuja el joystick derecho o las flechas, y al soltar vuelve sola.
    /// Solo se asoma, no gira libre: así no se rompe el encuadre de lado. Va en la cámara que sigue a Miga.
    /// </summary>
    public class AsomarCamara : MonoBehaviour
    {
        [Tooltip("Grados que sube o baja al asomarse")]
        public float arribaAbajo = 18f;
        [Tooltip("Grados que gira hacia los lados")]
        public float lados = 12f;
        [Tooltip("Qué tan rápido se asoma y vuelve")]
        public float rapidez = 4f;
        [Tooltip("Apagado, usa 'mirar' en vez del control (para pruebas)")]
        public bool usarControles = true;
        public Vector2 mirar;

        Quaternion inicial;
        Vector2 actual;
        InputAction accion;

        void Awake()
        {
            inicial = transform.rotation;
            accion = new InputAction("Mirar", InputActionType.Value);
            accion.AddCompositeBinding("2DVector")
                .With("Up", "<Keyboard>/upArrow").With("Down", "<Keyboard>/downArrow")
                .With("Left", "<Keyboard>/leftArrow").With("Right", "<Keyboard>/rightArrow");
            accion.AddBinding("<Gamepad>/rightStick");
        }

        void OnEnable() => accion.Enable();
        void OnDisable() => accion.Disable();
        void OnDestroy() => accion.Dispose();

        void Update()
        {
            var objetivo = Vector2.ClampMagnitude(usarControles ? accion.ReadValue<Vector2>() : mirar, 1f);
            actual = Vector2.Lerp(actual, objetivo, 1f - Mathf.Exp(-rapidez * Time.deltaTime));
            transform.rotation = inicial * Quaternion.Euler(-actual.y * arribaAbajo, actual.x * lados, 0f);
        }
    }
}
