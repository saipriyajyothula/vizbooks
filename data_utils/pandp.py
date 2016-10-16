import re
f= open("pg1342.txt","r")
data = f.read()
f.close()
data=data.splitlines()
f= open("pg1342_modified.txt","w")
for i in range(len(data)):
    if((data[i]=='')&(data[i-1]!='')):
        f.write("\nSomeRandomThing.\n")
    elif(data[i]!=''):
        f.write(' '+data[i])
f.close()
f= open("pg1342_modified.txt","r")
data = f.read()
f.close()
caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr|Miss|Sir|Lord|Lady|Mister|Madam|)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = text.replace('"','')
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

datum = split_into_sentences(data)
temp = [datum[0]]
d = 1
for k in range(1,len(datum)):
    if(datum[k]!=temp[d-1]):
        temp.append(datum[k])
        d+=1
datum = temp
g=open("finaldata.json","w")    
chapternum = 0
paragraphnum = 0
sentencenum = 0
g.write('{"name":"Pride and Prejudice",\n"sentiment":"",\n"children":[')
for i in range(len(datum)):
    if(re.search("Chapter \d", datum[i])!= None):
        chapternum += 1
        paragraphnum = 1
        sentencenum = 0
        g.write('\n{"name":"Chapter_'+str(chapternum)+'",\n"sentiment":"",\n"children":[{\n"name":"Paragraph_'+str(paragraphnum)+'",\n"sentiment":"",\n"children":[')     
    elif(datum[i]=="SomeRandomThing."):
        paragraphnum +=1
        sentencenum = 0
        if(re.search("Chapter \d", datum[i+1])!= None):
            g.write('\n]},')
        else:
            g.write('\n{\n"name":"Paragraph_'+str(paragraphnum)+'",\n"sentiment":"",\n"children":[')
    else:
        sentencenum +=1
        if((i+1)<len(datum)-1):
            if(datum[i+1]=="SomeRandomThing."):
                g.write('\n{"name":"Sentence_'+str(sentencenum)+'",\n"value":"'+datum[i]+'",\n"sentiment":"",\n"children":""}]},')
            else:
                               g.write('\n{"name":"Sentence_'+str(sentencenum)+'",\n"value":"'+datum[i]+'",\n"sentiment":"",\n"children":""},')
        else:
                           g.write('\n{"name":"Sentence_'+str(sentencenum)+'",\n"value":"'+datum[i]+'",\n"sentiment":"",\n"children":""}]},')
g.close()
