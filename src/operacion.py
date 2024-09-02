from logzero import logger
from servicio_sftp import Sftp_Options
from servicio_database import Db_Options
from config_settings import Get_Params
#import os
from pathlib import Path
from criptor import Criptor

class Tareas():
    def __init__(self, proceso):  
        self.proceso = proceso   
        self.params = Get_Params()
        self.criptor = Criptor()
        
    def verificar_estado_proceso(self):
        item_buscar = { "proceso_activo": "true" }
        db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, "validar")
        count_documents = db.count_documents_by_item(item_buscar)
        if (count_documents == 0):
            item_insertar = {"proceso_activo": "true"}
            db.insert_one(item_insertar)
            logger.info("Proceso nuevo")
        else:
            logger.info("Existe un proceso activo")
            
        return count_documents
            
    def actualizar_estado_proceso(self):
        db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, "validar")
        db.update_many({ "proceso_activo": "true" },
                                { "$set": {"proceso_activo": "false"}})
        logger.info("Proceso finalizado")
        
    def recuperar_casillas(self):
        # Recuperar datos parametros
        self.db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLPARAMS)
        casillas = self.db.find_item({"operacion": f"{self.proceso}" })
        
        # Desencriptar
        if(casillas != None):
            for casilla in casillas:
                casilla["privateKeyFilePath"] = self.criptor.decrypt(casilla["privateKeyFilePath"])
                casilla["local_sftp_purl"] = self.criptor.decrypt(casilla["local_sftp_purl"])
                casilla["local_path"] = self.criptor.decrypt(casilla["local_path"])
                casilla["remote_sftp_purl"] = self.criptor.decrypt(casilla["remote_sftp_purl"])
                casilla["remote_list_path"] = self.criptor.decrypt(casilla["remote_list_path"])
                casilla["remote_path"] = self.criptor.decrypt(casilla["remote_path"])
                casilla["pivot_path"] = self.criptor.decrypt(casilla["pivot_path"])
        
        #print(casillas)
        return casillas
        
    def ListToGetOrigen(self):
        # Recuperar datos parametros
        casillas = self.recuperar_casillas()
        
        if(casillas != None):
            ver = casillas[0]
            ver = ver["remote_sftp_purl"]
            logger.info(f"-remote_sftp_purl: {ver}")
                
            for casilla in casillas:
                #logger.info(casilla)

                sftp = Sftp_Options(casilla["remote_sftp_purl"],
                                    casilla["privateKeyFilePath"])

                resultado = sftp.listdir_attr(casilla["remote_list_path"])
                #logger.info(f"codigo retorno: {sftp.cod_status}")
                #logger.info(f"mensaje retorno: {sftp.msg_status}")
                #logger.info(resultado)
                
                # Que no hubo error al recuperar datos
                if (sftp.cod_status == 0):
                    if (resultado != None):
                        for item in resultado:
                            ver = item[0]
                            logger.info(f"---file_name: {ver}")
                            
                            item_buscar = { "$and" : [{"file_name": f"{item[0]}", "st_mode": f"{item[1]}",
                                        "st_size": f"{item[2]}", "st_atime": f"{item[3]}", "st_mtime": f"{item[4]}",
                                        "casilla": casilla["_id"], "operacion": f"{self.proceso}"},
                                        {"estado": { "$nin" : ["eliminar","eliminado"] } }]}
                            db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLJOURNAL)
                            count_documents = db.count_documents_by_item(item_buscar)
                            if (count_documents == 0):
                                prioridad = self.PrioridadExtension(f"{item[0]}")
                                item_insertar = {"file_name": f"{item[0]}", "st_mode": f"{item[1]}", "st_size": f"{item[2]}",
                                                "st_atime": f"{item[3]}", "st_mtime": f"{item[4]}", "prioridad" : prioridad,
                                                "casilla": casilla["_id"], "operacion": f"{self.proceso}" ,"estado": "listado"}
                                db.insert_one(item_insertar)
                                logger.info("---->insertado - listado")
                    

    def GetOrigen(self):        
        # Recuperar datos parametros
        casillas = self.recuperar_casillas()
        
        if(casillas != None):
            ver = casillas[0]
            ver = ver["remote_sftp_purl"]
            logger.info(f"-remote_sftp_purl: {ver}")
            
            for casilla in casillas:
                #logger.info(casilla)

                sftp = Sftp_Options(casilla["remote_sftp_purl"],
                                    casilla["privateKeyFilePath"])

                db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLJOURNAL)
                existe_item_en_db = db.find_item(
                    {"casilla": casilla["_id"], "operacion": f"{self.proceso}", "estado": "listado"})
                #logger.info(casilla["pivot_path"])
                #logger.info(casilla["remote_path"])
                local_path = casilla["pivot_path"]
                remote_path = casilla["remote_path"]
                
                if(existe_item_en_db != None):
                    #ordenar resultado por fecha modificacion (asc) y prioridad (desc)
                    existe_item_en_db.sort(key=lambda x: (x["st_mtime"], -x["prioridad"]))
                    
                    for item in existe_item_en_db:
                        
                        id = item['_id']
                        file_name = item['file_name']
                        #logger.info(f"id: {id}")
                        logger.info(f"---file_name: {file_name}")
                        
                        sftp.mget(f"{local_path}{file_name}",
                                f"{remote_path}{file_name}")
                        #logger.info(f"codigo retorno: {sftp.cod_status}")
                        #logger.info(f"mensaje retorno: {sftp.msg_status}")
                        if (sftp.cod_status == 0):
                            db.update_one({"_id": id}, {
                                "$set": {"estado": "recuperado"}})
                            logger.info("---->actualizado - recuperado")

    def PutDestino(self):
        # Recuperar datos parametros
        casillas = self.recuperar_casillas()

        if(casillas != None):
            ver = casillas[0]
            ver = ver["local_sftp_purl"]
            logger.info(f"-local_sftp_purl: {ver}")
            
            for casilla in casillas:
                #logger.info(casilla)

                sftp = Sftp_Options(casilla["local_sftp_purl"],
                                    casilla["privateKeyFilePath"])

                db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLJOURNAL)
                existe_item_en_db = db.find_item(
                    {"casilla": casilla["_id"], "operacion": f"{self.proceso}", "estado": "recuperado"})
                #logger.info(casilla["pivot_path"])
                #logger.info(casilla["local_path"])
                local_path = casilla["pivot_path"]
                remote_path = casilla["local_path"]
                
                if(existe_item_en_db != None):
                    #ordenar resultado por fecha modificacion (asc) y prioridad (desc)
                    existe_item_en_db.sort(key=lambda x: (x["st_mtime"], -x["prioridad"]))
                    
                    for item in existe_item_en_db:
                        id = item['_id']
                        file_name = item['file_name']
                        #logger.info(f"id: {id}")
                        logger.info(f"---file_name: {file_name}")
                        
                        sftp.mput(f"{local_path}{file_name}",
                                f"{remote_path}{file_name}")
                        #logger.info(f"codigo retorno: {sftp.cod_status}")
                        #logger.info(f"mensaje retorno: {sftp.msg_status}")
                        if (sftp.cod_status == 0):
                            db.update_one({"_id": id}, {
                                "$set": {"estado": "finalizado"}})
                            logger.info("---->actualizado - finalizado")
        
    def ListToDeleteDestino(self):
        # Recuperar datos parametros
        casillas = self.recuperar_casillas()
        
        if(casillas != None):
            ver = casillas[0]
            ver = ver["remote_sftp_purl"]
            logger.info(f"-remote_sftp_purl: {ver}")
            
            for casilla in casillas:
                #logger.info(casilla)

                sftp = Sftp_Options(casilla["remote_sftp_purl"],
                                    casilla["privateKeyFilePath"])

                resultado = sftp.listdir_attr(casilla["remote_list_path"])
                #logger.info(f"codigo retorno: {sftp.cod_status}")
                #logger.info(f"mensaje retorno: {sftp.msg_status}")
                #logger.info(resultado)
                
                items_omitir = []
                db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLJOURNAL)
                # Que no hubo error al recuperar datos
                if (sftp.cod_status == 0):
                    if (resultado != None):
                        for item in resultado:
                            #item_buscar = { "$and" : [
                            #                {"file_name": f"{item[0]}", "st_mode": f"{item[1]}",
                            #                 "st_size": f"{item[2]}", "st_atime": f"{item[3]}", "st_mtime": f"{item[4]}",
                            #                 "casilla": casilla["_id"], "operacion": f"{self.proceso}"},
                            #                {"estado": { "$nin" : ["eliminar","eliminado"] } }]}
                            
                            ver = item[0]
                            logger.info(f"---file_name: {ver}")
                            
                            #Solo interesa el nombre del archivo.
                            item_buscar = { "$and" : [
                                            {"file_name": f"{item[0]}","casilla": casilla["_id"], "operacion": f"{self.proceso}"},
                                            {"estado": { "$nin" : ["eliminar","eliminado"] } }
                                                     ]}
                            
                            items_encontrados = db.find_item(item_buscar)
                            #logger.info(f"items_encontrados: {items_encontrados}")
                            if(items_encontrados != None):
                                for item_encontrado in items_encontrados:
                                    #logger.info(f"item_encontrado: {item_encontrado}")
                                    id = item_encontrado["_id"]
                                    #logger.info(f"----id: {id}")
                                    items_omitir.append(id)
                
                #logger.info(f"items_omitir: {items_omitir}")
                if (items_omitir != []):
                    db.update_many({ "$and" : [
                                    { "_id": { "$nin" : items_omitir } }, 
                                    { "casilla": casilla["_id"], "operacion": f"{self.proceso}" },
                                    {"estado": { "$nin" : ["eliminar","eliminado"] } }
                                              ]},
                                { "$set": {"estado": "eliminar"}})
                    logger.info("---->actualizado - eliminar (omitiendo)")
                else:
                    db.update_many({ "$and" :[
                                     { "casilla": casilla["_id"], "operacion": f"{self.proceso}" },
                                     {"estado": { "$nin" : ["eliminar","eliminado"] } }
                                             ]},
                                { "$set": {"estado": "eliminar"}})
                    logger.info("---->actualizado - eliminar")
            
    def DeleteDestino(self):
        # Recuperar datos parametros
        casillas = self.recuperar_casillas()

        if(casillas != None):
            ver = casillas[0]
            ver = ver["local_sftp_purl"]
            logger.info(f"-local_sftp_purl: {ver}")
            
            for casilla in casillas:
                #logger.info(casilla)

                sftp = Sftp_Options(casilla["local_sftp_purl"],
                                    casilla["privateKeyFilePath"])

                db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLJOURNAL)
                existe_item_en_db = db.find_item(
                    {"casilla": casilla["_id"], "operacion": f"{self.proceso}", "estado": "eliminar"})
                #logger.info(casilla["pivot_path"])
                #logger.info(casilla["local_path"])
                local_path = casilla["pivot_path"]
                remote_path = casilla["local_path"]
                
                if(existe_item_en_db != None):
                    for item in existe_item_en_db:
                        id = item['_id']
                        file_name = item['file_name']
                        #logger.info(f"id: {id}")
                        logger.info(f"---file_name: {file_name}")
                        
                        sftp.mdelete(f"{remote_path}{file_name}")
                        #logger.info(f"codigo retorno: {sftp.cod_status}")
                        #logger.info(f"mensaje retorno: {sftp.msg_status}")
                        if (sftp.cod_status == 0):
                            db.update_one({"_id": id}, {
                                "$set": {"estado": "eliminado"}})
                            logger.info("---->actualizado - eliminado")
                            
                        sftp.mdelete(f"{local_path}{file_name}")
                    

    def PrioridadExtension(self, archivo):
        prioridad = 0
        try:
            #se extrae extension del archivo 
            #_, extension = os.path.split(archivo)
            extension = Path(archivo).suffix
            #logger.info(f"extension: {extension}")
            if(extension == ".CTR"):
                prioridad = 1
        except Exception as err:
            logger.info(f"prioridad_extension - err: {err}")
        finally:
            return prioridad

        