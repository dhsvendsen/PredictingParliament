from django.conf.urls import patterns, url

from query_folketinget import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^predict', views.predict, name='predict'),
)
