from json_shortener import *
from sentiment import *
from sentiment_adder import *
from interaction import *
from character_sentiment import *

if __name__ == "__main__":
    directoryname = "../Data/"
    # shortens the json by combining paragraphs and chapters
    jsonfile = "Persuasion_paradata.json"
    shortener(directoryname,jsonfile)
    # created only once - dictionary of emotion word vector
    # emotions_csvtojson("../Data/","NRCEmotionsLexicon.csv")

    # adds emotions to jsonfile;used for tree (1st viz)
    mainemotion_adder(directoryname,"original.json")
    # creates a json for force network (2nd viz)
    interaction_maincall(directoryname,"original.json")
    # creates a json for bar graph (3rd vis)
    char_emotionadder(directoryname,"original.json")

