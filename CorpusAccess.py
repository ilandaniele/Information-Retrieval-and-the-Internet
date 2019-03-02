import json
import io
import os

def CorpusAccess(arrayDocIDs,fileNames,titles,descriptions): #both are arrays, one with documentsIDS retrieved by the model
    #an the other one is void and it would be filled here to use it later in other module

    with io.open('texto.json',encoding='utf8') as f: #I assume i know the name of the file
        data = json.load(f)                         
    
    dirName="courses"
    if not os.path.exists(dirName):
        os.mkdir(dirName)

    for i in arrayDocIDs:
        for course in data['courses']:
            if(course['courseID'] == i):
                nameArchive=course['courseID'] + ".json"
                titleArchive=course['title']
                descriptionArchive=course['description']
                datos={}
                datos['course'] = [] 
                datos['course'].append({
                'courseID': course['courseID'],
                'title': course['title'],
                'description': course['description']
                })
                fileNames.append(nameArchive)
                titles.append(titleArchive)
                descriptions.append(descriptionArchive)
                with io.open(dirName+"/"+nameArchive, 'w', encoding='utf8') as outfile:  
                    json.dump(datos, outfile, ensure_ascii=False)
                break
            


