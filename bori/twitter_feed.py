import twitter
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
logger.addHandler(ch)


class twitter_feeder():
    def __init__(self):
        self.api = twitter.Api(consumer_key="mYh1sti2PMGKmiU0C8pPLbGGl",
                  consumer_secret='0Kf8DNw8HklsHnINLGOPRryZMo3EvSCJvIL0Edh9JKS6ShCfx1',
                  access_token_key='810489185861824512-sa6J6p1RAaolOFcLh1TOPmuOP9XHmDM',
                  access_token_secret='zczOpmqn2vpzIg68XuKhXQgXzE4nMhuJGTu1gGugyV6Mv',
                  )

        #logger.info(self.api.VerifyCredentials())
        
    def get_user_timeline(self, screen_name,count=10):
        logger.info('number of tweets:%d', count)
        
        t = self.api.GetUserTimeline(screen_name=screen_name,count=count)
        tweets = [i.AsDict() for i in t]

        return tweets
    
    
'''
for t in tweets:
    print(t['text'])
'''
