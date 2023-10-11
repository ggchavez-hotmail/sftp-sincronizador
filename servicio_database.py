# Get the database using the method we defined in pymongo_test_insert file
from conector_database import Db

conexion_db = None
db_name = None
collection_name = None

class Db_Options:
    def __init__(self, conexion_db, db_name, collection_name):
        print("Db_Options_init")
        db = Db(conexion_db, db_name)
        self.collection_name = db.get_collection_name(collection_name)

    def insert_one(self, item):
        self.collection_name.insert_one(item)

    def find_all(self):
        item_details = self.collection_name.find()
        # for item in item_details:
        #    # This does not give a very readable output
        #    print(item)

        return item_details

    def find_item(self, item):
        #print(item)
        item_details = self.collection_name.find(item)
        #for item_res in item_details:
        #   # This does not give a very readable output
        #   print(item_res)

        return item_details

    def count_documents_by_item(self, item):
        count = int(self.collection_name.count_documents(item))
        # This does not give a very readable output
        # print(count)

        return count

    def update_one(self, item_id, item_update):
        #print(item_id)
        #print(item_update)
        self.collection_name.update_one(
            item_id, item_update)

    def update_many(self, item_id, item_update):
        #print(item_id)
        #print(item_update)
        self.collection_name.update_many(
            item_id, item_update)
