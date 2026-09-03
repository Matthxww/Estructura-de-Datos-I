"""
main.py
-------
Punto de entrada de la aplicación. Une la Vista con el Controlador
siguiendo el patrón MVC.

Ejecutar con:
    python main.py
"""

from view.vista import VistaPolinomio
from controller.controlador import ControladorPolinomio


def main():
    vista = VistaPolinomio()
    ControladorPolinomio(vista)
    vista.mainloop()


if __name__ == "__main__":
    main()
