# -*- coding: utf-8 -*-
"""
Created on Sun May 22 14:55:00 2022

@author: ludo_
"""
import os
import warnings

import dates
import twitter_api
import Script_words as scw
import tweet_analysis as twa
#import scrapping_market as mrkt
#import market_analysis as mkrt_an


if __name__ == '__main__':
    #Not a good practice, but some needed deprecated functions raise errors
    warnings.filterwarnings("ignore")
    
    output = str(input("Enter the output directory of tweets data (write output or output2) :\n"))
    
    files_twitter = os.listdir(output)
    #Query twitter API only if no file is present in the output directory
    if len(files_twitter) == 0 :
        print(f"No files found in directory {output}, procedding scrapping of tweets data.\n")
        year = int(input("Enter a year :\n"))
        choice = str(input("Choose a scrapping method : 'company_name' or 'close_words'.\n"))

        companies = scw.get_cac40()
        start_list = dates.generate_dates_start(year)
        end_list = dates.generate_dates_end(start_list, year)
        max_per_day = 20
        
        if choice == "company_name" :
            for company in companies : 
                query = "(#"+company+" OR "+company+") -is:retweet lang:fr"
                twitter_api.get_tweets(start_list, end_list, query, company, max_per_day, output)
        elif choice == "close_words" :
            model = scw.get_model()

            for company in companies :
                keywords = scw.get_close_words(company,scw.get_model())
                query = "("+" OR ".join(keywords)+") -is:retweet lang:fr"
                print(query)
                twitter_api.get_tweets(start_list, end_list, query, company, max_per_day, output)
        else : 
            print("Choice not supported.")
            exit()
        
        sentiments = twa.get_sentiment(twa.tweets_cleanup(twa.read_tweets(output)))
        for key, values in sentiments.items():
            df = sentiments[key]
            df.to_csv('output_clean2/' + str(key) + '.csv')
    
    else :
        
        sentiments = twa.get_sentiment(twa.tweets_cleanup(twa.read_tweets(output)))
        for key, values in sentiments.items():
            df = sentiments[key]
            df.to_csv('output_clean2/' + str(key) + '.csv')
