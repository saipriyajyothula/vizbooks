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
    ignore_list = ["Mr","Mrs","I","He","She","Ah","Aha","Everybody","Mister","Master","Miss","Ugh","Madam","Lord","Lady","Sir","Little","Prof","Madame","Dr"]

    character_list = []
    if isinstance(para,list):
        para = " ".join(para)

    text = Text(para)
    for sentence in text.sentences:
        for entity in sentence.entities:
            if entity.tag == "I-PER" and entity[0][0].encode('ascii').isupper() and "'" not in entity[0].encode('ascii') and not entity[0].isupper() and not entity[0].encode('ascii') in ignore_list:
                character_list.append(entity[0])
   
    if not character_list:
        return None
    return [i.encode('ascii') for i in character_list]


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
            if "prevalue" in child.keys():
                temp_list = get_characternames(child["prevalue"])
                if temp_list is None:
                    return
                else:
                    for val in list(set(temp_list)):
                        character_list.append(val)
            else:
                recursive_character(child)

    recursive_character(data)
    return list(set(character_list))

