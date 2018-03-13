'''
__file:   driver.py
objective:  Is the driver for tweet download and pre-processing. Takes 'configuration.ini' to identify the download and
            pre-processing parameters.
'''

import sys, codecs
import ConfigParser
from datetime import datetime, timedelta
#from stocks import stockdata

import got
from tweet_preprocessor import clean_tweets

class driver():
    def fetch_tweets(self,configfile):

        Config = ConfigParser.ConfigParser()
        Config.read(configfile)
        companies=Config.sections()

        for company in companies:
            download_flag=Config.get(company, 'download_tweets')
            preprocess_tweets_flag = Config.get(company, 'preprocess_tweets')
            # Flag to check if a new Download is required
            if download_flag=="yes":
                outputFileName = Config.get(company, 'output')
                outputFile = codecs.open('data/twitter_raw_data/'+outputFileName, "w+", "utf-8")

                #outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
                outputFile.write('date;text;language')

                date_since = datetime.strptime(Config.get(company, 'since'), "%Y-%m-%d")
                date_until = datetime.strptime(Config.get(company, 'until'), "%Y-%m-%d")

                while date_since <= date_until:
                    next_date_since = date_since + timedelta(days=1)
                    stocksymbol = Config.get(company, 'stocksymbol')
                    username = Config.get(company, 'username')
                    since = datetime.strftime(date_since, "%Y-%m-%d")
                    until = datetime.strftime(next_date_since, "%Y-%m-%d")
                    querysearch = Config.get(company, 'querysearch')
                    near = Config.get(company, 'near')
                    within = Config.get(company, 'within')
                    maxtweets = Config.get(company, 'maxtweets')
                    toptweets = Config.get(company, 'toptweets')

                    tweetCriteria = got.manager.TweetCriteria().setUsername(username). \
                        setSince(since).setUntil(until).setQuerySearch(querysearch). \
                        setNear(near).setWithin(within).setMaxTweets(maxtweets). \
                        setTopTweets(toptweets)

                    def receiveBuffer(tweets):
                        for t in tweets:
                            if t.language == 'en' and t.language:
                                # outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (
                                # t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions,
                                # t.hashtags, t.id, t.permalink)))
                                outputFile.write(('\n%s;%s;%s' % (
                                    t.date.strftime("%Y-%m-%d %H:%M"), t.text, t.language)))
                        outputFile.flush();
                        print('%d more tweets saved on file...' % len(tweets))

                    got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

                    date_since += timedelta(days=1)

            if preprocess_tweets_flag=="yes":
                outputFileName = Config.get(company, 'output')
                clean_tweets(outputFileName)

            #sd=stockdata()
            #sd.getStockQuotes(stocksymbol,'google',since,until)

def ConfigSectionMap(configfile,section):
    dict1={}
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    options = Config.options(section)

    for option in options:
        try:
            dict1[option] = Config.get(section, option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None

    return dict1


def main():
    configfile = sys.argv[1]
    d = driver()
    d.fetch_tweets(configfile)


main()