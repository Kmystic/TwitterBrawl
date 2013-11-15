from django.db import models
from django import forms
# Create your models here.
from django.db import models
import twitterUsers





class BrawlForm(forms.Form):
	OPPONENT_CHOICES = []

	tb = twitterUsers.TwitterUser()
	tb.get_information("TheRealCaverlee")
	print "Users real name:" + tb.user_name
	print "Tweets:"
	#for tweet in tb.user_tweet_texts:
	#	print tweet
	print "Friends:"
	for i, friend_id in enumerate (tb.user_friends):
		OPPONENT_CHOICES.append((i,friend_id))
	#print friend_id

	opponent1 = forms.ChoiceField(choices = OPPONENT_CHOICES, required=True)
	opponent2 = forms.ChoiceField(choices = OPPONENT_CHOICES, required=True)

