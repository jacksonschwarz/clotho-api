from DbHelper import DbHelper

class WardrobeDAO:
    __db = None;
    def __init__(self):
        self.__db = DbHelper()
    """
    Gets the wardrobe of a specified user given the user ID
    """
    def getWardrobe(self, userId):
        return self.__db.read("select * from wardrobe where ARRAY[id]::uuid[] <@ (select wardrobe from user_profiles where id = %s)", (userId,)).fetchall()
    """
    Gets a wardrobe item via the item's UUID
    """
    def getItemById(self, id):
        return self.__db.read("SELECT * FROM wardrobe WHERE id = %s", (id,)).fetchall()

    """
    Gets a wardrobe item, or a list of wardrobe items, via the item's name.
    """
    def getItemByName(self, name):
        return self.__db.read("SELECT * from wardrobe WHERE name = %s", (name,)).fetchall()
    """
    Gets a wardrobe item, or a list of wardrobe items,  via the item's type.
    """
    def getItemByType(self, clothingType):
        return self.__db.read("SELECT * from wardrobe WHERE type = %s", (clothingType,)).fetchall()
    """
    Gets a wardrobe item, or a list of wardrobe items, via the item's section
    """
    def getItemBySection(self, section):
        return self.__db.read("SELECT * from wardrobe WHERE section = %s", (section,)).fetchall()
    """
    Gets a wardrobe item that has ANY of the matching tags
    """
    def getItemByAnyTags(self, tags):
        arrayStatement = "ARRAY%s" % str(tags)
        return self.__db.read("SELECT * from wardrobe WHERE tags @> %s" % arrayStatement, None).fetchall()

    """
    Adds an item with the given specification to the wardrobe database.
    """
    def addItem(self, payload):
        try:
            itemObject = payload["item"]
            self.__db.write("INSERT INTO wardrobe (id, name, section, type, tags) VALUES(%s, %s, %s, %s, %s)", 
            (itemObject["id"], itemObject["name"], itemObject["section"], itemObject["type"], itemObject["tags"]))
            userId = payload["userId"]
            self.__db.write("UPDATE user_profiles SET wardrobe = wardrobe || %s::uuid WHERE id = %s", (itemObject["id"], userId))
            return 1
        except Exception as error:
            return error

    """
    Adds a tag to the item with the specified ID
    """
    def addItemTags(self, id, tags):
        try:
            self.__db.write("UPDATE wardrobe SET tags = tags || %s WHERE id = %s", (tags, id))
            return 1
        except Exception as error:
            return error
    """
    Statically sets the item tags of an iteam with the specified ID
    This could potentially be used to bulk add and remove tags as well. 
    """
    def setItemTags(self, id, tags):
        try:
            self.__db.write("UPDATE wardrobe SET tags = %s WHERE id = %s", (tags, id))
            return 1
        except Exception as error:
            return error
    
    """
    Updates the entire Item Object, based on the set Id
    """
    def updateItem(self, id, newItemObject):
        query = "UPDATE wardrobe SET"
        params = []
        if "name" in newItemObject.keys():
            query += " name = %s,"
            params.append(newItemObject["name"])
        if "section" in newItemObject.keys():
            query += " section = %s,"
            params.append(newItemObject["section"])
        if "type" in newItemObject.keys():
            query += " type = %s,"
            params.append(newItemObject["type"])
        if "tags" in newItemObject.keys():
            query += " tags = %s,"
            params.append(newItemObject["tags"])
        query = query[0:-1]
        query += " WHERE id = %s"
        params.append(id)
        try:
            self.__db.write(query, tuple(params))
            return 1
        except Exception as error:
            return error
    def removeItem(self, id):
        try:
            self.__db.write("DELETE FROM wardrobe WHERE id = %s", (id,))
            return 1
        except Exception as error:
            return error



