# ventanita para crear una tarea nueva.

import wx


class DialogoNuevaTarea(wx.Dialog):
    # pide la descripcion de la tarea nueva y nada mas. hereda de wx.Dialog.

    def __init__(self, parent):
        super().__init__(parent, title='Nueva tarea', size=(360, 200))

        # armo todo sobre el dialogo (self) porque los botones aceptar/cancelar
        # cuelgan del dialogo y no de un panel aparte
        sizer = wx.BoxSizer(wx.VERTICAL)

        etiqueta = wx.StaticText(self, label='Descripción de la tarea:')
        sizer.Add(etiqueta, 0, wx.ALL, 10)

        # campo donde se escribe la tarea
        self.campo_desc = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        sizer.Add(self.campo_desc, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # botones aceptar / cancelar que ya trae wx
        botones = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(botones, 0, wx.ALL | wx.ALIGN_RIGHT, 10)

        self.SetSizer(sizer)

    # devuelve lo que se escribio, sin espacios de los costados
    def get_descripcion(self):
        return self.campo_desc.GetValue().strip()
