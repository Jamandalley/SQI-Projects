from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect
# Create your views here.

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url  = reverse_lazy("login")
    template_name = 'registration/signup.html'

@login_required
def my_account(request, userid):
    # Profile.objects.only("address", "email").filter(profile_id=userid) #selecting only this columns from the database
    # Profile.objects.exclude("address", "email").filter(profile_id=userid) #selecting all aside the ones selescted
    # Profile.objects.all() #selecting all the details in the database

    profile = Profile.objects.all().filter(user_id = userid)
    print(profile)
    return render(request=request, template_name='userapp/my_account.html', context={"userprofile":profile})

@login_required
def editAdmin_account(request, userid):
    user = get_object_or_404(User, id=userid)
    profile = get_object_or_404(Profile, user_id=userid)

    if request.method == "POST":
        user_form = User_form(request.POST, instance=user)
        admin_profile_form = AdminProfile_form(request.POST or None, request.FILES or None, instance=profile)

        if user_form.is_valid() and admin_profile_form.is_valid():
            user_form.save()
            admin_profile_form.save()
            
            if admin_profile_form.cleaned_data['staff']:
                user.is_staff = True
            else:
                user.is_staff = False

            
            user.save()
            profile.save()

            messages.success(request, 'Your profile was successfully updated!')
            return my_account(request, userid)
        else:
        #     print("invalid invalid")
            messages.error(request, 'Please correct the error below.')
            return HttpResponsePermanentRedirect(reverse('editAdmin_account', args=(userid,)))
    else:
        user_form = User_form(instance=user)
        admin_profile_form = AdminProfile_form(instance=profile)

        return render(request, 'userapp/edit_profile_form.html', {'user_form': user_form, 'admin_profile_form': admin_profile_form})
    

@login_required
def editUser_account(request, userid):
    user = get_object_or_404(User, id=userid)
    profile = get_object_or_404(Profile, user_id=userid)

    if request.method == "POST":
        user_form = User_form(request.POST, instance=user)
        user_profile_form = UserProfile_form(request.POST or None, request.FILES or None, instance=profile)

        if user_form.is_valid() and user_profile_form.is_valid():
            
            user_form.save()
            user_profile_form.save()
            

            messages.success(request, 'Your profile was successfully updated!')
            return my_account(request, userid)
        else:
        #     print("invalid invalid")
            messages.error(request, 'Please correct the error below.')
            return HttpResponsePermanentRedirect(reverse('editUser_account', args=(userid,)))
    else:
        user_form = User_form(instance=user)
        user_profile_form = UserProfile_form(instance=profile)

        return render(request, 'userapp/edit_profile_form.html', {'user_form': user_form, 'user_profile_form': user_profile_form})


@login_required
def deactivate_account(request, userid):
    user = User.objects.get(id = userid)
    print(user)
    
    if user.is_active:
        User.objects.filter(id = userid).update(is_active = False)
    else:
        User.objects.filter(id = userid).update(is_active = True)

    messages.success(request, 'Deactivation succesfull')
    return HttpResponsePermanentRedirect(reverse("my_account",args=(userid,)))

@login_required 
def allUser(request, user):
    if user == 'staff':
       all_user = Profile.objects.filter(staff=True)
    else:
       all_user = Profile.objects.filter(staff=False)

    return render(request,'userapp/display_user.html', {'allUsers':all_user, 'users':user})
