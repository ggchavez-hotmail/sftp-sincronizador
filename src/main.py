from logzero import logger
from operacion import Tareas

verificar_estado_proceso = Tareas("verificar")
if verificar_estado_proceso.verificar_estado_proceso() == 0:
    #Enviar archivos al Origen
    logger.info("--- [Inicio - Enviar archivos al Origen] -----------")
    enviarArchivos = Tareas("put")

    logger.info("---------- [ListToGetOrigen] -----------")
    enviarArchivos.ListToGetOrigen()
    logger.info("---------- [GetOrigen] -----------")
    enviarArchivos.GetOrigen()
    logger.info("---------- [PutDestino] -----------")
    enviarArchivos.PutDestino()
    logger.info("--- [Fin - Enviar archivos al Origen] -----------")

    #Verificar que archivos se eliminaron del Origen
    logger.info("--- [Inicio - Verificar que archivos eliminados del Origen -----------")
    eliminarArchivosPut = Tareas("put")
    #Marcar los archivos para eliminar en el Destino
    logger.info("---------- [ListToDeleteDestino] -----------")
    eliminarArchivosPut.ListToDeleteDestino()
    #Eliminar archivo del Destino
    logger.info("---------- [DeleteDestino] -----------")
    eliminarArchivosPut.DeleteDestino()
    logger.info("--- [Fin - Verificar que archivos eliminados del Origen -----------")

    #Recuperar archivos de Origen
    logger.info("--- [Inicio - Recuperar archivos de Origen] -----------")
    obtenerArchivos = Tareas("get")

    logger.info("---------- [ListToGetOrigen] -----------")
    obtenerArchivos.ListToGetOrigen()
    logger.info("---------- [GetOrigen] -----------")
    obtenerArchivos.GetOrigen()
    logger.info("---------- [PutDestino] -----------")
    obtenerArchivos.PutDestino()
    logger.info("--- [Fin - Recuperar archivos de Origen] -----------")

    #Verificar que archivos se eliminaron del Origen
    logger.info("--- [Inicio - Verificar que archivos eliminados del Origen -----------")
    eliminarArchivosGet = Tareas("get")
    #Marcar los archivos para eliminar en el Destino
    logger.info("---------- [ListToDeleteDestino] -----------")
    eliminarArchivosGet.ListToDeleteDestino()
    #Eliminar archivo del Destino
    logger.info("---------- [DeleteDestino] -----------")
    eliminarArchivosGet.DeleteDestino()
    logger.info("--- [Fin - Verificar que archivos eliminados del Origen -----------")

    #Finalizar proceso
    verificar_estado_proceso.actualizar_estado_proceso()