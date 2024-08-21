from django.shortcuts import render

def home_view(request):
    title = 'Welcome to Django'
    return render(request,'index.html',{'title' : title})