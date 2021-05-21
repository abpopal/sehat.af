from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from accounts.forms import RegistrationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import User
from mysite.models import Hospital, PUser

from django.http import HttpResponse

# Create your views here.
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user_bday = form.cleaned_data.get('birthdate')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            PUser.objects.create(username=request.user, birthdate=user_bday, name=form.cleaned_data.get('name'))
            return redirect('edit_profile')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'registration/register.html', context)




def delete_account_view(request):
    if request.method == 'GET':

        print("from dele account view: ")

        account = User.objects.get(username=request.user)
        account.delete()
        return redirect(reverse('home'))
    else:
        return render(request, 'home.html', {})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })