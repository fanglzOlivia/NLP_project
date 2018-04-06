

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import date2num

####-----
#### code to generate the full data by merging the timex, event, and tlink dataframes created by the xml parsing
# mt = dfTLinkTrain.merge(dfTimexTrain[['fileId', 'timexId', 'spanStart', 'spanEnd', 'value']], left_on=['fileId','timexId'], right_on=['fileId', 'timexId'])
# mt.columns = ['fileId', 'tlinkId', 'timexId', 'eventId', 'timexSpanStart', 'timexSpanEnd', 'timexValue']
# dfTLinkTrainMerged = mt.merge(dfEventTrain, left_on=['fileId', 'eventId'], right_on=['fileId', 'eventId'])
# dfTLinkTrainMerged.columns = ['fileId', 'tlinkId', 'timexId', 'eventId', 'timexSpanStart', 'timexSpanEnd', 'timexValue'
#                                 , 'eventSpanStart', 'eventSpan1', 'eventSpan2', 'eventSpanEnd', 'eventText', 'class', 'eventType', 'polarity', 'completion']

# dfTLinkTrainMerged['eventLabel'] = dfTLinkTrainMerged.eventType.map({'DNI':0, 'DNR':1, 'FEEDING TUBE':2, 'FOLEY':3, 'INTUBATION':4, 'RESUSCITATION':5, 'TRANSFER':6})
# dfTLinkTrainMerged['polarityLabel'] = dfTLinkTrainMerged.polarity.map({'POSITIVE':1, 'NEGATIVE':0})
# dfTLinkTrainMerged['minSpanStart'] = dfTLinkTrainMerged[['timexSpanStart', 'eventSpanStart', 'eventSpan2']].min(axis=1)
# dfTLinkTrainMerged['maxSpanEnd'] = dfTLinkTrainMerged[['timexSpanEnd', 'eventSpanEnd', 'eventSpan1']].max(axis=1)
####-----


####-----
#### test code
tt = ([[1, 'TL0', 'T2', 'E1', 6019, 6027, datetime.date(2118, 6, 7),
        6003, 6012, 6003, 6012, 'intubated', 'OCCURRENCE', 'INTUBATION',
        'POSITIVE', 'COMPLETED', 4, 1, 6003, 6027],
       [1, 'TL1', 'T5', 'E2', 6481, 6490, datetime.date(2118, 6, 11),
        6511, 6520, 6511, 6520, 'extubated', 'OCCURRENCE', 'INTUBATION',
        'NEGATIVE', 'COMPLETED', 4, 0, 6481, 6520],
       [1, 'TL2', 'T5', 'E3', 6481, 6490, datetime.date(2118, 6, 11),
        6629, 6661, 6629, 6661, 'transferred to the medical floor',
        'OCCURRENCE', 'TRANSFER', 'NEGATIVE', 'COMPLETED', 6, 0, 6481,
        6661],
       [1, 'TL3', 'T8', 'E5', 7669, 7678, datetime.date(2118, 6, 14),
        7631, 7662, 7631, 7662, 'Foley catheter was discontinued',
        'OCCURRENCE', 'FOLEY', 'NEGATIVE', 'COMPLETED', 3, 0, 7631, 7678]])
dfTLinkTrainMerged = pd.DataFrame(tt, columns = ['fileId', 'tlinkId', 'timexId', 'eventId', 'timexSpanStart', 'timexSpanEnd', 'timexValue'
                            , 'eventSpanStart', 'eventSpan1', 'eventSpan2', 'eventSpanEnd', 'eventText', 'class'
                            , 'eventType', 'polarity', 'completion', 'eventLabel', 'polarityLabel', 'minSpanStart', 'maxSpanEnd'])
####-----

## plotting
x = data2num(dfTLinkTrainMerged['timexValue'])
y = dfTLinkTrainMerged['eventLabel']
c = dfTLinkTrainMerged['polarityLabel']

plt.scatter(x=x, y=y, c=c)
plt.show()