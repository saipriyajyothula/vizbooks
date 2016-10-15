import json

def shortener(directoryname,filename):
    """
    Shortens the json
    """
    with open(directoryname + filename) as data_file:
        data = json.load(data_file)

    # combines paragraph and chapters; (you can comment to remove any combiner) 
    data["children"] = para_combiner(data["children"])
    data["children"] = chapter_combiner(data["children"])

    with open(directoryname + "mod" + filename,"wb") as data_file:
        json.dump(data,data_file,sort_keys = False,indent = 4,separators = (',',':'))

def chapter_combiner(data):
    """
    Combines chapters
    """
    # init
    children_list = []
    chapter_list = []
    count = 0
    main_count = 0

    for i,chap in enumerate(data):
        # combine 6 chapters
        if (i+1)%6 == 0:
            main_count += 1
            # create chapter dictionary
            chapter_dict = {}
            chapter_dict["name"] = "Chapter_" + str(main_count)
            chapter_dict["sentiment"] = ""
            chapter_dict["children"] = children_list
            chapter_list.append(chapter_dict)
            count = 0
            children_list = []
        para_list = chap["children"]
        for paragraphs in para_list:
            count += 1
            # change paragraph number
            paragraphs["name"] = "Paragraph_" + str(count)
            children_list.append(paragraphs)

    # combine the residual chapters
    if (i+1)%6 != 0:
        main_count += 1
        chapter_dict = {}
        chapter_dict["name"] = "Chapter_" + str(main_count)
        chapter_dict["sentiment"] = ""
        chapter_dict["children"] = children_list
        chapter_list.append(chapter_dict)

    return chapter_list

def para_combiner(data):
    """
    Combines paragraphs
    """
    children_list = []
    for child in data:
        child["children"] = recursive_paracombiner(child["children"])
        children_list.append(child)
    return children_list

def recursive_paracombiner(data):
    """
    Recursive combiner
    """
    # init
    count = 0
    children_list = []
    text = []

    for i,child in enumerate(data):
        # combine 6 paragraphs
        if (i+1)%6 == 0:
            count += 1
            para_dict = {}
            # create paragraph dictionary
            para_dict["name"] = "Paragraph_" + str(count)
            para_dict["sentiment"] = ""
            para_dict["children"] = ""
            para_dict["value"] = text
            children_list.append(para_dict)
            text = []
        text.append(child["value"])

    # combine the residual paragraphs
    if (i+1)%6 != 0:
        count += 1
        para_dict = {}
        para_dict["name"] = "Paragraph_" + str(count)
        para_dict["sentiment"] = ""
        para_dict["children"] = ""
        para_dict["value"] = text
        children_list.append(para_dict)

    return children_list

