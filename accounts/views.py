from django.shortcuts import render , redirect , HttpResponse
from django.contrib import messages
from django.contrib.auth import login , logout , authenticate
from .forms import RegistrationForm
from .models import Account
from django.contrib.auth.decorators import login_required

# email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



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


            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {

            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            # 'protocol': 'https' if request.is_secure() else 'http',
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, "We send a verification code to your email!")
            return redirect("register_user")
        
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register_form.html' , {'form' : form})



def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request , email = email , password = password)
        
        if user is not None:
            login(request , user)
            messages.success(request , 'Login was successfully.')
            return redirect('dashboard')
        else:
            messages.error(request , 'Invalid email or password.')
            return redirect('login_user')
        
    return render(request , 'accounts/login_form.html')



@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    return redirect('home')



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. You can now login to your account.')
        return redirect('login_user')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('register_user')



@login_required(login_url='login_user')
def dashboard(request):
    return render(request , 'accounts/dashboard.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email',)
        if Account.objects.filter(email = email).exists():
            user = Account.objects.get(email__iexact = email)

            # Forgot password send code
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password.'
            message = render_to_string('accounts/reset_password_email.html', {

            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            # 'protocol': 'https' if request.is_secure() else 'http',
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request , 'Please Check Your Email To Reset Your Password!')

        else:
            messages.error(request, "Email Doesn't Exist!")
            return redirect('forgot_password')


    return render(request , 'accounts/forgot_password.html')



def reset_password_validate(request , uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request , 'Please Reset Your Email!')
        return redirect('reset_password')
    
    else:
        messages.error(request , 'This link expired!')
        return redirect('login')
    


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password' , )
        confirm_password = request.POST.get('confirm_password' , )

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk = uid)
            user.set_password(password)
            user.save()

            messages.success(request , 'Password Successfully Rested')
            return redirect('login_user')
        
        else:
            messages.error(request , 'Password Successfully Rested')
            return redirect('reset_password')
    else:
        return render(request , 'accounts/reset_password.html')