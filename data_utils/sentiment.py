import json
from textblob import TextBlob

def get_sentiment_label(para):
    """
    Return sentiment label given text
    """
    blob = TextBlob(para)
    pol = blob.sentiment.polarity
    if pol > 0.5:
        return "pos"
    elif pol < -0.5:
        return "neg"
    else:
        return "neutral"

def get_emotions(para):
    """
    Get the emotions given the paragraph
    """
    word_vec = json.load("")
    pass

