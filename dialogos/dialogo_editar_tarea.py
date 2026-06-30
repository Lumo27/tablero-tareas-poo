# ventanita para editar una tarea: cambiar texto y estado.

import wx

from config import ESTADOS


class DialogoEditarTarea(wx.Dialog):
    # edita una tarea que ya existe: la descripcion y el estado. hereda de
    # wx.Dialog. viene con los datos ya cargados. si se cambia el estado,
    # despues la tarea se muda de columna.

    def __init__(self, parent, descripcion, estado):
        super().__init__(parent, title='Editar tarea', size=(360, 260))

        # igual que en el de nueva, todo cuelga del dialogo (self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(wx.StaticText(self, label='Descripción:'), 0, wx.ALL, 10)
        # campo de texto, ya cargado con la descripcion de la tarea
        self.campo_desc = wx.TextCtrl(self, value=descripcion, style=wx.TE_MULTILINE)
        sizer.Add(self.campo_desc, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        sizer.Add(wx.StaticText(self, label='Estado:'), 0, wx.ALL, 10)
        # en el combo muestro los nombres lindos pero por adentro uso las claves
        self._titulos = [ESTADOS[e]['titulo'] for e in ESTADOS]
        self._claves = list(ESTADOS.keys())
        self.combo_estado = wx.ComboBox(
            self, choices=self._titulos, style=wx.CB_READONLY)
        # dejo seleccionado el estado actual de la tarea
        self.combo_estado.SetSelection(self._claves.index(estado))
        sizer.Add(self.combo_estado, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        botones = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(botones, 0, wx.ALL | wx.ALIGN_RIGHT, 10)

        self.SetSizer(sizer)

    # devuelve la descripcion editada
    def get_descripcion(self):
        return self.campo_desc.GetValue().strip()

    # devuelve la clave del estado elegido en el combo
    def get_estado(self):
        return self._claves[self.combo_estado.GetSelection()]
