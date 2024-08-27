from django.db import models
import uuid

class Post(models.Model):
    title = models.CharField(max_length=500)
    artist = models.CharField(max_length=500 , null= True)
    url = models.URLField( max_length=500 , null= True)
    image = models.URLField(max_length=500)
    body = models.TextField()
    tags = models.ManyToManyField('Tag')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100 , default=uuid.uuid4 , unique= True , primary_key= True , editable= False)
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-created']
        
        
        
class Tag(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='icons/' , null=True , blank=True)
    slug = models.SlugField(max_length=20 , unique=True)
    order = models.IntegerField(null=True)
        
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']