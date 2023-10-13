from operacion import Tareas

#Verificar que archivos se eliminaron del Origen
print("--- [Inicio - Verificar que archivos eliminados del Origen -----------")
eliminarArchivos = Tareas("get")
#Marcar los archivos para eliminar en el Destino
print("---------- [ListToDeleteDestino] -----------")
eliminarArchivos.ListToDeleteDestino()
#Eliminar archivo del Destino
print("---------- [DeleteDestino] -----------")
eliminarArchivos.DeleteDestino()
print("--- [Fin - Verificar que archivos eliminados del Origen -----------")
