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

 # Clase GestionTareas
class SistemaGestionTareas:
    def __init__(self, archivo_dato = 'datos_usuario.json'):
        self.usuarios = {}
        self.archivo_dato = archivo_dato
        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open(self.archivo_dato, 'r') as archivo:
                datos = json.load(archivo)
                for nombre_usuario, info in datos.items():
                    usuario = Usuario(nombre_usuario, info['contrasena'])
                    for tarea_info in info['tareas']:
                        tarea = Tarea(tarea_info['titulo'], tarea_info['descripcion'], tarea_info['fecha_vencimiento'])
                        tarea.completado = tarea_info.get('completado', False)
                        usuario.agregar_tarea(tarea)
                    self.usuarios[nombre_usuario] = usuario
        except FileNotFoundError:
            print("Archivo de datos no encontrado, se creará uno nuevo al guardar.")

    def guardar_datos(self):
        datos = {}
        for nombre_usuario, usuario in self.usuarios.items():
            datos[nombre_usuario] = {
                'contrasena': usuario.contrasena,
                'tareas': [
                    {
                        'titulo': tarea.titulo,
                        'descripcion': tarea.descripcion,
                        'fecha_vencimiento': tarea.fecha_vencimiento,
                        'completado': tarea.completado
                    } for tarea in usuario.tareas
                ]
            }
        with open(self.archivo_dato, 'w') as archivo:
            json.dump(datos, archivo, indent=4)

    def registrar_usuario(self, nombre_usuario, contrasena):    
        if nombre_usuario in self.usuarios:
            print("El nombre de usuario ya está en uso.")
            return False
        else:
            self.usuarios[nombre_usuario] = Usuario(nombre_usuario, contrasena)
            self.guardar_datos()
            print("Usuario registrado exitosamente.")
            return True
    
    def iniciar_sesion(self, nombre_usuario, contrasena):
        usuario = self.usuarios.get(nombre_usuario)
        if usuario and usuario.contrasena == contrasena:
            print("Inicio de sesión exitoso.")
            return usuario
        else:
            print("Nombre de usuario o contraseña incorrectos.")
            return None

    def menu_usuario(self, usuario):
        while True:
            print(f"\n--- Menú de {usuario.nombre_usuario} ---")
            print("1. Crear tarea")
            print("2. Ver tarea")
            print("3. Editar tareas")
            print("4. Completar tarea")
            print("5. Eliminar tarea")
            print("6. Cerrar sesión")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                titulo = input("Título de la tarea: ")
                descripcion = input("Descripción de la tarea: ")
                fecha_vencimiento = input("Fecha de vencimiento (YYYY-MM-DD): ")
                tarea = Tarea(titulo, descripcion, fecha_vencimiento)
                usuario.agregar_tarea(tarea)
                self.guardar_datos()
                print("Tarea agregada exitosamente.")

            elif opcion == "2":
                tareas = usuario.obtener_tareas()
                if not tareas:
                    print("No hay tareas disponibles.")
                else:
                    for idx, tarea in enumerate(tareas, start=1):
                        estado = "Completada" if tarea.completado else "Pendiente"
                        print(f" {idx}. {tarea.titulo} {estado} (Vencimiento: {tarea.fecha_vencimiento} - {tarea.descripcion}   )")

            elif opcion == "3":
                titulo_tarea = input("Título de la tarea a editar: ")
                tarea = next((t for t in usuario.obtener_tareas() if t.titulo == titulo_tarea), None)
                if tarea:
                    nuevo_titulo = input("Nuevo título: ")
                    nueva_descripcion = input("Nueva descripción: ")
                    nueva_fecha_vencimiento = input("Nueva fecha de vencimiento (YYYY-MM-DD): ")
                    tarea.editar_tarea(nuevo_titulo, nueva_descripcion, nueva_fecha_vencimiento)
                    self.guardar_datos()
                    print("Tarea actualizada con éxito...")
                else:
                    print("Tarea no encontrada.") 

            elif opcion == "4":
                titulo_tarea = input("Título de la tarea a completar: ")
                tarea = next((t for t in usuario.obtener_tareas() if t.titulo == titulo_tarea), None)
                if tarea:
                    tarea.marcar_como_completado()
                    self.guardar_datos()
                    print("Tarea marcada como completada.")
                else:
                    print("Tarea no encontrada.")

            elif opcion == "5":
                titulo_tarea = input("Título de la tarea a eliminar: ")
                usuario.eliminar_tarea(titulo_tarea)
                self.guardar_datos()
                print("Tarea eliminada con éxito.")

            elif opcion == "6":
                print("Cerrando sesión...")
                break
            else:
                print("Opción no válida, por favor intente de nuevo.")

# ejecución del sistema
if __name__ == "__main__":
    sistema = SistemaGestionTareas()
    while True:
        print("\n--- Sistema de Gestión de Tareas ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre_usuario = input("Nombre de usuario: ")
            contrasena = input("Ingrese la contraseña: ")
            sistema.registrar_usuario(nombre_usuario, contrasena)

        elif opcion == "2":
            nombre_usuario = input("Nombre de usuario: ")
            contrasena = input("Ingrese la contraseña: ")
            usuario = sistema.iniciar_sesion(nombre_usuario, contrasena)
            if usuario:
                sistema.menu_usuario(usuario)

        elif opcion == "3":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida, por favor intente de nuevo.")