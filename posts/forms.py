from django import forms
from django.forms import ModelForm
from .models import *

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'image' , 'body' , 'tags']
        label ={
            'body' : 'Caption' , #be jay verbose_name ke dar dakhel Class model tarif mikardim,in kar ro ham mishe kard
            'tags' : "Category",
        }
        widgets = { #in baraye inke dakhel template on jaygah 'body' ro tanzim konim
            'body' : forms.Textarea(attrs={ 'rows':3 , 'placeholder' : 'Add a caption ...' , 'class' : 'font1 text-4xl'}),
            'url' : forms.Textarea(attrs={'placeholder' : 'Add URL ...' }),
            'tags': forms.CheckboxSelectMultiple(),
        }
        

class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title' , 'body' , 'tags']
        labels = {
            'body' : '',
            'tags' : "Category",
        }
        widgets ={
            'body' : forms.Textarea(attrs={ 'rows':3 ,'class' : 'font1 text-4xl'}),
            'tags': forms.CheckboxSelectMultiple(),
        }
        

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets ={
            'body': forms.TextInput(attrs={'placeholder':"Add comment ..."})
        }
        label = {
            'body': '',
        }
        

class ReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets ={
            'body': forms.TextInput(attrs={'placeholder':"Add Reply ..." , 'class' :"!text-sm"})
        }
        label = {
            'body': '',
        }