"""
model/nodo.py
-------------
Pieza mínima de la lista enlazada: guarda un dato (en este proyecto,
un objeto Estudiante) y una referencia al siguiente nodo.
"""


class Nodo:
    def __init__(self, valor):
        self.valor = valor        # aquí va el objeto Estudiante
        self.siguiente = None     # apuntador al siguiente nodo
