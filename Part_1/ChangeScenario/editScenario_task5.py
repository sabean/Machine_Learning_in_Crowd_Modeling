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

def loadPostvis(filename='postvis.trajectories'):
    count = 0
    pedestrians = {}
    with open(filename) as fp:
        for cnt, line in enumerate(fp):
            if cnt > 0:
                values = list(line.split())
                if int(values[0]) > 1:
                    break
                pedestrians[int(values[1])] = {"targetId": int(values[4]), "position": {"x" : float(values[2]), "y": float(values[3])}}
    return pedestrians

def addTarget(targetId_list):
    with open('dynamicElements.json') as f:
        data = json.load(f)
    return data

def createNew(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenarioFile", type=str, help="Name of scenario file.")
    parser.add_argument("--postvisFile", type=str, default="postvis.trajectories", help="Name of postvis file")
    parser.add_argument("--outputFile", type=str, default="edited.scenario", help="Specify the output file name.")
    parser.add_argument("--remove", type=str, default="False", help="True if you want to remove the source.")

    args = parser.parse_args()
    pedestrian = loadPostvis(args.postvisFile)
    scenario = loadScenario(args.scenarioFile)

    for key, value in pedestrian.items():
        dyn_elem = loadDElementStructure()
        dyn_elem["attributes"]["id"] = key
        dyn_elem["targetIds"] = [value['targetId']]
        dyn_elem["position"]["x"] = value['position']['x']
        dyn_elem["position"]["y"] = value['position']['y']
        pprint(dyn_elem)
        scenario["scenario"]["topography"]["dynamicElements"].append(dyn_elem)

    if args.remove != "False": 
        scenario["scenario"]["topography"]["sources"] = []
    scenario["name"] = args.outputFile
    createNew(args.outputFile, scenario)
    