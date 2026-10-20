"""
view/vista.py
-------------
VISTA (V de MVC)

Interfaz gráfica en Tkinter. Panel izquierdo: formulario de acciones.
Panel derecho: lista de estudiantes dibujada como TARJETAS conectadas
(cada una representa un nodo), con scroll, resaltando la CABEZA, y
con un campo de filtro que reduce las tarjetas visibles en vivo
mientras se escribe (sin tocar la lista real: es solo visual).

No sabe nada de cómo funciona la lista por dentro: solo pide datos
al Controlador y dibuja lo que le pasan.
"""

import tkinter as tk
from tkinter import ttk

# ---------------------------------------------------------------------
# Paleta de colores - tema "campus / tech" moderno
# ---------------------------------------------------------------------
FONDO = "#0f1b2d"
PANEL = "#16233a"
TARJETA = "#1c2a44"
TARJETA_CABEZA = "#203457"
BORDE = "#28374f"
BORDE_CABEZA = "#2dd4bf"
INDIGO = "#6366f1"
INDIGO_HOVER = "#7b7ff5"
TEAL = "#2dd4bf"
TEXTO = "#e8edf5"
TEXTO_SUAVE = "#94a3b8"
OK = "#34d399"
ERROR = "#f87171"
BADGE_ID_BG = "#0f1b2d"


class VistaEstudiantes(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Estudiantes — Lista Enlazada (MVC)")
        self.geometry("1180x720")
        self.configure(bg=FONDO)
        self.minsize(1040, 640)

        self._crear_estilos()
        self._crear_widgets()

    # ------------------------------------------------------------------
    def _crear_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure("TFrame", background=FONDO)
        estilo.configure("Panel.TFrame", background=PANEL)
        estilo.configure("TLabel", background=FONDO, foreground=TEXTO, font=("Segoe UI", 10))
        estilo.configure("Panel.TLabel", background=PANEL, foreground=TEXTO, font=("Segoe UI", 10))
        estilo.configure("Titulo.TLabel", background=FONDO, foreground=TEXTO, font=("Segoe UI", 20, "bold"))
        estilo.configure("Subtitulo.TLabel", background=FONDO, foreground=TEXTO_SUAVE, font=("Segoe UI", 10))
        estilo.configure("Seccion.TLabel", background=PANEL, foreground=TEAL, font=("Segoe UI", 11, "bold"))

        estilo.configure(
            "Accion.TButton",
            background=INDIGO, foreground="white",
            font=("Segoe UI", 9, "bold"), padding=8, borderwidth=0,
        )
        estilo.map("Accion.TButton", background=[("active", INDIGO_HOVER)])

        estilo.configure(
            "Peligro.TButton",
            background="#3d1010", foreground="#ff9b9b",
            font=("Segoe UI", 9, "bold"), padding=8, borderwidth=0,
        )
        estilo.map("Peligro.TButton", background=[("active", "#551616")])

    # ------------------------------------------------------------------
    def _crear_widgets(self):
        raiz = ttk.Frame(self, padding=18)
        raiz.pack(fill="both", expand=True)

        # ---------- Encabezado ----------
        ttk.Label(raiz, text="🎓  Gestión de Estudiantes", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(
            raiz, text="Lista enlazada simple, ordenada automáticamente por ID",
            style="Subtitulo.TLabel"
        ).pack(anchor="w", pady=(0, 14))

        cuerpo = ttk.Frame(raiz)
        cuerpo.pack(fill="both", expand=True)
        cuerpo.columnconfigure(0, weight=0, minsize=330)
        cuerpo.columnconfigure(1, weight=1)
        cuerpo.rowconfigure(0, weight=1)

        self._crear_panel_formulario(cuerpo)
        self._crear_panel_lista(cuerpo)

        # ---------- Mensaje de resultado ----------
        self.label_mensaje = tk.Label(
            raiz, text="Inscribe tu primer estudiante para comenzar.",
            bg=PANEL, fg=TEXTO_SUAVE, font=("Consolas", 11),
            anchor="w", justify="left", padx=14, pady=10, wraplength=1120,
        )
        self.label_mensaje.pack(fill="x", pady=(14, 0))

    # ------------------------------------------------------------------
    def _crear_panel_formulario(self, padre):
        panel = tk.Frame(padre, bg=PANEL, highlightbackground=BORDE, highlightthickness=1)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

        interior = tk.Frame(panel, bg=PANEL, padx=18, pady=18)
        interior.pack(fill="both", expand=True)

        def campo(label_texto):
            tk.Label(interior, text=label_texto, bg=PANEL, fg=TEXTO_SUAVE, font=("Segoe UI", 9)).pack(
                anchor="w", pady=(10, 2)
            )
            entrada = tk.Entry(
                interior, font=("Segoe UI", 11), bg="#0f1b2d", fg=TEXTO,
                insertbackground=TEXTO, relief="flat"
            )
            entrada.pack(fill="x", ipady=5)
            return entrada

        ttk.Label(interior, text="DATOS DEL ESTUDIANTE", style="Seccion.TLabel").pack(anchor="w")

        self.entrada_id = campo("ID (número único)")
        self.entrada_nombre = campo("Nombre")
        self.entrada_apellido = campo("Apellido")
        self.entrada_calificaciones = campo("Calificaciones iniciales (opcional, ej: 85, 90, 78)")

        self.btn_inscribir = ttk.Button(interior, text="➕  Inscribir estudiante", style="Accion.TButton")
        self.btn_inscribir.pack(fill="x", pady=(14, 4))

        ttk.Separator(interior).pack(fill="x", pady=14)
        ttk.Label(interior, text="OPERACIONES POR ID", style="Seccion.TLabel").pack(anchor="w")

        self.entrada_id_operacion = campo("ID del estudiante")
        self.entrada_nota = campo("Nueva calificación a agregar")

        self.btn_agregar_nota = ttk.Button(interior, text="📝  Agregar calificación", style="Accion.TButton")
        self.btn_agregar_nota.pack(fill="x", pady=(10, 4))

        self.btn_promedio = ttk.Button(interior, text="📊  Calcular promedio", style="Accion.TButton")
        self.btn_promedio.pack(fill="x", pady=4)

        self.btn_buscar = ttk.Button(interior, text="🔎  Buscar por ID", style="Accion.TButton")
        self.btn_buscar.pack(fill="x", pady=4)

        self.btn_dar_de_baja = ttk.Button(interior, text="🗑  Dar de baja", style="Peligro.TButton")
        self.btn_dar_de_baja.pack(fill="x", pady=4)

        ttk.Separator(interior).pack(fill="x", pady=14)
        ttk.Label(interior, text="EDITAR ESTUDIANTE (usa el ID de arriba)", style="Seccion.TLabel").pack(anchor="w")

        self.entrada_nuevo_nombre = campo("Nuevo nombre (opcional)")
        self.entrada_nuevo_apellido = campo("Nuevo apellido (opcional)")

        self.btn_editar = ttk.Button(interior, text="✏  Guardar cambios", style="Accion.TButton")
        self.btn_editar.pack(fill="x", pady=(10, 0))

        ttk.Separator(interior).pack(fill="x", pady=14)
        ttk.Label(interior, text="BÚSQUEDA Y ESTADÍSTICAS", style="Seccion.TLabel").pack(anchor="w")

        self.entrada_buscar_nombre = campo("Nombre o apellido a buscar")

        self.btn_buscar_nombre = ttk.Button(interior, text="🔎  Buscar por nombre", style="Accion.TButton")
        self.btn_buscar_nombre.pack(fill="x", pady=(10, 4))

        self.btn_mejor_peor = ttk.Button(interior, text="🏆  Mejor y peor promedio", style="Accion.TButton")
        self.btn_mejor_peor.pack(fill="x", pady=4)

        ttk.Separator(interior).pack(fill="x", pady=14)

        self.btn_reporte = ttk.Button(interior, text="📋  Generar reporte completo", style="Accion.TButton")
        self.btn_reporte.pack(fill="x", pady=4)

        self.btn_vaciar = ttk.Button(interior, text="🧹  Vaciar lista completa", style="Peligro.TButton")
        self.btn_vaciar.pack(fill="x", pady=(4, 0))

    # ------------------------------------------------------------------
    def _crear_panel_lista(self, padre):
        panel = tk.Frame(padre, bg=PANEL, highlightbackground=BORDE, highlightthickness=1)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.rowconfigure(2, weight=1)
        panel.columnconfigure(0, weight=1)

        encabezado = tk.Frame(panel, bg=PANEL, padx=18, pady=16)
        encabezado.grid(row=0, column=0, sticky="ew")

        ttk.Label(encabezado, text="LISTA ENLAZADA DE ESTUDIANTES", style="Seccion.TLabel").pack(anchor="w")

        fila_filtro = tk.Frame(encabezado, bg=PANEL)
        fila_filtro.pack(fill="x", pady=(10, 0))

        tk.Label(fila_filtro, text="🔍", bg=PANEL, fg=TEXTO_SUAVE, font=("Segoe UI", 11)).pack(side="left")
        self.entrada_filtro = tk.Entry(
            fila_filtro, font=("Segoe UI", 10), bg="#0f1b2d", fg=TEXTO,
            insertbackground=TEXTO, relief="flat"
        )
        self.entrada_filtro.pack(side="left", fill="x", expand=True, ipady=5, padx=(8, 10))
        self.entrada_filtro.insert(0, "")

        self.label_contador = tk.Label(
            fila_filtro, text="0 estudiantes", bg=PANEL, fg=TEAL, font=("Segoe UI", 9, "bold")
        )
        self.label_contador.pack(side="right")

        fila_orden = tk.Frame(encabezado, bg=PANEL)
        fila_orden.pack(fill="x", pady=(10, 0))
        tk.Label(fila_orden, text="Ordenar vista por:", bg=PANEL, fg=TEXTO_SUAVE, font=("Segoe UI", 9)).pack(
            side="left", padx=(0, 8)
        )

        self.criterio_orden = tk.StringVar(value="id")
        estilo_radio = ttk.Style(self)
        estilo_radio.configure("Orden.TRadiobutton", background=PANEL, foreground=TEXTO, font=("Segoe UI", 9))
        estilo_radio.map("Orden.TRadiobutton", background=[("active", PANEL)])

        self._callback_orden = None

        for valor, texto in [("id", "ID"), ("apellido", "Apellido (A-Z)"), ("promedio", "Promedio (mayor a menor)")]:
            ttk.Radiobutton(
                fila_orden, text=texto, value=valor, variable=self.criterio_orden,
                style="Orden.TRadiobutton",
                command=lambda: self._callback_orden() if self._callback_orden else None,
            ).pack(side="left", padx=(0, 12))

        ttk.Separator(panel).grid(row=1, column=0, sticky="ew")

        # ---------- Área scrollable con las tarjetas ----------
        area = tk.Frame(panel, bg=PANEL)
        area.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        area.rowconfigure(0, weight=1)
        area.columnconfigure(0, weight=1)

        self.canvas_scroll = tk.Canvas(area, bg=PANEL, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(area, orient="vertical", command=self.canvas_scroll.yview)
        self.canvas_scroll.configure(yscrollcommand=self.scrollbar.set)

        self.canvas_scroll.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.frame_tarjetas = tk.Frame(self.canvas_scroll, bg=PANEL)
        self._ventana_id = self.canvas_scroll.create_window((0, 0), window=self.frame_tarjetas, anchor="nw")

        self.frame_tarjetas.bind(
            "<Configure>",
            lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all")),
        )
        self.canvas_scroll.bind(
            "<Configure>",
            lambda e: self.canvas_scroll.itemconfig(self._ventana_id, width=e.width),
        )

        def _rueda(event):
            self.canvas_scroll.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.canvas_scroll.bind("<Enter>", lambda e: self.canvas_scroll.bind_all("<MouseWheel>", _rueda))
        self.canvas_scroll.bind("<Leave>", lambda e: self.canvas_scroll.unbind_all("<MouseWheel>"))

        self._todos_los_estudiantes = []   # cache para poder filtrar sin volver a pedirle al controlador
        self._id_cabeza = None

    # ------------------------------------------------------------------
    # Métodos que usará el Controlador
    # ------------------------------------------------------------------
    def obtener_id(self):
        return self.entrada_id.get()

    def obtener_id_operacion(self):
        return self.entrada_id_operacion.get()

    def obtener_nombre(self):
        return self.entrada_nombre.get()

    def obtener_apellido(self):
        return self.entrada_apellido.get()

    def obtener_calificaciones_iniciales(self):
        return self.entrada_calificaciones.get()

    def obtener_nota(self):
        return self.entrada_nota.get()

    def obtener_nuevo_nombre(self):
        return self.entrada_nuevo_nombre.get()

    def obtener_nuevo_apellido(self):
        return self.entrada_nuevo_apellido.get()

    def obtener_texto_busqueda_nombre(self):
        return self.entrada_buscar_nombre.get()

    def obtener_criterio_orden(self):
        return self.criterio_orden.get()

    def limpiar_formulario_inscripcion(self):
        self.entrada_id.delete(0, tk.END)
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_apellido.delete(0, tk.END)
        self.entrada_calificaciones.delete(0, tk.END)
        self.entrada_id.focus()

    def limpiar_campo_id(self):
        self.entrada_id.delete(0, tk.END)

    def limpiar_campo_id_operacion(self):
        self.entrada_id_operacion.delete(0, tk.END)

    def limpiar_campo_nota(self):
        self.entrada_nota.delete(0, tk.END)

    def limpiar_campos_edicion(self):
        self.entrada_nuevo_nombre.delete(0, tk.END)
        self.entrada_nuevo_apellido.delete(0, tk.END)

    def limpiar_campo_busqueda_nombre(self):
        self.entrada_buscar_nombre.delete(0, tk.END)

    def mostrar_mensaje(self, texto):
        self.label_mensaje.config(text=texto, fg=OK)

    def mostrar_error(self, texto):
        self.label_mensaje.config(text=f"⚠ {texto}", fg=ERROR)

    def mostrar_info(self, texto):
        self.label_mensaje.config(text=texto, fg=TEAL)

    # ------------------------------------------------------------------
    def dibujar_estudiantes(self, estudiantes, id_cabeza=None):
        """Guarda la lista completa y la dibuja (aplicando el filtro activo).
        id_cabeza es el ID real del primer nodo de la lista enlazada --
        se usa para resaltar la tarjeta correcta aunque el orden visual
        (por promedio/apellido) sea distinto al orden real de los nodos."""
        self._todos_los_estudiantes = estudiantes
        self._id_cabeza = id_cabeza
        self.label_contador.config(text=f"{len(estudiantes)} estudiante{'s' if len(estudiantes) != 1 else ''}")
        self._redibujar_con_filtro()

    def _redibujar_con_filtro(self):
        texto_filtro = self.entrada_filtro.get().strip().lower()
        orden_natural = (self.criterio_orden.get() == "id")

        for widget in self.frame_tarjetas.winfo_children():
            widget.destroy()

        if not self._todos_los_estudiantes:
            tk.Label(
                self.frame_tarjetas, text="(no hay estudiantes inscritos)",
                bg=PANEL, fg=TEXTO_SUAVE, font=("Segoe UI", 11, "italic")
            ).pack(pady=30)
            return

        visibles = []
        for est in self._todos_los_estudiantes:
            coincide = (
                texto_filtro == ""
                or texto_filtro in est.nombre.lower()
                or texto_filtro in est.apellido.lower()
                or texto_filtro in str(est.id)
            )
            if coincide:
                visibles.append(est)

        if not visibles:
            tk.Label(
                self.frame_tarjetas, text="Ningún estudiante coincide con el filtro.",
                bg=PANEL, fg=TEXTO_SUAVE, font=("Segoe UI", 10, "italic")
            ).pack(pady=20)
            return

        for i, est in enumerate(visibles):
            es_cabeza = (est.id == self._id_cabeza)
            self._crear_tarjeta(est, es_cabeza)

            if orden_natural:
                # Las flechas solo representan la cadena REAL (.siguiente)
                # cuando se muestra en orden natural por ID.
                if i < len(visibles) - 1:
                    tk.Label(self.frame_tarjetas, text="↓", bg=PANEL, fg=TEXTO_SUAVE, font=("Segoe UI", 13)).pack()
                else:
                    tk.Label(self.frame_tarjetas, text="↓ None", bg=PANEL, fg=TEXTO_SUAVE,
                             font=("Segoe UI", 9, "italic")).pack(pady=(2, 0))

    def _crear_tarjeta(self, estudiante, es_cabeza):
        color_fondo = TARJETA_CABEZA if es_cabeza else TARJETA
        color_borde = BORDE_CABEZA if es_cabeza else BORDE

        tarjeta = tk.Frame(self.frame_tarjetas, bg=color_fondo, highlightbackground=color_borde,
                            highlightthickness=1.5)
        tarjeta.pack(fill="x", pady=4)

        interior = tk.Frame(tarjeta, bg=color_fondo, padx=14, pady=10)
        interior.pack(fill="x")
        interior.columnconfigure(1, weight=1)

        # Badge de ID
        badge = tk.Label(
            interior, text=f"ID {estudiante.id}", bg=TEAL if es_cabeza else INDIGO, fg="#0f1b2d" if es_cabeza else "white",
            font=("Segoe UI", 9, "bold"), padx=8, pady=3,
        )
        badge.grid(row=0, column=0, sticky="w", rowspan=2)

        if es_cabeza:
            tk.Label(interior, text="CABEZA  •", bg=color_fondo, fg=TEAL, font=("Segoe UI", 8, "bold")).grid(
                row=0, column=2, sticky="e"
            )

        tk.Label(
            interior, text=estudiante.nombre_completo(), bg=color_fondo, fg=TEXTO,
            font=("Segoe UI", 12, "bold"), anchor="w",
        ).grid(row=0, column=1, sticky="w", padx=(12, 0))

        notas_txt = ", ".join(str(n) for n in estudiante.calificaciones) if estudiante.calificaciones else "sin calificaciones"
        tk.Label(
            interior, text=f"Notas: {notas_txt}", bg=color_fondo, fg=TEXTO_SUAVE,
            font=("Segoe UI", 9), anchor="w",
        ).grid(row=1, column=1, sticky="w", padx=(12, 0))

        promedio = estudiante.promedio()
        prom_txt = f"Prom: {promedio:.2f}" if promedio is not None else "Prom: —"
        tk.Label(
            interior, text=prom_txt, bg=color_fondo, fg=TEAL,
            font=("Segoe UI", 10, "bold"),
        ).grid(row=1, column=2, sticky="e")

    def asignar_filtro(self, callback):
        """Conecta la caja de búsqueda para que filtre en vivo mientras se escribe."""
        self.entrada_filtro.bind("<KeyRelease>", lambda e: callback())

    def asignar_comandos(self, controlador):
        self.btn_inscribir.config(command=controlador.inscribir)
        self.btn_dar_de_baja.config(command=controlador.dar_de_baja)
        self.btn_buscar.config(command=controlador.buscar)
        self.btn_agregar_nota.config(command=controlador.agregar_calificacion)
        self.btn_promedio.config(command=controlador.calcular_promedio)
        self.btn_editar.config(command=controlador.editar)
        self.btn_buscar_nombre.config(command=controlador.buscar_por_nombre)
        self.btn_mejor_peor.config(command=controlador.mejor_y_peor_promedio)
        self.btn_reporte.config(command=controlador.generar_reporte)
        self.btn_vaciar.config(command=controlador.vaciar)
        self.asignar_filtro(lambda: self._redibujar_con_filtro())
        self._callback_orden = controlador.cambiar_orden
