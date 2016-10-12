import pandas as pd

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

def get_authorname(bookname):
    """
    Get Authorname given bookname
    """
    names = get_names()
    return names[names["Book_Name"] == bookname]["Author_Name"]


