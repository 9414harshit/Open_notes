from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class notes(models.Model):
	title  = models.CharField(max_length=50)
	date = models.DateTimeField(default = datetime.now)
	write = models.TextField()
	image = models.ImageField(upload_to = "img/",blank=True)
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "notes")

	def __str__(self):
		return self.title

