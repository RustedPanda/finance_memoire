# -*- coding: utf-8 -*-
"""
Created on Sun May 22 14:56:25 2022

@author: ludo_
"""


# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
# For parsing the dates received from twitter in readable formats
import dateutil.parser
# For saving the response data in CSV format
import csv
#To add wait time between requests, randomness helps to not get marked as spam
import time
import random


def auth():
    return os.getenv('TOKEN')

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(query, start_date, end_date, max_results = 10):
    
    search_url = "https://api.twitter.com/2/tweets/search/all" #Change to the endpoint you want to collect data from

    #change params based on the endpoint you are using
    query_params = {'query': query,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'next_token': {}}
    return (search_url, query_params)

def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        # raise Exception(response.status_code, response.text)
        return(404)
    return response.json()

def append_to_csv(json_response, fileName):

    #A counter variable
    counter = 0

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    for tweet in json_response['data']:
        
        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that

        # 1. Author ID
        author_id = tweet['author_id']

        # 2. Time created
        created_at = dateutil.parser.parse(tweet['created_at'])


        # 4. Tweet ID
        tweet_id = tweet['id']

        # 5. Language
        lang = tweet['lang']

        # 6. Tweet metrics
        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']

        # 7. source
        source = tweet['source']

        # 8. Tweet text
        text = tweet['text']
        
        # Assemble all data in a list
        res = [author_id, created_at, tweet_id, lang, like_count, quote_count, reply_count, retweet_count, source, text]
        
        # Append the result to the CSV file
        csvWriter.writerow(res)
        counter += 1

    # When done, close the CSV file
    csvFile.close()

    # Print the number of tweets for this iteration
    print("# of Tweets added from this response: ", counter) 
    
def get_tweets(start_list,end_list,query,company,max_per_day,directory):
    #Inputs for tweets
    bearer_token = auth()
    print(bearer_token)
    headers = create_headers(bearer_token)
    max_results = max_per_day
    
    #Total number of tweets we collected from the loop
    total_tweets = 0
    
    # Create file
    csvFile = open(str(directory)+"/"+company+"data.csv", "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
    
    #Create headers for the data you want to save, in this example, we only want save these columns in our dataset
    csvWriter.writerow(['author id', 'created_at', 'id','lang', 'like_count', 'quote_count', 'reply_count','retweet_count','source','tweet'])
    csvFile.close()
    
    for i in range(0,len(start_list)):
    
        # Inputs
        count = 0 # Counting tweets per time period
        max_count = max_per_day # Max tweets per time period
        flag = True
        next_token = None
        
        # Check if flag is true
        while flag:
            # Check if max_count reached
            if count >= max_count:
                break
            print("-------------------")
            print("Token: ", next_token)
            url = create_url(query, start_list[i],end_list[i], max_results)
            json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
            if json_response == 404 :
                print("Too many requests or other failure, waiting 5s before retry.")
                time.sleep(5)
                continue
            else :
                result_count = json_response['meta']['result_count']
        
                if 'next_token' in json_response['meta']:
                    # Save the token to use for next call
                    next_token = json_response['meta']['next_token']
                    print("Next Token: ", next_token)
                    if result_count is not None and result_count > 0 and next_token is not None:
                        print("Start Date: ", start_list[i])
                        append_to_csv(json_response, str(directory)+"/"+company+"data.csv")
                        count += result_count
                        total_tweets += result_count
                        print("Total # of Tweets added: ", total_tweets)
                        print("-------------------")
                        time.sleep(random.random() +1)            
                # If no next token exists
                else:
                    if result_count is not None and result_count > 0:
                        print("-------------------")
                        print("Start Date: ", start_list[i])
                        append_to_csv(json_response, str(directory)+"/"+company+"data.csv")
                        count += result_count
                        total_tweets += result_count
                        print("Total # of Tweets added: ", total_tweets)
                        print("-------------------")
                        time.sleep(random.random() +1)
                    
                    #Since this is the final request, turn flag to false to move to the next time period.
                    flag = False
                    next_token = None
            time.sleep(random.random() +1)
    print("Total number of results: ", total_tweets)