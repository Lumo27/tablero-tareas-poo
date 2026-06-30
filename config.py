# config del proyecto.
# aca estan la carpeta base y el mapeo de cada estado a su nombre y su archivo.
# si hay que renombrar o agregar un estado se toca solo aca.

import os

# carpeta donde esta este archivo, o sea la raiz del proyecto donde van los txt
CARPETA = os.path.dirname(os.path.abspath(__file__))

# cada estado con su titulo para mostrar y el archivo donde se guarda
ESTADOS = {
    'todo':       {'titulo': 'A realizar', 'archivo': 'a_realizar.txt'},
    'inprogress': {'titulo': 'En proceso', 'archivo': 'en_proceso.txt'},
    'done':       {'titulo': 'Terminada',  'archivo': 'terminada.txt'},
}
