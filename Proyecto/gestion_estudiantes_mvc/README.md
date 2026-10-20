# Sistema de Gestión de Estudiantes — MVC en Python

ADT **Lista Enlazada de Estudiantes**, construida desde cero con
`Nodo` + `ListaEstudiantes`, que se mantiene **siempre ordenada por
ID** al insertar (sin usar `list`/`dict` de Python para la lógica
interna de la cadena de nodos).

Interfaz Tkinter moderna: panel de formulario a la izquierda, y a la
derecha una lista de **tarjetas** (una por estudiante/nodo) con
scroll, flechas "↓" entre ellas (para que se note que es una lista
enlazada), la tarjeta CABEZA resaltada, un campo de búsqueda que
filtra en vivo, y 3 criterios de orden visual (ID / apellido /
promedio).

```
gestion_estudiantes_mvc/
├── main.py                       # Punto de entrada
├── model/
│   ├── nodo.py                   # Clase Nodo (dato + puntero al siguiente)
│   ├── estudiante.py             # Clase Estudiante (el dato que vive en cada nodo)
│   └── lista_estudiantes.py      # Modelo: clase ListaEstudiantes (el ADT)
├── view/
│   └── vista.py                  # Vista: interfaz Tkinter (tarjetas + scroll + filtro)
└── controller/
    └── controlador.py            # Controlador: conecta Vista y Modelo
```

## Operaciones del ADT

| Método | Descripción |
|---|---|
| `inscribir(estudiante)` | Inserta manteniendo el orden por ID |
| `dar_de_baja(id)` | Elimina y retorna el estudiante con ese ID |
| `buscar(id)` | Retorna el estudiante con ese ID, o None |
| `buscar_por_nombre(texto)` | Retorna todos los estudiantes cuyo nombre/apellido contiene el texto |
| `editar_estudiante(id, nombre, apellido)` | Modifica nombre y/o apellido sin mover el nodo |
| `actualizar_calificaciones(id, nota)` | Agrega una calificación |
| `calcular_promedio(id)` | Calcula el promedio de notas |
| `obtener_mejor_y_peor_promedio()` | Retorna quién tiene el mejor y el peor promedio |
| `generar_reporte()` | Retorna todos los estudiantes en el orden real de la lista (por ID) |
| `generar_reporte_ordenado(criterio)` | Copia ordenada por `"id"`, `"apellido"` o `"promedio"`, SIN alterar la lista enlazada real |
| `esta_vacia()` / `tamano()` | Consultas básicas |
| `vaciar()` | Elimina a todos los estudiantes |

**Nota importante sobre el orden:** la lista enlazada interna (los
nodos conectados por `.siguiente`) siempre se mantiene ordenada por
ID — así está diseñado el ADT. Los radiobuttons "Ordenar vista por"
en la interfaz NO reordenan los nodos: generan una copia ordenada
distinta solo para mostrarla. Por eso las flechas "↓" entre tarjetas
(que representan los punteros reales) solo se dibujan cuando el
orden visual es "ID" — en los otros órdenes esas flechas no
representarían la cadena real de nodos.

## 1. Crear el entorno virtual (Windows)

```bat
cd gestion_estudiantes_mvc
python -m venv EnvWin-pc
```

## 2. Activar el entorno virtual

```bat
EnvWin-pc\Scripts\activate.bat
```

## 3. Ejecutar

No requiere ninguna dependencia externa (Tkinter viene incluido con Python):

```bat
python main.py
```

## 4. Cómo usarlo

1. Llena ID, Nombre, Apellido (y opcionalmente calificaciones separadas
   por coma) → clic en **Inscribir estudiante**.
2. En **"OPERACIONES POR ID"**, escribe el ID del estudiante en el
   campo dedicado de esa sección y usa el botón correspondiente
   (agregar calificación, calcular promedio, buscar, dar de baja).
3. En **"EDITAR ESTUDIANTE"**, usa el mismo ID de la sección anterior
   junto con el nuevo nombre y/o apellido (puedes dejar uno vacío si
   solo quieres cambiar el otro).
4. En **"BÚSQUEDA Y ESTADÍSTICAS"**, busca por nombre/apellido parcial,
   o pide el mejor y peor promedio del curso.
5. Usa los radiobuttons **"Ordenar vista por"** para ver el reporte
   ordenado por ID, apellido o promedio.
6. **Generar reporte completo** muestra todos los estudiantes y sus
   datos en el panel de mensajes.

## 5. Desactivar el entorno virtual

```bat
deactivate
```
