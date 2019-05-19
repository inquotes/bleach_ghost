import tweepy  # Tweepy facilitates easy Twitter API calls
from collections import *
from random import random
import re

class BleachBot:

    def __init__(self, twitter_consumer_key, twitter_consumer_secret,
             twitter_access_key, twitter_access_secret,
             search_terms=[]):

        """ Create generic twitter bot that tweets message on twitter account
        given twitter API consumer and access credentials"""

        # Access Keys and Secrets for Twitter API obtained at: https://developer.twitter.com/
        auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
        auth.set_access_token(twitter_access_key, twitter_access_secret)

        # Store API object for access to Twitter REST API
        self.__api = tweepy.API(auth)

        # Term(s) to search twitter
        self.search_terms = search_terms

        # Populated by self.search_twitter(), results = twitter results
        self.results = None

        # Populated by self.search_twitter(), source_text = concatenated string of the tweets
        self.source_text = None

        # counter object that saves data about character frequency in relation to previous n characters
        # n = self.order
        self.lm  = None

        # this is some property for the model
        self.order  = 7

        # populated by self.generate_text
        self.generated_text  = None


    def set_search_terms(self, list_of_terms=[]):
    	self.search_terms = list_of_terms
    	return 

    def search_twitter(self, count=500):
        q = " OR ".join(self.search_terms) + " -filter:retweets -filter:media"
        print(q)
        self.results = self.__api.search(q=q, lang='en', count=count, result_type='recent')

        text_list = []
        for tweet in self.results:
            text_list.append(tweet.text)

        output = re.sub(r"(?:\@|https?\://)\S+", "", ' '.join(text_list))
        output = output.replace('amp;', '')
        self.source_text=output
        return

    def show_tweet(self, limit=1):
        print(self.results[:limit])
        return
    
    def train_char_lm(self):
        lm = defaultdict(Counter)
        pad = "~" * self.order
        data = pad + self.source_text
        for i in range(len(data)-self.order):
            history, char = data[i:i+self.order], data[i+self.order]
            lm[history][char]+=1

        def normalize(counter):
            s = float(sum(counter.values()))
            return [(c,cnt/s) for c,cnt in counter.items()]
        
        self.lm = {hist:normalize(chars) for hist, chars in lm.items()}
        return

    def generate_letter(self, history):
            history = history[-self.order:]
            dist = self.lm[history]
            x = random()
            for c,v in dist:
                x = x - v
                if x <= 0: return c
                
    def generate_text(self, nletters=2000):
        history = "~" * self.order
        out = []
        for i in range(nletters):
            c = self.generate_letter(history)
            history = history[-self.order:] + c
            out.append(c)
        self.generated_text = "".join(out)
        return

    def generate_lines(self, line_length=27, num_lines=10):
        counter = 0
        window_start = 0
        window_end = line_length
        line_list = []
        while counter<num_lines:
            line = self.generated_text[window_start:window_end]
            if line[-1] == ' ':
                line_list.append(line)
                counter += 1
                window_start = window_end
                window_end = window_end+line_length
            window_end += 1
        print("\n".join(line_list))   
        return 
