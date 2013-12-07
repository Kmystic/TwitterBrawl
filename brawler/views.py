from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django import forms
from django.forms.widgets import *
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import EmailMessage

# Form includes
from django import forms
from django.db import models
import urllib
import twitterUsers
import twitterCalls
import twitterBrawl


# Global Variables
global opponent_1 
global opponent_2 
global user_name
user_name = "" 
global tb 
tb = twitterUsers.TwitterUser()
global OPPONENT_CHOICES
OPPONENT_CHOICES = []
global isLogged


# Form to get username infomration from web application
class LoginForm(forms.Form):
    username = forms.CharField(max_length = 200, required=True)

# Function to get a users information
def getUser(username):
    global tb
    tb.get_information(username)
    tb.get_friends()
    tb.get_all_friends()
    global OPPONENT_CHOICES
    for friend_id in (tb.user_friends):
        OPPONENT_CHOICES.append(friend_id)
        
# Determines if a user is logged in
def isLoggedIn():
    return isLogged


'''

Views

'''

# View for index.html
def index(request):
	return render_to_response('brawler/index.html', 0)

# View for login.html
def login(request):
    form = LoginForm()
    if request.method == 'POST': #If form has been sumbitted
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            # Get user information
            global isLogged
            isLogged = True
            global user_name
            user_name = form.cleaned_data['username']
            getUser(form.cleaned_data['username'])
            real_name = tb.user_name
            context = {'username' : user_name, 'realname' : real_name, 'logged_in':isLogged}
            return render(request, 'brawler/verification.html', context) # Redirect after POST 
    else:
        print '?'
    return render(request, 'brawler/login.html', {
        'form':form,
    })

# View for verification.html
def login_verification(request):
    context = {'username' : user_name, 'realname' : real_name, 'logged_in':isLogged}
    return render(request,'brawler/verification.html', context)

# View for logout.html
def logout(request):
    global isLogged
    isLogged = False
    global OPPONENT_CHOICES
    OPPONENT_CHOICES = []
    global user_name
    user_name = ""
    global tb 
    tb = twitterUsers.TwitterUser()
    return render(request,'brawler/logout.html', 0)

# View for about.html
def about(request):
    print isLoggedIn()
    context = {'logged_in':isLoggedIn()}
    return render_to_response('brawler/about.html', context)

# View for brawl.html
def brawl(request):
    global OPPONENT_CHOICES
    OPPONENT_CHOICES= sorted(OPPONENT_CHOICES)
    context = {'opponents1': OPPONENT_CHOICES, 'opponents2' : OPPONENT_CHOICES}
    return render(request, 'brawler/brawl.html', context)

# Function for results.html
def brawl_function(request):
    # This function handles the comparison calculations
    global opponent_1
    global opponent_2
   
    opponent_1 = request.POST['opponent1'] 
    opponent_2 = request.POST['opponent2']

    global tb
    main_user = tb

    opp1 = twitterUsers.TwitterUser()
    opp1.get_information(opponent_1)
    opp1.get_all_friends()
    profilePhotoURL = opp1.get_photo()
    photoName = "brawler/static/brawler/media/" + str(opponent_1) + ".jpg"
    file = str(photoName)
    f = open(file,'wb')
    f.write(urllib.urlopen(profilePhotoURL).read())

    opp2 = twitterUsers.TwitterUser()
    opp2.get_information(opponent_2)
    opp2.get_all_friends()
    profilePhotoURL = opp2.get_photo()
    photoName = "brawler/static/brawler/media/" + str(opponent_2) + ".jpg"
    file = str(photoName)
    f = open(file,'wb')
    f.write(urllib.urlopen(profilePhotoURL).read())

    twitter_tweets = twitterBrawl.TwitterBrawl()
    twitter_hashtags = twitterBrawl.TwitterBrawl()
	twitter_friends = twitterBrawl.TwitterBrawl()
	

    twitter_tweets.index(main_user.user_text, opp1.user_text, opp2.user_text)
    twitter_hashtags.index(main_user.user_hashtags, opp1.user_hashtags, opp2.user_hashtags)
	twitter_friends.index(main_user.friend_ids, opp1.friend_ids, opp2.friend_ids)

    hashtag_scores = twitter_hashtags.bestCosineSim()
    tweet_scores = twitter_tweets.bestCosineSim()
    friend_scores = twiiter_friends.bestCosineSim()

    op1_score = .5*hashtag_scores[0] + .35*tweet_scores[0] + .15*friend_scores[0]
    op2_score = .5*hashtag_scores[1] + .35*tweet_scores[1] + .15*friend_scores[1]
	

    win = ""

    if max(op1_score,op2_score) == op1_score:
        print "You're best friends with " + opponent_1 + "!"
        win = opponent_1
    else:
        print "You're best friends with " + opponent_2 + "!"
        win = opponent_2

    print win
    top_hash = {}
    top_hash[1] = [x[0] for x in twitter_hashtags.top_5[1]]
    top_hash[2] = [x[0] for x in twitter_hashtags.top_5[2]]
    top_tweet = {}
    top_tweet[1] = [x[0] for x in  twitter_tweets.top_5[1]] 
    top_tweet[2] = [x[0] for x in  twitter_tweets.top_5[2]] 
    top_friend = {}
    top_friend[1] = [x[0] for x in twitter_friends.top_5[1]]
    top_friend[2] = [x[0] for x in twitter_friends.top_5[2]]
    context = {'logged_in':isLogged,
            'opponent1' : opponent_1, 
            'opponent2':opponent_2, 
            'winner': win, 
            'hashtag' :hashtag_scores, 
            'tweet' : tweet_scores,
            'friend (score)' : friend_scores,
            'top_hashtags' : top_hash,
            'top_tweets' : top_tweet}
    return render(request, 'brawler/results.html', context)

# View for results.html
def brawl_results(request):
    return render(request,'brawler/results.html', context)




