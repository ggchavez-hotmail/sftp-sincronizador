from pymongo import MongoClient

client = None
db_name = None

class Db:
    def __init__(self, conexion_db, db_name, collection_name):
        self.conexion_db = conexion_db
        self.db_name = db_name
        self.collection_name = collection_name
            
    def connect(self):        
        try:
            # Provide the mongodb atlas url to connect python to mongodb using pymongo
            # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
            self.client = MongoClient(self.conexion_db)
            # Create the database for our example (we will use the same database throughout the tutorial
            db = self.client[self.db_name]
            #print(f"collection_name: {collection_name}")
            self.collection = db[self.collection_name]
            #print("Conexion DB OK")
        except Exception as err:
            print(f"Error Conexion DB: {err}")
            raise Exception(err)
            
    def insert_one(self, item):
        try:
            self.collection.insert_one(item)
        except Exception as err:
            print(f"insert_one - err: {err}")
            raise Exception(err)
            
    def find(self):
        try:
            return self.collection.find()
        except Exception as err:
            print(f"find_all - err: {err}")
            raise Exception(err)
            
    def find_item(self, item):
        try:
            return self.collection.find(item)
        except Exception as err:
            print(f"find_item - err: {err}")
            raise Exception(err)
        
    def count_documents_item(self, item):
        try:
            return self.collection.count_documents(item)
        except Exception as err:
            print(f"count_documents - err: {err}")
            raise Exception(err)
        
    def update_one(self, item_id, item_update):
        try:
            self.collection.update_one(item_id, item_update)
        except Exception as err:
            print(f"update_one - err: {err}")
            raise Exception(err)
        
    def update_many(self, item_id, item_update):
        try:
            self.collection.update_many(item_id, item_update)
        except Exception as err:
            print(f"update_many - err: {err}")
            raise Exception(err)
        
    def close(self):
        try:
            self.client.close()
            #print("Cerrada Conexion DB")
        except Exception as err:
            print(f"close - err: {err}")
            raise Exception(err)
