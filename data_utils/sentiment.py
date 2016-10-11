from textblob import TextBlob

def get_sentiment_label(text):
    blob = TextBlob(text)
    pol = blob.sentences[0].sentiment.polarity
    if pol > 0.5:
        return "pos"
    elif pol < -0.5:
        return "neg"
    else:
        return "neutral"

