from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from datetime import date
from django.utils import timezone

# Create your models here.

class Intern(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=150)
    preReq = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    place = models.CharField(max_length=100)
    eligibility = models.CharField(max_length=50)
    stiphend = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    dateAdded = models.DateField(auto_now_add=True)
    deadLine = models.CharField(max_length=50)
    duration = models.CharField(max_length=30)
    studentsEnrolled= models.CharField(max_length=200,default='')
    studentsApproved= models.CharField(max_length=200,default='')


    def __str__(self):
        return str(self.title)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    location = models.CharField(max_length=100)
    profilePhoto=models.FileField(upload_to='images/', null=True, verbose_name="")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()