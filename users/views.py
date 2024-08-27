from django.shortcuts import render
from .models import Profile

def profile_view(request):
    profile = request.user.profile
    return render(request , 'users/profile.html' , {'profile' : profile})