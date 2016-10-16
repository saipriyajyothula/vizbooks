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
    Get the list of character from the paragraph
    """
    para = " ".join(para)
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
    Get locations from paragraph
    """
    para = " ".join(para)
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
    Get organizations from paragraph
    """
    para = " ".join(para)
    text = Text(para)
    organization_list = []
    for sent in text.sentences:
        for entity in sent.entities:
            if entity.tag == "I-ORG":
                organization_list.append(entity[0])
    
    if not organization_list:
        return None

    return [i.encode('ascii') for i in organization_list]

def get_bookcharacternames(data):
    """
    Get all character names in the book
    """
    character_list = []

    def recursive_character(data):
        """
        Recursively get the character names
        """
        children = data["children"]
        for child in children:
            if "value" in child.keys():
                temp_list = get_characternames(child["value"])
                if temp_list is None:
                    return
                else:
                    for val in list(set(temp_list)):
                        character_list.append(val)
            else:
                recursive_character(child)

    recursive_character(data)

    return list(set(character_list))
