from django.http import Http404
from django.shortcuts import get_object_or_404, render , redirect
from django.urls import reverse
from .models import Profile 
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *

def profile_view(request , username=None):
    if username:
        profile = get_object_or_404(User , username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
    return render(request , 'users/profile.html' , {'profile' : profile})

@login_required
def profile_edit_view(request):
    form = ProfileForm(instance= request.user.profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST , request.FILES ,instance= request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    if request.path == reverse('profile-onboarding'):
        template = 'users/profile_onboarding.html'
    else:
        template = 'users/profile_edit.html' 
    
    return render(request , template , {'form' : form})


@login_required
def profile_delete_view(request):
    
    user = request.user
    
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request , "Account deleted  , what a pity")
        return redirect('home')
        
    return render(request , 'users/profile_delete.html')