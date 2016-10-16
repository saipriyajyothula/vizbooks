import pandas as pd
import json
from get_names import *
from itertools import combinations,permutations

def interaction_json(directoryname,jsonfile):
    """
    Creates a json file for interaction
    """
    with open(directoryname+jsonfile) as data_file:
        data = json.load(data_file)

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
                if val is None:
                    continue
                else:
                    # get paragraph name
                    temp_dict["name"] = i["name"]
                    # unique values
                    temp_dict["partners"] = list(set(val))
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

    matrix = []
    for child in data["children"]: 
        character_chapter = []
        partner_list = child["conversation"]
        for i in partner_list:
            for j in i["partners"]:
                character_chapter.append(j)

        if character_chapter is not None:
            matrix.append(list(set(character_chapter)))

    def matrixop(i,matrix):
        """
        Creates a matrix counter
        Inputs - 
            i : chapter number
            matrix : list of character names
        """

        df = pd.DataFrame(0,index = matrix, columns = matrix)
        chap_list = data["children"]

        partner_list = chap_list[i-1]["conversation"]
        for i in partner_list:
            partners = i["partners"]
            for subsets in permutations(partners,2):
                index_val,col_val = subsets
                df.loc[index_val,col_val] += 1

        return df


    final_matrix = []
    for i,chap in enumerate(matrix):
        temp_dict = {}
        temp_dict["name"] = "Chapter_" + str(i+1)
        temp_dict["matrix"] = matrixop(i+1,chap)
        final_matrix.append(temp_dict)
    
    return final_matrix


def matrix_tojson(matrix):
    """
    Converts matrix to json file
    """
    force_chap = {}
    force_chap["force_list"] = []
    for chap in matrix:
        force_dict = {}
        character_list = list(chap["matrix"].columns.values)
        force_dict["name"] = chap["name"]

        force_dict["nodes"] = []
        for character in character_list:
            temp_dict = {}
            temp_dict["id"] = str(character)
            temp_dict["group"] = 0
            force_dict["nodes"].append(temp_dict)

        force_dict["links"] = []

        for subsets in combinations(character_list,2):
            index_val,col_val = subsets
            temp_dict = {}
            temp_dict["source"] = index_val
            temp_dict["target"] = col_val
            temp_dict["value"] = chap["matrix"].loc[index_val,col_val]
            force_dict["links"].append(temp_dict)
        
        force_chap["force_list"].append(force_dict)
    
    return force_chap
    
def force_jsoncreator(dictionaryname,directoryname,filename):
    """
    Creates a json file for force layout
    """
    with open(directoryname+filename,"wb") as data_file:
        json.dump(dictionaryname,data_file,sort_keys = False,indent = 4,separators = (',',':'))



# if __name__ == "__main__":
    # interaction_json("../Data","modparadata.json")
#     matrix = interaction_matrix("../Data/","charmodparadata.json")
#     force = matrix_tojson(matrix)
#     force_jsoncreator(force,"../Data/","forceinteraction.json")
    
