#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 20:58:32 2017

@author: taranpreet
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.model_selection import cross_validate
import numpy as np
np.random.seed(7)

msft15=pd.read_excel("Msft 1500 to 2017.xlsx")
msft1=pd.read_excel("/Users/bhumikasingh/Downloads/Updated msft.xlsx")
aapl=pd.read_excel("/Users/bhumikasingh/Downloads/APPL.xlsx")


aapl.info()
aapl=aapl.dropna()
msft15.info()
msft1=msft1.dropna()

#giving same col names to all

msft15.columns= ['date','sent','text']

msft1.columns= ['date','sent','text']

aapl.columns= ['date','sent','text']

#merging df
data=msft1.append(msft15).append(aapl)
data.info()

X=data.text
y=data.sent

X_train,X_test,y_train,y_test=train_test_split(X,y, random_state=27,test_size=0.2)

#using count vectorizer instead of tfidf
# tokenizing only allpha numeric
tokenPatt = '[A-Za-z0-9]+(?=\\s+)'
#vectorizer
vec = CountVectorizer(token_pattern = tokenPatt)
#
vec.fit(data.text)
#number of tokens
len(vec.get_feature_names())
#4263 tokens

# pipeline 
pl = Pipeline([
        ('vec', CountVectorizer(token_pattern = tokenPatt)),
        ('clf', LogisticRegression())
    ])

pl.fit(X_train,y_train)

# accuracy
accuracy = pl.score(X_test,y_test)
print("\nAccuracy : ", accuracy)
# accuracy is 0.56 with logistic regression


pl = Pipeline([
        ('vec', CountVectorizer(token_pattern = tokenPatt)),
        ('clf', DecisionTreeClassifier())
    ])

pl.fit(X_train,y_train)

# accuracy
accuracy = pl.score(X_test,y_test)
print("\nAccuracy : ", accuracy)

#0.52 with decision tree


# logistic without alphanumeric tokens

pl = Pipeline([
        ('vec', CountVectorizer()),
        ('clf', LogisticRegression())
    ])

pl.fit(X_train,y_train)

# accuracy
accuracy = pl.score(X_test,y_test)
print("\nAccuracy : ", accuracy)
# accuracy is 0.57 without alphanumeric tokenizer tokenizer




pl = Pipeline([
        ('vec', CountVectorizer()),
        ('clf', MultinomialNB())
    ])

pl.fit(X_train,y_train)


#cv = cross_validate(pl, X_train,y_train,  cv=5)
# accuracy
accuracy = pl.score(X_test,y_test)
print("\nAccuracy : ", accuracy)

#multiniomial accuracy is 0.61


#class methods

from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

# import GridSearch
from sklearn.model_selection import GridSearchCV

# build a pipeline which does two steps all together:
# (1) generate tfidf, and (2) train classifier
# each step is named, i.e. "tfidf", "clf"

text_clf = Pipeline([('tfidf', TfidfVectorizer()),
                     ('clf', MultinomialNB())
                   ])


# set the range of parameters to be tuned
# each parameter is defined as 
# <step name>__<parameter name in step>
# e.g. mid_df is a parameter of TfidfVectorizer()
# "tfidf" is the name for TfidfVectorizer()
# therefore, 'tfidf__min_df' is the parameter in grid search

parameters = {'tfidf__min_df':[2,3],
              'tfidf__stop_words':[None,"english"],
              'clf__alpha': [0.5,1.0,2.0],
}

# the metric used to select the best parameters
metric =  "f1_macro"

# GridSearch also uses cross validation
gs_clf = GridSearchCV(text_clf, param_grid=parameters, scoring=metric, cv=5)

# due to data volume and large parameter combinations
# it may take long time to search for optimal parameter combination
# you can use a subset of data to test
gs_clf = gs_clf.fit(X, y)

for param_name in gs_clf.best_params_:
    print(param_name,": ",gs_clf.best_params_[param_name])

print("best f1 score:", gs_clf.best_score_)

"""
These are score for the tfidf vecrorizer

('tfidf__stop_words', ': ', 'english')
('tfidf__min_df', ': ', 3)
('clf__alpha', ': ', 0.5)
('best f1 score:', 0.42765650255185628)
"""



# build a pipeline which does two steps all together:
# (1) generate tfidf, and (2) train classifier
# each step is named, i.e. "tfidf", "clf"

text_clf = Pipeline([('vec', CountVectorizer()),
                     ('clf', MultinomialNB())
                   ])

# set the range of parameters to be tuned
# each parameter is defined as 
# <step name>__<parameter name in step>
# e.g. mid_df is a parameter of TfidfVectorizer()
# "tfidf" is the name for TfidfVectorizer()
# therefore, 'tfidf__min_df' is the parameter in grid search

parameters = {
              'clf__alpha': [0.5,1.0,2.0]
}

# the metric used to select the best parameters
metric =  "f1_macro"

# GridSearch also uses cross validation
gs_clf = GridSearchCV(text_clf, param_grid=parameters, scoring=metric, cv=5)

# due to data volume and large parameter combinations
# it may take long time to search for optimal parameter combination
# you can use a subset of data to test
gs_clf = gs_clf.fit(X, y)

for param_name in gs_clf.best_params_:
    print(param_name,": ",gs_clf.best_params_[param_name])

print("best f1 score:", gs_clf.best_score_)



"""
with count vectorizer

('clf__alpha', ': ', 0.5)
('best f1 score:', 0.46080859536511826)
"""



pl = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])

pl.fit(X_train,y_train)

# accuracy
accuracy = pl.score(X_test,y_test)
print("\nAccuracy : ", accuracy)



#0.57 for multinomial with tfidf 

# 


from sklearn.model_selection import cross_val_score
cross_val_score(pl,X,y)
'''
Warning
The least populated class in y has only 1 members, which is too few. The minimum number of members in any class cannot be less than n_splits=3.
  % (min_groups, self.n_splits)), Warning)
Out[101]: array([ 0.47236181,  0.47959184,  0.47692308])

'''
cross_val_score(pl,X,y)
'''
 array([ 0.47764228,  0.49796334,  0.4877551 ])
 
 
'''


pl = Pipeline([
        ('vec', CountVectorizer()),
        ('clf', MultinomialNB())
    ])

pl.fit(X_train,y_train)

# accuracy
accuracy = pl.score(X_test,y_test)
print("\nAccuracy : ", accuracy)

cross_val_score(pl,X,y)





pl = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])

pl.fit(X_train,y_train)

# accuracy
accuracy = pl.score(X_test,y_test)
print("\nAccuracy : ", accuracy)

cross_val_score(pl,X,y)



from sklearn.svm import LinearSVC



pl = Pipeline([
        ('vec', CountVectorizer()),
        ('clf', LinearSVC())
    ])

pl.fit(X_train,y_train)

# accuracy
accuracy = pl.score(X_test,y_test)
print("\nAccuracy : ", accuracy)

cross_val_score(pl,X,y)

'''
('\nAccuracy : ', 0.55084745762711862)
Out[108]: array([ 0.44817073,  0.49389002,  0.47346939])
'''


pl = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LinearSVC())
    ])

pl.fit(X_train,y_train)

# accuracy
accuracy = pl.score(X_test,y_test)
print("\nAccuracy : ", accuracy)

cross_val_score(pl,X,y)

#tfidf





