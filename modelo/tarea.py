# clase tarea, el dato mas chico del proyecto.


class Tarea:
    # una tarea sola: descripcion, fecha y estado.
    # es puro dato, no hace nada por su cuenta, de eso se encarga la columna.

    def __init__(self, descripcion, fecha_creacion, estado):
        self.descripcion = descripcion        # que hay que hacer
        self.fecha_creacion = fecha_creacion  # cuando se creo
        self.estado = estado                  # en que columna esta
