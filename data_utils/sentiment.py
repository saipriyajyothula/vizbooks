import json,pandas as pd,numpy as np
from textblob import TextBlob


def emotions_csvtojson(directoryname,filename):
    """
    Create a json for emotions csv
    """
    df = pd.read_csv(directoryname+filename)
    df = df.set_index(["English Word"])
    # convert to string
    for i in df.columns.values:
        df[i] = df[i].astype(str)
    df["new_col"] = df["Positive"].str.cat([df["Negative"],df["Anger"],df["Anticipation"],df["Disgust"],df["Fear"],df["Joy"],df["Sadness"],df["Surprise"],df["Trust"]])
    new_df = df["new_col"]
    # convert to dictionary
    data = new_df.to_dict()
    # save as json 
    with open(directoryname+"word_vec.json","wb") as data_file:
        json.dump(data,data_file,sort_keys = True,indent = 4,separators = (',',':'))


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
    Get the emotions given the paragraph(list of sentences)
    returns a dictionary of emotions 
    """
    with open("../Data/word_vec.json") as data_file:
        word_vec = json.load(data_file)
    # convert word vec values to numpy array
    for keys in word_vec.keys():
        word_vec[keys] = np.array(list(word_vec[keys].encode('ascii')),dtype = "|S4").astype(np.float)

    summer = np.zeros(10)
    if para is list:
        for sentences in para:
            words = sentences.split(" ")
            # vectorize the words
            words = [word_vec[i] if i in word_vec.keys() else np.zeros(10) for i in words]
            for nparrays in words:
                summer = np.sum([summer,nparrays],axis = 0)

    else:
        words = para.split(" ")
        # vectorize the words
        words = [word_vec[i] if i in word_vec.keys() else np.zeros(10) for i in words]
        for nparrays in words:
            summer = np.sum([summer,nparrays],axis = 0)

    # create dictionary of emotions
    data = pd.DataFrame(summer.reshape(1,10),columns = ["Positive","Negative","Anger","Anticipation","Disgust","Fear","Joy","Sadness","Surprise","Trust"])
    data =  data.to_dict(orient = 'list')
    for keys in data.keys():
        data[keys] = str(data[keys][0])

    
    return data


# if __name__ == "__main__":
#     emotions_csvtojson("../Data/","NRCEmotionLexicon.csv")
