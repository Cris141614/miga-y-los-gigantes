using UnityEngine;
using UnityEngine.InputSystem;

namespace Miga.Juego
{
    /// <summary>
    /// Lee teclado y mando con el Input System y se lo pasa a ControlMiga.
    /// Los controles son los de la tabla del GDD (docs/Juego/GDD.md).
    /// </summary>
    [DefaultExecutionOrder(-10)]   // antes que ControlMiga, para que use la entrada de este mismo frame
    [RequireComponent(typeof(ControlMiga))]
    public class EntradaMiga : MonoBehaviour
    {
        ControlMiga control;
        InputAction mover, correr, agachar, saltar;

        void Awake()
        {
            control = GetComponent<ControlMiga>();
            mover = new InputAction("Mover", InputActionType.Value);
            mover.AddCompositeBinding("2DVector")   // W y S: hacia el fondo y hacia la cámara
                .With("Up", "<Keyboard>/w").With("Down", "<Keyboard>/s")
                .With("Left", "<Keyboard>/a").With("Right", "<Keyboard>/d");
            mover.AddBinding("<Gamepad>/leftStick");
            correr = Boton("Correr", "<Keyboard>/leftShift", "<Gamepad>/rightTrigger");
            agachar = Boton("Agachar", "<Keyboard>/leftCtrl", "<Gamepad>/buttonEast");
            saltar = Boton("Saltar", "<Keyboard>/space", "<Gamepad>/buttonSouth");
        }

        static InputAction Boton(string nombre, string teclado, string mando)
        {
            var accion = new InputAction(nombre, InputActionType.Button, teclado);
            accion.AddBinding(mando);
            return accion;
        }

        void OnEnable()
        {
            mover.Enable();
            correr.Enable();
            agachar.Enable();
            saltar.Enable();
        }

        void OnDisable()
        {
            mover.Disable();
            correr.Disable();
            agachar.Disable();
            saltar.Disable();
        }

        void OnDestroy()
        {
            mover.Dispose();
            correr.Dispose();
            agachar.Dispose();
            saltar.Dispose();
        }

        void Update()
        {
            control.entrada = new ControlMiga.Entrada
            {
                mover = mover.ReadValue<Vector2>(),
                correr = correr.IsPressed(),
                agachar = agachar.IsPressed(),
            };
            if (saltar.WasPressedThisFrame())
                control.Saltar();
        }
    }
}
