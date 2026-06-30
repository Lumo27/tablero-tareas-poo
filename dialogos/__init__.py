# capa de dialogos: las ventanitas que piden datos.
# las dos heredan de wx.Dialog. las re-exporto para importarlas mas corto.

from dialogos.dialogo_nueva_tarea import DialogoNuevaTarea
from dialogos.dialogo_editar_tarea import DialogoEditarTarea

__all__ = ['DialogoNuevaTarea', 'DialogoEditarTarea']
