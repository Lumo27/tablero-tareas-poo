# Gestor de Tareas

Aplicación de escritorio tipo **Kanban** hecha en Python con **wxPython**,
para la materia de **Programación Orientada a Objetos**.

Muestra un tablero con tres columnas — *A realizar*, *En proceso* y *Terminada* —
donde podés crear, editar, mover y eliminar tareas. Cada columna se guarda sola
en su propio archivo de texto.

## Requisitos

- Python 3.x
- wxPython

```bash
pip install wxPython
```

## Ejecución

```bash
python gestor_tareas.py
```

Al arrancar, cada columna carga su archivo `.txt`. Si no existen, se crean
solos cuando guardás.

## Estructura del proyecto

El código está repartido en carpetas (modularizado) para que se note bien
cada concepto de POO. Cada archivo tiene una sola clase y arriba dice qué hace.

```
tablero-tareas/
├── gestor_tareas.py     → solo el arranque (la función main)
├── config.py            → constantes que usan todos (ESTADOS, CARPETA)
│
├── modelo/              → los datos, sin nada de pantalla
│   ├── tarea.py         → Tarea: un dato y nada más (no hereda de nada)
│   └── columna.py       → Columna: COMPOSICIÓN (tiene una lista de Tareas) + guardado
│
├── dialogos/            → las ventanitas que piden datos
│   ├── dialogo_nueva_tarea.py    → DialogoNuevaTarea  (HERENCIA de wx.Dialog)
│   └── dialogo_editar_tarea.py   → DialogoEditarTarea (HERENCIA de wx.Dialog)
│
└── vista/               → lo que se ve en pantalla
    ├── ventana_tarea.py      → VentanaTarea     (HERENCIA wx.Panel + POLIMORFISMO)
    └── ventana_principal.py  → VentanaPrincipal (HERENCIA wx.Frame + COMPOSICIÓN)
```

Cada carpeta tiene un `__init__.py` que re-exporta sus clases, así los imports
quedan cortos (por ejemplo `from modelo import Tarea, Columna`).

## Clases (POO)

| Clase | Hereda de | Qué hace |
|-------|-----------|----------|
| `Tarea` | — | El dato: descripción, fecha de creación y estado. |
| `Columna` | — | Maneja las tareas de un estado y su archivo `.txt`. |
| `DialogoNuevaTarea` | `wx.Dialog` | Pide la descripción de una tarea nueva. |
| `DialogoEditarTarea` | `wx.Dialog` | Edita la descripción y el estado de una tarea. |
| `VentanaTarea` | `wx.Panel` | El panel de una columna. **Polimorfismo**: cambia sus botones según el estado. |
| `VentanaPrincipal` | `wx.Frame` | La ventana grande: menú, botonera y coordina las columnas. |

### Conceptos de POO aplicados

- **Herencia**: todas las clases gráficas heredan de clases de wxPython
  (`wx.Frame`, `wx.Panel`, `wx.Dialog`). En cambio `Tarea` y `Columna` no
  heredan de nada, para que se note la diferencia.
- **Composición**: una `Columna` *está hecha de* `Tarea`s (tiene la lista
  `self.tareas`), y la `VentanaPrincipal` *tiene adentro* las columnas y los
  paneles. El todo se arma juntando las partes.
- **Polimorfismo**: `VentanaTarea` se porta distinto según el estado de su
  `Columna` — la columna *A realizar* muestra el botón "Nueva" y las demás no
  (mirá `VentanaTarea._crear_botones()`).

## Persistencia

Tres archivos de texto plano en la carpeta del proyecto:

| Archivo | Estado |
|---------|--------|
| `a_realizar.txt` | `todo` |
| `en_proceso.txt` | `inprogress` |
| `terminada.txt` | `done` |

Cada línea tiene este formato: `descripcion|fecha_creacion`

Cuando una tarea cambia de estado, se borra del archivo de origen y se escribe
en el de destino.
