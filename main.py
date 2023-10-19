from operacion import Tareas

# Enviar archivos al Destino
print("----||Inicio||---")
print("[Inicio - Enviar archivos al Destino]")
enviarArchivos = Tareas("put")
print("<---------- [ListOrigen] ----------->")
enviarArchivos.ListOrigen()
print("<---------- [GetOrigen] ----------->")
enviarArchivos.GetOrigen()
print("<---------- [PutDestino] ----------->")
enviarArchivos.PutDestino()
print("[Fin - Enviar archivos al Destino] ---")

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

print("----||Paso 2||---")
# Recuperar archivos de Destino
print("[Inicio - Recuperar archivos de Destion]")
obtenerArchivos = Tareas("get")
print("<---------- [ListDestino] ----------->")
obtenerArchivos.ListDestino()
print("<---------- [GetDestino] ----------->")
obtenerArchivos.GetDestino()
print("<---------- [PutDestino] ----------->")
obtenerArchivos.PutOrigen()
print("[Fin - Recuperar archivos de Destion]")

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
