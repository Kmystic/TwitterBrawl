from __future__ import division
from stemming import porter2
from operator import itemgetter
import stopwords
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
'''
This class handles the comparison evaluations

'''

# Tokenize the text
def tokenize(text):
    tokens = re.findall("[\w']+", text.lower())
    important_words = []
            
    for word in tokens:
        if word not in stopwords.stopwords:
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
            #stores all docs of tweets minus stop words
            self.mytweets = []
            # used to store inverted index information for all terms/tokens
            self.inverted_index = {}
            # store all terms/tokens in our documents as keys, values being their raw df 
            self.word_list = []
            # store (inverse) weighted document frequencies 
            self.idfs = {}
            # used to store the frequency of terms within documents (tf)
            self.term_freq = {}
            # used to store the tf-idf value of documents
            self.tf_idf = {}
            self.top_5 = {}

        def _term_tf_idf(self, token, count):
            #"""
            #purpose: Calculate tf-idf for a token in the document
            #parameters:
            #    token -  
            #    count - the number of occurrence of a term/token in one document
            #return: term/token's tf-idf
            #"""        
            idf = self.idfs.get(token)
            tf = 0
            if count > 0:
                    tf = 1 + math.log(count, 2)
            return (tf*idf)
                
        def bestCosineSim(self):
            """
            purpose: Calculate cosine similarity for two documents (vectors, represented as dictionaries)
            parameters:
                    vec_query - the vector (dictionary) with only raw term frequency for query
                    vec_doc   - the vector (dictionary) of tf-idf for a document
            return: cosine similarity between the query and a document
            """
            
            #cos sim between user and friend1
            query_mag = 0
            doc_mag = 0
            dot_product = 0
            for word in self.tf_idf[0]:
                    query_mag += self.tf_idf[0][word]**2
                    doc_mag += self.tf_idf[1][word]**2
                    dot_product += (self.tf_idf[0][word]*self.tf_idf[1][word])
            mag = math.sqrt(query_mag*doc_mag)
            uf1 = 0
            if (mag > 0):
                    uf1 = (dot_product/mag)
            
            #cos sim between user and friend2
            query_mag = 0
            doc_mag = 0
            dot_product = 0
            for word in self.tf_idf[0]:
                    query_mag += self.tf_idf[0][word]**2
                    doc_mag += self.tf_idf[2][word]**2
                    dot_product += (self.tf_idf[0][word]*self.tf_idf[2][word])
            mag = math.sqrt(query_mag*doc_mag)
            uf2 = 0
            if (mag > 0):
                    uf2 = (dot_product/mag)
            
            #return max (incase you couldn't tell.......) 
            #if max(uf1,uf2) == uf1:
            #        return 1
            #else:
            #        return 2
            
            return [uf1,uf2] #return the scores

        # Index tweets
        def index(self,user,friend1,friend2):
            tweets = []
            tweets.append(user) #index 0 = user
            tweets.append(friend1) #index 1 = friend1
            tweets.append(friend2) #index 2 = friend2
                            
            for i in range(0,len(tweets)): #for each doc of tweets from a user
                    self.tf_idf[i] = [] #tf-idf vector is an empty list/vector
                    temp = [item for item in tokenize(tweets[i])] #creates a list of every non-stop word in the tweet
                    
                    #TO DO: FIGURE OUT HASHTAGS
                    
                    for word in temp: #for every nonstop word in the doc
                            if word in self.inverted_index: #we have seen this word before
                                    self.inverted_index[word].append(i)
                                    self.term_freq[word][i] += 1
                            else: #we have never seen this word before!
                                    self.inverted_index[word] = [i] #add word to Inv Ind, reference to doc id
                                    self.word_list.append(word) #add word to word list
                                    self.term_freq[word] = [0,0,0] #start an empty list for term freq of that word
                                    self.term_freq[word][i] += 1
                                    self.idfs[word] = [] #empty list for the word
                    doc = dict(tokens=list(temp), tweet=tweets[i])
                    self.mytweets.append(doc)
                    
            for word in self.word_list:
                    df = len(set(self.inverted_index[word])) #document freq for a word "at most 3"
                    self.idfs[word] = math.log((len(self.mytweets))/df,2) #computing the idf for each word
                    for doc in self.tf_idf: #create each user's tf_idf vector populated with 0s
                            self.tf_idf.get(doc).append(0)
            
            #populate each user's tfidf vector with raw TFs for each word
            for doc in range(0,len(self.tf_idf)): #in each documents of tweets...
                tf_idf = {}
                for word in range(0,len(self.word_list)): #for every word
                    raw_tf = self.term_freq[self.word_list[word]][doc]
                    tf_idf[self.word_list[word]] = self._term_tf_idf(self.word_list[word],raw_tf) #calculate the tfidf score]
                self.tf_idf[doc] = tf_idf


            # Calculate most similary used words
            for doc in range(1,len(self.tf_idf)): #in each documents of tweets...
                comparison_scores = {}
                for word in self.tf_idf[doc].keys(): #for every word
                    if (self.tf_idf[doc][word] != 0 and self.tf_idf[0][word] != 0):
                        comparison_scores[word] = abs(self.tf_idf[doc][word] - self.tf_idf[0][word])
                    else:
                        comparison_scores[word] = 100
                self.top_5[doc] = comparison_scores

            # Only save the top 5 most similar words
            for doc in range(1,len(self.tf_idf)):
                self.top_5[doc] = sorted(self.top_5[doc].items(), key = lambda i: i[1])[:5]


                
            '''
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
            '''


def main():
    
    mainUser = twitterUsers.TwitterUser()
    mainUser.get_information("kmystic524")
    mainUser.get_friends()
    user1 = twitterUsers.TwitterUser()
    user1.get_information("cmdit")
    user1.get_friends()
    user2 = twitterUsers.TwitterUser()
    user2.get_information("TheRealCaverlee")
    user2.get_friends()
    tb_tweets = TwitterBrawl()
    tb_hashtags = TwitterBrawl()
    #tb_friends = TwitterBrawl()

    tb_tweets.index(mainUser.user_text, user1.user_text, user2.user_text)
    tb_hashtags.index(mainUser.user_hashtags, user1.user_hashtags, user2.user_hashtags)
    #tb_friends.index(mainUser.friend_ids, user1.friend_ids, user2.friend_ids)


    hashtag_scores = tb_hashtags.bestCosineSim()
    tweet_scores = tb_tweets.bestCosineSim()
    friend_scores = []
    friend_scores.append(len(set(mainUser.friend_ids).intersection(user1.friend_ids)))
    friend_scores.append(len(set(mainUser.friend_ids).intersection(user2.friend_ids)))
    print "Friends in common with user 1: "
    print friend_scores[0]
    print "Friends in common with user 2: "
    print friend_scores[1]
    #.6*hashtag_scores[0]
    f1_score = .5*hashtag_scores[0] + .35*tweet_scores[0] + .15*friend_scores[0]
    f2_score = .5*hashtag_scores[1] + .35*tweet_scores[1] + .15*friend_scores[1]
    top_tweet = {}
    top_tweet[1] = [x[0] for x in  tb_tweets.top_5[1]] 
    top_tweet[2] = [x[0] for x in  tb_tweets.top_5[2]] 
    print "Top 5 common words with user 1: "
    for word in top_tweet[1]:
        print word
    print "Top 5 common words with user 2: "
    for word in top_tweet[2]:
        print word


    #.6*hashtag_scores[0]
    if max(f1_score,f2_score) == f1_score:
            print "You're best friends with " + user1.user_name + "!"
    else:
            print "You're best friends with " + user2.user_name + "!"


    '''
    main_text = "banana and strawberry smoothie are the best, most fantastic smoothies ever! "
    opp1_text = "bananas are the best thing in the world, I can't believe how tasty they are"
    opp2_text = "strawberries are fantastic, I can't believe I've never eaten a strawberry before"
    tb_tweets = TwitterBrawl()
    tb_tweets.index(main_text, opp1_text, opp2_text)
    '''
if __name__ == "__main__":
        main()
