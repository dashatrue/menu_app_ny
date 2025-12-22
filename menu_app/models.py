from django.db import models

# Create your models here.
class First(models.Model):
    name = models.CharField(max_length=50)
    png = models.ImageField(upload_to='First/')

class Salad(models.Model):
    name = models.CharField(max_length=50)
    png = models.ImageField(upload_to='Salad/')

class Appetizer(models.Model):
    name = models.CharField(max_length=50)
    png = models.ImageField(upload_to='Appetizers/')

class Dessert(models.Model):
    name = models.CharField(max_length=50)
    png = models.ImageField(upload_to='Dessert/')