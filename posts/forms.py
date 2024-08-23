from django import forms
from django.forms import ModelForm
from .models import *

class PostCreateForm(ModelForm):
    
    class Meta:
        model = Post
        fields = '__all__'
        label ={
            'body' : 'Caption' , #be jay verbose_name ke dar dakhel Class model tarif mikardim,in kar ro ham mishe kard
        }
        widgets = { #in baraye inke dakhel template on jaygah 'body' ro tanzim konim
            'body' : forms.Textarea(attrs={ 'rows':3 , 'placeholder' : 'Add a caption ...' , 'class' : 'font1 text-4xl'}),
        }