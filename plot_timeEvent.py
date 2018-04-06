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


def plot_timeline(dataset, **kwargs):
    """
    Plots a timeline of events from different sources to visualize a relative sequence or density of events. Expects data in the form of:
(timestamp, source, category)
    Though this can be easily modified if needed. Expects sorted input.
    """
    outpath = kwargs.pop('savefig', None)  # Save the figure as an SVG
    #colors  = kwargs.pop('colors', {})     # Plot the colors for the series.
    series  = set([])                      # Figure out the unique series

    # Bring the data into memory and sort
    dataset = sorted(list(dataset), key=itemgetter(0))
    
# Make a first pass over the data to determine number of series, etc.
    for _, source, category in dataset:
        series.add(source)
        #if category not in colors:
            #colors[category] = 'k'

    # Sort and index the series
    series  = sorted(list(series))

    # Create the visualization
    x = []  # Scatterplot X values
    y = []  # Scatterplot Y Values
    c = []  # Scatterplot color values

    # Loop over the data a second time
    for timestamp, source, category in dataset:
        x.append(timestamp)
        y.append(series.index(source))
        #c.append(colors[category])

    plt.figure(figsize=(14,4))
    plt.title(kwargs.get('title', "Timeline Plot"))
    plt.ylim((-1,len(series)))
   # plt.xlim((-1000, dataset[-1][0]+1000))
    plt.yticks(range(len(series)-1), series)
    plt.scatter(x, y, color=c, alpha=0.85, s=10)

    if outpath:
        return plt.savefig(outpath, format='svg', dpi=1200)

    return plt

if __name__ == '__main__':
    colors = {'red': 'r', 'blue': 'b', 'green': 'g','cyan':'c','yellow':'y','black':'k','pink':'p','purple':'u'}
    with open('filter.csv', 'r') as f:
        reader = csv.reader(f)
        plt = plot_timeline([
            ((row[0]), row[1], row[2])
            for row in reader
        ], colors=colors)
        plt.show()



