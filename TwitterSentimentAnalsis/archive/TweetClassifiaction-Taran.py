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

#import matplotlib.pyplot as plt
# import pipeline class
#from sklearn.pipeline import Pipeline
#import GridSearch
#from sklearn.model_selection import GridSearchCV
#from sklearn.svm import LinearSVC 



#importing data
twt=pd.read_csv("/Users/kumarbipulesh/PycharmProjects/GetOldTweets-web-weavers/trainingandtestdata/training.1600000.processed.noemoticon.csv",
                header=None,usecols=[0,5])
#twt.shape
#twt.head()
#twt.info()
#53% labels are 2, balanced dataset


text=twt[5]
target=twt[0]
#Target details 0 - the polarity of the tweet (0 = negative, 2 = neutral, 4 = positive)




# initialize the sklearn TfidfVectorizer 
# decode_error ignore for tweets
tfidf_vect = TfidfVectorizer(decode_error='ignore') 

# generate tfidf matrix
dtm= tfidf_vect.fit_transform(text)
print dtm.shape

#print("type of dtm:", type(dtm))
#print("size of tfidf matrix:", dtm.shape)


#Classifier

metrics = ['precision_macro', 'recall_macro', "f1_macro"]

clf = MultinomialNB()

'''
'#cross validation on the data
cv = cross_validate(clf, dtm, target, scoring=metrics, cv=5)


print("Test data set average precision: {}".format(cv['test_precision_macro']))
print("Average Test data 5-Fold CV precision Score: {}".format(np.mean(cv['test_precision_macro'])))

print("\nTest data set average recall: {}".format(cv['test_recall_macro']))
print("Average 5-Fold CV recall Score: {}".format(np.mean(cv['test_recall_macro'])))


#importing msft tweets data


#msftT=pd.read_csv("/Users/bhumikasingh/Downloads/trainingandtestdata/msftT.csv",
#                header=None)


'''

processed_tweets=pd.read_csv("twitter_clean_data/"+'APPL.csv')
print processed_tweets.head()

text_new = processed_tweets['text']

tfidf_new = tfidf_vect.transform(text_new)

print tfidf_new.shape


model = clf.fit(dtm, target)


predicted=model.predict(tfidf_new)

for idx, tweet in enumerate(text_new):
    print('%r => %s' % (tweet, predicted[idx]))

#msftT.head()

# generate tfidf matrix
#dtmT= tfidf_vect.fit_transform(msftT[2])
#dtm.shape
#dtmT.shape

#clf.fit(dtm, target)


#predicted=clf.predict(dtmT)

