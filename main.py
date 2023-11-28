import tweepy
import json
import os 
import requests
import utilities
import sys
import traceback
from datetime import datetime
from dotenv import load_dotenv
load_dotenv("config_file.env")

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')


twitter_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
twitter_auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(twitter_auth)


today = datetime.today().strftime('%Y-%m-%d')
def get_tweets(name):
    tweets =  tweepy.Cursor(api.user_timeline, screen_name = name, tweet_mode = 'extended').items()
    # file = open('{}_tweets.json'.format(name), 'w', encoding='utf-8')
    tweet_list = []
    i = 0
    while True:
        try:
            tweet = next(tweets)
        except StopIteration:
            if i > 100:
                print('tweet limit reached!')
                break
            else:
                print('{} tweets from {} are loaded into the file!'.format(i, '@'+name))
            break
        tweet_jsoned = json.dumps(tweet._json,
                                  sort_keys = True,
                                  indent = 4,
                                  separators = (', ', ': '))
        tweet_dict = json.loads(tweet_jsoned)
        sub_dict_keys = ['full_text', 'created_at', 'is_retweet', 'retweet_count', 'favorite_count','in_reply_to_user_id_str']
        sub_tweet = {x: tweet_dict[x] for x in sub_dict_keys if x in tweet_dict.keys()}
        tweet_list.append(sub_tweet.copy())
        print(sub_tweet['created_at'])
        i += 1
        if i % 1 == 0:
            print('iterations: ', i)
            # json.dump(tweet_list, file)
            tweet_date = datetime.strftime(datetime.strptime(sub_tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d')
            tweet = tweet_list[0]['full_text']
            return tweet, tweet_date
        
        
    # print('%d tweets are loaded into %s.' % (len(tweet_list), '{}_tweets.json'.format(name)))
    # file.close()

def initialize_order():
    url = "https://api.strike.me/v1/currency-exchange-quotes"


    payload = json.dumps({
    "sell": "USD",
    "buy": "BTC",
    "amount": {
        "amount": "1.0",
        "currency": "USD"
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(os.getenv('bearer'))
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def execute_order(quote_id):
  url = "https://api.strike.me/v1/currency-exchange-quotes/{}/execute".format(quote_id)
  payload={}
  headers = {
    'Authorization': 'Bearer {}'.format(os.getenv('bearer'))
  }
  response = requests.request("PATCH", url, headers=headers, data=payload)
  print(response.text)

tweet, tweet_date = get_tweets(name = 'Any twitter account you want')
print(tweet)
try:
    # if today == tweet_date:
        print(today)
        print('Potus Latest Tweet: \n{}\nTweeted on {}'.format(tweet, tweet_date))
        post_response = initialize_order()
        quote_id = post_response['id']
        execute_response = execute_order(quote_id)
        utilities.send_email( "Any update email you want",
"{}".format(tweet.encode('ascii', 'ignore').decode('ascii')))

except Exception as  e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    utilities.send_email( 'BTC Stacking Script Failure','The exception stacktrace is:{}'.format(traceback.format_exception(exc_type, exc_value,exc_traceback)))
