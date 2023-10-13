from servicio_sftp import Sftp_Options
from servicio_database import Db_Options
from config_settings import Get_Params

class Tareas():
    def __init__(self, proceso):  
        self.proceso = proceso   
        self.params = Get_Params()
    
    def recuperar_casillas(self):
        # Recuperar datos parametros
        self.db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLPARAMS)
        casillas = self.db.find_item({"operacion": f"{self.proceso}" })
                    
        return casillas
        
    def ListToGetOrigen(self):
        # Recuperar datos parametros
        casillas = self.recuperar_casillas()
        
        if(casillas != None):
            ver = casillas[0]
            ver = ver["remote_sftp_purl"]
            print(f"-remote_sftp_purl: {ver}")
                
            for casilla in casillas:
                #print(casilla)

                sftp = Sftp_Options(casilla["remote_sftp_purl"],
                                    casilla["privateKeyFilePath"])

                resultado = sftp.listdir_attr(casilla["remote_list_path"])
                #print(f"codigo retorno: {sftp.cod_status}")
                #print(f"mensaje retorno: {sftp.msg_status}")
                #print(resultado)
                
                # Que no hubo error al recuperar datos
                if (sftp.cod_status == 0):
                    if (resultado != None):
                        for item in resultado:
                            ver = item[0]
                            print(f"---file_name: {ver}")
                            
                            item_buscar = { "$and" : [{"file_name": f"{item[0]}", "st_mode": f"{item[1]}",
                                        "st_size": f"{item[2]}", "st_atime": f"{item[3]}", "st_mtime": f"{item[4]}",
                                        "casilla": casilla["_id"], "operacion": f"{self.proceso}"},
                                        {"estado": { "$nin" : ["eliminar","eliminado"] } }]}
                            db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLJOURNAL)
                            count_documents = db.count_documents_by_item(item_buscar)
                            if (count_documents == 0):
                                item_insertar = {"file_name": f"{item[0]}", "st_mode": f"{item[1]}", "st_size": f"{item[2]}",
                                                "st_atime": f"{item[3]}", "st_mtime": f"{item[4]}", "casilla": casilla["_id"],
                                                "operacion": f"{self.proceso}" ,"estado": "listado"}
                                db.insert_one(item_insertar)
                                print("---->insertado - listado")
                    

    def GetOrigen(self):        
        # Recuperar datos parametros
        casillas = self.recuperar_casillas()
        
        if(casillas != None):
            ver = casillas[0]
            ver = ver["remote_sftp_purl"]
            print(f"-remote_sftp_purl: {ver}")
            
            for casilla in casillas:
                #print(casilla)

                sftp = Sftp_Options(casilla["remote_sftp_purl"],
                                    casilla["privateKeyFilePath"])

                db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLJOURNAL)
                existe_item_en_db = db.find_item(
                    {"casilla": casilla["_id"], "operacion": f"{self.proceso}", "estado": "listado"})
                #print(casilla["pivot_path"])
                #print(casilla["remote_path"])
                local_path = casilla["pivot_path"]
                remote_path = casilla["remote_path"]
                
                if(existe_item_en_db != None):
                    for item in existe_item_en_db:
                        
                        id = item['_id']
                        file_name = item['file_name']
                        #print(f"id: {id}")
                        print(f"---file_name: {file_name}")
                        
                        sftp.mget(f"{local_path}{file_name}",
                                f"{remote_path}{file_name}")
                        #print(f"codigo retorno: {sftp.cod_status}")
                        #print(f"mensaje retorno: {sftp.msg_status}")
                        if (sftp.cod_status == 0):
                            db.update_one({"_id": id}, {
                                "$set": {"estado": "recuperado"}})
                            print("---->actualizado - recuperado")

    def PutDestino(self):
        # Recuperar datos parametros
        casillas = self.recuperar_casillas()

        if(casillas != None):
            ver = casillas[0]
            ver = ver["local_sftp_purl"]
            print(f"-local_sftp_purl: {ver}")
            
            for casilla in casillas:
                #print(casilla)

                sftp = Sftp_Options(casilla["local_sftp_purl"],
                                    casilla["privateKeyFilePath"])

                db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLJOURNAL)
                existe_item_en_db = db.find_item(
                    {"casilla": casilla["_id"], "operacion": f"{self.proceso}", "estado": "recuperado"})
                #print(casilla["pivot_path"])
                #print(casilla["local_path"])
                local_path = casilla["pivot_path"]
                remote_path = casilla["local_path"]
                
                if(existe_item_en_db != None):
                    for item in existe_item_en_db:
                        id = item['_id']
                        file_name = item['file_name']
                        #print(f"id: {id}")
                        print(f"---file_name: {file_name}")
                        
                        sftp.mput(f"{local_path}{file_name}",
                                f"{remote_path}{file_name}")
                        #print(f"codigo retorno: {sftp.cod_status}")
                        #print(f"mensaje retorno: {sftp.msg_status}")
                        if (sftp.cod_status == 0):
                            db.update_one({"_id": id}, {
                                "$set": {"estado": "finalizado"}})
                            print("---->actualizado - finalizado")
        
    def ListToDeleteDestino(self):
        # Recuperar datos parametros
        casillas = self.recuperar_casillas()
        
        if(casillas != None):
            ver = casillas[0]
            ver = ver["remote_sftp_purl"]
            print(f"-remote_sftp_purl: {ver}")
            
            for casilla in casillas:
                #print(casilla)

                sftp = Sftp_Options(casilla["remote_sftp_purl"],
                                    casilla["privateKeyFilePath"])

                resultado = sftp.listdir_attr(casilla["remote_list_path"])
                #print(f"codigo retorno: {sftp.cod_status}")
                #print(f"mensaje retorno: {sftp.msg_status}")
                #print(resultado)
                
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
                            print(f"---file_name: {ver}")
                            
                            #Solo interesa el nombre del archivo.
                            item_buscar = { "$and" : [
                                            {"file_name": f"{item[0]}","casilla": casilla["_id"], "operacion": f"{self.proceso}"},
                                            {"estado": { "$nin" : ["eliminar","eliminado"] } }
                                                     ]}
                            
                            items_encontrados = db.find_item(item_buscar)
                            #print(f"items_encontrados: {items_encontrados}")
                            if(items_encontrados != None):
                                for item_encontrado in items_encontrados:
                                    #print(f"item_encontrado: {item_encontrado}")
                                    id = item_encontrado["_id"]
                                    #print(f"----id: {id}")
                                    items_omitir.append(id)
                
                #print(f"items_omitir: {items_omitir}")
                if (items_omitir != []):
                    db.update_many({ "$and" : [
                                    { "_id": { "$nin" : items_omitir } }, 
                                    { "casilla": casilla["_id"], "operacion": f"{self.proceso}" },
                                    {"estado": { "$nin" : ["eliminar","eliminado"] } }
                                              ]},
                                { "$set": {"estado": "eliminar"}})
                    print("---->actualizado - eliminar (omitiendo)")
                else:
                    db.update_many({ "$and" :[
                                     { "casilla": casilla["_id"], "operacion": f"{self.proceso}" },
                                     {"estado": { "$nin" : ["eliminar","eliminado"] } }
                                             ]},
                                { "$set": {"estado": "eliminar"}})
                    print("---->actualizado - eliminar")
            
    def DeleteDestino(self):
        # Recuperar datos parametros
        casillas = self.recuperar_casillas()

        if(casillas != None):
            ver = casillas[0]
            ver = ver["local_sftp_purl"]
            print(f"-local_sftp_purl: {ver}")
            
            for casilla in casillas:
                #print(casilla)

                sftp = Sftp_Options(casilla["local_sftp_purl"],
                                    casilla["privateKeyFilePath"])

                db = Db_Options(self.params.DBCONEXION, self.params.DBNAME, self.params.DBCLLJOURNAL)
                existe_item_en_db = db.find_item(
                    {"casilla": casilla["_id"], "operacion": f"{self.proceso}", "estado": "eliminar"})
                #print(casilla["pivot_path"])
                #print(casilla["local_path"])
                local_path = casilla["pivot_path"]
                remote_path = casilla["local_path"]
                
                if(existe_item_en_db != None):
                    for item in existe_item_en_db:
                        id = item['_id']
                        file_name = item['file_name']
                        #print(f"id: {id}")
                        print(f"---file_name: {file_name}")
                        
                        sftp.mdelete(f"{remote_path}{file_name}")
                        #print(f"codigo retorno: {sftp.cod_status}")
                        #print(f"mensaje retorno: {sftp.msg_status}")
                        if (sftp.cod_status == 0):
                            db.update_one({"_id": id}, {
                                "$set": {"estado": "eliminado"}})
                            print("---->actualizado - eliminado")
                            
                        sftp.mdelete(f"{local_path}{file_name}")
                    

