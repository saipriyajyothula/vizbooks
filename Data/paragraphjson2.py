import re
from string import punctuation
punctuation += ' '
def preprocess(l):
    temp = ' '
    for k in l:
        if k not in punctuation:
            temp +=k
        else:
            if(temp[-1]!=' '):
                temp+=' '
    return temp


bookname = "Anne_of_the_Island"
f= open(bookname+".txt","r")
data = f.read()
f.close()
data =[x.replace('\r\n',' ') for x in re.split('\r\n\r\n',data) if x.replace('\r\n',' ')!='']
data =[i.replace('"','') for i in data]
data =[i.replace("\'",'"') for i in data]
data =[i.replace('"',"'") for i in data]
# data = [i.encode('ascii') if is_ascii(i) else "" for i in data]

g=open(bookname+"_paradata.json","w")    
chapternum = 0
paragraphnum = 0
g.write('{"name":"'+bookname.replace('_',' ')+'",\n"sentiment":"",\n"children":[')
for i in range(len(data)):
    if(re.search("CHAPTER [A-Z]", data[i])!= None):
        chapternum += 1
        g.write('\n{"name":"Chapter_'+str(chapternum)+'",\n"sentiment":"",\n"children":[')
    else:
        paragraphnum+=1
        if(paragraphnum==1):
            g.write('\n{\n"name":"Paragraph_'+str(paragraphnum)+'",\n"value":"'+data[i].strip()+'",\n"prevalue":"'+preprocess(data[i]).strip()+'",\n"sentiment":"",\n"children":""}')
        else:
            g.write(',\n{\n"name":"Paragraph_'+str(paragraphnum)+'",\n"value":"'+data[i].strip()+'",\n"prevalue":"'+preprocess(data[i]).strip()+'",\n"sentiment":"",\n"children":""}')
    if(i+1!=len(data)):
        if(re.search("CHAPTER [A-Z]", data[i+1])!= None):
            paragraphnum = 0
            g.write(']},')
g.write(']}\n]}')
g.close()
