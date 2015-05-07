from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mining_folketinget.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^query_folketinget/', include('query_folketinget.urls', namespace='query_folketinget')),
	url(r'^movie_critics/', include('movie_critics.urls', namespace='movie_critics')),
    url(r'^admin/', include(admin.site.urls)),
)
