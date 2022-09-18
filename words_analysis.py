import tweet_analysis as twa

if __name__ == '__main__':
    output = "output2"
    twa.tweets_cleanup(twa.read_tweets(output))