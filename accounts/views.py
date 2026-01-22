from django.shortcuts import render , redirect , HttpResponse , get_object_or_404
from django.contrib import messages
from django.contrib.auth import login , logout , authenticate
from .forms import RegistrationForm
from .models import Account , UserProfile
from django.contrib.auth.decorators import login_required
from carts.models import CartItem , Cart
from carts.views import _cart_id
from orders.models import Order , OrderProduct

# email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

#forms
from .forms import UserForm, UserProfileForm



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
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Merge guest cart with logged-in user's cart
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item = CartItem.objects.filter(cart=cart)

                # Getting the product variations by cart id
                product_variation = []
                for item in cart_item:
                    variation = item.variations.all()
                    product_variation.append(list(variation))

                # Get the cart items from the user to access his product variations
                cart_item = CartItem.objects.filter(user=user)
                ex_var_list = []
                id = []
                for item in cart_item:
                    existing_variation = item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)

                # product_variation = [1, 2, 3, 4, 6]
                # ex_var_list = [4, 6, 3, 5]

                for pr in product_variation:
                    if pr in ex_var_list:
                        index = ex_var_list.index(pr)
                        item_id = id[index]
                        item = CartItem.objects.get(id=item_id)
                        item.quantity += 1
                        item.user = user
                        item.save()
                    else:
                        cart_item = CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user = user
                            item.save()
                
            except Cart.DoesNotExist:
                pass  # No guest cart → ignore

            login(request, user)
            
            # messages.success(request, 'You are now logged in.')
            # url = request.META.get('HTTP_REFERER')

            # try: 
            #     query = requests.utils.urlparse(url).query
            #     # next=/cart/checkout/
            #     params = dict(x.split('=') for x in query.split('&'))
            #     if 'next' in params:
            #         nextPage = params['next']
            #         return redirect(nextPage)
            # except:
            #     return redirect("dashboard")
            
            messages.success(request, "Login successful.")
            return redirect("home")

        messages.error(request, "Invalid email or password.")
        return redirect("login_user")

    return render(request, "accounts/login_form.html")




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
    

@login_required(login_url='login_user')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id = request.user.id , is_ordered = True)
    orders_count = orders.count()

    userprofile = UserProfile.objects.get_or_create(user_id = request.user.id)
    context = {
        'orders_count' : orders_count,
        'userprofile': userprofile,
    }
    return render(request , 'accounts/dashboard.html', context)

@login_required(login_url='login_user')
def dashboard(request):
    orders = Order.objects.filter(
        user_id=request.user.id,
        is_ordered=True
    ).order_by('-created_at')

    orders_count = orders.count()

    userprofile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)




@login_required(login_url='login_user')
def my_orders(request):
    orders = Order.objects.filter(user = request.user , is_ordered = True).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request , 'accounts/my_orders.html', context )



@login_required(login_url='login_user')
def edit_profile(request):
    userprofile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit_profile.html', context)



@login_required(login_url='login_user')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_new_password')

        user = Account.objects.get(username__exact = request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request , 'Your password has been updated')
                return redirect('change_password')
            
            else:
                messages.error(request, 'Current_password is wrong!')

        else:
            messages.warning(request , 'Passwords does not match!')
    return render(request, 'accounts/change_password.html')



@login_required(login_url='login_user')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number = order_id)
    order = Order.objects.get(order_number = order_id )

    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail' : order_detail,
        'order' : order,
        'subtotal': subtotal,
    }

    return render(request , 'accounts/order_detail.html' , context)