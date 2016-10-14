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
    # person - entities[0],location - entities[1]
    character_list = text.entities[0]
    return [i.encode('ascii') for i in character_list]



