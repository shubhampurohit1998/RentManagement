from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import *


def register(request):
    if request.method == 'POST':
        obj = request.POST
        return HttpResponseRedirect('index.html')
    form = RegisterForm()
    return render(request, 'signup.html', {'form': form})

