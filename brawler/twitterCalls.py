import tweepy
import json
import sys

class TwitterCaller():
	def __init__(self):
		self.consumer_key = '61hozL092ZeWckxfUAj0ag'
		self.consumer_secret = '13iIIYilAHBCEFoO5zm4Uu5fY4bLc0i5d1eozZJzw'
		self.access_token_key = '1970031594-VO2ZwdafHHnhxuBpEXHORnrfCa8tFOoH2SaQcHP'
		self.access_token_secret = 'paBFrXgzyHigHGXXtj4L02J3jB4KZrQhAO4QtgaS1WbFc'
		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		self.auth.set_access_token(self.access_token_key, self.access_token_secret)
		self.api = tweepy.API(self.auth)
		self.num_docs = 0
		self.num_tweets = 0
		#print self.api.rate_limit_status()

	def check_api_rate_limit(self, sleep_time):
		try:
			rate_limit_status = self.api.rate_limit_status()
		except Exception as error_message:
			if error_message['code'] == 88:
				#print "Sleeping for %d seconds." %(sleep_time)
				#print rate_limit_status['resources']['statuses']
				time.sleep(sleep_time)

			while rate_limit_status['resources']['statuses']['/statuses/user_timeline']['remaining'] < 10:
				#print "Sleeping for %d seconds." %(sleep_time)
				#print rate_limit_status['resources']['statuses']
				time.sleep(sleep_time)
				rate_limit_status = self.api.rate_limit_status()
			#print rate_limit_status['resources']['statuses']['/statuses/user_timeline']

	# Get user profile
	def get_user_profile(self, user_id):
		#self.check_api_rate_limit(900)
		try:
			user_profile = self.api.get_user(user_id)
		except:
			return None
		return user_profile

	# Get user's friends (i.e. the people they follow)
	def get_friends(self, user_id):
		#friend_ids = self.api.friends_ids(user_id)
		friends = self.api.friends(user_id, count = 10)
		friend_screens = []
		for friend in friends:
			friend_screens.append(friend.screen_name)
		return friend_screens;

	def get_user_tweets(self, user_id, count):
		#self.check_api_rate_limit(900)
		try:
			tweets = self.api.user_timeline(user_id, count = count, include_rts=0)
		except:
			tweets = None

		return tweets[:count]

	


	#def CreateJSON(self, user, tweets):
		#print user.get_user()
	
'''
def main():

	user_name = "JNowotny"
	#user_name = raw_input("Enter the screen name of the user: ")
	tc = TwitterCrawler()
	#tc.check_api_rate_limit(900)
	user = tc.get_user_profile(user_name)
	print " "
	print "User's real name:"
	print user.name
	#print 
	tweets = tc.get_user_tweets(user_name, 100)
	print " "
	print "The users last 10 tweets:"
	for tweet in tweets:
		print tweet.__getstate__()['text'].encode('ascii','ignore')
	print tc.api.rate_limit_status()
	#tc.CreateJSON(user, tweets)
	
	friends = tc.get_friends(user_name)
	print " "
	print "The pepople the user follows:"
	for friend in friends:
			print friend
	
	

if __name__ == "__main__":
	main()

'''
