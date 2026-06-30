# panel de una columna. aca esta el comportamiento polimorfico.

import datetime

import wx

from config import ESTADOS
from modelo import Tarea
from dialogos import DialogoNuevaTarea, DialogoEditarTarea


class VentanaTarea(wx.Panel):
    # el panel que dibuja una columna con sus tareas. hereda de wx.Panel.
    # la misma clase muestra botones distintos segun el estado de su columna,
    # eso se ve en _crear_botones.

    def __init__(self, parent, columna):
        super().__init__(parent)
        self.columna = columna  # la columna que muestra este panel

        sizer = wx.BoxSizer(wx.VERTICAL)

        # titulo de la columna, en negrita y un poco mas grande
        titulo = wx.StaticText(self, label=ESTADOS[columna.estado]['titulo'])
        fuente = titulo.GetFont()
        fuente.SetWeight(wx.FONTWEIGHT_BOLD)
        fuente.SetPointSize(fuente.GetPointSize() + 2)
        titulo.SetFont(fuente)
        sizer.Add(titulo, 0, wx.ALL | wx.ALIGN_CENTER, 6)

        # lista donde se ven las tareas (descripcion + fecha)
        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.lista.InsertColumn(0, 'Descripción', width=200)
        self.lista.InsertColumn(1, 'Creada', width=120)
        sizer.Add(self.lista, 1, wx.EXPAND | wx.ALL, 4)

        # los botones, que dependen del estado de la columna
        self._crear_botones(sizer)

        self.SetSizer(sizer)
        self.actualizar_lista()

    # arma los botones segun el estado, cada columna muestra los suyos
    def _crear_botones(self, sizer):
        fila = wx.BoxSizer(wx.HORIZONTAL)

        # el boton nueva solo va en la columna a realizar
        if self.columna.estado == 'todo':
            btn_nueva = wx.Button(self, label='Nueva')
            btn_nueva.Bind(wx.EVT_BUTTON, self.on_nueva)
            fila.Add(btn_nueva, 0, wx.ALL, 2)

        # editar y eliminar van en todas
        btn_editar = wx.Button(self, label='Editar')
        btn_editar.Bind(wx.EVT_BUTTON, self.on_editar)
        fila.Add(btn_editar, 0, wx.ALL, 2)

        btn_eliminar = wx.Button(self, label='Eliminar')
        btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        fila.Add(btn_eliminar, 0, wx.ALL, 2)

        sizer.Add(fila, 0, wx.ALIGN_CENTER | wx.BOTTOM, 4)

    # vuelve a llenar la lista con las tareas que tiene la columna ahora
    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        for i, tarea in enumerate(self.columna.tareas):
            self.lista.InsertItem(i, tarea.descripcion)
            self.lista.SetItem(i, 1, tarea.fecha_creacion)

    # dice que fila esta seleccionada, o -1 si no hay ninguna
    def _indice_seleccionado(self):
        return self.lista.GetFirstSelected()

    # crea una tarea nueva abriendo el dialogo de nueva tarea
    def on_nueva(self, event):
        dlg = DialogoNuevaTarea(self)
        if dlg.ShowModal() == wx.ID_OK:  # apreto aceptar
            descripcion = dlg.get_descripcion()
            if descripcion:  # solo si escribio algo
                fecha = datetime.date.today().strftime('%Y-%m-%d')
                tarea = Tarea(descripcion, fecha, self.columna.estado)
                self.columna.agregar(tarea)
                self.actualizar_lista()
        dlg.Destroy()

    # edita la tarea elegida; si cambia el estado la muda de columna
    def on_editar(self, event):
        indice = self._indice_seleccionado()
        if indice == -1:  # no eligio ninguna
            wx.MessageBox('Seleccioná una tarea para editar.',
                          'Sin selección', wx.OK | wx.ICON_INFORMATION)
            return

        tarea = self.columna.tareas[indice]
        dlg = DialogoEditarTarea(self, tarea.descripcion, tarea.estado)
        if dlg.ShowModal() == wx.ID_OK:
            nueva_desc = dlg.get_descripcion()
            nuevo_estado = dlg.get_estado()
            if nueva_desc:
                tarea.descripcion = nueva_desc
                if nuevo_estado != self.columna.estado:
                    # cambio de estado: que la ventana grande la mude de columna
                    ventana = wx.GetTopLevelParent(self)
                    ventana.mover_tarea(self.columna, indice, nuevo_estado)
                else:
                    # solo cambio el texto: guardo y refresco
                    self.columna.guardar()
                    self.actualizar_lista()
        dlg.Destroy()

    # borra la tarea elegida, pero antes pregunta si esta seguro
    def on_eliminar(self, event):
        indice = self._indice_seleccionado()
        if indice == -1:
            wx.MessageBox('Seleccioná una tarea para eliminar.',
                          'Sin selección', wx.OK | wx.ICON_INFORMATION)
            return

        confirm = wx.MessageDialog(
            self, '¿Eliminar la tarea seleccionada?', 'Confirmar',
            wx.YES_NO | wx.ICON_QUESTION)
        if confirm.ShowModal() == wx.ID_YES:
            self.columna.eliminar(indice)
            self.actualizar_lista()
        confirm.Destroy()
