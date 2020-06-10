"""
This file is used to house the algorithm used to determine suggestions.
It will be used in the form of a function, but the actual work will be split up into several parts.
"""
import itertools
import numpy as np
import json
import pprint
from rules import rules

pp = pprint.PrettyPrinter(indent=1)
#read in the example database query for the wardrobe and quiz answers
def read_example():
    data=[]
    with open("./example.json") as f:
        data=json.load(f)
    return data

"""
A filter function to guarantee that each combonation does not have multiple sections included. 
"""
def filterCombinations(combo):
    sectionsOnly = [c["section"] for c in combo]
    return len(sectionsOnly) == len(set(sectionsOnly))
def create_combinations(wardrobe):
    #creates combinations based on grouped sections. i.e for every torso section and leg section.
    uniqueSections = set(map(lambda x: x["section"], wardrobe))
    combos = list(itertools.combinations(wardrobe, r=len(uniqueSections)))
    #combos cannot have more than one of the same section. 
    filteredCombos = filter(filterCombinations, combos)
    #need to track how many sections are in each combination, so that there are no section duplicates.
    #turning this into a set wouldn't necessarily work. 
    return list(filteredCombos)

def create_outfits(outfitCombos):
    outfits = []
    for c in outfitCombos:
        outfit = {}
        outfit["items"] = list(c)
        outfit["score"] = 0
        outfit["passed_rules"] = []
        outfits.append(outfit)
    return outfits
    
"""
Scoring
Go through all of the rules and determine the scores of each suggestion object
"""
def suggest(outfits, rules, quiz_answers):
    for outfit in outfits:
        for rule in rules:
            rule(outfit, answers = quiz_answers)
    result = sorted(outfits, reverse=True, key=lambda e:e["score"])
    return list(result)


example_data = read_example()
combinations = create_combinations(example_data["wardrobe"])
exampleOutfits = example_data["outfits"]
outfits = create_outfits(combinations)

suggestions = suggest(exampleOutfits, rules, example_data["quiz_answers"])
for o in suggestions:
    print(o)
    print()