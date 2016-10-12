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
    data = recursive_adder(data)

    with open(directoryname + "mod" + filename,"wb") as data_file:
        json.dump(data,data_file,sort_keys = False,indent = 4, separators = (',',':'))

def recursive_adder(data):
    """
    Recursively add sentiment to children
    """
    # Intialize
    pos_count = 0
    neg_count = 0
    summer = 0.0
    counter = 0

    children = data["children"]
    for i in children:
        # leaves
        if "value" in i.keys():
            i["sentiment"] = get_sentiment_label(i["value"])
            if i["sentiment"] == "pos":
                pos_count += 1
            if i["sentiment"] == "neg":
                neg_count += 1 
        else:
            i = recursive_adder(i)
            # if not neutral
            if i["sentiment"] != "0":
                counter += 1
                num = float(i["sentiment"])
                if num > 0:
                    # collect only positive
                    summer += num
    # leaves' parent 
    if pos_count > neg_count:
        val = float(pos_count)/float(pos_count + neg_count)
        data["sentiment"] = str(val)
    elif neg_count > pos_count:
        val = -1 * float(neg_count)/float(pos_count + neg_count)
        data["sentiment"] = str(val)
    # rest of the tree
    else:
        if counter > 0:
            data["sentiment"] = str(summer/counter)
        else:
            data["sentiment"] = "0"
    return data

if __name__ == "__main__":
    sentiment_adder("../Data/","finaldata.json")
