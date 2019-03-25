from .twitter_feed import twitter_feeder
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class TwitterReader():
    
    def __init__(self, twt_number):
        self.tweet_nummber = twt_number

    def read_user_tweet(self,user):
        tweet_feed = twitter_feeder()
        user_tweets = tweet_feed.get_user_timeline(user,self.tweet_nummber)
        logger.debug("Size of user tweets: %d", len(user_tweets))

        return user_tweets
