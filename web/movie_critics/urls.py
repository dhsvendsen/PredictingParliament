from django.conf.urls import patterns, url

from movie_critics import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)