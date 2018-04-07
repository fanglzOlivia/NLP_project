import xml.etree.ElementTree as ET
import pandas as pd 
import glob
import re

#filename = 'AnnotationFinal0-80/goldstandard0.xml'
gsFiles = sorted(glob.glob("/Users/oliviazhu/Desktop/Cornell/Winter2018/NLP/AnnotationFinal0-80/*.xml",recursive=True))

#fileid = filename.replace('/Users/oliviazhu/Desktop/Cornell/Winter2018/NLP/AnnotationFinal0-80/goldstandard', '').replace('.xml', '')

#tree = ET.parse(filename)
#root = tree.getroot()

timexCols = ['fileId', 'timexId', 'spanStart', 'spanEnd', 'value','Date']
timexLst = []
eventCols = ['fileId', 'eventId', 'spanStart', 'span1', 'span2', 'spanEnd', 'text', 'class', 'eventType', 'polarity', 'completion']
eventLst = []
tLinkCols = ['fileId', 'tlinkId', 'timexId', 'eventId']
tLinkLst = []

# pull out attributes for each type of annotation element in the file and add to list
for filename in gsFiles:
    fileid = filename.replace('/Users/oliviazhu/Desktop/Cornell/Winter2018/NLP/AnnotationFinal0-80/goldstandard', '').replace('.xml', '')

    tree = ET.parse(filename)
    root = tree.getroot()
    #print(fileid)
    
    for ann in root.iter('TIMEX3'):
        #print('ID', ann.attrib['id'])
        tid = ann.attrib['id']
        [spanStart, spanEnd] = [int(r) for r in ann.attrib['spans'].split('~')]
        fx = ann.attrib['functionInDocument']
        if 'value' in ann.attrib:
            val = ann.attrib['value']
        else:
            val = ann.attrib['text']

        timexLst.append([fileid, tid, spanStart, spanEnd, val, fx])
    
    for ann in root.iter('EVENT'):
        eid = ann.attrib['id']
        sp = ann.attrib['spans']
        if sp.find(',') > 0:
            [spanStart, span1, span2, spanEnd] = [int(r) for r in re.split('[~,]', sp)]
        else:
            [spanStart, spanEnd] = [int(r) for r in sp.split('~')]
            [span2, span1] = [int(r) for r in sp.split('~')]
        text = ann.attrib['text']
        cls = ann.attrib['class']
        et = ann.attrib['eventType']
        pol = ann.attrib['polarity']
        if 'completion' in ann.attrib:
            comp = ann.attrib['completion']
        else: comp = None
        
        eventLst.append([fileid, eid, spanStart, span1, span2, spanEnd, text, cls, et, pol, comp])
    
    for ann in root.iter('TLINK'):
        tlid = ann.attrib['id']
        tid = ann.attrib['fromID']
        eid = ann.attrib['toID']
        
        tLinkLst.append([fileid, tlid, tid, eid])
        
dfTimex = pd.DataFrame(timexLst, columns=timexCols)
dfEvent = pd.DataFrame(eventLst, columns=eventCols)
dfTLink = pd.DataFrame(tLinkLst, columns=tLinkCols)

#save as csv files
dfTimex.to_csv('Timex.csv')
dfEvent.to_csv('Event.csv')
dfTLink.to_csv('TLink.csv')


import csv
import matplotlib.pyplot as plt

from operator import itemgetter
from collections import defaultdict
import matplotlib.dates as mdates
#from matplotlib.finance import date2num
from matplotlib.dates import date2num


#### code to generate the full data by merging the timex, event, and tlink dataframes created by the xml parsing
mt = dfTLink.merge(dfTimex[['fileId', 'timexId', 'spanStart', 'spanEnd', 'value']], left_on=['fileId','timexId'], right_on=['fileId', 'timexId'])
mt.columns = ['fileId', 'tlinkId', 'timexId', 'eventId', 'timexSpanStart', 'timexSpanEnd', 'timexValue']

dfTLinkTrainMerged = mt.merge(dfEvent, left_on=['fileId', 'eventId'], right_on=['fileId', 'eventId'])
dfTLinkTrainMerged.columns = ['fileId', 'tlinkId', 'timexId', 'eventId', 'timexSpanStart', 'timexSpanEnd', 'timexValue'
, 'eventSpanStart', 'eventSpan1', 'eventSpan2', 'eventSpanEnd', 'eventText', 'class', 'eventType', 'polarity', 'completion']

dfTLinkTrainMerged['eventLabel'] = dfTLinkTrainMerged.eventType.map({'DNI':0, 'DNR':1, 'FEEDING TUBE':2, 'FOLEY':3, 'INTUBATION':4, 'RESUSCITATION':5, 'TRANSFER':6})

dfTLinkTrainMerged['polarityLabel'] = dfTLinkTrainMerged.polarity.map({'POSITIVE':"red", 'NEGATIVE':"blue"})

dfTLinkTrainMerged['minSpanStart'] = dfTLinkTrainMerged[['timexSpanStart', 'eventSpanStart', 'eventSpan2']].min(axis=1)

dfTLinkTrainMerged['maxSpanEnd'] = dfTLinkTrainMerged[['timexSpanEnd', 'eventSpanEnd', 'eventSpan1']].max(axis=1)


tt = ([[1, 'TL0', 'T2', 'E1', 6019, 6027, datetime.date(2118, 6, 7),6003, 6012, 6003, 6012, 'intubated', 'OCCURRENCE', 'INTUBATION','POSITIVE', 'COMPLETED', 4, 1, 6003, 6027],[1, 'TL1', 'T5', 'E2', 6481, 6490, datetime.date(2118, 6, 11),6511, 6520, 6511, 6520, 'extubated', 'OCCURRENCE', 'INTUBATION','NEGATIVE', 'COMPLETED', 4, 0, 6481, 6520],[1, 'TL2', 'T5', 'E3', 6481, 6490, datetime.date(2118, 6, 11),6629, 6661, 6629, 6661, 'transferred to the medical floor','OCCURRENCE', 'TRANSFER', 'NEGATIVE', 'COMPLETED', 6, 0, 6481,6661],[1, 'TL3', 'T8', 'E5', 7669, 7678, datetime.date(2118, 6, 14),7631, 7662, 7631, 7662, 'Foley catheter was discontinued','OCCURRENCE', 'FOLEY', 'NEGATIVE', 'COMPLETED', 3, 0, 7631, 7678]])


dfTLinkTrainMerged = pd.DataFrame(tt, columns = ['fileId', 'tlinkId', 'timexId', 'eventId', 'timexSpanStart', 'timexSpanEnd', 'timexValue', 'eventSpanStart', 'eventSpan1', 'eventSpan2', 'eventSpanEnd', 'eventText', 'class', 'eventType', 'polarity', 'completion', 'eventLabel', 'polarityLabel', 'minSpanStart', 'maxSpanEnd'])

## plotting
x = date2num(dfTLinkTrainMerged['timexValue'])
x2 = date2num(datetime.date(2118,6,2))
y = dfTLinkTrainMerged['eventText']
c = dfTLinkTrainMerged['polarityLabel']
d = dfTLinkTrainMerged['polarity']

#plt.scatter(x=x, y=y, c=c,s=60)
#plt.title("Timeline Plot")
#plt.xlabel('Date')
#plt.show()

import numpy as np

labels = ["Positive","Negative","Negative","Negative"]
df = pd.DataFrame(dict(x=x-x2, y=y, label=labels))
groups = df.groupby('label')

fig, ax = plt.subplots()
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='',ms=12, label=name)
ax.legend()
plt.title("Timeline Plot",fontsize=18)
plt.xlabel('Days since Admission date',fontsize=16)
plt.show()








































