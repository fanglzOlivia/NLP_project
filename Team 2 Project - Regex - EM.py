# -*- coding: utf-8 -*-
"""
Created on Sunday, March 19

@author: E McGivney

Lab on preprocessing text - lab 4 
"""
#####################################################################
import pandas as pd 
import datetime
import re 

def DetRange(Adm,x,Dis):
    if x < Adm:
        return "Before"
    if x > Dis:
        return "After"
    else :  
        return "Yes"

df = pd.read_csv('NOTEEVENTS.csv', nrows = 20)
dfDischarge = df.loc[df['CATEGORY']== 'Discharge summary'] 

admissionPattern = r'Admission\s+Date:\s+(\[\*\*([0-9][0-9][0-9][0-9])-([1-9][0-9]{0,1})-([0-9][0-9]{0,1})\*\*\])' 
dischargePattern = r'Discharge\s+Date:\s+(\[\*\*([0-9][0-9][0-9][0-9])-([1-9][0-9]{0,1})-([0-9][0-9]{0,1})\*\*\])'  
DatePattern = r'\[\*\*((\d{0,4})-)?(\d{1,2})-(\d{1,2})\*\*\]' 

cols=["ID","ADMIT_DT","DIS_DT","RAW_DT","RANGE","NEW_DT","START","END"]
lst = []
for index, note in dfDischarge.iterrows(): 
    AdmitG = re.search(admissionPattern,note["TEXT"],re.M )
    AdmitYY = AdmitG.group(2)
    AdmitDate = datetime.date(int (AdmitYY),int (AdmitG.group(3)),int (AdmitG.group(4))) 
    DischargG = re.search(dischargePattern,note["TEXT"],re.M )
    DischargDate = datetime.date(int (DischargG.group(2)),int (DischargG.group(3)),int (DischargG.group(4))) 
    for m in re.finditer(DatePattern,note["TEXT"],re.M):
        print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))
        Workday = m.group(4)
        Workmonth = m.group(3)
        if m.group(2) == None:
            WorkYear = AdmitYY
        else:
            WorkYear = m.group(2)
        NoteDate = datetime.date(int (WorkYear), int (m.group(3)),int (m.group(4)))
        WorkRange = DetRange(AdmitDate,NoteDate,DischargDate)
        lst.append([note["ROW_ID"],AdmitDate,DischargDate,m.group(0),WorkRange,NoteDate,m.start(), m.end()])
   #     strStart = 50
   #     strEnd = len(Note)
   #     if m.start() > 50:
   #         strStart = m.start() - 50
   #     if m.end() + 50 < len(Note):
   #         strEnd = m.end() + 50  
   #     print (Note[strStart:strEnd])
dfDates = pd.DataFrame(lst, columns=cols)        

  


         
