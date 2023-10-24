from operacion import Tareas

print("----||Paso 3||---")
# Verificar que archivos se eliminaron del Origen
print("[Inicio - Verificar que archivos eliminados del Destino]")
eliminarArchivosGet = Tareas("get")
# Marcar los archivos para eliminar en el Destino
print("<---------- [ListToDeleteDestino] ----------->")
eliminarArchivosGet.ListToDeleteDestino()
# Eliminar archivo del Destino
print("<---------- [DeleteOrigen] ----------->")
eliminarArchivosGet.DeleteOrigen()
print("[Fin - Verificar que archivos eliminados del Destino]")
print("----||Fin||---")
