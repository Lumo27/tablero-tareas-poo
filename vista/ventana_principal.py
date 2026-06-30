# ventana principal: coordina el modelo y la vista de todo el tablero.

import wx

from modelo import Columna
from vista.ventana_tarea import VentanaTarea


class VentanaPrincipal(wx.Frame):
    # la ventana grande de la app. hereda de wx.Frame. tiene adentro las tres
    # columnas y los tres paneles, arma el menu y los botones de arriba, y
    # coordina lo que toca a mas de una columna, por ejemplo mover una tarea.

    def __init__(self):
        super().__init__(None, title='Gestor de Tareas', size=(820, 520))

        # iconito de la ventana, de los que ya trae wx asi no depende de un archivo
        icono = wx.ArtProvider.GetIcon(wx.ART_LIST_VIEW, wx.ART_FRAME_ICON)
        self.SetIcon(icono)

        # una columna por estado, cada una se carga de su txt
        self.col_todo = Columna('todo')
        self.col_prog = Columna('inprogress')
        self.col_done = Columna('done')
        for col in (self.col_todo, self.col_prog, self.col_done):
            col.cargar()

        self.paneles = []  # aca van los tres paneles

        self.init_menu()
        self.init_ui()
        self.Maximize(True)
        self.Centre()

    # arma la barra de menu: archivo y ayuda
    def init_menu(self):
        barra = wx.MenuBar()

        menu_archivo = wx.Menu()
        item_guardar = menu_archivo.Append(wx.ID_SAVE, 'Guardar todo')
        menu_archivo.AppendSeparator()
        item_salir = menu_archivo.Append(wx.ID_EXIT, 'Salir')

        menu_ayuda = wx.Menu()
        item_creditos = menu_ayuda.Append(wx.ID_ABOUT, 'Créditos')

        barra.Append(menu_archivo, 'Archivo')
        barra.Append(menu_ayuda, 'Ayuda')
        self.SetMenuBar(barra)

        # engancho cada opcion del menu con su funcion
        self.Bind(wx.EVT_MENU, self.on_guardar_todo, item_guardar)
        self.Bind(wx.EVT_MENU, self.on_salir, item_salir)
        self.Bind(wx.EVT_MENU, self.on_creditos, item_creditos)

    # arma la botonera de arriba y los tres paneles uno al lado del otro
    def init_ui(self):
        panel_base = wx.Panel(self)
        sizer_base = wx.BoxSizer(wx.VERTICAL)

        # botonera de arriba, trabaja sobre a realizar o sobre lo seleccionado
        barra_btns = wx.BoxSizer(wx.HORIZONTAL)
        btn_nueva = wx.Button(panel_base, label='Nueva tarea')
        btn_editar = wx.Button(panel_base, label='Editar tarea')
        btn_eliminar = wx.Button(panel_base, label='Eliminar tarea')
        btn_creditos = wx.Button(panel_base, label='Créditos')
        btn_nueva.Bind(wx.EVT_BUTTON, self.on_nueva_global)
        btn_editar.Bind(wx.EVT_BUTTON, self.on_editar_global)
        btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar_global)
        btn_creditos.Bind(wx.EVT_BUTTON, self.on_creditos)
        for b in (btn_nueva, btn_editar, btn_eliminar, btn_creditos):
            barra_btns.Add(b, 0, wx.ALL, 4)
        sizer_base.Add(barra_btns, 0, wx.ALIGN_CENTER)

        # los tres paneles, uno por columna, en fila
        sizer_cols = wx.BoxSizer(wx.HORIZONTAL)
        for columna in (self.col_todo, self.col_prog, self.col_done):
            panel = VentanaTarea(panel_base, columna)
            self.paneles.append(panel)
            sizer_cols.Add(panel, 1, wx.EXPAND | wx.ALL, 4)
        sizer_base.Add(sizer_cols, 1, wx.EXPAND)

        panel_base.SetSizer(sizer_base)

    # devuelve el panel que muestra esa columna
    def _panel_de(self, columna):
        for panel in self.paneles:
            if panel.columna is columna:
                return panel
        return None

    # devuelve la columna que corresponde a ese estado
    def _columna_por_estado(self, estado):
        for col in (self.col_todo, self.col_prog, self.col_done):
            if col.estado == estado:
                return col
        return None

    # mueve una tarea de una columna a otra, cambia archivo y pantalla.
    # la saca del origen y la mete en el destino; las dos guardan su txt solas.
    def mover_tarea(self, columna_origen, indice, nuevo_estado):
        tarea = columna_origen.tareas[indice]
        columna_destino = self._columna_por_estado(nuevo_estado)

        columna_origen.eliminar(indice)            # la saca del origen y guarda
        columna_destino.agregar(tarea)             # la mete en el destino y guarda

        # refresco los dos paneles que cambiaron
        self._panel_de(columna_origen).actualizar_lista()
        self._panel_de(columna_destino).actualizar_lista()

    # botones de arriba: le pasan la pelota al panel que corresponde

    # nueva tarea: siempre cae en la columna a realizar
    def on_nueva_global(self, event):
        self._panel_de(self.col_todo).on_nueva(event)

    # busca en que panel hay una tarea seleccionada
    def _panel_con_seleccion(self):
        for panel in self.paneles:
            if panel.lista.GetFirstSelected() != -1:
                return panel
        return None

    # editar: trabaja sobre el panel que tenga algo seleccionado
    def on_editar_global(self, event):
        panel = self._panel_con_seleccion()
        if panel is None:
            wx.MessageBox('Seleccioná una tarea en alguna columna.',
                          'Sin selección', wx.OK | wx.ICON_INFORMATION)
            return
        panel.on_editar(event)

    # eliminar: trabaja sobre el panel que tenga algo seleccionado
    def on_eliminar_global(self, event):
        panel = self._panel_con_seleccion()
        if panel is None:
            wx.MessageBox('Seleccioná una tarea en alguna columna.',
                          'Sin selección', wx.OK | wx.ICON_INFORMATION)
            return
        panel.on_eliminar(event)

    # opciones del menu

    # guarda las tres columnas en sus txt
    def on_guardar_todo(self, event):
        self.col_todo.guardar()
        self.col_prog.guardar()
        self.col_done.guardar()
        wx.MessageBox('Tareas guardadas correctamente.',
                      'Guardar todo', wx.OK | wx.ICON_INFORMATION)

    # cierra la app
    def on_salir(self, event):
        self.Close()

    # muestra los creditos del trabajo
    def on_creditos(self, event):
        texto = (
            'Gestor de Tareas\n\n'
            'Autor: Lucas Motta\n'
            'Github: https://github.com/Lumo27/tablero-tareas-poo\n'
            'Materia: Programación Orientada a Objetos\n'
            'Trabajo práctico - Tablero de tareas (Kanban)\n'
        )
        wx.MessageBox(texto, 'Créditos', wx.OK | wx.ICON_INFORMATION)
