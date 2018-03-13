#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 19:14:40 2017

@author: TP
"""



#importing libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
#from sklearn.model_selection import train_test_split
#from sklearn.metrics import precision_recall_fscore_support
from sklearn import metrics
from sklearn.model_selection import cross_validate

import matplotlib.pyplot as plt
# import pipeline class
#from sklearn.pipeline import Pipeline
#import GridSearch
#from sklearn.model_selection import GridSearchCV
#from sklearn.svm import LinearSVC 


import matplotlib.pyplot as plt
from pandas_datareader.data import DataReader
# date time to use date objects
from datetime import date






#importing data
twt=pd.read_csv("/Users/bhumikasingh/Downloads/trainingandtestdata/training.1600000.processed.noemoticon.csv",
                header=None,usecols=[0,5])
#twt.shape

#twt.describe()

#twt.head()
#twt.info()
#53% labels are 2, balanced dataset


text=twt[5]
target=twt[0]
#Target details 0 - the polarity of the tweet (0 = negative,  4 = positive)

# initialize the sklearn TfidfVectorizer 
# decode_error ignore for tweets
tfidf_vect = TfidfVectorizer(decode_error='ignore') 

# generate tfidf matrix
dtm= tfidf_vect.fit_transform(text)

#print("type of dtm:", type(dtm))
#print("size of tfidf matrix:", dtm.shape)


#Classifier


clf = MultinomialNB()



#indexing with date is important, since its easier to work with time series
aapl=pd.read_csv("appl.csv",index_col='date', parse_dates=True)

aapl.head()



# generate tfidf matrix
dtmT= tfidf_vect.transform(aapl['text'])
dtm.shape
dtmT.shape

clf.fit(dtm, target)


predicted=clf.predict(dtmT)

final = pd.DataFrame()

final['Text'] = aapl['text']
final["polar"]=predicted


#checking count of tweets for each day, by using daily sampling
final.resample('D').count()

# need to group by date and calculate the avreage
# if average is greater than 2 polar is positive else negative

#final['n']=final.polar.resample('D').count()


check=pd.DataFrame()

#  Daily average of polarity of tweets
check['mean']=final.polar.resample('D').mean()
#Daily sentiment based on average
#we need to consider the issue of tweets coming after market is closed
#we can take open value and use one previous day sentiment


#takinng mean cutoff at 1.5, it should be two
check['sent']=np.where(check['mean']>1.5,1,0)

#one means postive 0 means negative 
#final.to_csv('aaplPolar.csv')


start = date(2017,10,01)
end = date(2017,11,06)


stockApl = DataReader('AAPL', 'yahoo', start, end)['Close']
stockApl.head()


#plotting
stockApl.plot(title='APPLE')
plt.show()

#calculating daily returns of the stock
# To check the movement of the stock on that day
dr_apl = stockApl.pct_change(1)

#encoding returns for comparison
dr_apl[ dr_apl <0 ] = 0   

dr_apl[ dr_apl >0 ] = 1  

#removing first row whic is Nan
dr_apl=dr_apl[1:]

# adding stock movement to check
check['stock']=dr_apl
# dropping NA for dates on which market was close
check=check.dropna()

#creating a flag to see the similarity between sentiment and stock movement
check['flag'] = np.where(check.sent == check.stock, 1,0) 
#checking corr                               

check.flag.describe()

# 48% times they have moved together movement with cutoff at 1.5
check.loc[:,['sent','stock']].plot()



