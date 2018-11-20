import tweepy
import re
MAX_TWEETS = 50
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""
full_tweets = []
processed_tweets = []
search_terms = ["GBPUSD -filter:retweets","EURUSD -filter:retweets"]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
f = open("myfinal.csv","a",encoding="utf-8")
def savefiles():
    for tweet in tweepy.Cursor(api.search, q=search_terms[0], rpp=100,tweet_mode='extended',lang='en').items(MAX_TWEETS):
        full_tweets.append(tweet)
def check():
    for x in full_tweets:
         if re.findall('[1-9]+(.[0-9][0-9][0-9][0-9]?[0-9])',x.full_text):
            if(re.findall('\W*(Closed)\W*',x.full_text)) or (re.findall('\W*(Close)\W*',x.full_text)) or (re.findall('\W*(closed)\W*',x.full_text)) or (re.findall('\W*(close)\W*',x.full_text)):
                if(re.findall('\W*(T/P)\W*',x.full_text))or(re.findall('\W*(t/p)\W*',x.full_text)):
                    if(re.findall('\W*(S/L)\W*',x.full_text)):
                        processed_tweets.append({"text":str(x.full_text),"time":str(x.created_at),"type":"Closed","T/P_S/L":"OK"})
                else:
                    processed_tweets.append({"text":str(x.full_text),"time":str(x.created_at),"type":"Closed","T/P_S/L":"NA"})
            elif(re.findall('\W*(Bought)\W*',x.full_text)) or (re.findall('\W*(bought)\W*',x.full_text)) or (re.findall('\W*(Buy)\W*',x.full_text)) or (re.findall('\W*(buy)\W*',x.full_text)):
                 if(re.findall('\W*(T/P)\W*',x.full_text))or(re.findall('\W*(t/p)\W*',x.full_text)):
                    if(re.findall('\W*(S/L)\W*',x.full_text)):
                        processed_tweets.append({"text":str(x.full_text),"time":str(x.created_at),"type":"Bought","T/P_S/L":"OK"})
                 else:
                    processed_tweets.append({"text":str(x.full_text),"time":str(x.created_at),"type":"Bought","T/P_S/L":"NA"})
            elif(re.findall('\W*(Sold)\W*',x.full_text)) or (re.findall('\W*(Sell)\W*',x.full_text)) or (re.findall('\W*(sold)\W*',x.full_text)) or (re.findall('\W*(sell)\W*',x.full_text)):
                 if(re.findall('\W*(T/P)\W*',x.full_text))or(re.findall('\W*(t/p)\W*',x.full_text)):
                    if(re.findall('\W*(S/L)\W*',x.full_text)):
                        processed_tweets.append({"text":str(x.full_text),"time":str(x.created_at),"type":"Sold","T/P_S/L":"OK"})
                 else:
                    processed_tweets.append({"text":str(x.full_text),"time":str(x.created_at),"type":"Sold","T/P_S/L":"NA"})
            elif(re.findall('\W*(Pending)\W*',x.full_text)) or (re.findall('\W*(Order)\W*',x.full_text)) or (re.findall('\W*(pending)\W*',x.full_text)) or (re.findall('\W*(order)\W*',x.full_text)):
                 if(re.findall('\W*(T/P)\W*',x.full_text))or(re.findall('\W*(t/p)\W*',x.full_text)):
                    if(re.findall('\W*(S/L)\W*',x.full_text)):
                        processed_tweets.append({"text":str(x.full_text),"time":str(x.created_at),"type":"Pending","T/P_S/L":"OK"})
                 else:
                    processed_tweets.append({"text":str(x.full_text),"time":str(x.created_at),"type":"Pending","T/P_S/L":"NA"})
         else:
                processed_tweets.append({"text":str(x.full_text),"time":str(x.created_at),"type":"UNKNOWN","T/P_S/L":"UNKNOWN"})
def pretty_print():
    for item in processed_tweets:
        for key,value in item.items():
            print(key+": "+value)
        print("----------------------------------------------------------------")
                
savefiles()
check()
pretty_print()
    
