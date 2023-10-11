from operacion import Tareas

##Recuperar archivos de Origen
#obtenerArchivos = Tareas("get")
#
#obtenerArchivos.ListToGetOrigen()
#obtenerArchivos.GetOrigen()
#obtenerArchivos.PutDestino()
#
##Enviar archivos al Origen
#enviarArchivos = Tareas("put")
#
#enviarArchivos.ListToGetOrigen()
#enviarArchivos.GetOrigen()
#enviarArchivos.PutDestino()

#Verificar que archivos se eliminaron del Origen
#Marcar los archivos para eliminar en el Destino
eliminarArchivos = Tareas("get")
#eliminarArchivos.ListToDeleteDestino()


#Eliminar archivo del Destino
eliminarArchivos.DeleteDestino()