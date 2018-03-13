import pandas as pd
import re
from datetime import datetime
import preprocessor as p



df = pd.read_csv('data/manually_labeled_data/APPL-Original.csv')
# print df['text'].head()
d = []

for index, tweet in df.iterrows():

    original_tweet = tweet['text']
    original_date = tweet['date']
    original_sentiment = tweet['sentiment']

    # print original_tweet
    tweet = original_tweet.decode("utf8").encode("ascii", "ignore")

    tweet = re.sub(r'http.?:\/\/.?', 'https://', tweet)
    tweet = re.sub(r'% 2F', '%2F', tweet)
    tweet = re.sub(r'https?:\/\/.*\/[\w\d\S\n]*', '', tweet)

    processed_tweet = p.clean(tweet)
    processed_date = datetime.strftime(datetime.strptime(original_date, "%m/%d/%y"), "%Y-%m-%d")

    if processed_tweet:
        d.append({'date': processed_date, 'text': processed_tweet, 'sentiment': original_sentiment})

df_processed = pd.DataFrame(d)
df_processed.to_csv('data/manually_labeled_data/APPL.csv', index=False)