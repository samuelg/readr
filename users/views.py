from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from users.forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from datetime import datetime, timedelta

def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('pub_latest'))

    form = LoginForm(request.POST or None)
    
    if request.POST and form.is_valid():
        cleaned_data = form.cleaned_data
        user_id = cleaned_data['user_id']
        password = cleaned_data['password']
        remember = cleaned_data['remember']

        user = authenticate(username=user_id, password=password)
        login(request, user)
        if remember:
            # set session expiry to 2 weeks
            request.session.set_expiry(datetime.now() + timedelta(days=14))

        return HttpResponseRedirect(request.POST.get('next', reverse('pub_latest')))

    context = {'form': form}
    if 'next' in request.REQUEST:
        context['next'] = request.REQUEST['next']
    return render_to_response('users/login.html', context, context_instance=RequestContext(request))

def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
    
    # reset session expiry    
    request.session.set_expiry(0)

    return HttpResponseRedirect(reverse('pub_latest'))

def register_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('pub_latest'))

    form = RegisterForm(request.POST or None)
    
    if request.POST and form.is_valid():
        cleaned_data = form.cleaned_data
        user_id = cleaned_data['user_id']
        password = cleaned_data['password']
        email = cleaned_data['email']

        # create user
        user = User.objects.create_user(user_id, email, password)
        user.save()

        return HttpResponseRedirect(reverse('login'))

    context = {'form': form}
    return render_to_response('users/register.html', context, context_instance=RequestContext(request))
