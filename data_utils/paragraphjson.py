import re
f= open("pg1342.txt","r")
data = f.read()
f.close()
data =[x.replace('\r\n',' ') for x in re.split('\r\n\r\n',data) if x.replace('\r\n',' ')!='']
data =[i.replace('"','') for i in data]
data =[i.replace("\'",'"') for i in data]
data =[i.replace('"',"'") for i in data]
g=open("paradata.json","w")    
chapternum = 0
paragraphnum = 0
g.write('{"name":"Pride and Prejudice",\n"sentiment":"",\n"children":[')
for i in range(len(data)):
    if(re.search("Chapter \d", data[i])!= None):
        chapternum += 1
        g.write('\n{"name":"Chapter_'+str(chapternum)+'",\n"sentiment":"",\n"children":[')
    else:
        paragraphnum+=1
        if(paragraphnum==1):
            g.write('\n{\n"name":"Paragraph_'+str(paragraphnum)+'",\n"value":"'+data[i]+'",\n"sentiment":"",\n"children":""}')
        else:
            g.write(',\n{\n"name":"Paragraph_'+str(paragraphnum)+'",\n"value":"'+data[i]+'",\n"sentiment":"",\n"children":""}')
    if(i+1!=len(data)):
        if(re.search("Chapter \d", data[i+1])!= None):
            paragraphnum = 0
            g.write(']},')
g.write(']}\n]}')
g.close()
