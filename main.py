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
eliminarArchivos = Tareas("get")
#Marcar los archivos para eliminar en el Destino
print("---------- [ListToDeleteDestino] -----------")
eliminarArchivos.ListToDeleteDestino()
#Eliminar archivo del Destino
print("---------- [DeleteDestino] -----------")
eliminarArchivos.DeleteDestino()
print("--- [Fin - Verificar que archivos eliminados del Origen -----------")
