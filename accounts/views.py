from django.shortcuts import render , redirect
from django.contrib import messages
from .forms import RegistrationForm
from .models import Account


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name   = form.cleaned_data['first_name']
            last_name    = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email        = form.cleaned_data['email']
            password     = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name = first_name  , last_name = last_name , username = username , email = email , password = password )
            user.phone_number = phone_number
            user.save()
            
            messages.success(request, "Account created successfully!")
            return redirect("login_user")
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register_form.html' , {'form' : form})


def login_user(request):
    return render(request , 'accounts/login_form.html')


def logout_user(request):
    pass

