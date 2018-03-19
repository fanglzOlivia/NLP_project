#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 22:40:49 2018

@author: oliviazhu
"""

import pandas as pd 
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords 
df = pd.read_csv('NOTEEVENTS.csv', nrows = 20)
dfDischarge = df.loc[df['CATEGORY']== 'Discharge summary'] 
dfDischarge.to_csv('first20.csv')

notesList = dfDischarge["TEXT"].tolist()
f = open('first20.txt', 'w')
for pt_note in notesList: 
    f.write("-"*80)
    f.write(pt_note)
f.close()

# basics of regex 
import re 
from nltk.tokenize import word_tokenize
import datetime

#for i, each in enumerate(notesList): 
    #print('Note %d: ' %(i+1))
    #print(re.findall(admissionPattern, each, re.M)) 

    
#extract admission & discharge date in the first 20 notes     
admissionPattern = r'Admission Date: [\s./-]* \[\*\*\d{4}-\d{1,2}-\d{1,2}\*\*\]'

import dateutil.parser as dparser  

admitdate =[]
for i, each in enumerate(notesList): 
    
    for a in re.finditer(admissionPattern, each,re.M): #this finds each date        
            
        print('%s' % admitdate)  #extract date patterns
        print('Note %d: ' %(i+1))
        print(re.findall(admissionPattern , each, re.M))
        admitdate.append(dparser.parse(a.group(0),fuzzy=True))                            
        print(admitdate)
    
    
dischargePattern = r'Discharge Date: [\s./-]* \[\*\*\d{4}-\d{1,2}-\d{1,2}\*\*\]'
# [\s./-]* ignore whitespace between 'Discharge Date:" and "time records", some of the records have 2 spaces while some have 3 spaces
dischargedate =[]
for i, each in enumerate(notesList): 
   
    for b in re.finditer(dischargePattern, each,re.M): #this finds each date        
            
        #print('%s' % dischargedate)  #extract date patterns
        print('Note %d: ' %(i+1))
        print(re.findall(dischargePattern , each, re.M))
        dischargedate.append(dparser.parse(b.group(0),fuzzy=True))                            
        print(dischargedate)
        
        
#Determine if Obtained Date is between Admission and Discharge Dates 
        
 #extract and normalize all explicit dates mentioned in the first 20 notes
DatePattern = r'\[\*\*((\d{0,4})-)?(\d{1,2})-(\d{1,2})\*\*\]' 
 
dateall = []   
for i, each in enumerate(notesList):  

    for m in re.finditer(DatePattern, each,re.M): #this finds each date
        
        print('%s' % m.group(0),m.group(1),m.group(2),m.group(3),m.group(4))   ## this breaks it into month/day/year -> so it can be used to                                                                                                                                                 ##  create a date object for comparisons  
        Workday = m.group(4)
        Workmonth = m.group(3)
        if m.group(2) == None:
            WorkYear = 0000
        else:
            WorkYear = m.group(2)
        print('Note %d: ' %(i+1))
        dateall.append(dparser.parse(m.group(0),fuzzy=True))  #create datetimeobject to save these results


#put all admissiondate + dischargedate into a list
datelist = list(zip(admitdate,dischargedate))

#define interval

def within(the_date): 
    for a, each in enumerate(datelist):
        if datelist[a][a] <= the_date <= datelist[a][a+1]:
            print(datelist[a][a],the_date,datelist[a][a+1])
        else:
            return False
        
#have trouble on how to classify extracted datepattern into each note and them condition on it.



 

    

      
    
   
    
    
    
    
    
    
    
    
    
    
    
    