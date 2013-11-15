import twitterCalls


class TwitterUser():
	def __init__(self):
		self.user_name = ""
		self.user_tweets = [] 
		self.user_tweet_texts = []
		self.user_text = ""
		self.user_friends = []
		self.user_hashtags = []

	def get_information(self, user_id):
		tc = twitterCalls.TwitterCaller()
		user = tc.get_user_profile(user_id)
		self.user_name = user.name
		self.user_tweets = tc.get_user_tweets(user_id, 10)
		for tweet in self.user_tweets:
			self.user_tweet_texts.append(tweet.__getstate__()['text'].encode('ascii','ignore'))	
		for tweet in self.user_tweet_texts:
			self.user_text = self.user_text + tweet
		self.user_friends = tc.get_friends(user_id)

'''
def main():
	tb = TwitterUser()
	tb.get_information("kmystic524")
	print "Users real name:" + tb.user_name
	print "Tweets:"
	for tweet in tb.user_tweet_texts:
		print tweet
	print "Friends:"
	for friend_id in tb.user_friends:
		print friend_id

	

if __name__ == "__main__":
	main()
'''