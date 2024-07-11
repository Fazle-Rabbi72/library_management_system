from django.db import models
from categories.models import Categories
from django.contrib.auth.models import User
# Create your models here.
class Books(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=500)
    price=models.IntegerField()
    image=models.ImageField(upload_to='book/media/uploads/',blank=True,null=True)
    categories=models.ForeignKey(Categories,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.title
    
class Review(models.Model):
    books=models.ForeignKey(Books,on_delete=models.CASCADE,related_name='reviews')
    name=models.CharField(max_length=30)
    body=models.TextField()     
    created_on=models.DateTimeField(auto_now_add=True)#live time

    def __str__(self):
        return f'Commented by {self.name}'