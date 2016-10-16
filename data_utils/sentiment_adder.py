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
    # load json file
    with open(directoryname + filename) as data_file:
        data = json.load(data_file)
    # convert from unicode to utf-8
    data = convert(data)
    data = recursive_sentiment(data)
    
    # save json file
    with open(directoryname + "mod" + filename,"wb") as data_file:
        json.dump(data,data_file,sort_keys = False,indent = 4, separators = (',',':'))

def recursive_sentiment(data):
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
        # rest of the tree
        else:
            i = recursive_sentiment(i)
            # if not neutral
            if i["sentiment"] != "0":
                counter += 1
                num = float(i["sentiment"])
                if num > 0:
                    # collect only positive
                    summer += num
    # leaves' parent 
    # positive value for positive paragraph
    if pos_count > neg_count:
        val = float(pos_count)/float(pos_count + neg_count)
        data["sentiment"] = str(val)
    # negative value for negative paragraph
    elif neg_count > pos_count:
        val = -1 * float(neg_count)/float(pos_count + neg_count)
        data["sentiment"] = str(val)
    # rest of the tree
    else:
        if counter > 0:
            # avg over positive sum
            data["sentiment"] = str(summer/counter)
        else:
            data["sentiment"] = "0"
    return data

def emotion_adder(directoryname,filename):
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
    with open(directoryname + "emo","wb") as data_file:
        json.dump(data,data_file,sort_keys = False,indent = 4, separators = (',',':'))

    allemotion_adder(directoryname,"emo")


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
    with open(directoryname + "emo","wb") as data_file:
        json.dump(data,data_file,sort_keys = False,indent = 4, separators = (',',':'))

def recursive_emotion(data):
    """
    Recursively add emotions 
    """
    children = data["children"]
    for i in children:
        #leaves
        if "value" in i.keys():
            # get emotions dict
            i["sentiment"] = get_emotions(i["value"]) 
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

