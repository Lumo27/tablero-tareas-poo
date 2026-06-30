# gestor de tareas - trabajo de programacion orientada a objetos.
#
# app de escritorio con wxPython, un tablero kanban de tres columnas:
# a realizar / en proceso / terminada.
#
# este archivo es solo el arranque. el resto del codigo esta separado en
# carpetas: config.py (las constantes), modelo/ (los datos), dialogos/ (las
# ventanitas que piden datos) y vista/ (lo que se ve en pantalla).

import wx

from vista import VentanaPrincipal


def main():
    # arranco wx, abro la ventana principal y la dejo andando
    app = wx.App(False)
    ventana = VentanaPrincipal()
    ventana.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
