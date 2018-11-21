# -*- coding: utf-8 -*-
import tweepy
import re
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue
MAX_TWEETS = 10
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
search_terms = ["GBPUSD -filter:retweets", "EURUSD -filter:retweets"]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
processed_tweets = []
full_tweets = []
def savefiles(term):
    full_tweets.clear()
    if term == 1:
        for tweet in tweepy.Cursor(api.search, q=search_terms[0], rpp=10, tweet_mode='extended', lang='en').items(
                MAX_TWEETS):
            full_tweets.append(tweet)
    elif term == 2:
        for tweet in tweepy.Cursor(api.search, q=search_terms[1], rpp=10, tweet_mode='extended', lang='en').items(
                MAX_TWEETS):
            full_tweets.append(tweet)


def check():
    processed_tweets.clear()
    for x in full_tweets:
        if re.findall('[1-9]+(.[0-9][0-9][0-9][0-9]?[0-9])', x.full_text):
            if (re.findall('\W*(Closed)\W*', x.full_text)) or (re.findall('\W*(Close)\W*', x.full_text)) or (
            re.findall('\W*(closed)\W*', x.full_text)) or (re.findall('\W*(close)\W*', x.full_text)):
                if (re.findall('\W*(T/P)\W*', x.full_text)) or (re.findall('\W*(t/p)\W*', x.full_text)) or (re.findall('\W*(TP)\W*', x.full_text)) or (re.findall('\W*(tp)\W*', x.full_text)):
                    if (re.findall('\W*(S/L)\W*', x.full_text)):
                        processed_tweets.append(
                            {"text": str(x.full_text), "time": str(x.created_at), "type": "Closed", "T/P_S/L": "OK"})
                else:
                    processed_tweets.append(
                        {"text": str(x.full_text), "time": str(x.created_at), "type": "Closed", "T/P_S/L": "NA"})
            elif (re.findall('\W*(Bought)\W*', x.full_text)) or (re.findall('\W*(bought)\W*', x.full_text)) or (
            re.findall('\W*(Buy)\W*', x.full_text)) or (re.findall('\W*(buy)\W*', x.full_text)):
                if (re.findall('\W*(T/P)\W*', x.full_text)) or (re.findall('\W*(t/p)\W*', x.full_text)) or (re.findall('\W*(TP)\W*', x.full_text)) or (re.findall('\W*(tp)\W*', x.full_text)):
                    if (re.findall('\W*(S/L)\W*', x.full_text)) or (re.findall('\W*(SL)\W*', x.full_text)) or (re.findall('\W*(sl)\W*', x.full_text)) or (re.findall('\W*(s/l)\W*', x.full_text)):
                        processed_tweets.append(
                            {"text": str(x.full_text), "time": str(x.created_at), "type": "Bought", "T/P_S/L": "OK"})
                else:
                    processed_tweets.append(
                        {"text": str(x.full_text), "time": str(x.created_at), "type": "Bought", "T/P_S/L": "NA"})
            elif (re.findall('\W*(Sold)\W*', x.full_text)) or (re.findall('\W*(Sell)\W*', x.full_text)) or (
            re.findall('\W*(sold)\W*', x.full_text)) or (re.findall('\W*(sell)\W*', x.full_text)):
                if (re.findall('\W*(T/P)\W*', x.full_text)) or (re.findall('\W*(t/p)\W*', x.full_text)):
                    if (re.findall('\W*(S/L)\W*', x.full_text)) or (re.findall('\W*(SL)\W*', x.full_text)) or (re.findall('\W*(sl)\W*', x.full_text)) or (re.findall('\W*(s/l)\W*', x.full_text)):
                        processed_tweets.append(
                            {"text": str(x.full_text), "time": str(x.created_at), "type": "Sold", "T/P_S/L": "OK"})
                else:
                    processed_tweets.append(
                        {"text": str(x.full_text), "time": str(x.created_at), "type": "Sold", "T/P_S/L": "NA"})
            elif (re.findall('\W*(Pending)\W*', x.full_text)) or (re.findall('\W*(Order)\W*', x.full_text)) or (
            re.findall('\W*(pending)\W*', x.full_text)) or (re.findall('\W*(order)\W*', x.full_text)):
                if (re.findall('\W*(T/P)\W*', x.full_text)) or (re.findall('\W*(t/p)\W*', x.full_text)):
                    if (re.findall('\W*(S/L)\W*', x.full_text)):
                        processed_tweets.append(
                            {"text": str(x.full_text), "time": str(x.created_at), "type": "Pending", "T/P_S/L": "OK"})
                else:
                    processed_tweets.append(
                        {"text": str(x.full_text), "time": str(x.created_at), "type": "Pending", "T/P_S/L": "NA"})
        else:
            processed_tweets.append(
                {"text": str(x.full_text), "time": str(x.created_at), "type": "UNKNOWN", "T/P_S/L": "UNKNOWN"})


def pretty_print():
    fi2 = open("output.txt","w",encoding="utf-8")
    for item in processed_tweets:
        for key, value in item.items():
            fi2.write(str(key) + ": " + str(value)+"\n")
        fi2.write("----------------------------------------------------------------\n")
    fi2.close()


def start(bot, update):
    """Send a message when the command /start is issued."""
    if int(update.message.text)==1: 
        savefiles(1)
        print(update.message.text)
        check()
        pretty_print()
        file = open("output.txt", "r",encoding='utf-8')
        t = file.read()
        file.close()
        print(t)
        try:
            bot.sendMessage(chat_id="@fortestchan", text=str(t))
        except(error):
            print(error)
    elif int(update.message.text)==2:
        savefiles(2)
        print(update.message.text)
        check()
        pretty_print()
        file = open("output.txt", "r",encoding='utf-8')
        t = file.read()
        file.close()
        print(t)
        try:
            bot.sendMessage(chat_id="@fortestchan", text=str(t))
        except(error):
            print(error)
        
    


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.

    updater = Updater("TOKEN")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(MessageHandler(Filters.text, start))
    # on different commands - answer in Telegram
    updater.start_polling(poll_interval = 1.0,timeout=20)
    updater.idle()
    



if __name__ == '__main__':
    main()




