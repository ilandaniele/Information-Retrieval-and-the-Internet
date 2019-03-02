from pythonds.basic.stack import Stack
import json
import io
import math

#This code is inspired of:
#http://interactivepython.org/runestone/static/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
#https://www.saltycrane.com/blog/2007/09/how-to-sort-python-dictionary-by-keys/
#https://pypi.org/project/pythonds/ 
#https://www.tutorialspoint.com/python/python_sets.html
#https://pythonspot.com/python-set/

def infixToPostfix(infixexpr):
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = []
    tokenListAux = infixexpr.split()
    
    for t in tokenListAux:
        flag=0
        if(not(t == "")):
            if((t.startswith("(") and t != "(") or (t.endswith(")") and t != ")")):
                if(t.startswith("(") and t != "("):
                    t=t.replace("(",'')
                    tokenList.append("(")
                    if(t.endswith(")") and t != ")"):
                        t=t.replace(")",'')
                        tokenList.append(t)
                        tokenList.append(')')
                        flag = 1
                    else:
                        tokenList.append(t)

                if(t.endswith(")") and t != ")"):
                    t=t.replace(")",'')
                    if(flag == 0):
                        tokenList.append(t)

                    tokenList.append(")")
            else:
                tokenList.append(t)
    
    for token in tokenList:
        if (token != "*" and token != "/" and token != "+" and token != "-" and token != "(" and token != ")" ):
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and (prec[opStack.peek()] >= prec[token]):
                postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)

def postfixEval(postfixExpr):
    operandStack = Stack()
    tokenList = postfixExpr.split()
    with io.open('diccionario.json',encoding='utf8') as f:  
        data = json.load(f)

    docIDs = set()
    for token in tokenList:
        if (token != "*" and token != "/" and token != "+" and token != "-"):
            for indice in data['indexes']:
                if(indice['index'] == token):
                    aux = indice['documents']
                    for doc in aux:
                        docIDs.add(doc[0])
                    break
            operandStack.push(docIDs)
            docIDs = set()
        else:
            set2 = operandStack.pop()
            set1 = operandStack.pop()
            result = doMath(token,set1,set2)
            operandStack.push(result)
    return operandStack.pop()

def doMath(op, op1, op2):
    if op == "*":
        return op1 & op2
    elif op == "/":
        return op1 / op2
    elif op == "+":
        return op1 | op2
    else:
        return op1 - op2

def vsm(query):
    with io.open('diccionario.json',encoding='utf8') as f:  
        data = json.load(f)
    docStack = Stack()
    docIDs = set()
    tokenList = query.split()
    for token in tokenList:
        for indice in data['indexes']:
            if(indice['index'] == token):
                aux = indice['documents']
                for doc in aux:
                    docIDs.add(doc[0])
                break
        docStack.push(docIDs)
        docIDs = set()

    while not docStack.isEmpty():
        docIDs = docStack.pop() | docIDs #get all the documents in a row
    
    sparse = {}
    
    for doc in docIDs:
        for token in tokenList:
            element = []
            element.append(token)
            peso = 0
            for indice in data['indexes']:
                if(indice['index'] == token):
                    documents = indice['documents']
                    for document in documents:
                        if(document[0] == doc):
                            peso = document[1]
                            break
            
            element.append(peso)
            if(sparse.get(doc) is None):
                array=[]
                sparse[doc] = array
            sparse[doc].append(element)

    claves = sparse.keys()
    scores={}
    for c in sorted(claves):
        index = c
        queryWords = sparse.get(c)
        
        #calculate the query weight (I assume each word has a weight of 1):
        q= math.sqrt(len(queryWords))
        
        vector = []
        l2 = 0
        for word in queryWords:
            vector.append(word[1])
            l2 = l2 + (word[1])**2
        
        l2 = math.sqrt(l2)
        
        score = 0
        for i in range(0,len(vector)):
            
            score = score + vector[i] / l2 * q
        
        if(scores.get(index) is None):
            scores[index] = 0
        scores[index]= score
        
    scores_sorted = sorted(scores.items(),key=lambda kv:kv[1], reverse= True)
   
    docIDsFinal=[]
    for key,value in scores_sorted:
        docIDsFinal.append(key)
    
                
    return docIDsFinal