"""
view/vista.py
-------------
VISTA (V de MVC)

Interfaz gráfica hecha con Tkinter. Solo se encarga de mostrar
elementos visuales y capturar la entrada del usuario. No sabe nada
de cómo se calculan los polinomios: eso lo hace el Controlador.
"""

import tkinter as tk
from tkinter import ttk


class VistaPolinomio(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ADT Polinomio - MVC")
        self.geometry("560x430")
        self.resizable(False, False)
        self.configure(bg="#0f1117")

        self._crear_widgets()

    # ------------------------------------------------------------------
    def _crear_widgets(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TLabel", background="#0f1117", foreground="white", font=("Segoe UI", 10))
        estilo.configure("TButton", font=("Segoe UI", 9))
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 14, "bold"))

        contenedor = ttk.Frame(self, padding=15)
        contenedor.configure(style="TFrame")
        contenedor.pack(fill="both", expand=True)

        ttk.Label(contenedor, text="Operaciones del ADT Polinomio", style="Titulo.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 15)
        )

        # ---------- Entradas de polinomios ----------
        ttk.Label(contenedor, text="P(x):").grid(row=1, column=0, sticky="w")
        self.entrada_p = ttk.Entry(contenedor, width=35)
        self.entrada_p.grid(row=1, column=1, columnspan=2, sticky="w", pady=4)
        self.entrada_p.insert(0, "3x^2 + 2x - 5")

        ttk.Label(contenedor, text="Q(x):").grid(row=2, column=0, sticky="w")
        self.entrada_q = ttk.Entry(contenedor, width=35)
        self.entrada_q.grid(row=2, column=1, columnspan=2, sticky="w", pady=4)
        self.entrada_q.insert(0, "x^2 - 4")

        ttk.Label(contenedor, text="Valor de x:").grid(row=3, column=0, sticky="w")
        self.entrada_x = ttk.Entry(contenedor, width=10)
        self.entrada_x.grid(row=3, column=1, sticky="w", pady=4)
        self.entrada_x.insert(0, "2")

        ttk.Label(contenedor, text="Formato: 3x^2 + 2x - 5   (usa ^ para el exponente)",
                  font=("Segoe UI", 8, "italic")).grid(row=4, column=0, columnspan=3, sticky="w", pady=(0, 10))

        # ---------- Botones de operaciones ----------
        botones_frame = ttk.Frame(contenedor)
        botones_frame.grid(row=5, column=0, columnspan=3, sticky="w", pady=10)

        self.btn_evaluar_p = ttk.Button(botones_frame, text="Evaluar P(x)")
        self.btn_evaluar_q = ttk.Button(botones_frame, text="Evaluar Q(x)")
        self.btn_sumar = ttk.Button(botones_frame, text="P(x) + Q(x)")
        self.btn_restar = ttk.Button(botones_frame, text="P(x) - Q(x)")
        self.btn_multiplicar = ttk.Button(botones_frame, text="P(x) * Q(x)")
        self.btn_grado_p = ttk.Button(botones_frame, text="Grado P(x)")
        self.btn_grado_q = ttk.Button(botones_frame, text="Grado Q(x)")
        self.btn_derivar_p = ttk.Button(botones_frame, text="Derivar P(x)")
        self.btn_derivar_q = ttk.Button(botones_frame, text="Derivar Q(x)")

        botones = [
            self.btn_evaluar_p, self.btn_evaluar_q, self.btn_sumar,
            self.btn_restar, self.btn_multiplicar, self.btn_grado_p,
            self.btn_grado_q, self.btn_derivar_p, self.btn_derivar_q,
        ]
        for i, boton in enumerate(botones):
            fila, columna = divmod(i, 3)
            boton.grid(row=fila, column=columna, padx=4, pady=4, sticky="ew")

        # ---------- Label de resultado ----------
        ttk.Label(contenedor, text="Resultado:", font=("Segoe UI", 10, "bold")).grid(
            row=6, column=0, columnspan=3, sticky="w", pady=(15, 2)
        )

        self.label_resultado = tk.Label(
            contenedor,
            text="Aquí aparecerá el resultado...",
            bg="#1b1e29",
            fg="#7cf29c",
            font=("Consolas", 12),
            wraplength=500,
            justify="left",
            anchor="w",
            padx=10,
            pady=10,
        )
        self.label_resultado.grid(row=7, column=0, columnspan=3, sticky="ew")

    # ------------------------------------------------------------------
    # Métodos que usará el Controlador
    # ------------------------------------------------------------------
    def obtener_texto_p(self):
        return self.entrada_p.get()

    def obtener_texto_q(self):
        return self.entrada_q.get()

    def obtener_valor_x(self):
        return self.entrada_x.get()

    def mostrar_resultado(self, texto):
        self.label_resultado.config(text=texto, fg="#7cf29c")

    def mostrar_error(self, texto):
        self.label_resultado.config(text=f"⚠ {texto}", fg="#ff6b6b")

    def asignar_comandos(self, controlador):
        """El controlador se conecta aquí a cada botón."""
        self.btn_evaluar_p.config(command=controlador.evaluar_p)
        self.btn_evaluar_q.config(command=controlador.evaluar_q)
        self.btn_sumar.config(command=controlador.sumar)
        self.btn_restar.config(command=controlador.restar)
        self.btn_multiplicar.config(command=controlador.multiplicar)
        self.btn_grado_p.config(command=controlador.grado_p)
        self.btn_grado_q.config(command=controlador.grado_q)
        self.btn_derivar_p.config(command=controlador.derivar_p)
        self.btn_derivar_q.config(command=controlador.derivar_q)
