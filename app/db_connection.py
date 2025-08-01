import psycopg2
from dotenv import load_dotenv
import os
class DBConnection:
    def __init__(self):
        load_dotenv()
        self.conn = psycopg2.connect(
               dbname = os.getenv("DB_Name"),
               user = os.getenv("DB_Username"),
               password = os.getenv("DB_password"),
               host = os.getenv("DB_host"),
               port =  os.getenv("DB_Port")
        )

        self.cursor = self.conn.cursor()

    def close(self):
            self.cursor.close()
            self.conn.close()
