from hsluv import hex_to_hsluv
import json
import numpy as np
import itertools
"""
This file is used for rule definition. 
Each function should take in an outfit(an array of objects) and keyword arguments (**kwargs)
This is so each rule can be called in the array below with the same set of keyword arguments, but they can have different functionalities. 
"""
def professionalism(outfit, **kwargs):
    answer = kwargs["answers"][0]
    tag = "Professionalism"
    #first, filter out all items without a professionalism tag.
    items = outfit["items"]
    filteredItems = list(filter(lambda i: tag in "".join(i["tags"]),items))
    answerOnly = list(filter(lambda i: answer in "".join(i["tags"]), filteredItems))
    #this means that the amount of clothes that have Professionalism are the same that contain the answer, meaning the rule passes.
    if(len(filteredItems) > 0) and (len(filteredItems) == len(answerOnly)):
        outfit["score"] = outfit["score"] + 1
        outfit["passed_rules"] = "PROFESSIONALISM"
#gets the HSL values of the item's color(s).
def _getColors(item):
    if(len(item["tags"]) > 0):
        tags = item["tags"]
        filtered = list(filter(lambda i: "Color" in i, tags))
        colors = list(map(lambda t: hex_to_hsluv(t.split(":")[1]), filtered))
        return colors
def contrast_score(outfit, **kwargs):
    contrastRange = kwargs["answers"][1]
    tag = "Color"
    items = outfit["items"]
    colors = list(map(_getColors, items))
    #an array of hues based on the HSL colors
    hues = np.array([item[0] for sublist in colors for item in sublist])
    print(hues)
         
rules = [professionalism]

def read_example():
    data=[]
    with open("./example.json") as f:
        data=json.load(f)
    return data

example_data = read_example()
outfits = example_data["outfits"]
quiz_answers = example_data["quiz_answers"]
contrast_score(outfits[0], answers=quiz_answers)