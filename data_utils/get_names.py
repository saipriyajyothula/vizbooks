import pandas as pd
import nltk,polyglot
from polyglot.text import Text,Word

def get_names():
    """
    Get author and books names
    returns - dataframe names
        Author's Name
        Book Name
    """
    names = pd.read_csv("../Data/author_names.csv")
    names = names.set_index(["Sno"])
    return names

def get_authorsbook(authorname):
    """
    Get Books of the author
    returns - series of book list
    """
    names = get_names()
    return names[names["Author_Name"] == authorname]["Book_Name"]

def get_allauthornames(bookname):
    """
    Get all Authorname given bookname
    """
    names = get_names()
    return names[names["Book_Name"] == bookname]["Author_Name"]

def get_allbooknames():
    """
    Get the list of all books
    """
    names = get_names()
    return names["Book_Name"]

def get_characternames(para):
    """
    Get the list of character
    """
    text = Text(para)
    character_list = []
    for sent in text.sentences:
        for entity in sent.entities:
            if entity.tag == "I-PER":
                character_list.append(entity[0])
    
    if not character_list:
        return None

    return [i.encode('ascii') for i in character_list]

def get_locationnames(para):
    """
    Get locations 
    """
    text = Text(para)
    location_list = []
    for sent in text.sentences:
        for entity in sent.entities:
            if entity.tag == "I-LOC":
                location_list.append(entity[0])
    
    if not location_list:
        return None

    return [i.encode('ascii') for i in location_list]


def get_organizationnames(para):
    """
    Get organizations 
    """
    text = Text(para)
    organization_list = []
    for sent in text.sentences:
        for entity in sent.entities:
            if entity.tag == "I-ORG":
                organization_list.append(entity[0])
    
    if not organization_list:
        return None

    return [i.encode('ascii') for i in organization_list]

