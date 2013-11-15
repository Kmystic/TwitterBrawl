from django.shortcuts import render
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
#from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
#from groups.models import RegistrationForm, Event, EventForm
# Create your views here.
from django import forms
from django.forms.widgets import *
from django.core.mail import send_mail, BadHeaderError
#from models import ContactForm
from django.core.mail import EmailMessage
from brawler.models import BrawlForm

opponent_1 = "?"
opponent_2 = ""

#main page, normally called with main
def index(request):
	return render_to_response('brawler/index.html', 0)

def login(request):
    return render_to_response('brawler/login.html', 0)

def about(request):
    return render_to_response('brawler/about.html', 0)

def brawl(request):
    form = BrawlForm()
    if request.method == 'POST': #If form has been sumbitted
        form = BrawlForm(request.POST, request.FILES)
        if form.is_valid():
            opponent_1 = form.cleaned_data['opponent1']
            opponent_2 = form.cleaned_data['opponent2']
            return render(request, 'brawler/results.html', 0) # Redirect after POST 
    else:
        print '?'

    return render(request, 'brawler/brawl.html', {
        'form':form
    })

def brawl_results(request):
    context = {'opponent1' : opponent_1, 'opponent2' : opponent_2}
    #print opponent_2
    return render(request,'brawler/results.html', context)




'''
@strategy('socialauth_complete', load_strategy=load_strategy)
def auth(request, backend):
    return do_auth(request.strategy, redirect_name=REDIRECT_FIELD_NAME)

#main page
'''
'''
def main(request):
#facebook tage to ensure user is logged in
    try:
        me = facebook.get_myself()
    except NameError:
        return render(request, 'groups/login.html', 0)


def about(request):
#facebook tage to ensure user is logged in
    try:
        me = facebook.get_myself()
    except NameError:
        return render(request, 'groups/login.html', 0)
    context = {'has_registered': MemberHasRegistered()}
    return render(request, 'groups/about.html',context)

'''
#This view redirects the user to facebook in order to get the code that allows
#pyfb to obtain the access_token in the facebook_login_success view
'''
def facebook_login(request):

    facebook = Pyfb(FACEBOOK_APP_ID)
    return HttpResponseRedirect(facebook.get_auth_code_url(redirect_uri=FACEBOOK_REDIRECT_URL))

#This view must be refered in your FACEBOOK_REDIRECT_URL. For example: http://www.mywebsite.com/facebook_login_success/
def facebook_login_success(request):

    code = request.GET.get('code')

    global facebook 
    facebook = Pyfb(FACEBOOK_APP_ID)
    facebook.get_access_token(FACEBOOK_SECRET_KEY, code, redirect_uri=FACEBOOK_REDIRECT_URL)  
    
    return _render_user(facebook,request)

def _render_user(facebook,request):

    me = facebook.get_myself()	
    member = CreateMember(me)
    AddMember(member, me)
    
    context = {'has_registered': MemberHasRegistered()}
    return render(request,'groups/index.html',context)
'''