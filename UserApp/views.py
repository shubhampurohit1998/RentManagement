from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse


def index(request, ownr_id):
    ownr = get_object_or_404(Owner, id=ownr_id)
    return render(request, 'index.html', {'ownr': ownr})

