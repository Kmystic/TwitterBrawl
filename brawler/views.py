from django.shortcuts import render
# Create your views here.
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
# Forms
# Form to pick the two opponents

class BrawlForm(forms.Form):
    def __init__(self, choices, *args):
        super(BrawlForm, self).__init__(*args)
        #super(BrawlForm, self).__init__(*args,**kwargs)
        #print choices
        self.fields["opponent1"] = forms.ChoiceField(choices=choices, required = True)
        self.fields["opponent2"] = forms.ChoiceField(choices=choices, required = True)
    #opponent1 = forms.ChoiceField(choices = OPPONENT_CHOICES, required=True)
    #opponent2 = forms.ChoiceField(choices = OPPONENT_CHOICES, required=True)

# Form to get username infomration
class LoginForm(forms.Form):
    username = forms.CharField(max_length = 200, required=True)


def getUser(username):
    global tb
    tb.get_information(username)
    tb.get_friends(username)
    global OPPONENT_CHOICES
    for friend_id in (tb.user_friends):
        OPPONENT_CHOICES.append(friend_id)
        

def isLoggedIn():
    return isLogged


# Views
def index(request):
	return render_to_response('brawler/index.html', 0)

def login(request):
    form = LoginForm()
    if request.method == 'POST': #If form has been sumbitted
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
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

def login_verification(request):
    context = {'username' : user_name, 'realname' : real_name, 'logged_in':isLogged}
    return render(request,'brawler/verification.html', context)

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

def about(request):
    print isLoggedIn()
    context = {'logged_in':isLoggedIn()}
    return render_to_response('brawler/about.html', context)

def brawl(request):
    '''
    global OPPONENT_CHOICES
    form = BrawlForm(OPPONENT_CHOICES)
    if request.method == 'POST': #If form has been sumbitted
        #print OPPONENT_CHOICES
        global OPPONENT_CHOICES
        form = BrawlForm(request.POST, request.FILES, OPPONENT_CHOICES)
        if form.is_valid():
            global opponent_1
            opponent_1 = form.cleaned_data["opponent1"]
            global opponent_2
            opponent_2 = form.cleaned_data["opponent2"]
            context = {'logged_in':isLoggedIn()}
            return render(request, 'brawler/results.html', context) # Redirect after POST 
        print'here!'
    else:
        #print OPPONENT_CHOICES
        print "nothing"
        #form = BrawlForm(initial={'gender':me.gender,'name':me.name,'birth_date':me.birthday, 'email':me.email})
        return render(request, 'brawler/brawl.html', {
        'form':form 
        })
    return render(request, 'brawler/brawl.html', 0)
    #print OPPONENT_CHOICES
    '''
    global OPPONENT_CHOICES
    context = {'opponents1': OPPONENT_CHOICES, 'opponents2' : OPPONENT_CHOICES}
    return render(request, 'brawler/brawl.html', context)

def brawl_function(request):
    global opponent_1
    global opponent_2
   
   # try:
        
    opponent_1 = request.POST['opponent1'] 
    opponent_2 = request.POST['opponent2']
    #except:
     #   opponent_1 = None    
      #  opponent_2 = None

    global tb
    main_user = tb

    opp1 = twitterUsers.TwitterUser()
    opp1.get_information(opponent_1)
    profilePhotoURL = opp1.get_photo(opponent_1)
    photoName = "brawler/static/brawler/media/" + str(opponent_1) + ".jpg"
    file = str(photoName)
    f = open(file,'wb')
    f.write(urllib.urlopen(profilePhotoURL).read())

    opp2 = twitterUsers.TwitterUser()
    opp2.get_information(opponent_2)
    profilePhotoURL = opp2.get_photo(opponent_2)
    photoName = "brawler/static/brawler/media/" + str(opponent_2) + ".jpg"
    file = str(photoName)
    f = open(file,'wb')
    f.write(urllib.urlopen(profilePhotoURL).read())

    twitBrawl = twitterBrawl.TwitterBrawl()
    twitBrawl.index_tweets(main_user, opp1, opp2)

    win = ""
    if twitBrawl.bestCosineSim() == 1:
        print "You're best friends with " + opponent_1 + "!"
        win = opponent_1
    else:
        print "You're best friends with " + opponent_2 + "!"
        win = opponent_2

    print win


    context = {'logged_in':isLogged,'opponent1' : opponent_1, 'opponent2':opponent_2, 'winner': win}
    return render(request, 'brawler/results.html', context)

def brawl_results(request):
    

    #print opponent_2
    return render(request,'brawler/results.html', context)




