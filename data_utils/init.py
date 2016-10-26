from json_shortener import *
from sentiment import *
from sentiment_adder import *
from interaction import *
from paragraphjson import *
from character_sentiment import *

if __name__ == "__main__":
    directoryname = "../Data"
    # shortens the json by combining paragraphs and chapters
    shortener(directoryname,jsonfile)
    # created only once - dictionary of emotion word vector
    # emotions_csvtojson("../Data/","NRCEmotionsLexicon.csv")
    # adds emotions to jsonfile;used for tree
    mainemotion_adder(directoryname,jsonfile)
    # adds interactions field to json
    interaction_json(directoryname,jsonfile)
    # creates a json for force network
    interaction_maincall(directoryname,jsonfile)
    # creates a json for bar graph
    char_emotionadder(directoryname,jsonfile)

