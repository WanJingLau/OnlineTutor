from django.db import models

# Create your models here.

class student(models.Model):
    
	st_name =models.CharField(max_length=100)
	st_class=models.CharField(max_length=20)
	st_sex  =models.CharField(max_length=20)
	st_mark =models.IntegerField()