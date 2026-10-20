"""
main.py
-------
Punto de entrada. Une la Vista (Tkinter) con el Controlador.

Ejecutar con:
    python main.py
"""

from view.vista import VistaEstudiantes
from controller.controlador import ControladorEstudiantes


def main():
    vista = VistaEstudiantes()
    ControladorEstudiantes(vista)
    vista.mainloop()


if __name__ == "__main__":
    main()
