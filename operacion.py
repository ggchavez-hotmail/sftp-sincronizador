from servicio_sftp import Sftp_Options
from servicio_database import Db_Options
from config_settings import Get_Params

class Tareas():
    def __init__(self, proceso):  
        self.proceso = proceso   
        self.params = Get_Params()
        # Recuperar datos parametros
        self.db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLPARAMS)
        
    def ListToGetOrigen(self):
        casillas = self.db.find_item({"operacion": f"{self.proceso}" })

        for casilla in casillas:
            print(casilla)

            sftp = Sftp_Options(casilla["remote_sftp_purl"],
                                casilla["privateKeyFilePath"])

            resultado = sftp.listdir_attr(casilla["remote_list_path"])
            print(f"codigo retorno: {sftp.cod_status}")
            print(f"mensaje retorno: {sftp.msg_status}")
            print(resultado)
            
            # Que no hubo error al recuperar datos
            if (sftp.cod_status == 0):
                if (resultado != None):
                    db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLJOURNAL)
                    for item in resultado:
                        item_buscar = {"file_name": f"{item[0]}", "st_mode": f"{item[1]}",
                                       "st_size": f"{item[2]}", "st_atime": f"{item[3]}", "st_mtime": f"{item[4]}",
                                       "casilla": casilla["_id"], "operacion": f"{self.proceso}"}
                        count_documents = db.count_documents_by_item(item_buscar)
                        if (count_documents == 0):
                            item_insertar = {"file_name": f"{item[0]}", "st_mode": f"{item[1]}", "st_size": f"{item[2]}",
                                            "st_atime": f"{item[3]}", "st_mtime": f"{item[4]}", "casilla": casilla["_id"],
                                            "operacion": f"{self.proceso}" ,"estado": "listado"}
                            db.insert_one(item_insertar)

    def GetOrigen(self):        
        casillas = self.db.find_item({"operacion": f"{self.proceso}" })

        for casilla in casillas:
            print(casilla)

            sftp = Sftp_Options(casilla["remote_sftp_purl"],
                                casilla["privateKeyFilePath"])

            db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLJOURNAL)
            existe_item_en_db = db.find_item(
                {"casilla": casilla["_id"], "operacion": f"{self.proceso}", "estado": "listado"})
            print(casilla["pivot_path"])
            print(casilla["remote_path"])
            local_path = casilla["pivot_path"]
            remote_path = casilla["remote_path"]

            for item in existe_item_en_db:
                id = item['_id']
                file_name = item['file_name']
                print(f"{id}")
                print(f"{file_name}")
                sftp.mget(f"{local_path}{file_name}",
                        f"{remote_path}{file_name}")
                print(f"codigo retorno: {sftp.cod_status}")
                print(f"mensaje retorno: {sftp.msg_status}")
                if (sftp.cod_status == 0):
                    db.update_one({"_id": id}, {
                        "$set": {"estado": "recuperado"}})

    def PutDestino(self):
        casillas = self.db.find_item({"operacion": f"{self.proceso}" })

        for casilla in casillas:
            print(casilla)

            sftp = Sftp_Options(casilla["local_sftp_purl"],
                                casilla["privateKeyFilePath"])

            db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLJOURNAL)
            existe_item_en_db = db.find_item(
                {"casilla": casilla["_id"], "operacion": f"{self.proceso}", "estado": "recuperado"})
            print(casilla["pivot_path"])
            print(casilla["local_path"])
            local_path = casilla["pivot_path"]
            remote_path = casilla["local_path"]

            for item in existe_item_en_db:
                id = item['_id']
                file_name = item['file_name']
                print(f"{id}")
                print(f"{file_name}")
                sftp.mput(f"{local_path}{file_name}",
                        f"{remote_path}{file_name}")
                print(f"codigo retorno: {sftp.cod_status}")
                print(f"mensaje retorno: {sftp.msg_status}")
                if (sftp.cod_status == 0):
                    db.update_one({"_id": id}, {
                        "$set": {"estado": "finalizado"}})

    def ListToDeleteOrigen(self):
        casillas = self.db.find_item({"operacion": f"{self.proceso}" })

        db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLJOURNAL)
        
        for casilla in casillas:
            print(casilla)

            sftp = Sftp_Options(casilla["remote_sftp_purl"],
                                casilla["privateKeyFilePath"])

            resultado = sftp.listdir_attr(casilla["remote_list_path"])
            print(f"codigo retorno: {sftp.cod_status}")
            print(f"mensaje retorno: {sftp.msg_status}")
            print(resultado)
            
            items_omitir = []
            # Que no hubo error al recuperar datos
            if (sftp.cod_status == 0):
                if (resultado != None):
                    for item in resultado:
                        item_buscar = { "$and" : [
                                        {"file_name": f"{item[0]}", "st_mode": f"{item[1]}",
                                         "st_size": f"{item[2]}", "st_atime": f"{item[3]}", "st_mtime": f"{item[4]}",
                                         "casilla": casilla["_id"], "operacion": f"{self.proceso}"},
                                        {"estado": { "$ne" : "eliminar" } }]}
                        
                        items_encontrados = db.find_item(item_buscar)
                        
                        for item_encontrado in items_encontrados:
                            id = item_encontrado['_id']
                            items_omitir.append(id)

            if (items_omitir != []):
                db.update_many({ "$and" : [{ "_id": { "$ne" : items_omitir } }, 
                                           { "casilla": casilla["_id"], "operacion": f"{self.proceso}" }]},
                               { "$set": {"estado": "eliminar"}})
            else:
                db.update_many({ "casilla": casilla["_id"], "operacion": f"{self.proceso}" },
                               { "$set": {"estado": "eliminar"}})