from hsluv import hex_to_hsluv
import json
import numpy as np
import itertools
"""
This file is used for rule definition. 
Each function should take in an outfit(an array of objects) and keyword arguments (**kwargs)
This is so each rule can be called in the array below with the same set of keyword arguments, but they can have different functionalities. 
"""
"""
Checks to see if an outfit fits the quiz answer regarding the desired level of professionalism. 
"""
def professionalism(outfit, **kwargs):
    
    answer = int(kwargs["answers"][0])

    tag = "Professionalism"
    items = outfit["items"]

    # The max possible distance of formality is 2, since the range of formality is currently 1-3
    maxDistance=2
    # Used to scale the final score. With a max distance of 2 and scale factor of 2, the final score will be in the range of 0.0-1.0
    scaleFactor=2

    # The minimum value of the formality score to pass the rule. This rule will modify the score regardless if the rule is passed or not,
    # but it does affect whether or not the rule is added to the outfit's list of passed rules
    rulePassingValue=.50

    # Creates list composed of the formalities of each item in the outfit by checking for each Professionalism tag. 
    # Could use something better than for loops (I don't have a great grasp on Lambda functions and parsing JSON)
    formalityValues=[]
    for item in items:
        for itemTag in item["tags"]:
            if tag in itemTag:
                formalityValues.append(int(itemTag[-1:]))

    # Calculates the distance between the total formality score of the outfit items and the formality level specified by the user
    # by subtracting the formality quiz question answer from the mean of each item's formality level.
    # Then, this is subtracted from the maximum possible distance of formality and divided by the scaling factor (specified above).
    outfitFormalityScore=(maxDistance-(np.abs(np.mean(formalityValues)-answer)))/scaleFactor

    outfit["score"]=outfit["score"]+outfitFormalityScore

    # Outfit passes rule if the formality score is at least the value specified above
    if outfitFormalityScore>=rulePassingValue:
        outfit["passed_rules"].append("PROFESSIONALISM")

#gets the HSL values of the item's color(s).
def _getColors(item):
    if(len(item["tags"]) > 0):
        tags = item["tags"]
        filtered = list(filter(lambda i: "Color" in i, tags))
        colors = list(map(lambda t: hex_to_hsluv(t.split(":")[1]), filtered))
        return colors
"""
How the hues of each individual outfit item contrast one another. 
"""
def hue_contrast_score(outfit, **kwargs):
    contrastRange = kwargs["answers"][1]
    tag = "Color"
    items = outfit["items"]
    colors = list(map(_getColors, items))
    #an array of hues based on the HSL colors
    hues = np.array([item[0] for sublist in colors for item in sublist])
    hueCombos = list(itertools.combinations(hues, r=2))
    colorDistance = np.array([abs(x[0] - x[1]) for x in hueCombos])
    #if the distance is close to 180, then the colors contrast. If the distance is close to 0, the colors are analogous. 
    #the ranges in the quiz questions should take into account that the scale is from 0-180.
    #since we are subtracting by 180 here, the lower number is better. 
    contrastScores = np.abs(colorDistance - 180)
    for score in contrastScores:
        if(score >= contrastRange[0] and score <= contrastRange[1]):
            outfit["score"] += 1
            outfit["passed_rules"].append("HUE_CONTRAST")
            break
"""
How the lights of each infividual object contrast with one another
"""
def light_contrast(outfit, **kwargs):
    lightRange = kwargs["answers"][2]
    items = outfit["items"]
    colors = list(map(_getColors, items))
    lights = np.array([item[2] for sublist in colors for item in sublist])
    lightCombos = list(itertools.combinations(lights, r=2))
    lightDistance = np.array([abs(x[0] - x[1]) for x in lightCombos])

"""
How light an overall outfit is
"""
def light_score(outfit, **kwargs):
    lightRange = kwargs["answers"][2]
    items = outfit["items"]
    colors = list(map(_getColors, items))
    lights = np.array([item[2] for sublist in colors for item in sublist])
    lightScore = np.sum(lights) / len(items)
    if (lightScore >= lightRange[0] and lightScore <= lightRange[1]):
        outfit["score"] += 1
        outfit["passed_rules"].append("LIGHT_SCORE")

#Pattern rule has to be the last in the list because it X 0 multiplier
rules = [professionalism, hue_contrast_score, light_score]

def read_example():
    data=[]
    with open("./example.json") as f:
        data=json.load(f)
    return data

# example_data = read_example()
# outfits = example_data["outfits"]
# quiz_answers = example_data["quiz_answers"]

# for o in outfits:
#     print()
#     light_score(o, answers=quiz_answers)
# # for o in outfits:
# #     print()
# #     print(o)
