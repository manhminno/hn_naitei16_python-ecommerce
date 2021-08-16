from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelform_factory
from django.shortcuts import redirect, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from .forms import SignUpForm


def index(request):
    return render(request, "index.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()           
            my_message = _('Successful registration, you can log in now.')
            messages.success(request, my_message)
            
            return redirect('login')
    else:
        form = SignUpForm()
    
    return render(request, 'shop/signup.html', {'form': form})

@login_required
def detail_profile(request):
    UserEditForm = modelform_factory(
        get_user_model(), 
        fields=('first_name', 'last_name', 'username', 'phone', 'address'), 
        help_texts = {'username': None}
    )
    form = UserEditForm(instance=request.user)
    if request.method == "POST":
        form = UserEditForm(instance=request.user, data=request.POST or None)
        if form.is_valid():
            form.save()
    return render(request, 'shop/detail-profile.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
