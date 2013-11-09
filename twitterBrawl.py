from __future__ import division
from stemming import porter2
from operator import itemgetter
from nltk.corpus import stopwords
import tweepy
import json
import sys
import twitterCalls
import re
import math
import json
import os
import time
import twitterUsers
#import twitterUsers

def tokenize(text):
	tokens = re.findall("[\w']+", text.lower())
	important_words = []
	for word in tokens:
		if word not in stopwords.words('english'):
			important_words.append(word)
	return [porter2.stem(token) for token in important_words]


class TwitterBrawl():
	""" A search engine for tweets. """
	def __init__(self):
		"""
		purpose: Create the search engine for tweets
		parameters:
			database - store tweets information
		"""
		# used to store inverted index information for all terms/tokens
		self.inverted_index = {}
		# store all terms/tokens in our documents as keys, values being their raw df 
		self.word_list = {}
		# store (inverse) weighted document frequencies 
		self.idfs = {}
		# used to store the frequency of terms within documents (tf)
		self.term_freq = {}
		# used to store the tf-idf value of documents
		self.tf_idf = {}

	def _term_tf_idf(self, token, count):
		"""
		purpose: Calculate tf-idf for a token in the document
		parameters:
			token - 
			count - the number of occurrence of a term/token in one document in logarithmic terms
		return: term/token's tf-idf
		"""
		#Return the tf-idf
		return count * self.idfs[token] 
		
	def CosineSim(self, vec_query, vec_doc):
		"""
		purpose: Calculate cosine similarity for two documents (vectors, represented as dictionaries)
		parameters:
			vec_query - the vector (dictionary) with only raw term frequency for query
			vec_doc   - the vector (dictionary) of tf-idf for a document
		return: cosine similarity between the query and a document
		"""
		#Stores dot product of two vectors
		dot_product = 0.0
		#Stores the magnitude of query vector (without sqrt)
		query_magnitude = 0.0
		#Stores the magnitude of doc vector (without sqrt)
		doc_magnitude = 0.0
		#Stores product of magnitudes
		magnitude_product = 0.0
		
		# Calculate dot product
		for token in vec_query:
			if token in vec_doc:
				dot_product += vec_query[token] * vec_doc[token]

		# Calculate magnitude product
		for token in vec_query:
			query_magnitude += math.pow(vec_query[token],2)
		for token in vec_doc:
			doc_magnitude += math.pow(vec_doc[token],2)
		magnitude_product += math.sqrt(query_magnitude) * math.sqrt(doc_magnitude)

		# Return cosine simularity
		return dot_product/magnitude_product


	def index_tweets(self,tweets):
		"""
		purpose: process raw tweets and calculate pagerank of users in tweets
		parameters:
		  tweets - an iterator of tweet dictionaries
		returns: none
		Note: please make sure you create a field "rank" in the tweet for storing pagerank score.
		"""
		#doc_count stores total number of documents
		doc_count = 0
		
		#For each tweet store it in our database, add to our inverted_index, word_list, and calculate tf per document
		for tweet in enumerate(tweets):
			doc_count+=1
			doc_id = doc_count - 1;
			tokenized_tweet_text = tokenize(tweet) #Tokenize tweet
			no_dup_tok_tweet_text = set(tokenized_tweet_text) #Remove duplicate tokens
			#Tf_dict used to store tf values for each document
			tf_dict = {}
			#Add our tokens for this tweet into our inverted index if not present, then add the tweet to it's value
			for token in no_dup_tok_tweet_text:
				if (token in self.inverted_index) == False:
					self.inverted_index[token] = []
					#Also, add our unique tokens into our word_list
					self.word_list[token] = 0
				self.inverted_index[token].append(doc_id)
				#Add 1 to the count of that token for df
				self.word_list[token] += 1
				#Add that token to our tf_dict for that document
				tf_dict[token] = 0
			#Caluclate raw tfs for that document
			for token in tokenized_tweet_text:
				tf_dict[token] +=1
			# Calculate log tf
			for key in tf_dict:
				tf_dict[key] = 1+ math.log(tf_dict[key],2)
			# Add that tweets tf dict to our term_freq dictionary
			self.term_freq[doc_id] = tf_dict
  
				
		#Calculate idf for all of the terms in the tweets.
		for key in self.word_list:  
			self.idfs[key] = math.log(doc_count/self.word_list[key],2)

		
		#Calculate tf_idf for all documents
		for doc_id, item in enumerate(self.mytweets):
			tf_idf_dict = {}
			for token in self.term_freq[doc_id]:
				tf_idf_dict[token] = self._term_tf_idf(token, self.term_freq[doc_id][token])
			self.tf_idf[doc_id] = tf_idf_dict











def main():
	mainUser = twitterUsers.TwitterUser()
	mainUser.get_information("kmystic524")
	#user1 = twitterUsers.TwitterUser()
	#user1.get_information("katyperry")
	#user2 = twitterUsers.TwitterUser()
	#user2.get_information("TheRealCaverlee")
	tweets = []
	print mainUser.user_text
	tweets.append(mainUser.user_text)
	#tweets.append(user1.user_text)
	#tweets.append(user2.user_text)
	tb = TwitterBrawl()
	tb.index_tweets(tweets)

if __name__ == "__main__":
	main()


