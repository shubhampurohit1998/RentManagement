from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from RentManagement import settings
from .models import *
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from .forms import *


def index(request):
    query = request.GET.get('search')
    if query:
        return HttpResponseRedirect(reverse('search_city', args=[query]))
    else:
        return render(request, 'index.html')


def add_property(request):

    if request.method == 'POST':
        form = PropertyRegisterForm(request.POST)
        # if form.is_valid():
        form.save()
        # import pdb;pdb.set_trace()
        # return HttpResponseRedirect(reverse('add_image', args=[request.property.id]))
        return HttpResponseRedirect(reverse('home'))
    form = PropertyRegisterForm(initial={'owner': request.user.person.id})
    return render(request, 'PropertyRegistration.html', {'form': form})


def search_property_by_locality(request, city_name):
    property_list = Property.objects.filter(city__icontains=city_name)
    context = {'property_list': property_list}
    return render(request, 'index.html', context)


def show_property_list(request):
    flag = True
    property_list = Property.objects.filter(owner_id=request.user.person.id)
    context = {'property_list': property_list, 'flag': flag}
    return render(request, 'ShowProperty.html', context)


def add_property_images(request, property_id):
    if request.method == 'POST':
        # import pdb;
        # pdb.set_trace()
        form = InsertImageForm(request.POST, request.FILES)
        form.save()
        return HttpResponseRedirect(reverse('add_image', args=[property_id]))

    images = Picture.objects.filter(property_id=property_id)
    form = InsertImageForm(initial={'property': property_id})
    return render(request, 'Add_Pictures.html', {'form': form, 'images': images, 'media_url': settings.MEDIA_URL})


def delete_property(request, property_id):
    obj = get_object_or_404(Property, pk=property_id)
    # import pdb;
    # pdb.set_trace()
    obj.delete()
    return HttpResponseRedirect(reverse('show_property'))


def update_property_details(request, property_id):
    if request.method == 'POST':
        # import pdb;
        # pdb.set_trace()
        form = PropertyRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('show_property'))

    property_obj = get_object_or_404(Property, pk=property_id)
    form = PropertyRegisterForm(instance=property_obj)
    # initial = {'owner': request.user.person.id},
    context = {'form': form}
    return render(request, 'UpdatePropertyDetail.html', context)


def property_detail(request, property_id):
    # import pdb;
    # pdb.set_trace()
    property_obj = get_object_or_404(Property, pk=property_id)
    owner_obj = get_object_or_404(Person, pk=property_obj.owner_id)
    user_obj = get_object_or_404(User, pk=owner_obj.user_id)
    context = {'property': property_obj, 'owner': owner_obj, 'user': user_obj}
    return render(request, 'ViewPropertyDetails.html', context)
