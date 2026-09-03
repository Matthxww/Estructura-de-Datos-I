# ADT Polinomio - Proyecto MVC en Python

Implementación del TDA (Tipo de Dato Abstracto) **Polinomio** con las
operaciones de la tabla (`evaluar`, `sumar`, `restar`, `multiplicar`,
`grado`, `derivar`), organizada con el patrón **MVC**:

```
polinomio_mvc/
├── main.py                     # Punto de entrada
├── model/
│   └── polinomio.py            # Modelo: clase Polinomio (el ADT)
├── view/
│   └── vista.py                # Vista: interfaz Tkinter (incluye el Label de resultado)
└── controller/
    └── controlador.py          # Controlador: conecta Vista y Modelo
```

## 1. Crear el entorno virtual (Windows)

Abre **cmd** o **PowerShell** dentro de la carpeta `polinomio_mvc` y ejecuta:

```bat
python -m venv EnvWin-pc
```

Esto crea la carpeta `EnvWin-pc` con el entorno virtual.

## 2. Activar el entorno virtual

**CMD:**
```bat
EnvWin-pc\Scripts\activate.bat
```

**PowerShell:**
```powershell
EnvWin-pc\Scripts\Activate.ps1
```

> Si PowerShell bloquea el script, ejecuta primero:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

Cuando esté activo verás `(EnvWin-pc)` al inicio de la línea de comandos.

## 3. Instalar dependencias

Este proyecto solo usa **Tkinter** (ya viene incluido con la instalación
estándar de Python en Windows), así que no necesitas instalar nada más.
Si en el futuro agregas librerías, créalas en `requirements.txt` e instala con:

```bat
pip install -r requirements.txt
```

## 4. Ejecutar la aplicación

```bat
python main.py
```

Se abrirá una ventana donde puedes:

1. Escribir un polinomio **P(x)**, por ejemplo: `3x^2 + 2x - 5`
2. Escribir un polinomio **Q(x)**, por ejemplo: `x^2 - 4`
3. Escribir un valor de **x** para evaluar
4. Presionar cualquiera de los botones (Evaluar, Sumar, Restar,
   Multiplicar, Grado, Derivar)
5. El resultado aparece en el **Label** inferior de la ventana.

## 5. Desactivar el entorno virtual

Cuando termines:

```bat
deactivate
```

## Notas sobre el formato de entrada

- Usa `^` para el exponente: `x^3`, `2x^2`
- Los términos se separan con `+` o `-`: `3x^2 + 2x - 5`
- `x` sin exponente equivale a `x^1`
- Un número solo (sin `x`) es el término independiente (grado 0)
