from django.conf.urls import patterns, url
from django.utils import timezone
from brawler import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login/verification$', views.login_verification, name='login_verification'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^about/$', views.about, name='about'),
    url(r'^brawl/$', views.brawl, name='brawl'),
    url(r'^test/$', views.test, name='test'),
    url(r'^test/function$', views.test_function, name='test_function'),
    url(r'^brawl/function$', views.brawl_function, name='brawl_function'),
    url(r'^brawl/results$', views.brawl_results, name='brawl_results'),
)