# -*- coding: utf-8 -*-
"""
Created on Sunday, March 11

@author: ham2026

Lab on preprocessing text - lab 4 
"""
#####################################################################
import pandas as pd 
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords 
df = pd.read_csv('NOTEEVENTS.csv', nrows = 20)
dfDischarge = df.loc[df['CATEGORY']== 'Discharge summary'] 
#print(df)
notesList = dfDischarge["TEXT"].tolist()

# preprocesses each note separately 
# processedNotesList1 = lowercase, no punct, no numbers or symbols 
processedNotesList1 = []
for text in notesList: 
    textlower = text.lower() #lowercase
    tokenizer = RegexpTokenizer(r'[a-z]+') #tokenize & keep only lowercase words 
    tokens = tokenizer.tokenize(textlower)
    processedNotesList1.append(tokens)

### 
#Now remove stop words
# processedNotesList2 = no stopwords, lowercase, no punct, no numbers or symbols 
processedNotesList2 = []
for text in notesList: 
    textlower = text.lower() #lowercase
    tokenizer = RegexpTokenizer(r'[a-z]+') #tokenize & keep only lowercase words 
    tokens = tokenizer.tokenize(textlower)
    stoplist = set(stopwords.words('english'))
    #remove stopwords 
    cleanwordlist = [word for word in tokens if word not in stoplist]
    processedNotesList2.append(cleanwordlist)
#processedNotesList2 is a list of lists 

# one simple formula to preprocess 
def preprocess(text):
    text = text.lower()
    # remove just punctuation
    # tokenizer = RegexpTokenizer(r'\w+')
    
    # remove punctuation & numbers
    tokenizer = RegexpTokenizer(r'[a-z]+')
    tokens = tokenizer.tokenize(text)
    # remove stop words
    stoplist = set(stopwords.words('english'))
    cleanwordlist = [word for word in tokens if word not in stoplist]
    
    return " ".join(cleanwordlist)

################################################################
## Part B: Regex - looking for patterns in text 
    
# basics of regex 
import re 
from nltk.tokenize import word_tokenize

tokenizedList = []
for each in notesList: 
    tokenizedList.append(word_tokenize(each)) 

#******************* Regex Stuff **********************************************
    
# This Routine Looks for typical Date Pattern per Note - with or without the 
#leading Year - it also finds the start and end date in the string and retrieves the 
#50 characters before and after it - which might be able to be used for context
# it prints it but it needs to store the information in a dataframe
# The routine also extracts the Admission Date but isn't able to do anything with it in it's current format
#       

admissionPattern = r'Admission\s+Date:\s+(\[\*\*[0-9][0-9][0-9][0-9]-[1-9][0-9]{0,1}-[0-9][0-9]{0,1}\*\*\])'            
DatePattern = r'\[\*\*(\d{1,4}-)?(\d{1,2}-\d{1,2})\*\*\]' 

   
for i, each in enumerate(notesList): 
    print('Note %d: ' %(i+1))   
    Admit = re.search(admissionPattern,each,re.M ).group(1)
    print(Admit)
    for m in re.finditer(DatePattern, each,re.M):
        print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))
   #     if Admit > m.group(0):
   #         print ('%s' % m.group(0))
        strStart = 50
        strEnd = len(each)
        if m.start() > 50:
            strStart = m.start() - 50
        if m.end() + 50 < len(each):
            strEnd = m.end() + 50  
        print (each[strStart:strEnd])

# This saw that we could retrieve data into Year, Month,Day and inserted logic in it to put a default value for Year - if not in it 
# The default should be as a start Admission Year which we can retrieve - but I didn't retrieve it yet
# I also converted the date strings to a date object so that we can order them and do comparisons  (like are they after Admit Date) 
#These obviously need to be stored in lists - not in single variables and integrated with the above processes        

        
import datetime

DatePattern2 = r'\[\*\*((\d{0,4})-)?(\d{1,2})-(\d{1,2})\*\*\]' 
   
for i, each in enumerate(notesList): 
    print('Note %d: ' %(i+1))   
    for m in re.finditer(DatePattern2, each,re.M):
        print('%s' % m.group(0),m.group(1),m.group(2),m.group(3),m.group(4))
        Workday = m.group(4)
        Workmonth = m.group(3)
        if m.group(2) == None:
            WorkYear = 2121
        else:
            WorkYear = m.group(2)

x = datetime.date(int (WorkYear), int (Workmonth),int (Workday))
AdmitDate = datetime.date(2118,12,7) 

if x > AdmitDate:
 #   print ("%d" % x)
    print("ok") 


