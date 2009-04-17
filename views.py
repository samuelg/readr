from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext

def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('pub_latest'))

    form = LoginForm(request.POST or None)
    
    if request.POST and form.is_valid():
        cleaned_data = form.cleaned_data
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')
        user = authenticate(username=user_id, password=password)
        login(request, user)

        return HttpResponseRedirect(reverse('pub_latest'))

    return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))

def logout_user(request):
    if request.user.is_authenticated():
        logout(request)

    return HttpResponseRedirect(reverse('login'))
