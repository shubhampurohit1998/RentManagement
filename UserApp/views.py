from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from RentManagement import settings
from .models import *
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from .forms import *
from django.views import View
from django.views.generic import ListView, DetailView
from datetime import date


def index(request):
    form = SearchForm()
    query = request.GET.get('query')
    flag = False
    context = {'form': form, 'flag': flag}
    if query:
        flag = True
        form = SearchForm()

        property_list = Property.objects.filter(Q(city__icontains=query),
                                                Q(is_active=True))
        context = {'property_list': property_list, 'form': form, 'flag': flag}
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html', context)


def add_property(request):

    if request.method == 'POST':
        form = PropertyRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
    form = PropertyRegisterForm(initial={'owner': request.user.person.id, 'is_active':  True})
    return render(request, 'PropertyRegistration.html', {'form': form})


def show_property_list(request):
    property_list = Property.objects.filter(owner_id=request.user.person.id)
    context = {'property_list': property_list}
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


# def add_property_images(request, property_id):
#     InsertImageFormSet = formset_factory(InsertImageForm, extra=0)
#     if request.method == 'POST':
#         formset = InsertImageFormSet(request.POST, request.FILES)
#         for f in formset:
#             # cd = f.cleaned_data
#             pic_name = f.pic_name
#             picture = Picture(pic_name=pic_name)
#             picture.save()
#         return HttpResponseRedirect(reverse('add_image', args=[property_id]))
#
#     images = Picture.objects.filter(property_id=property_id)
#     # import pdb;pdb.set_trace()
#     InsertImageFormSet = formset_factory(InsertImageForm, extra=0)
#     form = InsertImageFormSet(initial=[{'property': property_id}])
#     return render(request, 'Add_Pictures.html', {'form': form, 'images': images})


def delete_property(request, property_id):
    obj = get_object_or_404(Property, pk=property_id)
    # import pdb;
    # pdb.set_trace()
    if obj.is_active:
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


# Function based view

# def profile(request):
#     user_obj = get_object_or_404(User, pk=request.user.id)
#     person_obj = get_object_or_404(Person, user_id=request.user.id)
#     # owned_properties = Property.objects.all(owner_id=person_obj.id).count()
#     context = {'user': user_obj, 'person': person_obj}
#     return render(request, 'Profile.html', context)

# Class based view

class ProfileView(View):
    template_name = 'Profile.html'

    def get(self, request):
        user_obj = get_object_or_404(User, pk=request.user.id)
        person_obj = get_object_or_404(Person, user_id=request.user.id)
        # owned_properties = Property.objects.all(owner_id=person_obj.id).count()
        context = {'user': user_obj, 'person': person_obj}
        return render(request, self.template_name, context)


def update_user_profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    person = get_object_or_404(Person, user_id=user.id)
    person_form = UpdateProfilePersonForm(request.POST or None, instance=person)
    user_form = UpdateProfileUserForm(request.POST or None, instance=user)
    if request.method == 'POST':
        if user_form.is_valid() and person_form.is_valid():
            user_form.save()
            person_form.save()
            return HttpResponseRedirect(reverse('profile'))
    context = {'user': user_form, 'person': person_form}
    return render(request, 'UpdateProfile.html', context)


def property_on_rent(request, property_id):
    if request.method == 'POST':
        form = RentForm(request.POST)
        # import pdb;
        # pdb.set_trace()
        if form.is_valid():
            form = RentForm(request.POST)
            Property.objects.filter(id=property_id).update(is_active=False)
            form.save()
            return HttpResponseRedirect(reverse('rental_assets'))
    form = RentForm(initial={'property': property_id, 'customer': request.user.person.id,
                             'date_on_rent': date.today})
    context = {'form': form}
    return render(request, 'AddOnRentPeriod.html', context)


def rental_property_list(request):
    person = Person.objects.get(user_id=request.user.id)
    rental_properties = Rent.objects.filter(customer_id=person.id)
    context = {'rent': rental_properties}
    return render(request, 'OnRentProperty.html', context)


def delete_property_image(request, image_id):
    picture_obj = Picture.objects.get(id=image_id)
    picture_obj.delete()
    return HttpResponseRedirect(reverse('add_image', args=[picture_obj.property_id]))


def renter_details(request, property_id):
    # import pdb;
    # pdb.set_trace()
    property_obj = Property.objects.get(id=property_id)
    rent_obj = Rent.objects.get(property_id=property_id)
    person_obj = get_object_or_404(Person, id=rent_obj.customer.id)
    user_obj = get_object_or_404(User, id=person_obj.user_id)
    context = {'person': person_obj, 'user': user_obj, 'rent': rent_obj, 'property': property_obj}
    return render(request, 'RenterDetails.html', context)


def search_random_properties(request):
    # import pdb;
    # pdb.set_trace()
    property_obj = Property.objects.filter(is_active__exact=True)
    flag = True
    form = SearchForm()
    context = {'property_list': property_obj, 'flag': flag, 'form': form}
    return render(request, 'index.html', context)


def add_profile_picture(request, person_id):
    instance = get_object_or_404(Person, id=person_id)
    form = ProfilePictureForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            form = ProfilePictureForm(request.POST, request.FILES, instance=instance)
            form.save()
            return HttpResponseRedirect('profile')
    return render(request, 'AddProfilePicture.html', {'form': form, 'person_id': person_id})


def leave_request(request, renter_id):
    pass


def request_panel(request):
    pass


class UserList(ListView):
    model = User
    template_name = 'UserList.html'
    context_object_name = 'user_list'


class UserDetail(DetailView):
    model = User
    template_name = 'UserDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person_list'] = Person.objects.all()
        return context
