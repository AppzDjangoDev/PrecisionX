from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
	phone_number =models.CharField(max_length = 12,null=True)
	proofile_image = models.ImageField(upload_to = 'uploads/',null=True)
	country = models.CharField(max_length=250,null=True)
	status = models.IntegerField(default=0,verbose_name='status', null=True)
	role = models.CharField(max_length=250,null=True)

	REQUIRED_FIELDS = []
	def __str__(self):
       	 return self.username
