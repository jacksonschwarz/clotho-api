from DbHelper import DbHelper

class UserDAO:
    __db = None;
    def __init__(self):
        self.__db = DbHelper()
    def getUserById(self, id):
        self.__db.read("SELECT * FROM users WHERE id = %s", (id,))