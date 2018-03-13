from nltk.tokenize import TweetTokenizer
import nltk
from nltk.corpus import stopwords
import string

# -*- coding: UTF-8 -*-
import HTMLParser


###
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC


class SentimentAnalysisSupervized():
    def sentiment_analysis_LinearSVC(self, df_training, df_new, filepath):
        traing_tweet_texts = df_training['text']
        traing_tweet_targets = df_training['sentiment']
        # Target details 0 - the polarity of the tweet (0 = negative,  2 =  neutral, 4 = positive)

        p8_2 = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words=None, token_pattern='[A-Za-z0-9]+(?=\\s+)', min_df=3)),
            ('clf', LinearSVC(loss='squared_hinge'))
        ])

        p8_2.fit(traing_tweet_texts, traing_tweet_targets)

        predicted = p8_2.predict(df_new['text'])

        df_processed = pd.DataFrame()

        df_processed['date'] = df_new['date']
        df_processed['text'] = df_new['text']
        #df_processed['sentiment'] = df_new['sentiment']
        df_processed['predicted'] = predicted

        df_processed.to_csv(filepath, index=False)


    def sentiment_analysis2(self, df, filepath):
        tweet = "This is a cooool #dummysmiley: :-) :-P <3 and some arrows < > -> <--"

        vocab = set(word.lower() for word in nltk.corpus.words.words())
        stop_words = stopwords.words('english')
        '''tokens = [token.strip() \
            for token in nltk.word_tokenize(tweet.lower()) \
            if token.strip() not in stop_words and \
            token.strip() not in string.punctuation \
            and token.strip() in vocab]'''
        tokens = [token.strip() \
                  for token in nltk.word_tokenize(tweet.lower()) \
                  if token.strip() not in stop_words and \
                  token.strip() not in string.punctuation]
        print token
        print "-------"
        tknzr = TweetTokenizer()
        tokens2 = tknzr.tokenize(tweet)
        print tokens2


def main():
    sa = SentimentAnalysisSupervized()
    input_file_name = 'APPL.csv'
    training_file_path = "data/manually_labeled_data/" + input_file_name
    training_df = pd.read_csv(training_file_path)

    new_tweets_file_path = "data/twitter_clean_data/" + input_file_name
    new_tweets_df = pd.read_csv(new_tweets_file_path)

    output_file_path = 'results/sentiment_analysis_LinearSVC/' + input_file_name
    sa.sentiment_analysis_LinearSVC(training_df, new_tweets_df, output_file_path)

main()