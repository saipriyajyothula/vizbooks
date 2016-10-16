import pandas as pd
from get_names import *

def interaction_csv(directoryname,jsonfile):
    """
    Creates a csv file for interaction
    """
    with open(directoryname,jsonfile) as data_file:
        data = json.load(data_file)

    data = recursive_extractor(data)
    character_list = []

    def recursive_extractor(data):
        """
        Recursively extract interaction between characters
        """
        pass


