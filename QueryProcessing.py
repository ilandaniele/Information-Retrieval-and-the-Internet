import nltk
import io
import json

#This code is inspired on:
#https://www.tutorialspoint.com/python/python_sets.html
#http://carrefax.com/new-blog/2017/5/20/stackoverflow-how-can-i-generate-bigrams-for-words-using-nltk-python-library
#https://pythonspot.com/python-set/

def lookForWildcard(exp):
    
    with io.open('secondaryIndex.json',encoding='utf8') as f: 
        data = json.load(f)
    

    tokenList = []
    tokenList = exp.split()
    #print(tokenList)
    queryFinal = ''
    bigrama2=[]
    for t in tokenList:
        indexFound = t.find('*')
        #print(indexFound)
        if(indexFound >= 0):

            if(indexFound == 0):
                spaced = ''
                for ch in t:
                    spaced = spaced + ch + ' '

                tokenized = spaced.split()
                #print(tokenized)
                raiz = []
                for c in tokenized:
                    if(c != '*'):
                        raiz.append(c)
                #raiz = tokenized.remove('*')
                print(raiz)
                bigrama = bigram(raiz,0,1)

                #for indice in data['indexes']:
                    #word = indice['index'].split('$')
                    
            elif(indexFound == (len(t) -1)):
                spaced = ''
                for ch in t:
                    spaced = spaced + ch + ' '

                tokenized = spaced.split()
                raiz = []
                for c in tokenized:
                    if(c != '*'):
                        raiz.append(c)
                #raiz = tokenized.remove('*')
                bigrama = bigram(raiz,1,0)
                

            else: #the * is in the middle of the word
                raiz = t.split('*')
                raiz1 = raiz[0]
                #print(raiz1)
                spaced = ''
                for ch in raiz1:
                    spaced = spaced + ch + ' '

                tokenized1 = spaced.split()
                bigrama = bigram(tokenized1,1,0)
                #print(bigrama)
                raiz2 = raiz[1]
                #print(raiz2)
                spaced = ''
                for ch in raiz2:
                    spaced = spaced + ch + ' '

                tokenized2 = spaced.split()
                bigrama2 = bigram(tokenized2,0,1)
                #print(bigrama2)
            
            set1=set()

            for indice in data['indexes']:
                for comp in bigrama:

                    if(indice['index'] == comp):
                        #print(comp)
                        setaux= set()
                        for term in indice['terms']:
                            #print(term)
                            setaux.add(term)
                        
                        if(len(set1) == 0 ):
                            set1 = set1|setaux
                        else: #intersecto ya que me quedo nomas con los que se comparten entre si
                            #osea por ejemplo empizan con o, luego siguen con op, y asi
                            set1 = set1 & setaux
                
                if(not(len(bigrama2)==0)):
                    for comp in bigrama2:
                        if(indice['index'] == comp):
                            setaux= set()
                            for term in indice['terms']:
                                setaux.add(term)
                            set1 = set1 & setaux
            k=0
            for termino in set1:
                if(k == len(set1) - 1):
                    if(k == 0):
                        queryFinal = queryFinal + '( ' + termino + ' ) '
                    else:
                        queryFinal = queryFinal + termino + ' '+ ')'
                elif(k == 0):
                    queryFinal = queryFinal + '( ' + termino + ' or '
                else:
                    queryFinal = queryFinal + termino + ' or '
                k=k+1          
        else: #no hay ningun *
            if(queryFinal == ''):
                queryFinal = t + ' '
            else:
                queryFinal = queryFinal + ' ' + t + ' '
    
    return queryFinal


def createSecondaryIndex():

    with io.open('diccionario.json',encoding='utf8') as f: 
        data = json.load(f)
    secondIndex = {}
    
    for indice in data['indexes']:
        
        word = indice['index']
        spaced = ''
        for ch in word:
            spaced = spaced + ch + ' '

        tokenized = spaced.split()
        
        arreglo = bigram(tokenized,1,1)
        
        
        for syllabe in arreglo:
            
            if(secondIndex.get(syllabe) is None):
                array = []
                secondIndex[syllabe] = array
            secondIndex[syllabe].append(word)
    
    datos = {}
    datos['indexes'] = []
    claves = secondIndex.keys()
    
    for c in sorted(claves):
        indice = c
        valor = secondIndex.get(c)

        datos['indexes'].append({
        'index': c,
        'terms': valor
        })      

    with io.open('secondaryIndex.json', 'w', encoding='utf8') as outfile:  
        json.dump(datos, outfile, ensure_ascii=False)

        

def bigram(array, begin, end):  #if begin == 1 then we add the term $letter to the bigram, same with end
                                #if not then we do not add it
    i = 0
    bigram = []
    anterior=''
    for letter in array:
        word=''
        if(i == 0 and begin == 1):
            word = '$'+ letter
        else:
            if(i != 0):
                word = anterior + letter

        if(word != ''):
            bigram.append(word)
        anterior=letter
        i=i+1
        if(i == len(array) and end==1):
            word=letter + '$'
            if(word != ''):
                bigram.append(word)
    
    return bigram

