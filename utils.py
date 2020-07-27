import simplejson as json


"""
Turns the tuple result into dicts to convert to JSON objects. 
"""
def translateWardrobe(result):
    return {
        "id":result[0],
        "name":result[1],
        "section":result[2],
        "type":result[3],
        "tags":result[4]
    }
def translateWardrobeListObj(resultList):
    return [translateWardrobe(row) for row in resultList]

def translateWardrobeList(resultList):
    return json.dumps([translateWardrobe(row) for row in resultList])

"""
Takes the tuple result from the Database into dicts to convert into JSON objects
"""
def translateOutfit(result):
    return {
        "id":result[3],
        "items":result[0],
        "score":result[1],
        "passed_rules":result[2],
        "owner":result[4],
        "time_created":result[5]
    }
def translateOutfitListObj(resultList):
    return [translateOutfit(row) for row in resultList]
def translateOutfitList(resultList):
    return json.dumps([translateOutfit(row) for row in resultList], use_decimal=True, default=str)

def translateUserProfile(result):
    return {
        "id":result[0],
        "username":result[1],
        "email_address":result[2],
        "password":result[3],
        "complexion":result[4],
        "undertones":result[5],
        "wardrobe":result[6]
    }

def translateUserProfileList(resultList):
    return json.dumps([translateUserProfile(row) for row in resultList])