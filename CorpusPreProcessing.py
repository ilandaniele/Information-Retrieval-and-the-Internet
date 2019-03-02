import argparse # built-in module
import sys
import os.path
import csv
import json
import io
import urllib
import dictionary
from bs4 import BeautifulSoup

#This code is inspired on:
#https://www.analyticsvidhya.com/blog/2017/03/read-commonly-used-formats-using-python/
#https://stackoverflow.com/questions/2521482/getting-beautifulsoup-to-find-a-specific-p
#https://www.tutorialspoint.com/python/python_reading_html_pages.htm
#https://stackoverflow.com/questions/30147223/beautiful-soup-findall-multiple-class-using-one-query
#https://stackoverflow.com/questions/13949637/how-to-update-json-file-with-python
#https://stackoverflow.com/questions/18337407/saving-utf-8-texts-in-json-dumps-as-utf8-not-as-u-escape-sequence

def html(file):
    archivo = open(file,'rb')
    html_doc = archivo.read() 
   
    #tell the encoder to use anothr one in the meta information look th encoding
    soup = BeautifulSoup(html_doc.decode('utf-8','ignore'),'html.parser')
    flagTitulo=0

    datos={}
    datos['courses'] = [] 
    for curso in soup.find_all('p', attrs={'class' : ['courseblocktitle noindent', 'courseblockdesc noindent'] }): 
        attributes = curso.attrs
        if(attributes['class'][0] == 'courseblocktitle'):
            if(flagTitulo == 1):
                datos['courses'].append({
                'courseID': courseID,
                'title': nombre,
                'description': ''
                })
            titulo=curso.string
            courseID1 = titulo[0:3]
            courseID2 = titulo[4:8]
            courseID= courseID1 + courseID2
            nombre = titulo[9:]
            flagTitulo=1
        else:
            if(attributes['class'][0] == 'courseblockdesc'):
                aux=curso.string
                if aux is None:
                    descripcion=''
                else:
                    descripcion=aux[2:]
                
                datos['courses'].append({
                'courseID': courseID,
                'title': nombre,
                'description': descripcion
                })
                flagTitulo=0
    
    with io.open('texto.json', 'w',encoding='utf8') as outfile:  
        json.dump(datos, outfile, ensure_ascii=False)
    dictionary.main('texto.json',0,0,1) #aca agrego el termino de diccionario pasado si es que me pasan uno
    

def main(file):
    file_extension = os.path.splitext(file)[1]
    if(file_extension == '.json'):
        print("1")
    else:
        if(file_extension == '.csv'):
            print("1")
        else:
            if(file_extension == '.xml'):
                print("1")
            else:
                if(file_extension == '.html'):
                    html(file)
                else:
                    if(file_extension == '.pdf'):
                        print("1")
                    else:
                        if(file_extension == '.docx'):
                            print("1")
                        else:
                            if(file_extension == '.txt'):
                                print("1")
                            else:
                                if(file_extension == '.xlsx'):
                                    print("1")
                                else:
                                    if(file_extension == '.h5'):
                                        print("1")


        
