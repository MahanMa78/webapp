from django.shortcuts import redirect, render , get_object_or_404
from .models import *
from .forms import *
from bs4 import BeautifulSoup
import requests
from django.contrib import messages

def home_view(request):
    posts = Post.objects.all()
    return render(request,'posts/home.html' , {'posts' : posts})

def post_create_view(request):
    form = PostCreateForm()
    
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) #baraye in commit ro False mizarim ke migim felan save nakon ta etelaat dige ro ham begiri(add a few more things)
            
            website = requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.text, 'html.parser')
                            
            
            find_image = sourcecode.select('meta[content^="https://live.staticflicker.com/"]')
            if find_image:  
                image = find_image[0]['content']
                post.image = image
            else:
                print("No images found.")
            
            
            
            find_title = sourcecode.select('h1.photo-title')
            try:
                if title:
                    title = find_title[0].text.strip()
                    post.title = title
            except UnboundLocalError:
                print("No titles found.")
            
            
            find_artist = sourcecode.select('a.owner-name')
            
            artist = find_artist[0].text.strip()
            post.artist = artist
            
            
            post.save()
            return redirect('home')
            
    return render(request , 'posts/post_create.html' , {'form' : form})



def post_delete_view(request , pk):
    post = get_object_or_404(Post , id = pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request , 'Post deleted!')
        return redirect('home')
    
    return render(request , 'posts/post_delete.html' , {'post' : post} )


def post_edit_view(request , pk):
    post = get_object_or_404(Post , id = pk)  
    form = PostEditForm(instance=post)
    
    if request.method == "POST":
        form = PostEditForm(request.POST , instance=post)
        if form.is_valid():
            form.save()
            messages.success(request , "Post Updated!")
            return redirect('home')
    
    context = {
        'post' : post,
        'form' : form,
    }
    return render(request , 'posts/post_edit.html' , context)


def post_page_view(request , pk):
    post = get_object_or_404(Post , id = pk)
    return render(request , "posts/post_page.html" , {'post' : post})