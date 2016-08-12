import tweepy
import twitterconfig

class TwitterAPI:
	def __init__(self):
		consumer_key=twitterconfig.consumer_key
		consumer_secret=twitterconfig.consumer_secret
		auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
		access_token=twitterconfig.access_token
		access_token_secret=twitterconfig.access_token_secret
		auth.set_access_token(access_token,access_token_secret)
		self.api=tweepy.API(auth)
	
	def tweet(self, message):
		self.api.update_status(status=message)