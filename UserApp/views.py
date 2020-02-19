from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from RentManagement import settings
from .models import *
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from .forms import *


def index(request):
    form = SearchForm()
    context = {'form': form}
    query = request.GET.get('query')
    if query:
        form = SearchForm()
        property_list = Property.objects.filter(city__icontains=query)
        Lst = []
        for list in property_list:
            try:
                if list.rent.customer is None:
                    Lst.append(list)
            except Exception:
                Lst.append(list)
        context = {'property_list': Lst, 'form': form}
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html', context)


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


def show_property_list(request):
    flag = True
    property_list = Property.objects.filter(owner_id=request.user.person.id)
    rent_properties = Rent.objects.filter(customer_id=request.user.person.id)
    context = {'property_list': property_list, 'flag': flag, 'on_rent': rent_properties}
    return render(request, 'ShowProperty.html', context)


def add_property_images(request, property_id):
    if request.method == 'POST':
        # import pdb;
        # pdb.set_trace()
        form = InsertImageForm(request.POST, request.FILES)
        form.save()
        return HttpResponseRedirect(reverse('add_image', args=[property_id]))

    images = Picture.objects.filter(property_id=property_id)
    # import pdb;pdb.set_trace()
    form = InsertImageForm(initial={'property': property_id})
    return render(request, 'Add_Pictures.html', {'form': form, 'images': images})


def delete_property(request, property_id):
    obj = get_object_or_404(Property, pk=property_id)
    # import pdb;
    # pdb.set_trace()
    obj.delete()
    return HttpResponseRedirect(reverse('show_property'))


def update_property_details(request, property_id):

    property_obj = get_object_or_404(Property, pk=property_id)
    form = PropertyRegisterForm(request.POST or None, instance=property_obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('show_property'))
    context = {'form': form}
    return render(request, 'UpdatePropertyDetail.html', context)


def property_detail(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id)
    owner_obj = get_object_or_404(Person, pk=property_obj.owner_id)
    user_obj = get_object_or_404(User, pk=owner_obj.user_id)
    picture_obj = Picture.objects.filter(property_id=property_id)
    context = {'property': property_obj,
               'owner': owner_obj,
               'user': user_obj,
               "images": picture_obj}
    return render(request, 'ViewPropertyDetails.html', context)


def profile(request):
    user_obj = get_object_or_404(User, pk=request.user.id)
    # import pdb;
    # pdb.set_trace()
    person_obj = get_object_or_404(Person, user_id=request.user.id)
    # owned_properties = Property.objects.all(owner_id=person_obj.id).count()
    context = {'user': user_obj, 'person': person_obj}
    return render(request, 'Profile.html', context)


def update_user_profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    form = RegisterForm(request.POST or None, instance=user)
    # if form.is_valid():
    #     form.save(request)
    #     return HttpResponseRedirect(reverse('profile'))
    context = {'form': form}
    return render(request, 'UpdateProfile.html', context)


def property_on_rent(request, property_id):
    # customer_obj = Person.objects.get(id=request.user.person.id)
    # property_obj = Property.objects.get(id=property_id)
    if request.method == 'POST':
        form = RentForm(request.POST)
        # import pdb;
        # pdb.set_trace()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('show_property'))
    form = RentForm(initial={'property': property_id, 'customer': request.user.person.id})
    context = {'form': form}
    return render(request, 'AddOnRentPeriod.html', context)
