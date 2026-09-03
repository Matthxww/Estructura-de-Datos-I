"""
controller/controlador.py
--------------------------
CONTROLADOR (C de MVC)

Recibe eventos de la Vista (clics de botones), le pide los datos
de entrada, construye objetos Polinomio (Modelo), ejecuta la
operación pedida y devuelve el resultado a la Vista para que
lo muestre en el label.
"""

from model.polinomio import Polinomio


class ControladorPolinomio:
    def __init__(self, vista):
        self.vista = vista
        self.vista.asignar_comandos(self)

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------
    def _obtener_p(self):
        return Polinomio.desde_cadena(self.vista.obtener_texto_p())

    def _obtener_q(self):
        return Polinomio.desde_cadena(self.vista.obtener_texto_q())

    def _obtener_x(self):
        texto = self.vista.obtener_valor_x().strip()
        if texto == "":
            raise ValueError("Ingresa un valor de x.")
        return float(texto)

    # ------------------------------------------------------------------
    # Acciones ligadas a los botones de la Vista
    # ------------------------------------------------------------------
    def evaluar_p(self):
        try:
            p = self._obtener_p()
            x = self._obtener_x()
            resultado = p.evaluar(x)
            self.vista.mostrar_resultado(f"P({x}) = {resultado}")
        except Exception as e:
            self.vista.mostrar_error(str(e))

    def evaluar_q(self):
        try:
            q = self._obtener_q()
            x = self._obtener_x()
            resultado = q.evaluar(x)
            self.vista.mostrar_resultado(f"Q({x}) = {resultado}")
        except Exception as e:
            self.vista.mostrar_error(str(e))

    def sumar(self):
        try:
            p, q = self._obtener_p(), self._obtener_q()
            resultado = p.sumar(q)
            self.vista.mostrar_resultado(f"P(x) + Q(x) = {resultado}")
        except Exception as e:
            self.vista.mostrar_error(str(e))

    def restar(self):
        try:
            p, q = self._obtener_p(), self._obtener_q()
            resultado = p.restar(q)
            self.vista.mostrar_resultado(f"P(x) - Q(x) = {resultado}")
        except Exception as e:
            self.vista.mostrar_error(str(e))

    def multiplicar(self):
        try:
            p, q = self._obtener_p(), self._obtener_q()
            resultado = p.multiplicar(q)
            self.vista.mostrar_resultado(f"P(x) * Q(x) = {resultado}")
        except Exception as e:
            self.vista.mostrar_error(str(e))

    def grado_p(self):
        try:
            p = self._obtener_p()
            self.vista.mostrar_resultado(f"grado(P(x)) = {p.grado()}")
        except Exception as e:
            self.vista.mostrar_error(str(e))

    def grado_q(self):
        try:
            q = self._obtener_q()
            self.vista.mostrar_resultado(f"grado(Q(x)) = {q.grado()}")
        except Exception as e:
            self.vista.mostrar_error(str(e))

    def derivar_p(self):
        try:
            p = self._obtener_p()
            resultado = p.derivar()
            self.vista.mostrar_resultado(f"P'(x) = {resultado}")
        except Exception as e:
            self.vista.mostrar_error(str(e))

    def derivar_q(self):
        try:
            q = self._obtener_q()
            resultado = q.derivar()
            self.vista.mostrar_resultado(f"Q'(x) = {resultado}")
        except Exception as e:
            self.vista.mostrar_error(str(e))
