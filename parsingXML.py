import xml.etree.ElementTree as ET
filename = 'AnnotationFinal0-80/goldstandard0.xml'
fileid = filename.replace('AnnotationFinal0-80/goldstandard', '').replace('.xml', '')

tree = ET.parse(filename)
root = tree.getroot()

timexCols = ['fileId', 'timexId', 'spanStart', 'spanEnd', 'value']
timexLst = []

# pull out attributes for each TIMEX3 element in the file and add to list
for ann in root.iter('TIMEX3'):
    #print('ID', ann.attrib['id'])
    tid = ann.attrib['id']
    [spanStart, spanEnd] = [int(r) for r in ann.attrib['spans'].split('~')]
    val = ann.find('value')
    if val is not None:
        val = ann.attrib['value']
    else:
        val = ann.attrib['text']

    timexLst.append([fileid, tid, spanStart, spanEnd, val])