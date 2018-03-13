import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentAnalysisUnsupervized():
    def sentiment_analysis_vader_validation(self, df, filepath):
        sid = SentimentIntensityAnalyzer()
        # print df.head()
        d = []
        sentiment_map = {'pos': 4, 'neg': 0, 'neu': 2}
        for index, tweet in df.iterrows():

            if len(str(tweet['text']).split()) > 4:
                tweet_txt = tweet['text']
                tweet_date = tweet['date']
                tweet_manual_label = tweet['sentiment']

                ss = sid.polarity_scores(tweet_txt)

                '''MAX LOGIC'''
                score_sentiment = max(ss['neg'], ss['neu'], ss['pos'])

                '''
                # COMPLEX LOGIC
                if ss['neg']>0 and ss['pos']>0 and ss['neu']>0:
                    score_sentiment = max(ss['neg'], ss['neu'], ss['pos'])
                elif ss['neg']==0 and ss['pos']>0 and ss['neu']>0:
                    score_sentiment = ss['pos']
                elif ss['pos'] == 0 and ss['neg'] > 0 and ss['neu'] > 0:
                    score_sentiment = ss['neg']
                elif ss['pos'] == 0 and ss['neg'] == 0 and ss['neu'] > 0:
                    score_sentiment = ss['neu']
                '''
                sentiment = [k for k, v in ss.items() if v == score_sentiment][0]
                sentiment_mapping = sentiment_map[sentiment]
                if tweet_manual_label == sentiment_mapping:
                    validation_result=1
                else:
                    validation_result=0

                d.append({'date': tweet_date, 'text': tweet_txt, 'polarity_score_neg':ss['neg'], 'polarity_score_neu':ss['neu'], 'polarity_score_pos':ss['pos'], 'predicted_sentiment': sentiment_mapping, 'labeled_sentiment':tweet_manual_label, 'validation_result': validation_result})

        df_processed = pd.DataFrame(d)
        df_processed.to_csv(filepath, index=False)

    def sentiment_analysis_vader_prediction(self, df, filepath):
        sid = SentimentIntensityAnalyzer()
        # print df.head()
        d = []
        sentiment_map = {'pos': 4, 'neg': 0, 'neu': 2}
        for index, tweet in df.iterrows():

            if len(str(tweet['text']).split()) > 4:
                tweet_txt = tweet['text']
                tweet_date = tweet['date']

                ss = sid.polarity_scores(tweet_txt)

                # max_score_sentiment = max(ss, key=ss.get)
                max_score_sentiment = max(ss['neg'], ss['neu'], ss['pos'])
                sentiment = [k for k, v in ss.items() if v == max_score_sentiment][0]
                sentiment_mapping = sentiment_map[sentiment]

                d.append({'date': tweet_date, 'text': tweet_txt, 'polarity_score_neg':ss['neg'], 'polarity_score_neu':ss['neu'], 'polarity_score_pos':ss['pos'], 'predicted_sentiment': sentiment_mapping})

        df_processed = pd.DataFrame(d)
        df_processed.to_csv(filepath, index=False)


def main():
    sa = SentimentAnalysisUnsupervized()
    input_file_name = 'MSFT.csv'
    manually_labeled_df = pd.read_csv("data/manually_labeled_data/" + input_file_name)
    output_file_path = 'results/unsupervised_vader/validation/' + input_file_name
    sa.sentiment_analysis_vader_validation(manually_labeled_df, output_file_path)


''' 
    processed_tweets_df = pd.read_csv("data/twitter_clean_data/" + input_file_name)
    output_file_path = 'results/unsupervised_vader/' + input_file_name
    sa.sentiment_analysis_vader_prediction(processed_tweets_df, output_file_path)
'''


main()
