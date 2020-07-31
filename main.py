import os
import psycopg2
from flask import Flask, request
import simplejson as json

from WardrobeDAO import WardrobeDAO
from OutfitDAO import OutfitDAO
from UserDAO import UserDAO
from SuggestionGen import generate_suggestion

from utils import translateOutfitList, translateUserProfileList, translateWardrobe, translateWardrobeList
app = Flask(__name__)

__wdao = WardrobeDAO()
__odao = OutfitDAO()
__udao = UserDAO()
@app.route("/")
def index():
    return "Hello Clotho!"
"""
WARDROBE ROUTES
"""
"""
Parameters: User ID
Returns: The list of wardrobe elements for that user
"""
@app.route("/wardrobe/getWardrobe")
def getWardrobe():
    userID=request.args.get("id")
    results = __wdao.getWardrobe(userID)
    return translateWardrobeList(results)
"""
Parameters: Wardrobe Item ID
Returns: The wardrobe item corresponding to that ID (is unique)
"""
@app.route("/wardrobe/getItemById")
def getItemById():
    itemID=request.args.get("id")
    results = __wdao.getItemById(itemID)
    return translateWardrobeList(results)
@app.route("/wardrobe/getItemsByIdList", methods=["POST"])
def getItemsByIdList():
    itemIds = request.get_json()["idList"]
    results = __wdao.getItemsByIdList(itemIds)
    return translateWardrobeList(results)
"""
Parameters: Wardrobe Item Name
Returns: The wardrobe item corresponding to that name (may not be unique).
"""
@app.route("/wardrobe/getItemByName")
def getItembyName():
    name=request.args.get("name")
    results = __wdao.getItemByName(name)
    return translateWardrobeList(results)
"""
Parameters: Wardrobe Clothing Type
Returns: A list of items that are grouped by their clothing type.
"""
@app.route("/wardrobe/getItemByType")
def getItemByType():
    clothingType = request.args.get("type")
    results = __wdao.getItemByType(clothingType)
    return translateWardrobeList(results)
"""
Parameters: Wardrobe Section Type
Returns: A list of items that are grouped by their clothing section.
"""
@app.route("/wardrobe/getItemBySection")
def getItemBySection():
    section = request.args.get("section")
    results=__wdao.getItemBySection(section)
    return translateWardrobeList(results)
"""
Body: A list of Wardrobe Item Tags
Returns: Any wardrobe items with the specified tags in its 
"""
@app.route("/wardrobe/getItemByAnyTags")
def getItemByAnyTags():
    tags = request.get_json()["tags"]
    asciitags = [x.encode("ascii") for x in tags]
    results = __wdao.getItemByAnyTags(asciitags)
    return translateWardrobeList(results)
"""
Body: A Wardrobe Element object
Returns: A success message if it succeeds, an error message if it does not.
"""
@app.route("/wardrobe/addItem", methods=['POST'])
def addItem():
    payload = request.get_json()
    result = __wdao.addItem(payload)
    if (result == 1):
        return "Added object " + json.dumps(payload["item"]) + " to the user with the ID " + payload["userId"]
    else:
        return str(result)
"""
Parameters: Wardrobe Item ID, a wardrobe item tag
Returns: A confirmation message if the desired tag is added. 
"""
@app.route("/wardrobe/addItemTags", methods=['POST'])
def addItemTags():
    itemId = request.get_json()["id"]
    tagsToAdd = request.get_json()["tags"]
    result = __wdao.addItemTags(itemId, tagsToAdd)
    if (result == 1):
        return "Added tags " + json.dumps(tagsToAdd) + " to item with the id " + itemId 
    else:
        return str(result)
"""
Body:Wardrobe Item ID, a list of wardrobe item tags. 
Returns: A confirmation message when the specified list of tags is set to the specified object
"""
@app.route("/wardrobe/setItemTags", methods=['POST'])
def setItemTags():
    itemId = request.get_json()["id"]
    tagsToSet = request.get_json()["tags"]
    result = __wdao.setItemTags(itemId, tagsToSet)
    if (result == 1):
        return "Set tags " + str(tagsToSet) + " to item with the id " + itemId 
    else:
        return str(result)
"""
Body:Wardrobe Item ID, a wardrobe object
Returns: A confirmation when the wardrobe object has been updated. 
"""
@app.route("/wardrobe/updateItem", methods=['POST'])
def updateItem():
    itemId = request.get_json()["id"]
    newItemObject = request.get_json()["newItem"]
    result = __wdao.updateItem(itemId, newItemObject)
    if (result == 1):
        return "Set item with id " + itemId + " to definition " + json.dumps(newItemObject)
    else:
        return str(result)
"""
Body:Wardrobe Item ID
Returns: A Confirmation message when the item is removed. 
"""
@app.route("/wardrobe/removeItem", methods=["DELETE"])
def removeItem():
    itemId = request.args.get("itemId")
    result = __wdao.removeItem(itemId)
    if (result == 1):
        return "Removed item with the id: " + itemId
    else:
        return str(result)

"""
SUGGESTION ROUTES
"""

@app.route("/suggest", methods=["POST"])
def suggest():
    userId = request.get_json()["id"]
    wardrobe = [translateWardrobe(x) for x in __wdao.getWardrobe(userId)]
    quiz_answers = request.get_json()["quiz_answers"]
    suggestions = generate_suggestion(wardrobe, quiz_answers)
    return json.dumps(suggestions[0:2])

@app.route("/suggestAll", methods=["POST"])
def suggestAll():
    userId = request.get_json()["id"]
    wardrobe = [translateWardrobe(x) for x in __wdao.getWardrobe(userId)]
    quiz_answers = request.get_json()["quiz_answers"]
    suggestions = generate_suggestion(wardrobe, quiz_answers)
    return json.dumps(suggestions)
"""
OUTFIT ROUTES
"""
"""
Parameters: the target outfit ID, should be unique
Returns: An outfit corresponding to that ID
"""
@app.route("/outfits/getOutfitById")
def getOutfitById():
    outfitID = request.args.get("outfitID")
    results = __odao.getOutfitById(outfitID)
    return translateOutfitList(results)
"""
Parameters: An ID that corresponds to a user
Returns: All outfits "owned" by that user.
"""
@app.route("/outfits/getOutfitsByOwner")
def getOutfitsByOwner():
    ownerID = request.args.get("ownerID")
    results = __odao.getOutfitsByOwner(ownerID)
    return json.dumps(results, default=str)
"""
Parameters: A timestamp in unix epoch time
Returns: All outfits created since that timestamp
"""
@app.route("/outfits/getOutfitsSinceTimestamp")
def getOutfitsSinceTimestamp():
    timestamp = request.args.get("timestamp")
    ownerId = request.args.get("ownerId")
    results = __odao.getOutfitsSinceTimestamp(timestamp, ownerId)
    return translateOutfitList(results)
@app.route("/outfits/getUserRecord")
def getUserRecord():
    timestamp = request.args.get("timestamp")
    ownerID = request.args.get("ownerID")
    results = __odao.getUserRecord(ownerID, timestamp)
    return translateOutfitList(results)
"""
Body: An outfit definition
Returns: A confirmation message with the added definition if successful, otherwise, it will show the error.
"""
@app.route("/outfits/addOutfit", methods=["POST"])
def addOutfit():
    outfitDef = request.get_json()
    result = __odao.addOutfit(outfitDef)
    if(result == 1):
        return "Added outfit with the definition: " + json.dumps(outfitDef)
    else:
        return str(result)

"""
Parameters: An outfit ID
Returns: A confirmation message if the outfit was deleted successfully, otherwise, an error message
"""
@app.route("/outfits/removeOutfit", methods=["DELETE"])
def removeOutfit():
    outfitID = request.args.get("outfitID")
    result = __odao.removeOutfit(outfitID)
    if(result == 1):
        return "Removed outfit with the id " + outfitID
    else:
        return str(result)


"""
USER PROFILE ROUTES
"""

@app.route("/users/getUserById")
def getUserById():
    userId = request.args.get("userId")
    result = __udao.getUserById(userId)
    return translateUserProfileList(result)
@app.route("/users/login", methods=["POST"])
def verify():
    credentials = request.get_json()
    username = credentials["username"]
    password = credentials["password"]
    result = __udao.getUserByLogin(username, password)
    return translateUserProfileList(result)
@app.route("/users/addUser", methods=["POST"])
def addUser():
    userDef = request.get_json()
    result = __udao.addUser(userDef)
    if(result == 1):
        return "Successfully added user"
    else:
        return str(result)
@app.route("/users/updateUser", methods=["POST"])
def updateUser():
    userId = request.get_json()["userId"]
    userDef = request.get_json()["userDef"]
    result = __udao.updateUser(userId, userDef)
    if(result == 1):
        return "Successfully updated user with the id: " + userId
    else:
        return str(result)
@app.route("/users/removeUser", methods=["DELETE"])
def removeUser():
    userId = request.args.get("userId")
    result = __udao.removeUser(userId)
    if(result == 1):
        return "Removed user with the id: " + userId
    else:
        return str(result)