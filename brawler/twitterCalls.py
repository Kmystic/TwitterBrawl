import tweepy
import json
import sys
'''
This class handles the Twitter API calls for TwitterBrawl

'''

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


	#Checks API rate limit, code from Dr. Caverlee's example
	def check_api_rate_limit(self, sleep_time):
		try:
			rate_limit_status = self.api.rate_limit_status()
		except Exception as error_message:
			if error_message['code'] == 88:
				print "Sleeping for %d seconds." %(sleep_time)
				print rate_limit_status['resources']['statuses']
				time.sleep(sleep_time)

			while rate_limit_status['resources']['statuses']['/statuses/user_timeline']['remaining'] < 10:
				print "Sleeping for %d seconds." %(sleep_time)
				print rate_limit_status['resources']['statuses']
				time.sleep(sleep_time)
				rate_limit_status = self.api.rate_limit_status()
			

	# Get user profile
	def get_user_profile(self, user_id):
		try:
			user_profile = self.api.get_user(user_id)
		except:
			return None
		return user_profile

	# Get user's friends (i.e. the people they follow)
	def get_friends(self, user_id):
		friends = self.api.friends(user_id, count = 250)
		friend_screens = []
		for friend in friends:
			friend_screens.append(friend.screen_name)
		return friend_screens;
	
	def get_all_friends(self, user_id):
		friends = self.api.friends.ids(user_id)
		return friends
	
	# Get user's count number of tweets
	def get_user_tweets(self, user_id, count):
		try:
			tweets = self.api.user_timeline(user_id, count = count, include_rts=1)
		except:
			tweets = None

		return tweets[:count]

	# Get user's profile photo
	def get_photo(self, user_id):
		try:
			user_profile = self.api.get_user(user_id)
		except:
			return None
		return user_profile.profile_image_url
	

	
'''
def main():

	user_name = "kmystic524"
	#user_name = raw_input("Enter the screen name of the user: ")
	tc = TwitterCaller()
	#tc.check_api_rate_limit(900)
	user = tc.get_user_profile(user_name)
	print " "
	print "User's real name:"
	print user.name
	#print 
	#tweets = tc.get_user_tweets(user_name, 100)
	print " "
	profilePhotoURL = tc.get_photo(user_name)
	photoName = "static/brawler/media/" + str(user_name) + ".jpg"
	file = str(photoName)
	f = open(file,'wb')
	f.write(urllib.urlopen(profilePhotoURL).read())
	f.close()
	

if __name__ == "__main__":
	main()
'''

