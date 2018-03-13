'''
file:   preprocessor.py
objective:  Pick the tweets from raw file which are of english language, and clean them before writing to the output file
'''

import pandas as pd
import re
from datetime import datetime
import preprocessor as p

def clean_tweets(input_file):
    print "[INFO] Cleaning tweets from file data/twitter_raw_data/" + input_file + " and creating new file " \
                                                                                   "data/twitter_clean_data/" + input_file
    df = pd.read_csv('data/twitter_raw_data/' + input_file, sep=";")
    # print df['text'].head()
    d = []
    for index, tweet in df.iterrows():
        if tweet['language'] == 'en':
            original_tweet = tweet['text']
            original_date = tweet['date']

            # print original_date
            processed_date = datetime.strftime(datetime.strptime(original_date, "%Y-%m-%d %H:%M"), "%Y-%m-%d")

            # print processed_date

            # print original_tweet
            tweet = original_tweet.decode("utf8").encode("ascii", "ignore")

            tweet = re.sub(r'http.?:\/\/.?', 'https://', tweet)
            tweet = re.sub(r'% 2F', '%2F', tweet)
            tweet = re.sub(r'https?:\/\/.*\/[\w\d\S\n]*', '', tweet)

            processed_tweet = p.clean(tweet)

            if processed_tweet:
                d.append({'date': processed_date, 'text': processed_tweet})

    df_processed = pd.DataFrame(d)
    df_processed.to_csv('data/twitter_clean_data/' + input_file, index=False)


if __name__ == "__main__":
    print "Starting....."
    raw_file = 'APPL.csv'
    clean_tweets(raw_file)
