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
        outfit["passed_rules"].append("PROFESSIONALISM")
#gets the HSL values of the item's color(s).
def _getColors(item):
    if(len(item["tags"]) > 0):
        tags = item["tags"]
        filtered = list(filter(lambda i: "Color" in i, tags))
        colors = list(map(lambda t: hex_to_hsluv(t.split(":")[1]), filtered))
        return colors
def hue_contrast_score(outfit, **kwargs):
    contrastRange = kwargs["answers"][1]
    tag = "Color"
    items = outfit["items"]
    colors = list(map(_getColors, items))
    #an array of hues based on the HSL colors
    hues = np.array([item[0] for sublist in colors for item in sublist])
    print("Hues")
    print(hues)
    hueCombos = list(itertools.combinations(hues, r=2))
    print("Hue Combos")
    print(hueCombos)
    colorDistance = np.array([abs(x[0] - x[1]) for x in hueCombos])
    print("Color Distance")
    print(colorDistance)
    #if the distance is close to 180, then the colors contrast. If the distance is close to 0, the colors are analogous. 
    #the ranges in the quiz questions should take into account that the scale is from 0-180.
    #since we are subtracting by 180 here, the lower number is better. 
    contrastScores = np.abs(colorDistance - 180)
    print("Contrast Scores")
    print(contrastScores)
    for score in contrastScores:
        if(score > contrastRange[0] and score < contrastRange[1]):
            outfit["score"] += 1
            outfit["passed_rules"].append("HUE_CONTRAST")
            break


#Pattern rule has to be the last in the list because it X 0 multiplier
rules = [professionalism, hue_contrast_score]

# def read_example():
#     data=[]
#     with open("./example.json") as f:
#         data=json.load(f)
#     return data

# example_data = read_example()
# outfits = example_data["outfits"]
# quiz_answers = example_data["quiz_answers"]
# for o in outfits:
#     print()
#     hue_contrast_score(o, answers=quiz_answers)
# for o in outfits:
#     print()
#     print(o)