from operacion import Tareas

#Enviar archivos al Origen
print("--- [Inicio - Enviar archivos al Origen] -----------")
enviarArchivos = Tareas("put")

print("---------- [ListToGetOrigen] -----------")
enviarArchivos.ListToGetOrigen()
print("---------- [GetOrigen] -----------")
enviarArchivos.GetOrigen()
print("---------- [PutDestino] -----------")
enviarArchivos.PutDestino()
print("--- [Fin - Enviar archivos al Origen] -----------")

#Verificar que archivos se eliminaron del Origen
print("--- [Inicio - Verificar que archivos eliminados del Origen -----------")
eliminarArchivosPut = Tareas("put")
#Marcar los archivos para eliminar en el Destino
print("---------- [ListToDeleteDestino] -----------")
eliminarArchivosPut.ListToDeleteDestino()
#Eliminar archivo del Destino
print("---------- [DeleteDestino] -----------")
eliminarArchivosPut.DeleteDestino()
print("--- [Fin - Verificar que archivos eliminados del Origen -----------")

#Recuperar archivos de Origen
print("--- [Inicio - Recuperar archivos de Origen] -----------")
obtenerArchivos = Tareas("get")

print("---------- [ListToGetOrigen] -----------")
obtenerArchivos.ListToGetOrigen()
print("---------- [GetOrigen] -----------")
obtenerArchivos.GetOrigen()
print("---------- [PutDestino] -----------")
obtenerArchivos.PutDestino()
print("--- [Fin - Recuperar archivos de Origen] -----------")

#Verificar que archivos se eliminaron del Origen
print("--- [Inicio - Verificar que archivos eliminados del Origen -----------")
eliminarArchivosGet = Tareas("get")
#Marcar los archivos para eliminar en el Destino
print("---------- [ListToDeleteDestino] -----------")
eliminarArchivosGet.ListToDeleteDestino()
#Eliminar archivo del Destino
print("---------- [DeleteDestino] -----------")
eliminarArchivosGet.DeleteDestino()
print("--- [Fin - Verificar que archivos eliminados del Origen -----------")
