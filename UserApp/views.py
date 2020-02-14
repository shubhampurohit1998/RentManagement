from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import *


def index(request):
    lst = Property.objects.all()[:5]
    return render(request, 'index.html', {'property': lst})


def add_property(request):

    if request.method == 'POST':
        form = PropertyRegisterForm(request.POST)
        # if form.is_valid():
        form.save()
        import pdb;pdb.set_trace()
        return HttpResponseRedirect(reverse('add_image', args=[request.property.id]))
    form = PropertyRegisterForm(initial={'owner': request.user.person.id})
    return render(request, 'PropertyRegistration.html', {'form': form})


def search_property_by_locality(request, location):
    if request.method == 'POST':
        property_list = Property.objects.filter(city__icontains=location)
        context = {'property_list': property_list}
        return render(request, 'SearchResult.html', context)


def show_property_list(request):
    property_list = Property.objects.filter(owner_id=request.user.person.id)
    context = {'property_list': property_list}
    return render(request, 'ShowProperty.html', context)


def add_property_images(request, property_id):
    if request.method == 'POST':
        form = InsertImageForm(request.POST, request.FILES)
        form.save()
        return HttpResponseRedirect(reverse('add_image'))
    form = InsertImageForm(initial={'property': property_id})
    context = {'form': form}
    return render(request, 'Add_Pictures.html', context)
