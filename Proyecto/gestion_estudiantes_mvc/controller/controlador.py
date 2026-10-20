"""
controller/controlador.py
--------------------------
CONTROLADOR (C de MVC)

Recibe los clics de los botones de la Vista, construye/consulta
objetos Estudiante sobre el Modelo (ListaEstudiantes) y le devuelve
a la Vista lo que debe mostrar: mensajes, tarjetas y contador.
"""

from model.estudiante import Estudiante
from model.lista_estudiantes import ListaEstudiantes


class ControladorEstudiantes:
    def __init__(self, vista):
        self.lista = ListaEstudiantes()
        self.vista = vista
        self.criterio_orden = "id"
        self.vista.asignar_comandos(self)
        self._actualizar_vista()

    # ------------------------------------------------------------------
    # Helpers de validación
    # ------------------------------------------------------------------
    def _parsear_id(self, texto, nombre_campo="ID"):
        texto = texto.strip()
        if texto == "":
            raise ValueError(f"Ingresa el {nombre_campo}.")
        if not texto.isdigit():
            raise ValueError(f"El {nombre_campo} debe ser un número entero.")
        return int(texto)

    def _parsear_nota(self, texto):
        texto = texto.strip()
        if texto == "":
            raise ValueError("Ingresa una calificación.")
        try:
            return float(texto)
        except ValueError:
            raise ValueError("La calificación debe ser un número (ej: 85 o 7.5).")

    def _parsear_calificaciones_iniciales(self, texto):
        texto = texto.strip()
        if texto == "":
            return []
        notas = []
        for parte in texto.split(","):
            parte = parte.strip()
            if parte == "":
                continue
            try:
                notas.append(float(parte))
            except ValueError:
                raise ValueError(f"'{parte}' no es una calificación válida.")
        return notas

    # ------------------------------------------------------------------
    # Operaciones
    # ------------------------------------------------------------------
    def inscribir(self):
        try:
            id_estudiante = self._parsear_id(self.vista.obtener_id())
            nombre = self.vista.obtener_nombre().strip()
            apellido = self.vista.obtener_apellido().strip()

            if nombre == "" or apellido == "":
                raise ValueError("El nombre y el apellido no pueden estar vacíos.")

            calificaciones = self._parsear_calificaciones_iniciales(self.vista.obtener_calificaciones_iniciales())

            estudiante = Estudiante(id_estudiante, nombre, apellido, calificaciones)
            self.lista.inscribir(estudiante)

            self.vista.limpiar_formulario_inscripcion()
            self.vista.mostrar_mensaje(f"Estudiante inscrito: {estudiante.nombre_completo()} (ID {id_estudiante}).")
        except ValueError as e:
            self.vista.mostrar_error(str(e))

        self._actualizar_vista()

    def dar_de_baja(self):
        try:
            id_estudiante = self._parsear_id(self.vista.obtener_id_operacion())
            eliminado = self.lista.dar_de_baja(id_estudiante)
            self.vista.limpiar_campo_id_operacion()
            self.vista.mostrar_mensaje(f"Dado de baja: {eliminado.nombre_completo()} (ID {id_estudiante}).")
        except ValueError as e:
            self.vista.mostrar_error(str(e))

        self._actualizar_vista()

    def buscar(self):
        try:
            id_estudiante = self._parsear_id(self.vista.obtener_id_operacion())
            estudiante = self.lista.buscar(id_estudiante)
            if estudiante is None:
                self.vista.mostrar_error(f"No existe un estudiante con ID {id_estudiante}.")
            else:
                self.vista.mostrar_info(f"Encontrado → {estudiante}")
        except ValueError as e:
            self.vista.mostrar_error(str(e))

        self._actualizar_vista()

    def agregar_calificacion(self):
        try:
            id_estudiante = self._parsear_id(self.vista.obtener_id_operacion())
            nota = self._parsear_nota(self.vista.obtener_nota())
            estudiante = self.lista.actualizar_calificaciones(id_estudiante, nota)
            self.vista.limpiar_campo_nota()
            self.vista.mostrar_mensaje(f"Calificación {nota} agregada a {estudiante.nombre_completo()}.")
        except ValueError as e:
            self.vista.mostrar_error(str(e))

        self._actualizar_vista()

    def calcular_promedio(self):
        try:
            id_estudiante = self._parsear_id(self.vista.obtener_id_operacion())
            promedio = self.lista.calcular_promedio(id_estudiante)
            estudiante = self.lista.buscar(id_estudiante)
            self.vista.mostrar_info(f"Promedio de {estudiante.nombre_completo()}: {promedio:.2f}")
        except ValueError as e:
            self.vista.mostrar_error(str(e))

        self._actualizar_vista()

    def generar_reporte(self):
        estudiantes = self.lista.generar_reporte()
        if not estudiantes:
            self.vista.mostrar_error("No hay estudiantes inscritos para generar el reporte.")
        else:
            lineas = [str(e) for e in estudiantes]
            self.vista.mostrar_info("REPORTE COMPLETO:\n" + "\n".join(lineas))

        self._actualizar_vista()

    def vaciar(self):
        self.lista.vaciar()
        self.vista.mostrar_mensaje("La lista de estudiantes fue vaciada por completo.")
        self._actualizar_vista()

    def editar(self):
        try:
            id_estudiante = self._parsear_id(self.vista.obtener_id_operacion())
            nuevo_nombre = self.vista.obtener_nuevo_nombre().strip()
            nuevo_apellido = self.vista.obtener_nuevo_apellido().strip()

            if nuevo_nombre == "" and nuevo_apellido == "":
                raise ValueError("Escribe al menos un nuevo nombre o apellido para editar.")

            estudiante = self.lista.editar_estudiante(
                id_estudiante,
                nuevo_nombre=nuevo_nombre or None,
                nuevo_apellido=nuevo_apellido or None,
            )
            self.vista.limpiar_campos_edicion()
            self.vista.mostrar_mensaje(f"Datos actualizados: ahora es {estudiante.nombre_completo()} (ID {id_estudiante}).")
        except ValueError as e:
            self.vista.mostrar_error(str(e))

        self._actualizar_vista()

    def buscar_por_nombre(self):
        texto = self.vista.obtener_texto_busqueda_nombre().strip()
        if texto == "":
            self.vista.mostrar_error("Escribe un nombre o apellido para buscar.")
            return

        coincidencias = self.lista.buscar_por_nombre(texto)
        if not coincidencias:
            self.vista.mostrar_error(f"No se encontró ningún estudiante que coincida con '{texto}'.")
        else:
            lineas = [str(e) for e in coincidencias]
            self.vista.mostrar_info(f"{len(coincidencias)} coincidencia(s):\n" + "\n".join(lineas))

        self._actualizar_vista()

    def mejor_y_peor_promedio(self):
        try:
            mejor, peor = self.lista.obtener_mejor_y_peor_promedio()
            if mejor is peor:
                self.vista.mostrar_info(
                    f"Solo hay un estudiante con calificaciones: {mejor.nombre_completo()} "
                    f"(promedio {mejor.promedio():.2f})."
                )
            else:
                self.vista.mostrar_info(
                    f"🏆 Mejor promedio: {mejor.nombre_completo()} ({mejor.promedio():.2f})  |  "
                    f"📉 Peor promedio: {peor.nombre_completo()} ({peor.promedio():.2f})"
                )
        except ValueError as e:
            self.vista.mostrar_error(str(e))

        self._actualizar_vista()

    def cambiar_orden(self):
        """Se llama cuando el usuario elige un criterio de orden distinto
        en la Vista (radiobuttons). Solo cambia cómo se MUESTRAN las
        tarjetas -- la lista enlazada interna sigue ordenada por ID."""
        self.criterio_orden = self.vista.obtener_criterio_orden()
        self._actualizar_vista()

    # ------------------------------------------------------------------
    def _actualizar_vista(self):
        estudiantes = self.lista.generar_reporte_ordenado(self.criterio_orden)
        id_cabeza = self.lista.obtener_id_cabeza()
        self.vista.dibujar_estudiantes(estudiantes, id_cabeza)
