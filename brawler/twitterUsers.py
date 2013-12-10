import twitterCalls

'''
This class handles a Twitter User to interface with TwitterCalls for 
the main user, and the two opponents

'''

class TwitterUser():
        def __init__(self):
                self.user_name = ""
                self.user_tweets = [] 
                self.user_tweet_texts = []
                self.user_text = ""
                self.user_friends = [] # Friend's screen names
                self.friend_ids = "" # Friend's user ids
                self.friend_ids_list = [] # Friend's user ids
                self.user_hashtags = ""
                self.user_id = ""
                self.number_id = ""

        # Get user's name, tweets, and hashtags
        def get_information(self, user_id):
                tc = twitterCalls.TwitterCaller()
                user = tc.get_user_profile(user_id)
                self.user_name = user.name
                self.user_id = user_id
                self.number_id = user.id
                self.user_tweets = tc.get_user_tweets(user_id, 200)
                for tweet in self.user_tweets:
                        self.user_tweet_texts.append(tweet.__getstate__()['text'].encode('ascii','ignore'))        
                for tweet in self.user_tweet_texts:
                        text = tweet
                        for hashtag in [word for word in tweet.split() if word.startswith('#')]:
                                self.user_hashtags = self.user_hashtags + " " + hashtag
                                text = text.replace(hashtag, "")
                        self.user_text = self.user_text + " " + text

        # Get user's friends
        def get_friends(self):        
                tc = twitterCalls.TwitterCaller()
                friends = tc.get_friends(self.user_id)
                for friend in friends:
                        self.user_friends.append(friend.screen_name)
                        #self.friend_ids.append(friend.id)
                        #self.friend_names.append(friend.name)
		
	# Get user's friends ids
	def get_friend_ids(self):
		tc = twitterCalls.TwitterCaller()
                ids = tc.get_friend_ids(self.user_id)
                self.friend_ids_list = ids
                for id in ids:
                        self.friend_ids = self.friend_ids + " " + str(id)
                
        # Get user's profile photo
        def get_photo(self):
                tc = twitterCalls.TwitterCaller()
                return tc.get_photo(self.user_id)

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