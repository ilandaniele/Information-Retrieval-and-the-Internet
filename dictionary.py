import json
import io
import math
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import QueryProcessing

#This code is inspired of:
#https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
#https://stackoverflow.com/questions/35807433/import-nltk-no-module-nltk-corpus
#https://www.tutorialspoint.com/python/python_sets.htm

def indexar(diccionario,string,courseID,stopwordRemoval,stemming,normalization):
    stop_wordsE = set(stopwords.words('english'))
    stop_wordsF = set(stopwords.words('french')) 
    ps = PorterStemmer() 
    word = ''
    skip=0
    string = string.lower()
    for c in string:
        if(normalization == 1):
            if (c == '.' or c == '-'):
                skip=1
            else:
                skip=0

        if(skip == 0): 
            if(not(c == '(' or c == ')' or c == '"' or c == '/' or c == '&' or c == ',' or c == ';' or c == ':')):
                if(c == ' ' or string.endswith(word + c)):
                    if(string.endswith(word + c)):
                        word = word + c
                    if(not(word == '') ):
                        if(stopwordRemoval == 0):
                            if(stemming == 1):
                                word=ps.stem(word)
                            if(diccionario.get(word) is None):
                                array=[]
                                diccionario[word] = array
                                #adding it to the wildcards index
                                #QueryProcessing.add(word)

                            diccionario[word].append(courseID)
                        else:
                            if(not(word in stop_wordsE or word in stop_wordsF)):
                                if(stemming == 1):
                                    word=ps.stem(word)
                                if(diccionario.get(word) is None):
                                    array=[]
                                    diccionario[word] = array
                                    #adding it to the wildcards index
                                    #QueryProcessing.add(word)

                                diccionario[word].append(courseID)
                        
                        word=''
                else:
                    word = word + c
    
                

def main(corpusFile, stopwordRemoval, stemming, normalization, dictionaryFile=None):
    
    if(dictionaryFile == None):
        diccionario={}
        with io.open(corpusFile,encoding='utf8') as f:  
            data = json.load(f)
        
        length = len(data["courses"])
        N = length
        for i in range(0,length):
            courseID = data['courses'][i]['courseID']
            title = data['courses'][i]['title']
            description =  data['courses'][i]['description']

            #tokenize 
            indexar(diccionario,title,courseID,stopwordRemoval,stemming,normalization)
            indexar(diccionario,description,courseID,stopwordRemoval,stemming,normalization)
        
        claves = diccionario.keys()
        datos = {}
        datos['indexes'] = []
        for c in sorted(claves):
            indice = c
            valor = diccionario.get(c)
            pesos = {}
            matriz = []

            dF = termFrequency(valor,pesos)
            idF = math.log(N/dF)
            
            for curso in valor:
                weight = []
                weight.append(curso)
                weight.append(pesos.get(curso) * idF)
                matriz.append(weight)
            
            datos['indexes'].append({
                'index': indice,
                'documents': matriz
                })
            
            
        with io.open('diccionario.json', 'w',encoding='utf8') as outfile:  
            json.dump(datos, outfile, ensure_ascii=False)
    QueryProcessing.createSecondaryIndex()


    
def termFrequency(array,pesos):
    for curso in array:
        tf=0
        for curso2 in array:
            if(curso == curso2):
                tf=tf+1
        if(pesos.get(curso) is None):
            pesos[curso] = tf
    
    return len(pesos.keys())



