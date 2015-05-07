from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
	context = {'intro': 'Movie Critics Page'}
	return render(request, 'movie_critics/index.html', context)