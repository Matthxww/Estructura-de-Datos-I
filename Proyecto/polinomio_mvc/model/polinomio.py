"""
model/polinomio.py
-------------------
MODELO (M de MVC)

Implementa el TDA (Tipo/Abstract Data Type) Polinomio.

Representación interna:
    Se guarda como una lista de coeficientes donde el índice
    representa el exponente de x.

    Ejemplo:  3x^2 + 2x + 1  ->  [1, 2, 3]
              índice 0 -> coef de x^0
              índice 1 -> coef de x^1
              índice 2 -> coef de x^2

No contiene NINGUNA lógica de interfaz gráfica: solo datos + operaciones.
"""

import re


class Polinomio:
    def __init__(self, coeficientes=None):
        """
        coeficientes: lista de números, donde coeficientes[i] es el
        coeficiente que acompaña a x^i.
        """
        if coeficientes is None or len(coeficientes) == 0:
            coeficientes = [0]
        self.coeficientes = list(coeficientes)
        self._limpiar_ceros_finales()

    # ------------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------------
    def _limpiar_ceros_finales(self):
        """Elimina ceros sobrantes al final (términos de mayor grado nulos)."""
        while len(self.coeficientes) > 1 and self.coeficientes[-1] == 0:
            self.coeficientes.pop()

    @staticmethod
    def _num(n):
        """Convierte 2.0 -> 2 (int) para que se vea más limpio al imprimir."""
        if float(n).is_integer():
            return int(n)
        return n

    # ------------------------------------------------------------------
    # Operaciones del ADT (según la tabla)
    # ------------------------------------------------------------------
    def evaluar(self, x):
        """Calcular P(x) para un valor de x."""
        resultado = 0
        for exp, coef in enumerate(self.coeficientes):
            resultado += coef * (x ** exp)
        return self._num(resultado) if isinstance(resultado, float) else resultado

    def sumar(self, Q):
        """Retornar P(x) + Q(x)."""
        n = max(len(self.coeficientes), len(Q.coeficientes))
        resultado = [0] * n
        for i in range(n):
            a = self.coeficientes[i] if i < len(self.coeficientes) else 0
            b = Q.coeficientes[i] if i < len(Q.coeficientes) else 0
            resultado[i] = a + b
        return Polinomio(resultado)

    def restar(self, Q):
        """Retornar P(x) - Q(x)."""
        n = max(len(self.coeficientes), len(Q.coeficientes))
        resultado = [0] * n
        for i in range(n):
            a = self.coeficientes[i] if i < len(self.coeficientes) else 0
            b = Q.coeficientes[i] if i < len(Q.coeficientes) else 0
            resultado[i] = a - b
        return Polinomio(resultado)

    def multiplicar(self, Q):
        """Retornar P(x) * Q(x)."""
        n = len(self.coeficientes) + len(Q.coeficientes) - 1
        resultado = [0] * n
        for i, a in enumerate(self.coeficientes):
            for j, b in enumerate(Q.coeficientes):
                resultado[i + j] += a * b
        return Polinomio(resultado)

    def grado(self):
        """Retornar el exponente más alto (con coeficiente distinto de 0)."""
        return len(self.coeficientes) - 1

    def derivar(self):
        """Retornar P'(x)."""
        if self.grado() == 0:
            return Polinomio([0])
        resultado = [self.coeficientes[i] * i for i in range(1, len(self.coeficientes))]
        return Polinomio(resultado)

    # ------------------------------------------------------------------
    # Representación en texto (para mostrar en la Vista)
    # ------------------------------------------------------------------
    def __str__(self):
        terminos = []
        for exp in range(len(self.coeficientes) - 1, -1, -1):
            coef = self.coeficientes[exp]
            if coef == 0:
                continue

            coef_txt = self._num(coef)
            signo = "-" if coef_txt < 0 else "+"
            valor_abs = abs(coef_txt)

            if exp == 0:
                termino = f"{valor_abs}"
            elif exp == 1:
                termino = "x" if valor_abs == 1 else f"{valor_abs}x"
            else:
                termino = f"x^{exp}" if valor_abs == 1 else f"{valor_abs}x^{exp}"

            terminos.append((signo, termino))

        if not terminos:
            return "0"

        # Construir la cadena final con signos bien colocados
        primer_signo, primer_termino = terminos[0]
        texto = ("-" if primer_signo == "-" else "") + primer_termino
        for signo, termino in terminos[1:]:
            texto += f" {signo} {termino}"
        return texto

    # ------------------------------------------------------------------
    # Construcción de un Polinomio a partir de texto ingresado por el usuario
    # ------------------------------------------------------------------
    @staticmethod
    def desde_cadena(cadena):
        """
        Convierte un texto como "3x^2 + 2x - 5" o "x^3 - 1" en un objeto
        Polinomio. Lanza ValueError si el formato es inválido.
        """
        if cadena is None or cadena.strip() == "":
            raise ValueError("El polinomio no puede estar vacío.")

        texto = cadena.replace(" ", "").replace("X", "x")

        if texto[0] not in "+-":
            texto = "+" + texto

        # Separa por términos, cada uno empieza con + o -
        terminos = re.findall(r'[+-][^+-]+', texto)
        if not terminos:
            raise ValueError("Formato de polinomio inválido.")

        coeficientes_dict = {}

        for termino in terminos:
            signo = -1 if termino[0] == "-" else 1
            cuerpo = termino[1:]

            if cuerpo == "":
                raise ValueError(f"Término inválido: '{termino}'")

            if "x" in cuerpo:
                partes = cuerpo.split("x")
                coef_str = partes[0]
                coef = 1.0 if coef_str == "" else float(coef_str)

                resto = partes[1] if len(partes) > 1 else ""
                if resto.startswith("^"):
                    exp = int(resto[1:])
                elif resto == "":
                    exp = 1
                else:
                    raise ValueError(f"Término inválido: '{termino}'")
            else:
                coef = float(cuerpo)
                exp = 0

            coef *= signo
            coeficientes_dict[exp] = coeficientes_dict.get(exp, 0) + coef

        grado_max = max(coeficientes_dict.keys())
        lista = [0] * (grado_max + 1)
        for exp, coef in coeficientes_dict.items():
            lista[exp] = coef

        return Polinomio(lista)
