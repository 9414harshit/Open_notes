from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
<<<<<<< HEAD
from taggit.managers import TaggableManager

=======
>>>>>>> e99d61e90a78438ba3b3786b93a5b35b2ee8b8c2

# Create your models here.
class notes(models.Model):
	title  = models.CharField(max_length=50)
	date = models.DateTimeField(default = datetime.now)
	write = models.TextField()
<<<<<<< HEAD
	privacy= models.BooleanField(default=False)
	user = models.ManyToManyField(User)
=======
	image = models.ImageField(upload_to = "img/",blank=True)
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "notes")
>>>>>>> e99d61e90a78438ba3b3786b93a5b35b2ee8b8c2

	def __str__(self):
		return self.title

class group(models.Model):
	admin= models.ForeignKey(User, on_delete=models.CASCADE, related_name = "group")
	note=models.ForeignKey(notes,on_delete=models.CASCADE)
	make=models.CharField(max_length=50)

class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('notes', on_delete=models.CASCADE)