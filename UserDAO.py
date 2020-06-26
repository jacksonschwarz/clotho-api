from DbHelper import DbHelper

class UserDAO:
    __db = None;
    def __init__(self):
        self.__db = DbHelper()
    """
    Gets a user based on the specific UUID
    Parameters: UUID of the target user.
    """
    def getUserById(self, userId):
        return self.__db.read("SELECT * FROM user_profiles WHERE id = %s", (userId,)).fetchall()
    """
    Gets the user by a username-password pair. 
    Parameter: Username and Password
    """
    def getUserByLogin(self, username, password):
        return self.__db.read("SELECT * from user_profiles WHERE username = %s and password = %s", (username, password)).fetchall()
    def addUser(self, userDef):
        try:
            self.__db.write("INSERT INTO user_profiles (username, email_address, password, complexion, undertones, wardrobe) VALUES (%s, %s, %s, %s, %s, %s)",
            (userDef["username"],userDef["email_address"], userDef["password"], userDef["complexion"], userDef["undertones"], userDef["wardrobe"]))
            return 1
        except Exception as error:
            return error
    """
    Updates user with the supplied specification.
    Parameters: A userID and a userDef
    """
    def updateUser(self, userId, userDef):
        query = "UPDATE user_profiles SET"
        params = []
        if "username" in userDef.keys():
            query += " username = %s,"
            params.append(userDef["username"])
        if "email_address" in userDef.keys():
            query += " email_address = %s,"
            params.append(userDef["email_address"])
        if "password" in userDef.keys():
            query += " password = %s,"
            params.append(userDef["password"])
        if "complexion" in userDef.keys():
            query += " complexion = %s,"
            params.append(userDef["complexion"])
        if "undertones" in userDef.keys():
            query += " undertones = %s,"
            params.append(userDef["undertones"])
        if "wardrobe" in userDef.keys():
            query += " wardrobe = %s,"
            params.append(userDef["wardrobe"])
        query = query[0:-1]
        query += " WHERE id = %s"
        params.append(userId)
        try:
            self.__db.write(query, tuple(params))
            return 1
        except Exception as error:
            return error
    """
    Removes a user from the database
    Parameters: A userID
    """
    def removeUser(self, userId):
        try:
            self.__db.write("DELETE FROM user_profiles WHERE id = %s", (userId,))
            return 1
        except Exception as error:
            return error