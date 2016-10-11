import json
from pprint import pprint 
from sentiment import *

def convert(input):
    """
    Converts input dictionary from unicode to utf
    """
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def sentiment_adder(directoryname,filename):
    """
    Adds sentiment to json files
    """
    with open(directoryname + filename) as data_file:
        data = json.load(data_file)
    
    data = convert(data)
    data["children"] = recursive_adder(data["children"])

    with open(directoryname + "mod" + filename,"wb") as data_file:
        json.dump(data,data_file,sort_keys = False,indent = 4, separators = (',',':'))

def recursive_adder(data):
    """
    Recursively add sentiment to children
    """
    for i in data:
        if "value" in i.keys():
            i["sentiment"] = get_sentiment_label(i["value"])
        else:
            if i["children"] == "":
                return i["children"] 
            i["children"] = recursive_adder(i["children"])

    return data

if __name__ == "__main__":
    sentiment_adder("../Data/","finaldata.json")
