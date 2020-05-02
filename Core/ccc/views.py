from django.shortcuts import get_object_or_404,render
from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.staticfiles import finders

#models
from .models import  *

#Comic stuff------------------------------------
def ComicHome(request):
	return render(request, 'ccc/index.html')

def ComicSplash(request, inComic):
	return render(request, 'ccc/index.html')

def ComicPage(request, inComic, inPage):
	return render(request, 'ccc/index.html')

#HopePage
def cccindex(request):
	return render(request, 'ccc/index.html')

def PanelHelper(request):
	return render(request, 'ccc/PanelHelper.html')