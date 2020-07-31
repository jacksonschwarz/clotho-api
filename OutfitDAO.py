from DbHelper import DbHelper

from utils import translateWardrobeListObj, translateOutfitListObj

class OutfitDAO:
    __db = None
    def __init__(self):
        self.__db = DbHelper()
    """
    Get a specific outfit id 
    """
    def getOutfitById(self, outfitID):
        return self.__db.read("SELECT * FROM outfits WHERE id = %s", (outfitID,))
    """
    Gets all outfits owned by a specific user
    """
    def getOutfitsByOwner(self, ownerId):
        return self.__db.read("SELECT * FROM outfits WHERE owner = %s", (ownerId,))

    """
    Gets all outfits from all users since a certain timestamp
    """
    def getOutfitsSinceTimestamp(self, timestamp, ownerId):
        return self.__db.read("select * from outfits where extract(epoch from time_created) > %s::int and owner = %s::uuid", (timestamp,ownerId))
    """
    Gets the user's historical outfit record. Takes in an ownerID for the user, and a timestamp for the range time for the history
    """
    def getUserRecord(self, ownerId, timestamp):
        return self.__db.read("select * from outfits where extract(epoch from time_created) > %s::int AND owner = %s", (timestamp, ownerId))
    """
    Adds an outfit using the specified definition.
    """
    def addOutfit(self, outfitDef):
        try:
            self.__db.write("INSERT INTO outfits (items, score, passed_rules, owner) VALUES (%s::uuid[], %s, %s, %s)", 
            (outfitDef["items"], outfitDef["score"], outfitDef["passed_rules"], outfitDef["owner"]))
            return 1
        except Exception as error:
            return error
    """
    Removes the outfit with the specified ID
    """
    def removeOutfit(self, outfitId):
        try:
            self.__db.write("DELETE FROM outfits WHERE id = %s", (outfitId, ))
            return 1
        except Exception as error:
            return error