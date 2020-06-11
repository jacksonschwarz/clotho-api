import os
import psycopg2
from flask import Flask, request
import simplejson as json

from WardrobeDAO import WardrobeDAO
from OutfitDAO import OutfitDAO
from SuggestionGen import generate_suggestion

"""
Turns the tuple result into dicts for flask to convert to JSON objects. 
"""
def translateWardrobe(result):
    return {
        "id":result[0],
        "name":result[1],
        "section":result[2],
        "type":result[3],
        "tags":result[4]
    }
def translateWardrobeList(resultList):
    return json.dumps([translateWardrobe(row) for row in resultList])

def translateOutfit(result):
    return {
        "id":result[3],
        "items":result[0],
        "score":result[1],
        "passed_rules":result[2],
        "owner":result[4],
        "time_created":result[5]
    }
def translateOutfitList(resultList):
    return json.dumps([translateOutfit(row) for row in resultList], use_decimal=True, default=str)
app = Flask(__name__)

__wdao = WardrobeDAO()
__odao = OutfitDAO()
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
    itemObject = request.get_json()
    result = __wdao.addItem(itemObject)
    if (result == 1):
        return "Added object " + json.dumps(itemObject)
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
    itemId = request.get_json()["id"]
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
    return translateOutfitList(results)
"""
Parameters: A timestamp in unix epoch time
Returns: All outfits created since that timestamp
"""
@app.route("/outfits/getOutfitsSinceTimestamp")
def getOutfitsSinceTimestamp():
    timestamp = request.args.get("timestamp")
    results = __odao.getOutfitsSinceTimestamp(timestamp)
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

        