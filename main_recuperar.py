from operacion import Tareas

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
