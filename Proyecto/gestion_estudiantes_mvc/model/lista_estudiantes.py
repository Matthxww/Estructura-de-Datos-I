"""
model/lista_estudiantes.py
---------------------------
MODELO (M de MVC)

ADT "Sistema de Gestión de Estudiantes": una LISTA ENLAZADA SIMPLE,
construida desde cero con Nodo (sin usar list/dict de Python para la
lógica interna), que se mantiene SIEMPRE ORDENADA POR ID al insertar.

    self.cabeza -> apunta al primer nodo (el de menor ID)

No sabe nada de interfaces gráficas: solo maneja los nodos y la
lógica de negocio de inscribir/dar de baja/consultar estudiantes.
"""

from model.nodo import Nodo


class ListaEstudiantes:
    def __init__(self):
        self.cabeza = None
        self._tamano = 0

    # ------------------------------------------------------------------
    def esta_vacia(self):
        return self.cabeza is None

    def obtener_id_cabeza(self):
        """Retorna el ID del estudiante que es la CABEZA real de la lista
        enlazada (el primer nodo), o None si está vacía. Sirve para que
        la vista resalte al nodo correcto aunque el reporte se muestre
        en otro orden (por promedio o apellido)."""
        return self.cabeza.valor.id if self.cabeza is not None else None

    def tamano(self):
        return self._tamano

    # ------------------------------------------------------------------
    def buscar(self, id_estudiante):
        """Retorna el objeto Estudiante con ese ID, o None si no existe."""
        actual = self.cabeza
        while actual is not None:
            if actual.valor.id == id_estudiante:
                return actual.valor
            actual = actual.siguiente
        return None

    # ------------------------------------------------------------------
    def inscribir(self, estudiante):
        """Inserta un nuevo estudiante MANTENIENDO LA LISTA ORDENADA POR ID.
        Recorre la lista buscando el punto exacto donde insertar."""
        if self.buscar(estudiante.id) is not None:
            raise ValueError(f"Ya existe un estudiante con ID {estudiante.id}.")

        nuevo_nodo = Nodo(estudiante)

        if self.esta_vacia() or estudiante.id < self.cabeza.valor.id:
            # Va al principio (es el nuevo ID más pequeño)
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo
        else:
            # Recorre hasta encontrar el nodo justo antes de donde debe ir
            actual = self.cabeza
            while actual.siguiente is not None and actual.siguiente.valor.id < estudiante.id:
                actual = actual.siguiente
            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo

        self._tamano += 1

    def dar_de_baja(self, id_estudiante):
        """Elimina y retorna el estudiante con ese ID."""
        if self.esta_vacia():
            raise ValueError("No hay estudiantes inscritos.")

        if self.cabeza.valor.id == id_estudiante:
            eliminado = self.cabeza.valor
            self.cabeza = self.cabeza.siguiente
            self._tamano -= 1
            return eliminado

        anterior = self.cabeza
        actual = self.cabeza.siguiente
        while actual is not None:
            if actual.valor.id == id_estudiante:
                anterior.siguiente = actual.siguiente
                self._tamano -= 1
                return actual.valor
            anterior = actual
            actual = actual.siguiente

        raise ValueError(f"No existe un estudiante con ID {id_estudiante}.")

    def actualizar_calificaciones(self, id_estudiante, nota):
        """Agrega una nueva calificación al estudiante con ese ID."""
        estudiante = self.buscar(id_estudiante)
        if estudiante is None:
            raise ValueError(f"No existe un estudiante con ID {id_estudiante}.")
        estudiante.agregar_calificacion(nota)
        return estudiante

    def calcular_promedio(self, id_estudiante):
        """Retorna el promedio de calificaciones del estudiante con ese ID."""
        estudiante = self.buscar(id_estudiante)
        if estudiante is None:
            raise ValueError(f"No existe un estudiante con ID {id_estudiante}.")
        promedio = estudiante.promedio()
        if promedio is None:
            raise ValueError(f"El estudiante {estudiante.nombre_completo()} todavía no tiene calificaciones.")
        return promedio

    def generar_reporte(self):
        """Retorna una lista de Python con todos los objetos Estudiante,
        en orden (solo para MOSTRARLOS en la vista; la lógica interna
        siempre funciona recorriendo los nodos)."""
        resultado = []
        actual = self.cabeza
        while actual is not None:
            resultado.append(actual.valor)
            actual = actual.siguiente
        return resultado

    # ------------------------------------------------------------------
    # Operaciones adicionales
    # ------------------------------------------------------------------
    def editar_estudiante(self, id_estudiante, nuevo_nombre=None, nuevo_apellido=None):
        """Modifica el nombre y/o apellido de un estudiante ya inscrito.
        NO cambia su posición en la lista: el orden sigue siendo por ID,
        y el ID nunca cambia, así que el nodo se queda donde estaba."""
        estudiante = self.buscar(id_estudiante)
        if estudiante is None:
            raise ValueError(f"No existe un estudiante con ID {id_estudiante}.")

        if nuevo_nombre:
            estudiante.nombre = nuevo_nombre
        if nuevo_apellido:
            estudiante.apellido = nuevo_apellido

        return estudiante

    def buscar_por_nombre(self, texto):
        """Retorna una lista con todos los estudiantes cuyo nombre o
        apellido contiene 'texto' (sin importar mayúsculas/minúsculas).
        Recorre nodo por nodo, igual que buscar() por ID."""
        texto = texto.strip().lower()
        coincidencias = []
        actual = self.cabeza
        while actual is not None:
            est = actual.valor
            if texto in est.nombre.lower() or texto in est.apellido.lower():
                coincidencias.append(est)
            actual = actual.siguiente
        return coincidencias

    def obtener_mejor_y_peor_promedio(self):
        """Retorna una tupla (mejor, peor) con los objetos Estudiante que
        tienen el promedio más alto y más bajo. Ignora a quienes no
        tienen calificaciones todavía. Lanza ValueError si nadie califica."""
        mejor = None
        peor = None

        actual = self.cabeza
        while actual is not None:
            est = actual.valor
            prom = est.promedio()
            if prom is not None:
                if mejor is None or prom > mejor.promedio():
                    mejor = est
                if peor is None or prom < peor.promedio():
                    peor = est
            actual = actual.siguiente

        if mejor is None:
            raise ValueError("Ningún estudiante tiene calificaciones todavía.")

        return mejor, peor

    def generar_reporte_ordenado(self, criterio="id"):
        """Retorna una copia (lista de Python) de los estudiantes,
        ordenada según 'criterio': 'id' (orden natural de la lista
        enlazada), 'apellido' (alfabético) o 'promedio' (de mayor a
        menor). IMPORTANTE: esto NO reordena los nodos de la lista
        enlazada real -- la lista enlazada se mantiene siempre
        ordenada por ID internamente. Esto es solo una vista/copia
        ordenada distinta, para fines de reporte."""
        estudiantes = self.generar_reporte()

        if criterio == "apellido":
            return sorted(estudiantes, key=lambda e: e.apellido.lower())
        elif criterio == "promedio":
            # Los que no tienen promedio (None) van al final
            return sorted(
                estudiantes,
                key=lambda e: (e.promedio() is None, -(e.promedio() or 0))
            )
        else:
            return estudiantes  # "id": el orden natural, ya viene ordenado

    def vaciar(self):
        self.cabeza = None
        self._tamano = 0

    def __str__(self):
        estudiantes = self.generar_reporte()
        if not estudiantes:
            return "(no hay estudiantes inscritos)"
        return "\n".join(str(e) for e in estudiantes)
