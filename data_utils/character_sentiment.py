import json
from pprint import pprint 
from sentiment import *
from get_names import *

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

def char_emotionadder(directoryname,filename):
    """
    Calculates emotions of each characters
    """
    # load json file
    with open(directoryname + filename) as data_file:
        data = json.load(data_file)
    # convert from unicode to utf-8
    data = convert(data)
    data = characterjson_creator(data)

    # save json file
    with open(directoryname + "third.json","wb") as data_file:
        json.dump(data,data_file,sort_keys = False,indent = 4, separators = (',',':'))

def window_creator(sent_list,pos):
    """
    Creates windows
    """
    sent_len = len(sent_list)
    if sent_len < 10:
        return sent_list
    elif pos < 5:
        return sent_list[:pos + 5] 
    elif pos >= 5 and pos + 5 > sent_len:
        return sent_list[pos - 5 :]
    elif pos >= 5 and pos + 5 < sent_len:
        return sent_list[pos - 5: pos + 5]

def fetch_emotion(sent_list,pos):
    """
    Fetch emotions given sentence and position of character
    """
    window = window_creator(sent_list,pos)
    if window is None:
        return None
    return get_emotions(window)

def characterjson_creator(data):
    """
    Create json for character emotions
    """
    book_characters_list = get_bookcharacternames(data)

    char_emotion_list = []
    for character in book_characters_list:
        char_emotion = {}
        char_emotion["character_name"] = character
        temp_list = []
        children = data["children"]
        # for each chapter
        for child in children:
            temp_dict = {}
            temp_dict["chapter_name"] = child["name"]
            temp_dict["value"] = {}
            # for each paragraph
            for i in child["children"]:
                for sent in i["prevalue"]:
                    sent_list = sent.split(" ")
                    if character in sent_list:
                        pos = sent_list.index(character)
                        emotion_dict = fetch_emotion(sent_list,pos) 
                        if emotion_dict is not None:
                            for key in emotion_dict.keys():
                                if key in temp_dict["value"].keys():
                                    temp_dict["value"][key] += float(emotion_dict[key])
                                else:
                                    temp_dict["value"][key] = float(emotion_dict[key])
            temp_list.append(temp_dict)
        flag = 0
        for k in temp_list:
            if bool(k["value"]):
                flag = 1
                break
        if flag:
            char_emotion["chap_sentiment"] = temp_list
            char_emotion_list.append(char_emotion)

    data = {}
    data["character_emotion"] = char_emotion_list 

    return data

if __name__ == "__main__":
    char_emotionadder("../Data/","modOliver_Twist_paradata.json")
