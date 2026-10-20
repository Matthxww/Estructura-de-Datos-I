"""
model/estudiante.py
--------------------
Representa el dato que guarda cada nodo de la lista: un estudiante
con su ID, nombre, apellido y sus calificaciones.

Esta clase NO es la lista enlazada en sí -- es solo el "contenido"
que viaja dentro de cada Nodo (nodo.valor = Estudiante(...)).
"""


class Estudiante:
    def __init__(self, id_estudiante, nombre, apellido, calificaciones=None):
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.calificaciones = list(calificaciones) if calificaciones else []

    def agregar_calificacion(self, nota):
        self.calificaciones.append(nota)

    def promedio(self):
        if not self.calificaciones:
            return None
        return sum(self.calificaciones) / len(self.calificaciones)

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def __str__(self):
        notas = ", ".join(str(n) for n in self.calificaciones) if self.calificaciones else "sin notas"
        prom = self.promedio()
        prom_txt = f"{prom:.2f}" if prom is not None else "—"
        return f"[{self.id}] {self.nombre_completo()} | notas: {notas} | promedio: {prom_txt}"
