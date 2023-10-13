from operacion import Tareas

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

