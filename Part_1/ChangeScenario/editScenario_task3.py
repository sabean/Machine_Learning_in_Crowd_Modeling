import json
import argparse
from pprint import pprint

def loadScenario(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def loadDElementStructure():
    with open('dynamicElements.json') as f:
        data = json.load(f)
    return data

def createNew(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenarioFile", type=str, default='Test6.scenario', help="Name of scenario file.")
    parser.add_argument("--outputFile", type=str, default="editedTest6.scenario", help="Specify the output file name.")
    args = parser.parse_args()
    scenario = loadScenario(args.scenarioFile)
    targetId_list = []
    targets  = scenario["scenario"]["topography"]["targets"]
    for i in targets:
        targetId_list.append(i["id"])
    dyn_elem = loadDElementStructure()
    dyn_elem["targetIds"] = targetId_list
    dyn_elem["position"]["x"] = 12.0
    dyn_elem["position"]["y"] = 1.5
    scenario["scenario"]["topography"]["dynamicElements"].append(dyn_elem)
    #pprint(scenario, width=1)
    scenario["name"] = args.outputFile
    createNew(args.outputFile, scenario)