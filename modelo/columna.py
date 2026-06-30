# clase columna: agarra las tareas de un estado y las guarda en disco.

import os

from config import CARPETA, ESTADOS
from modelo.tarea import Tarea


class Columna:
    # maneja las tareas de un estado y su archivo de texto.
    # tiene una lista de tareas y se encarga de cargarlas, agregarlas,
    # borrarlas y guardarlas. cada columna usa su propio archivo.

    def __init__(self, estado):
        self.estado = estado
        self.tareas = []  # lista de tareas de esta columna
        # archivo propio de la columna
        self.archivo = os.path.join(CARPETA, ESTADOS[estado]['archivo'])

    # lee el txt y arma la lista de tareas
    def cargar(self):
        self.tareas = []
        # si todavia no existe el archivo no hay nada que cargar
        if not os.path.exists(self.archivo):
            return
        with open(self.archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.rstrip('\n')
                if not linea:
                    continue  # salteo lineas vacias
                # cada linea viene como descripcion|fecha
                partes = linea.split('|')
                descripcion = partes[0]
                fecha = partes[1] if len(partes) > 1 else ''
                self.tareas.append(Tarea(descripcion, fecha, self.estado))

    # pisa el txt con las tareas que tiene ahora la columna
    def guardar(self):
        with open(self.archivo, 'w', encoding='utf-8') as f:
            for tarea in self.tareas:
                f.write('{0}|{1}\n'.format(tarea.descripcion, tarea.fecha_creacion))

    # mete una tarea en la columna y guarda
    def agregar(self, tarea):
        tarea.estado = self.estado
        self.tareas.append(tarea)
        self.guardar()

    # borra la tarea de esa posicion y guarda
    def eliminar(self, indice):
        if 0 <= indice < len(self.tareas):
            del self.tareas[indice]
            self.guardar()
