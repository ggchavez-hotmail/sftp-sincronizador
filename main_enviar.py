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
