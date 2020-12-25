from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/profile_pic_GeN3scU.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user} Profile'

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)
        print("profile created!")

#post_save.connect(create_profile, sender=User)

def update_profile(sender, instance, created, **kwargs):

    if created == False:
        instance.profile.save()
        print("profile updated!")

#post_save.connect(update_profile, sender=User)


class Computer(models.Model):
    computerName = models.CharField(max_length=100, null=True, blank=False)
    computerLocation = models.CharField(max_length=100, null=True, blank=False)
    dateAdded = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.computerName

class Customer(models.Model):
    customerName = models.CharField(max_length=100, null=True, blank=False)
    customerAddress = models.CharField(max_length=200, null=True, blank=True)
    customerPhoneNumber = models.CharField(max_length=10, null=True, blank=False)
    customerEmail = models.CharField(max_length=100, null=True, blank=True)
    computerChoice = models.CharField( max_length=100, null=True, blank=False)
    customerIdProof = models.CharField(max_length=50, null=True, blank=True)
    checkInTime = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    # ~~~~~~On checkout ~~~~~~~
    # price
    # Remarks


    def __str__(self):
        return self.customerName