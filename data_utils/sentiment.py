import urllib
import json

def get_sentiment(text):
    """
    Inputs - 
        text:Sentence that u want to find sentiment of
    Returns - A Dictionary
        probability - Probability dictionary
            pos - Pos probability
            neg - Neg probability
            neutral - Neutral probability
        label - argmax(pos,neg,neutral)
    """
    data = urllib.urlencode({"text": text}) 
    u = urllib.urlopen("http://text-processing.com/api/sentiment/", data)
    the_page = json.load(u)
    return the_page

