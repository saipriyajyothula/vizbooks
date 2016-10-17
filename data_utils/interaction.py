import pandas as pd
import json
from get_names import *
from sentiment import *
from itertools import combinations

def interaction_json(directoryname,jsonfile):
    """
    Creates a json file for interaction
    """
    with open(directoryname+jsonfile) as data_file:
        data = json.load(data_file)

    # get list of characters in a book
    character_list = get_bookcharacternames(data)

    def recursive_extractor(data):
        """
        Recursively extract interaction between characters
        """
        children = data["children"]
        chapter_list = []
        for child in children:
            conversation_partners = []
            for i in child["children"]:
                temp_dict = {}
                val = get_characternames(i["value"])
                # if no characters in paragraph
                if val is None:
                    # get paragraph name
                    temp_dict["name"] = i["name"]
                    temp_dict["partners"] = []
                    i["partners"] = []
                else:
                    # get paragraph name
                    temp_dict["name"] = i["name"]
                    # unique values
                    temp_dict["partners"] = list(set(val))
                    i["partners"] = list(set(val))
                conversation_partners.append(temp_dict)
            child["conversation"] = conversation_partners
            chapter_list.append(child)
    
        data["children"] = chapter_list
        return data

    data = recursive_extractor(data)

    with open(directoryname+"char"+jsonfile,"wb") as data_file:
        json.dump(data,data_file,sort_keys = False,indent = 4,separators = (',',':'))


def interaction_matrix(directoryname,jsonfile):
    """
    Creates a matrix that shows the number of interactions
    """
    with open(directoryname+jsonfile) as data_file:
        data = json.load(data_file)

    # char_chaplist - list of characters in each chapter
    char_chaplist = []
    for child in data["children"]: 
        character_chapter = []
        partner_list = child["conversation"]
        for i in partner_list:
            for j in i["partners"]:
                character_chapter.append(j)

        if character_chapter is not None:
            char_chaplist.append(list(set(character_chapter)))

    def matrixop(i,char_list):
        """
        Creates a matrix counter
        Inputs - 
            i : chapter number
            char_list : list of character names
        """

        df = pd.DataFrame(0,index = char_list, columns = char_list)
        chap_list = data["children"]

        partner_list = chap_list[i-1]["conversation"]
        for i in partner_list:
            partners = i["partners"]
            # Combination of list and add values
            for subsets in combinations(partners,2):
                index_val,col_val = subsets
                df.loc[index_val,col_val] += 1

        return df

    # final_matrix - list of matrix for each chapter
    final_matrix = []
    for i,chap in enumerate(char_chaplist):
        temp_dict = {}
        temp_dict["name"] = "Chapter_" + str(i+1)
        temp_dict["matrix"] = matrixop(i+1,chap)
        final_matrix.append(temp_dict)
    
    return final_matrix

def interaction_panel(directoryname,jsonfile):
    """
    Create 3D matrix for interaction and emotions
    """
    with open(directoryname+jsonfile) as data_file:
        data = json.load(data_file)

    # char_chaplist - list of characters in each chapter
    char_chaplist = []
    for child in data["children"]: 
        character_chapter = []
        partner_list = child["conversation"]
        for i in partner_list:
            for j in i["partners"]:
                character_chapter.append(j)

        if character_chapter is not None:
            char_chaplist.append(list(set(character_chapter)))

    # emotions list
    emotions = ["Positive","Negative","Anger","Anticipation","Disgust","Fear","Joy","Sadness","Surprise","Trust"]

    def matrixop(i,char_list):
        """
        Creates a matrix counter
        Inputs - 
            i : chapter number
            char_list : list of character names
        """
        # Pandas Panel 
        df = pd.Panel(0.0,items = char_list, major_axis = char_list, minor_axis = emotions)
        # get chapter i
        chap = data["children"][i-1]
        # for each paragraph
        for child in chap["children"]:
            partners = child["partners"]
            # paragraph list
            para_list = child["value"]
            # Combination of list and add values
            for subsets in combinations(partners,2):
                index_val,col_val = subsets
                for sent in para_list:
                    if (index_val) and (col_val) in sent:
                        emotion_dict = get_emotions(sent)
                        for key in emotion_dict.keys():
                            df.loc[index_val,col_val,key] += float(emotion_dict[key])

        return df

    # final_matrix - list of matrix for each chapter
    final_matrix = []
    for i,chap in enumerate(char_chaplist):
        temp_dict = {}
        temp_dict["name"] = "Chapter_" + str(i+1)
        temp_dict["matrix"] = matrixop(i+1,chap)
        final_matrix.append(temp_dict)
        break
    
    return final_matrix

def matrix_tojson(matrix):
    """
    Converts matrix to json file
    Input - matrix : list of interaction matrix for each chapter
    """
    force_chap = {}
    force_chap["force_list"] = []
    for chap in matrix:
        force_dict = {}
        if chap["matrix"].ndim == 2:
            character_list = list(chap["matrix"].columns.values)
        elif chap["matrix"].ndim == 3:
            character_list = list(chap["matrix"].items.values)
        # chapter name
        force_dict["name"] = chap["name"]
        # nodes
        force_dict["nodes"] = []
        for character in character_list:
            temp_dict = {}
            temp_dict["id"] = str(character)
            temp_dict["group"] = 0
            force_dict["nodes"].append(temp_dict)
        # links
        force_dict["links"] = []
        for subsets in combinations(character_list,2):
            index_val,col_val = subsets
            temp_dict = {}
            temp_dict["source"] = index_val
            temp_dict["target"] = col_val
            # number of interaction
            if chap["matrix"].ndim == 2:
                temp_dict["value"] = chap["matrix"].loc[index_val,col_val]
            # emotions
            elif chap["matrix"].ndim == 3:
                temp_dict["value"] = chap["matrix"].loc[index_val,col_val,:].to_dict()

            force_dict["links"].append(temp_dict)

        force_chap["force_list"].append(force_dict)

    return force_chap
    
def force_jsoncreator(dictionaryname,directoryname,filename):
    """
    Creates a json file for force layout
    """
    with open(directoryname+filename,"wb") as data_file:
        json.dump(dictionaryname,data_file,sort_keys = False,indent = 4,separators = (',',':'))

def interaction_maincall(directoryname,filename):
    """
    Main call to interaction file
    """
    interaction_json(directoryname,filename)
    # count force json
    matrix = interaction_matrix("../Data/","charmodparadata.json")
    force = matrix_tojson(matrix)
    force_jsoncreator(force,"../Data/","forceinteraction_count.json")
    # emotion force json
    matrix = interaction_panel("../Data/","charmodparadata.json")
    force = matrix_tojson(matrix)
    force_jsoncreator(force,"../Data/","forceinteraction_emotions.json")
