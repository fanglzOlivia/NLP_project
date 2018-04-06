import xml.etree.ElementTree as ET
import glob
import datetime
from dateutil.parser import parse

#filename = 'AnnotationFinal0-80/goldstandard0.xml'
gsFiles = sorted(glob.glob("/Users/julia/Desktop/NLP/AnnotationFinal0-80/*.xml"))

fileid = filename.replace('/Users/julia/Desktop/NLP/AnnotationFinal0-80/goldstandard', '').replace('.xml', '')

tree = ET.parse(filename)
root = tree.getroot()

timexCols = ['fileId', 'timexId', 'spanStart', 'spanEnd', 'value']
timexLst = []
eventCols = ['fileId', 'eventId', 'spanStart', 'span1', 'span2', 'spanEnd', 'text', 'class', 'eventType', 'polarity', 'completion']
eventLst = []
tLinkCols = ['fileId', 'tlinkId', 'timexId', 'eventId']
tLinkLst = []

# pull out attributes for each type of annotation element in the file and add to list
for filename in gsFiles:
    fileid = int(filename.replace('/Users/julia/Desktop/NLP/AnnotationFinal0-80/goldstandard', '').replace('.xml', ''))
    tree = ET.parse(filename)
    root = tree.getroot()
    #print(fileid)
    
    for ann in root.iter('TIMEX3'):
        #print('ID', ann.attrib['id'])
        tid = ann.attrib['id']
        [spanStart, spanEnd] = [int(r) for r in ann.attrib['spans'].split('~')]
        fx = ann.attrib['functionInDocument']
        if 'value' in ann.attrib:
            val = datetime.datetime.strptime(ann.attrib['value'], '%Y-%m-%d')
        else:
            val = datetime.datetime.strptime(ann.attrib['text'], '%Y-%m-%d')

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
