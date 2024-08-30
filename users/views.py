from django.shortcuts import get_object_or_404, render , redirect
from .models import Profile 
from django.contrib.auth.models import User
from .forms import *

def profile_view(request , username=None):
    if username:
        profile = get_object_or_404(User , username=username).profile
    else:
        profile = request.user.profile
    return render(request , 'users/profile.html' , {'profile' : profile})

def profile_edit_view(request):
    form = ProfileForm(instance= request.user.profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST , request.FILES ,instance= request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    
    return render(request , 'users/profile_edit.html' , {'form' : form})
