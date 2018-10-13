from django.shortcuts import get_object_or_404,render
from django.contrib.auth.decorators import permission_required
from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.staticfiles import finders

#models
# from .models import  *


#Show a list of all the groups
def cccindex(request):
	return render(request, 'ccc/index.html')

