from tkinter import *
from tkinter import messagebox
import tkinter
import Retrieval
import CorpusPreProcessing
import CorpusAccess
import io
import json
import QueryProcessing

#This code is inspired on:
#https://github.com/CaptainSame/Search-Engine-in-Python/blob/master/gui.py


def callback(filename):
    window=Tk()
    window.wm_title("Document: "+ filename +' -Vanilla Search Engine')
    blank='           '

    dirName="courses"
    with io.open(dirName+"/"+filename,encoding='utf8') as f:  
            data = json.load(f)
    
    title= data['course'][0]['courseID'] + " - " +data['course'][0]['title']
    description= data['course'][0]['description']
    blanklabel=Label( window,text=blank*10,font=("ComicSansMS", 10))
    label1 = Label( window,text=title+'\n',font=("ComicSansMS", 10))
    label1.pack()
    blanklabel.pack()

    blanklabel=Label( window,text=blank*20,font=("ComicSansMS", 10))
    label1 = Label( window,text=description+'\n',font=("ComicSansMS", 10), wraplength=750)
    label1.pack(expand=True, fill=BOTH)
    blanklabel.pack()
    
    

def executeQuery(query,retrievalModel):
    finalquery = ''
    iquery=query.lower()
    
    fquery = QueryProcessing.lookForWildcard(iquery)
    tokenList = fquery.split()
    
    if(retrievalModel == 'Boolean Model'):
        for token in tokenList:
            #print(token)   
            if(not(token == '') or not(token== ' ')):
                if(token == 'and'):
                    finalquery= finalquery + '* '
                elif(token == 'or'):
                    finalquery= finalquery + '+ '
                elif(token == 'not'):
                    finalquery= finalquery + '- '
                else:
                    finalquery= finalquery + token + ' '
        
        finalquery=Retrieval.infixToPostfix(finalquery)
        docIDs=Retrieval.postfixEval(finalquery)
    else:
        for token in tokenList:
            if(not(token == '') or not(token== ' ')):
                finalquery=finalquery + token + ' '
        docIDs=Retrieval.vsm(finalquery)
        

    filenames=[]
    titles=[]
    descriptions=[]
    CorpusAccess.CorpusAccess(docIDs,filenames,titles,descriptions)

    searchf=Tk()
    searchf.wm_title(query +'-Vanilla Search Engine')

    blank='           '
    blanklabel=Label( searchf,text=blank*20,font=("ComicSansMS", 10))
    label1 = Label( searchf,text="Query: "+query+'\n',font=("ComicSansMS", 20))
    label1.pack()
    blanklabel.pack()

    text = Text(searchf,wrap="none")
    vsb = Scrollbar(orient="vertical", command=text.yview)
    text.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    text.pack(fill="both", expand=True)

    j=0
    for i in filenames:
        
        blanklabel=Label( searchf,text=blank*5,font=("ComicSansMS", 6))
        blanklabel.pack()
        text.window_create("end", window=blanklabel)
        text.insert("end", "\n")

        Button = tkinter.Button(searchf, text=i.replace('.json','') + " - " + titles[j][:30] + '...' ,font=("ComicSansMS", 15),justify=LEFT, fg="blue", cursor="hand2", command=lambda i=i: callback(i))
        text.window_create("end", window=Button)
        text.insert("end", "\n")
        
        labl=Label( searchf,text=descriptions[j][:100] + '...',font=("ComicSansMS", 12),justify=LEFT, fg="black")
        labl.pack()
        text.window_create("end", window=labl)
        text.insert("end", "\n")
        
        j=j+1
        
    text.configure(state="disabled")
    

def main():    
    #to create the window
    root=Tk()
    root.wm_title("Vanilla Search Engine")
    #add widgets here
    f = Frame(root, width=600,height=450)
    f.pack(fill=X, expand=True)

    e1=Entry(root,bd=6,width=60)
    e1.insert(END, 'search here')
    e1.place(relx=0.45, rely=0.35, anchor=CENTER)
    
    b1=Button(root,text="Search in UofO Courses",command= lambda: executeQuery(e1.get(),tkvar.get()))
    b1.place(relx=0.25, rely=0.45, anchor=CENTER)

    b2=Button(root,text="Search in Reuters",command= lambda: executeQuery(e1.get(), tkvar.get()))
    b2.place(relx=0.5, rely=0.45, anchor=CENTER)

    b3=Button(root,text="Search in Web Collection",command= lambda: executeQuery(e1.get(), tkvar.get()))
    b3.place(relx=0.75, rely=0.45, anchor=CENTER)
    
    #code for the optionmenu
    
    # Create a Tkinter variable
    tkvar = StringVar(root)

    # Dictionary with options
    choices = ['Boolean Model','Vector Space Model']
    tkvar.set(choices[0]) # set the default option

    popupMenu = OptionMenu(root, tkvar, *choices)
    popupMenu.place(relx=0.80, rely=0.35, anchor=CENTER)

    # on change dropdown value
    def change_dropdown(*args):
        print( tkvar.get() )

    # link function to change dropdown
    tkvar.trace('w', change_dropdown)
    
    CorpusPreProcessing.main("texto.html")
    #necessary code to run it
    root.mainloop()


if __name__ == '__main__':
    main()