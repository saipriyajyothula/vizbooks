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

def mainemotion_adder(directoryname,filename):
    """
    Adds emotions to the json
    """
    # load json file
    with open(directoryname + filename) as data_file:
        data = json.load(data_file)
    # convert from unicode to utf-8
    data = convert(data)
    data = recursive_emotion(data)

    # save json file
    with open(directoryname + "emo.json","wb") as data_file:
        json.dump(data,data_file,sort_keys = False,indent = 4, separators = (',',':'))

    allemotion_adder(directoryname,"emo.json")


def allemotion_adder(directoryname,filename):
    """
    Adds emotions to all fields
    """
    # load json file
    with open(directoryname + filename) as data_file:
        data = json.load(data_file)
    # convert from unicode to utf-8
    data = convert(data)
    
    data = chap_emotion(data)
    data = recursivechap_emotion(data)

    # save json file
    with open(directoryname + "emo.json","wb") as data_file:
        json.dump(data,data_file,sort_keys = False,indent = 4, separators = (',',':'))

def recursive_emotion(data):
    """
    Recursively add emotions 
    """
    children = data["children"]
    for i in children:
        #leaves
        if "prevalue" in i.keys():
            # get emotions dict of paragraph
            i["sentiment"] = get_emotions(i["prevalue"]) 
        else:
            i = recursive_emotion(i)

    return data

def chap_emotion(data):
    """
    Add emotions to chapters
    """
    children_list = []
    for child in data["children"]:
        children_list.append(recursivechap_emotion(child))

    data["children"] = children_list
    return data

def recursivechap_emotion(data):
    """
    Recursively adds emotions to chapters
    """
    temp_dict = None

    for i in data["children"]:
        if temp_dict is None:
            temp_dict = i["sentiment"].copy()
        else:
            for keys in i["sentiment"].keys():
                # add sentiments
                temp_dict[keys] = str(float(temp_dict[keys]) + float(i["sentiment"][keys]))

    for keys in temp_dict.keys():
        # normalize to make it independent of length
        temp_dict[keys] = str(float(temp_dict[keys])/len(data["children"]))
    data["sentiment"] = temp_dict

    return data

if __name__ == "__main__":
    mainemotion_adder("../Data/","modPride_and_Prejudice_paradata.json")
    # mainemotion_adder(directoryname,jsonfile)
