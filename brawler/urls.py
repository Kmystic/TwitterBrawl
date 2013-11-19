from django.conf.urls import patterns, url
from django.utils import timezone
from brawler import views


urlpatterns = patterns('',
    # ex: /groups/
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login/verification$', views.login_verification, name='login_verification'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^brawl/$', views.brawl, name='brawl'),
    url(r'^brawl/function$', views.brawl_function, name='brawl_function'),
    url(r'^brawl/results$', views.brawl_results, name='brawl_results'),
    # ex: /groups/main
	#url(r'^main/$', views.main, name='main'),
    #url(r'^about/$', views.about, name='about'),
    #url(r'^results/$', views.runners, name='runners'),
	#url(r'^twitter_login/$', views.facebook_login, name = 'facebook_login'),
    #url(r'^twitter_login_success/$', views.facebook_login_success, name = 'facebook_login_success'),
)