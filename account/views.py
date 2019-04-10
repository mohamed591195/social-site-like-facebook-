from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from django.contrib import messages
from django.views.generic import TemplateView
from .models import Profile
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage 
from django.http import HttpResponse


def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            #instantiate the user from the form ___ to make active false
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            #get the current site for sending it with the email confirmation #
            current_site = get_current_site(request)
            ##the messgae template
            message = render_to_string('account/acc_activate_email.html',
                                        {'user': new_user, 
                                         'domain': current_site.domain,
                                         'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                                         'token': account_activation_token.make_token(new_user)})
            # get some information from the form 
            cd = form.cleaned_data
            email = cd['email']
            ##writing the mail
            final_email = EmailMessage(subject='Activate your account', body=message, to=[email])
            #send it
            final_email.send()
            return HttpResponse('please confirm your email by clicking the link we have sent to you')
            username = cd['username']
            password = cd['password2']
            user = authenticate(request , username=username, password=password)
            login(request, user)
            messages.success(request, 'you have registered and logged in successfully {}'.format(user.get_full_name()))
            return redirect('account:dash_url')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form, 'title': 'register', 'source': 'register'})

class DashView(TemplateView):
    template_name = 'account/dash.html'
    extra_context = {'source': 'dash'}

# def Edit(request):
#     if request.method == 'POST':
