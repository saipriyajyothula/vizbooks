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

