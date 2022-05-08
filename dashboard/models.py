from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    Title = models.CharField(max_length=200)
    Description = models.TextField()
    def __str__(self):
        return self.Title

    class Meta:
        verbose_name="Notes"
        verbose_name_plural="Notes"

# By default, Django adds a 's' to a table name in the admin page.
# So there is a way in Django, you can explicitly declare what
# the singular form of the database objects should be and what the
# plural form of the database objects should be. And this can be done
# by using verbose_name and verbose_name_plural attributes.

# So, in the code below, we explicitly declare the singular form of each of the objects
# of the Child database table to be 'Child' and the plural form of the objects to be 'Children'.

class HomeWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    due = models.DateTimeField()
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.subject

    class Meta:
        verbose_name="HomeWork"
        verbose_name_plural="HomeWork"

class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name="ToDo"
        verbose_name_plural="ToDo"





