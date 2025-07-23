import json
from datetime import datetime

# Clase tarea 
class Tarea:
    def __init__(self, titulo, descripcion, fecha_vencimiento):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.completado = False

    def marcar_como_completado(self):
        self.completado = True

    def editar_tarea(self, nuevo_titulo, nueva_descripcion, nueva_fecha):
        self.titulo = nuevo_titulo
        self.descripcion = nueva_descripcion
        self.fecha_vencimiento = nueva_fecha

# Clase Usuario
class Usuario:
    def __init__(self, nombre_usuario, contrasena):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.tareas = []

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def eliminar_tarea(self, titulo_tarea):
        self.tareas = [tarea for tarea in self.tareas if tarea.titulo != titulo_tarea]
        # Recorre las tareas y elimina la que coincida con el título

    def obtener_tareas(self):
        return self.tareas
