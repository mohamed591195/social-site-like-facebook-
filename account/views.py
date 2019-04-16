from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, ProfileEditForm, UserEditForm
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from .models import Profile, Contact
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage 
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from common.decorators import is_ajax
from posts.models import Post



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
            
           
            
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form, 'title': 'register', 'source': 'register'})

class DashView(TemplateView):
    template_name = 'account/dash.html'
    extra_context = {'source': 'dash'}

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'you have registered and confirmed your email successfully {}'.format(user.get_full_name()))
        return redirect('account:dash_url')
    else:
        return HttpResponse('activation link is invalid')

@login_required
def EditInfo(request, username):
    user = get_object_or_404(User, username=username)
    if request.user == user:
        if request.method == 'POST':
            pro_form = ProfileEditForm(data=request.POST, files=request.FILES, instance=user.profile)
            user_form = UserEditForm(data=request.POST, instance=user)
            if pro_form.is_valid() and user_form.is_valid():
                pro_form.save()
                user_form.save()
                messages.success(request, 'your account have been updated successfully {}'.format(user.get_full_name()))
        else:
            pro_form = ProfileEditForm(instance=user.profile)
            user_form = UserEditForm(instance=user)
        return render(request, 'account/Eprofile.html', {'user_form': user_form, 'pro_form': pro_form, 'source': 'edit_profile'})
    else:
        return HttpResponse('it\'s forbidden , you are not allowed to get this page')


class ListProfilesView(ListView):
    template_name = 'account/profiles_list.html'
    model = Profile
    context_object_name = 'profiles'

@login_required
@require_POST
@is_ajax
def follow_user(request):
    user_id = request.POST.get('id')
    user = get_object_or_404(User, id=user_id)
    action = ''
    if Contact.objects.filter(user_to=user, user_from=request.user).exists():
        Contact.objects.filter(user_to=user, user_from=request.user).delete()
        action = 'follow'
    else:
        Contact.objects.get_or_create(user_to=user, user_from=request.user)
        action = 'unfollow'
    return JsonResponse({'action': action})



def ProfileDetail(request, id):

    posts = Post.objects.filter(profile__id=id)
    profile = Profile.objects.get(id=id)
    return render(request, 'account/user_post.html', {'posts': posts, 'profile': profile})
    