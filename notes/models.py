from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


# Create your models here.
class notes(models.Model):
	title  = models.CharField(max_length=50)
	date = models.DateTimeField(default = datetime.now)
	write = models.TextField()
	privacy= models.BooleanField(default=False)
	user = models.ManyToManyField(User)
	creator = models.CharField(max_length=50)
	last= models.CharField(max_length=50)
	last_date = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.title

class group(models.Model):
	admin= models.ForeignKey(User, on_delete=models.CASCADE, related_name = "group")
	note=models.ForeignKey(notes,on_delete=models.CASCADE)
	make=models.CharField(max_length=50)

	def __str__(self):
		return self.make

class Comment(models.Model):
    author = models.CharField(max_length=150)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('notes', on_delete=models.CASCADE)