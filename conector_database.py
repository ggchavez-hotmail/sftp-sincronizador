from pymongo import MongoClient

client = None
db_name = None

class Db:
    def __init__(self, conexion_db, db_name):
        print("Db_init")
        try:
            # Provide the mongodb atlas url to connect python to mongodb using pymongo
            # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
            self.client = MongoClient(conexion_db)
            # Create the database for our example (we will use the same database throughout the tutorial
            self.db_name = self.client[db_name]

        except Exception as err:
            print(f"Db_init {err}")

    def get_collection_name(self, collection_name):
        print(collection_name)
        return self.db_name[collection_name]

    def __exit__(self):
        self.client.close()
        print("Conexion cerrada")
