from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import *
from django.views import View
from datetime import date
from django.contrib.auth.decorators import login_required, permission_required


def index(request):
    form = SearchForm()
    query = request.GET.get('query')
    flag = False
    context = {'search_form': form, 'flag': flag}
    if query:
        flag = True
        form = SearchForm()
        property_list = Property.objects.filter(Q(city__icontains=query),
                                                Q(is_active=True))
        context = {'property_list': property_list, 'search_form': form, 'flag': flag}
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html', context)


@login_required
@permission_required('UserApp.add_property')
def add_property(request):
    if request.method == 'POST':
        form = PropertyRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'PropertyRegistration.html', {'form': form})
    form = PropertyRegisterForm(initial={'owner': request.user.id, 'is_active':  True})
    return render(request, 'PropertyRegistration.html', {'form': form})


@login_required
def show_property_list(request):
    property_list = Property.objects.filter(owner_id=request.user.id)
    context = {'property_list': property_list}
    return render(request, 'ShowProperty.html', context)


@login_required
@permission_required('UserApp.add_picture', raise_exception=True)
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


@login_required
@permission_required('UserApp.delete property', raise_exception=True)
def delete_property(request, property_id):
    # import pdb;
    # pdb.set_trace()
    obj = Property.objects.get(id=property_id)
    if obj.is_active:
        obj.delete()
    return HttpResponseRedirect(reverse('show_property'))


@login_required
@permission_required('UserApp.change property', raise_exception=True)
def update_property_details(request, property_id):

    property_obj = get_object_or_404(Property, pk=property_id)
    form = PropertyRegisterForm(request.POST or None, instance=property_obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('show_property'))
    context = {'form': form}
    return render(request, 'UpdatePropertyDetail.html', context)


@login_required
def property_detail(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id)
    user_obj = get_object_or_404(User, pk=property_obj.owner.id)
    picture_obj = Picture.objects.filter(property_id=property_id)
    context = {'property': property_obj,
               'user': user_obj,
               "images": picture_obj}
    return render(request, 'ViewPropertyDetails.html', context)


# Function based view
@login_required
def profile(request):
    user_obj = get_object_or_404(User, pk=request.user.id)
    # owned_properties = Property.objects.all(owner_id=person_obj.id).count()
    context = {'user': user_obj}
    return render(request, 'Profile.html', context)


# Class based view
# @login_required
# class ProfileView(View):
#     template_name = 'Profile.html'
#
#     def get(self, request):
#         user_obj = get_object_or_404(User, pk=request.user.id)
#         # owned_properties = Property.objects.all(owner_id=person_obj.id).count()
#         context = {'user': user_obj}
#         return render(request, self.template_name, context)


@login_required
def update_user_profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    user_form = UpdateProfileUserForm(request.POST or None, instance=user)
    if request.method == 'POST':
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('profile'))
    context = {'user': user_form}
    return render(request, 'UpdateProfile.html', context)


@login_required
@permission_required('UserApp.add_rent', raise_exception=True)
def property_on_rent(request, property_id):
    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            Property.objects.filter(id=property_id).update(is_active=False)
            form.save()
            return HttpResponseRedirect(reverse('rental_assets'))
        else:
            return render(request, 'AddOnRentPeriod.html', {'form': form})
    form = RentForm(initial={'property': property_id, 'customer': request.user.id,
                             'date_on_rent': date.today, 'is_active': True})
    context = {'form': form}
    return render(request, 'AddOnRentPeriod.html', context)


@login_required
def rental_property_list(request):
    # user = User.objects.get(id=request.user.id)
    rental_properties = Rent.objects.filter(customer_id=request.user.id)
    context = {'rent': rental_properties}
    return render(request, 'OnRentProperty.html', context)


@login_required
def delete_property_image(request, image_id):
    picture_obj = Picture.objects.get(id=image_id)
    picture_obj.delete()
    return HttpResponseRedirect(reverse('add_image', args=[picture_obj.property_id]))


@login_required
def renter_details(request, property_id):
    # import pdb;
    # pdb.set_trace()
    property_obj = Property.objects.get(id=property_id)
    rent_obj = Rent.objects.get(property_id=property_id, is_active=True)
    user_obj = get_object_or_404(User, id=rent_obj.customer.id)
    context = {'user': user_obj, 'rent': rent_obj, 'property': property_obj}
    return render(request, 'RenterDetails.html', context)


def search_random_properties(request):
    # import pdb;
    # pdb.set_trace()
    property_obj = Property.objects.filter(is_active__exact=True)
    flag = True
    form = SearchForm()
    context = {'property_list': property_obj, 'flag': flag, 'form': form}
    return render(request, 'index.html', context)


@login_required
def add_profile_picture(request, person_id):
    # instance = get_object_or_404(Person, id=person_id)
    form = ProfilePictureForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            form = ProfilePictureForm(request.POST, request.FILES, instance=instance)
            form.save()
            return HttpResponseRedirect('profile')
    return render(request, 'AddProfilePicture.html', {'form': form, 'person_id': person_id})


@login_required
def leave_request(request, rent):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        # import pdb;pdb.set_trace()
        leave = LeaveRequest.objects.filter(Q(rent_id=rent), Q(request_accept__isnull=True))
        if not leave:
            form.save()
        return HttpResponseRedirect(reverse('rental_assets'))
    # property_obj = Property.objects.get(id=r)
    rent_obj = Rent.objects.get(id=rent)
    form = LeaveRequestForm(initial={'rent': rent, 'user': rent_obj.property.owner})
    return render(request, 'LeaveMessage.html', {'form': form})


@login_required
def leave_request_panel(request):
    leave_obj = LeaveRequest.objects.filter(user_id=request.user.id)
    context = {'leave_request': leave_obj}
    return render(request, 'LeaveRequestPanel.html', context)


@login_required
def leave_request_accept(request, request_id):
    leave_status = LeaveRequest.objects.get(id=request_id)
    property_obj = Property.objects.get(pk=leave_status.rent.property.id)
    rent_obj = Rent.objects.get(pk=leave_status.rent.id)
    leave_status.request_accept = True
    leave_status.save()
    property_obj.is_active = True
    property_obj.save()
    rent_obj.is_active = False
    rent_obj.save()
    return HttpResponseRedirect(reverse('owner_leave_panel'))


@login_required
def leave_request_cancel(request, request_id):
    leave_status = LeaveRequest.objects.get(id=request_id)
    leave_status.request_accept = False
    leave_status.save()
    return HttpResponseRedirect(reverse('owner_leave_panel'))


@login_required
def renter_message(request, rent):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # import pdb;pdb.set_trace()
            form.save()
            return HttpResponseRedirect(reverse('renter_message', args=[form['rent'].data]))
        else:
            return render(request, 'Message.html', {'form': form})
    rent_obj = Rent.objects.get(id=rent)
    messages = Message.objects.filter(rent_id=rent)
    if request.user.id is rent_obj.customer.id:
        receiver = rent_obj.property.owner
    else:
        receiver = rent_obj.customer
    form = MessageForm(initial={'rent': rent, 'user': request.user.id, 'receiver': receiver})
    return render(request, 'Message.html', {'form': form, 'messages': messages})


@login_required
def leave_status(request, rent):
    # import pdb;pdb.set_trace()
    leave = LeaveRequest.objects.filter(rent_id=rent)
    return render(request, 'LeaveStatus.html', {'leave': leave})


@login_required
# @permission_required()
def rent_history(request):

    rent_obj = Rent.objects.filter(property__owner_id=request.user.id, is_active__exact=False)
    return render(request, 'RentHistory.html', {'rent_obj': rent_obj})
