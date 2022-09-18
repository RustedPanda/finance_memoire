import os 
import pandas as pd
from pandas import factorize
import numpy as np
import re
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

def read_tweets(directory = "output"):
    dfs = {}
    files = os.listdir(str(directory))
    for file in files:
        df = pd.read_csv(str(directory)+"/"+file,header=0)
        dfs[file]=df
    
    return dfs

def tweets_cleanup(df_twt):
    #First clean bots messages from clearly stated bot sources
    df_twt_cl = {}
    patternbots = ["bot","bots","Bot","Bots"]

    for file_name,df in df_twt.items():
        df_cl = df[~df.source.str.contains('|'.join(patternbots))]
        print(f"{len(df)-len(df_cl)} bots tweets were deleted from source "
              f"name in {file_name}.")
        df_cl_uni = df_cl.drop_duplicates(subset=['tweet'], keep=False)
        print(f"{len(df_cl)-len(df_cl_uni)} duplicate tweets (possible bots repetitions & ads) were deleted in {file_name}.")
        df_twt_cl[file_name] = df_cl_uni
        print(f"Final {file_name} has {len(df_cl_uni)} tweets.\n")
    
    return df_twt_cl

def get_sentiment(df_twt):
    
    sentiments = {}
    #Setup polarity analyzer script from VADER
    SIA = SentimentIntensityAnalyzer()
    
    for file_name, df in df_twt.items():
        score_tweet = []
        score_tweetblob = []
        date_tweet = []
        likes_tweet = []
        retweets_tweet = []
        #We get the coumpound score, which is a weigthed normalization of positive and negative score
        for tweet,date,likes,retweets in zip(df.tweet,df.created_at,df.like_count,df.retweet_count) :
            score_vader = SIA.polarity_scores(tweet)['compound']
            score_blob = TextBlob(tweet).sentiment.polarity
            score_tweet.append(score_vader)
            score_tweetblob.append(score_blob)

            date_tweet.append(date)
            likes_tweet.append(likes)
            retweets_tweet.append(retweets)
        scores = pd.DataFrame(list(zip(date_tweet, score_tweet,
                                       score_tweetblob, likes_tweet, retweets_tweet)),
                              columns= ['Date','Score','Score_blob',"Likes",
                                        "Retweets"])
        scores['Date'] = pd.to_datetime(scores.Date, infer_datetime_format=True, format='%Y-%m-%d') 
        scores.set_index('Date', inplace=True)
        sentiments[file_name] = scores
    
    return sentiments

def score_cleanup(sent_df, frequency = "D", weight = "likes"):
    
    final_sent = {}
    
    for filename, sents in sent_df.items():        
        #We create normalized columns from likes and retweets to use as weight in the score average of each day
        sents.drop(sents[sents["Score"] == 0].index, inplace=True)
        sents["Normalized_likes"] = (sents["Likes"] - sents["Likes"].min()) / (sents["Likes"].max() - sents["Likes"].min())
        sents["Normalized_retweets"] = (sents["Retweets"] - sents["Retweets"].min()) / (sents["Retweets"].max() - sents["Retweets"].min())
        sents["Overall_weight"] = sents[["Normalized_retweets","Normalized_likes"]].mean(axis = 1)
        print(sents)

        sents.comp = sents.groupby(pd.Grouper(freq = frequency)).sum()

        score_cat = []
        score_cat_blob = []
        for score_vader in sents.comp['Score']:
            print(score_vader)
            if np.abs(score_vader) >= 0.4:
                score_cat.append("High")
            elif np.abs(score_vader) >= 0.2 and abs(score_vader) < 0.4:
                score_cat.append("Good")
            elif np.abs(score_vader) < 0.2 :
                score_cat.append("Low")
        for score_blob in sents.comp['Score_blob']:
            if np.abs(score_blob) >= 0.4:
                score_cat_blob.append("High")
            elif np.abs(score_blob) >= 0.2 and abs(score_blob) < 0.4:
                score_cat_blob.append("Good")
            elif np.abs(score_blob) < 0.2 :
                score_cat_blob.append("Low")

        codesV, uniquesV = pd.factorize(score_cat)
        codesB, uniquesB = pd.factorize(score_cat_blob)
        sents.comp["Vader_cat"] = (codesV)
        sents.comp["Blob_cat"] = (codesB)

        final_sent[filename] = sents.comp

    return final_sent