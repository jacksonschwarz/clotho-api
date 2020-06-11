import os
import psycopg2
from flask import Flask, request
import json

from WardrobeDAO import WardrobeDAO
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

app = Flask(__name__)

__wdao = WardrobeDAO()
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
    id=request.args.get("id")
    results = __wdao.getWardrobe(id)
    return translateWardrobeList(results)
"""
Parameters: Wardrobe Item ID
Returns: The wardrobe item corresponding to that ID (is unique)
"""
@app.route("/wardrobe/getItemById")
def getItemById():
    id=request.args.get("id")
    results = __wdao.getItemById(id)
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
Parameters: Wardrobe Item Tag
Returns: Any wardrobe items with the specified tags in its 
"""
@app.route("/wardrobe/getItemByAnyTags")
def getItemByAnyTags():
    tags = request.get_json()["tags"]
    asciitags = [x.encode("ascii") for x in tags]
    results = __wdao.getItemByAnyTags(asciitags)
    return translateWardrobeList(results)
"""
Parameters: Wardrobe Section Type
Returns: A list of items that are grouped by their clothing section.
"""
@app.route("/wardrobe/addItem", methods=['POST'])
def addItem():
    itemObject = request.get_json()
    result = __wdao.addItem(itemObject)
    if (result == 1):
        return "Added object " + str(itemObject)
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
        return "Added tags " + str(tagsToAdd) + " to item with the id " + itemId 
    else:
        return str(result)
"""
Parameters:Wardrobe Item ID, a list of wardrobe item tags. 
Returns: A confirmation message when the specified list of tags is seto the specified object
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
Parameters:Wardrobe Item ID, a wardrobe object
Returns: A confirmation when the wardrobe object has been updated. 
"""
@app.route("/wardrobe/updateItem", methods=['POST'])
def updateItem():
    itemId = request.get_json()["id"]
    newItemObject = request.get_json()["newItem"]
    result = __wdao.updateItem(itemId, newItemObject)
    if (result == 1):
        return "Set item with id " + itemId + " to definition " + str(newItemObject)
    else:
        return str(result)
"""
Parameters:Wardrobe Item ID
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

@app.route("/suggest")
def suggest():
    userId = request.get_json()["id"]
    wardrobe = [translateWardrobe(x) for x in __wdao.getWardrobe(userId)]
    quiz_answers = request.get_json()["quiz_answers"]
    suggestions = generate_suggestion(wardrobe, quiz_answers)
    return json.dumps(suggestions[0:2])