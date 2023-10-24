from operacion import Tareas

print("----||Paso 1||---")
# Verificar que archivos se eliminaron del Destino
print("[Inicio - Verificar que archivos eliminados del Destino]")
eliminarArchivosPut = Tareas("put")
# Marcar los archivos para eliminar en el Destino
print("<---------- [ListToDeleteDestino] ----------->")
eliminarArchivosPut.ListToDeleteDestino()
# Eliminar archivo del Destino
print("<---------- [DeleteOrigen] ----------->")
eliminarArchivosPut.DeleteOrigen()
print("[Fin - Verificar que archivos eliminados del Destino]")
