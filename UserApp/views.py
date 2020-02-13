from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect


def index(request):
    lst = Property.objects.all()[:5]
    return render(request, 'index.html', {'property': lst})


