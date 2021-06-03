import os
import psycopg2

if("PRODUCTION" in os.environ):
    DATABASE_URL = "{POSTGRES_SQL_FILE}"
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
else:
    DATABASE_URL = "postgresql://localhost"
    conn = psycopg2.connect(DATABASE_URL)



class DbHelper:
    __connection = None
    __cursor = None
    def __init__(self):
        self.__connection = psycopg2.connect(DATABASE_URL)
        self.__cursor = self.__connection.cursor()
    """
        Sends a query to the database, used for read operations
    """
    def read(self, query, params):
        self.__cursor.execute(query, params)
        print(self.__cursor.query)
        return self.__cursor
    """
        Sends a query to the database, but commits the change. Used for write operations
    """
    def write(self, query, params):
        self.__cursor.execute(query, params)
        print(self.__cursor.query)
        self.__connection.commit()
        return self.__cursor
    def close(self):
        self.__connection.close()
        
