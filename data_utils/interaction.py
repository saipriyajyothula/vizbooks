import pandas as pd
import json
from get_names import *

def interaction_csv(directoryname,jsonfile):
    """
    Creates a csv file for interaction
    """
    with open(directoryname+jsonfile) as data_file:
        data = json.load(data_file)

    character_list = get_bookcharacternames(data)
	
    def recursive_extractor(data):
        """
        Recursively extract interaction between characters
        """
        pass
    
    # data = recursive_extractor(data)
    print character_list


if __name__ == "__main__":
    interaction_csv("../Data/","modparadata.json")
