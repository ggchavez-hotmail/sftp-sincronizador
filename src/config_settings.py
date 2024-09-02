import os
from dotenv import load_dotenv

class Get_Params:
    CONEXIONDB = None
    DBNAME = None
    COLLECTIONNAME = None
    DBPARAMS = None
    ENCRYPTION_KEY = None
    BLOQUES = None
    
    def __init__(self):
      load_dotenv()
      self.DBCONEXION = os.environ["DB_CONEXION"]
      self.DBNAME = os.environ["DB_NAME"]
      self.DBCLLJOURNAL = os.environ["DB_CLL_JOURNAL"]
      self.DBCLLPARAMS = os.environ["DB_CLL_PARAMS"]
      self.ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
      self.BLOQUES = os.environ["BLOQUES"]
      
      
      
