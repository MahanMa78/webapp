from django.shortcuts import redirect, render , get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from bs4 import BeautifulSoup
import requests
from django.contrib import messages

def home_view(request , tag=None ):
    if tag:
        posts = Post.objects.filter(tags__slug = tag)
        tag = get_object_or_404(Tag , slug = tag )
    else:
        posts = Post.objects.all()
        
    categories = Tag.objects.all()
    
    context ={
        'posts' : posts ,
        'categories' : categories,
        'tag' : tag , 
    }
    
    return render(request,'posts/home.html' , context )


#in code pain ghalat nist ama bekhater osole DRY dorost nist pas baraye hamin be home_view on ro merge mikonim
# def category_view(request , tag):
#     posts = Post.objects.filter(tags__slug = tag)
#     return render(request,'posts/home.html' , {'posts' : posts})


@login_required
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
            
            post.author = request.user
            
            post.save()
            form.save_m2m() #bayad hatman in ro bezarim ta betone on ManyToMany haro save kone.
            
            return redirect('home')
            
    return render(request , 'posts/post_create.html' , {'form' : form})


@login_required
def post_delete_view(request , pk):
    post = get_object_or_404(Post , id = pk , author = request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request , 'Post deleted!')
        return redirect('home')
    
    return render(request , 'posts/post_delete.html' , {'post' : post} )


@login_required
def post_edit_view(request , pk):
    post = get_object_or_404(Post , id = pk , author = request.user)  
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
    
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()
    
    context = {
        'post' : post,
        'commentform' : commentform,
        'replyform': replyform,
    }
    
    return render(request , "posts/post_page.html" ,context)



@login_required
def comment_sent(request , pk):
    post = get_object_or_404(Post , id = pk)
    
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
            
    return redirect('post' , post.id)


@login_required
def reply_sent(request , pk):
    comment = get_object_or_404(Comment , id = pk)
    
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()
            
    return redirect('post' , comment.parent_post.id)


@login_required
def comment_delete_view(request , pk):
    post = get_object_or_404(Comment , id = pk , author = request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request , 'Comment deleted!')
        return redirect('post' , post.parent_post.id) #post dovomi baraye inke moshakhas kone id post chie ke baad az taghirat behesh bargarde
    
    return render(request , 'posts/comment_delete.html' , {'comment' : post} )