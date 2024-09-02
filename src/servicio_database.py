# Get the database using the method we defined in pymongo_test_insert file
from conector_database import Db

conexion_db = None
db_name = None
collection_name = None

class Db_Options:
    def __init__(self, conexion_db, db_name, collection_name):
        self.conexion_db = conexion_db
        self.db_name = db_name
        self.collection_name = collection_name

    def open_connexion(self):
        self.db = Db(self.conexion_db, self.db_name, self.collection_name)
        self.db.connect()
        
    def insert_one(self, item):
        try:
            self.open_connexion()
            self.db.insert_one(item)
            
            self.cod_status = 0
            self.msg_status = "Proceso OK"
            
        except Exception as err:
            self.cod_status = 1
            self.msg_status = f"Error insert_one: {err}"
            
        finally:
            self.close_connexion()

    def find_all(self):        
        try:
            self.open_connexion()
            item_details = list(self.db.find())
            # for item in item_details:
            #    # This does not give a very readable output
            #    print(item)
            
            self.cod_status = 0
            self.msg_status = "Proceso OK"
            return item_details
            
        except Exception as err:
            self.cod_status = 1
            self.msg_status = f"Error find_all: {err}"
            
        finally:
            self.close_connexion()


    def find_item(self, item):
        try:
            self.open_connexion()
            #print(item)
            item_details = list(self.db.find_item(item))
            #for item_res in item_details:
            #   # This does not give a very readable output
            #   print(item_res)
            
            self.cod_status = 0
            self.msg_status = "Proceso OK"
            return item_details
            
        except Exception as err:
            self.cod_status = 1
            self.msg_status = f"Error find_all: {err}"
            
        finally:
            self.close_connexion()

    def count_documents_by_item(self, item):
        try:
            self.open_connexion()
            count = int(self.db.count_documents_item(item))
            # This does not give a very readable output
            # print(count)
            
            self.cod_status = 0
            self.msg_status = "Proceso OK"
            return count
                    
        except Exception as err:
            self.cod_status = 1
            self.msg_status = f"Error find_all: {err}"
            
        finally:
            self.close_connexion()

    def update_one(self, item_id, item_update):
        try:
            self.open_connexion()
            #print(item_id)
            #print(item_update)
            self.db.update_one(item_id, item_update)
            
            self.cod_status = 0
            self.msg_status = "Proceso OK"
                    
        except Exception as err:
            self.cod_status = 1
            self.msg_status = f"Error find_all: {err}"
            
        finally:
            self.close_connexion()

    def update_many(self, item_id, item_update):
        try:
            self.open_connexion()
            #print(item_id)
            #print(item_update)
            self.db.update_many(item_id, item_update)
        
            self.cod_status = 0
            self.msg_status = "Proceso OK"
                    
        except Exception as err:
            self.cod_status = 1
            self.msg_status = f"Error find_all: {err}"
            
        finally:
            self.close_connexion()
    
    def __exit__(self):
        self.close_connexion()
        
    def close_connexion(self):
        self.db.close()