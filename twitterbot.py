from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
from tweepy import Stream
import json
import logging
import warnings
from pprint import pprint

warnings.filterwarnings("ignore")

access_token = "CHANGEME"
access_token_secret = "CHANGEME"
consumer_key = "CHANGEME"
consumer_secret = "CHANGEME"

auth_handler = OAuthHandler(consumer_key, consumer_secret)
auth_handler.set_access_token(access_token, access_token_secret)

twitter_client = API(auth_handler)

logging.getLogger("main").setLevel(logging.DEBUG)

AVOID = ["australtech", "monty", "leather", "skin", "bag", "blood", "bite", "cam", "AdultWork.com"]
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PyStreamListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        try:
            publish = True
            for word in AVOID:
                if word in tweet['text'].lower():
                    logging.error(f"{bcolors.WARNING}+SKIPPED FOR {word}+{bcolors.ENDC}")
                    publish = False

            if tweet.get('lang') and tweet.get('lang') != 'en':
                publish = False

            if publish:
                twitter_client.retweet(tweet['id'])
                logging.error(f"{bcolors.OKGREEN}+RT: {tweet['text']}+{bcolors.ENDC}")

        except Exception as ex:
            logging.error(f"{bcolors.OKBLUE}{ex}+{bcolors.ENDC}")

        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    listener = PyStreamListener()
    stream = Stream(auth_handler, listener)
    stream.filter(track=['AWS', 'Amazon Web Service', 'Salesforce', 'Cloud Academy'])
