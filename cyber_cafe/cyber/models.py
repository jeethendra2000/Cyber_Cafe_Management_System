from django.db import models

# Create your models here.
class Computer(models.Model):
    computerName = models.CharField(max_length=100, null=True, blank=False)
    computerLocation = models.CharField(max_length=100, null=True, blank=False)
    # computerIdAddress = models.CharField(max_length=100)
    dateAdded = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    def __str__(self):
        return self.computerName

class Customer(models.Model):
    customerName = models.CharField(max_length=100, null=True, blank=False)
    customerAddress = models.CharField(max_length=200, null=True, blank=True)
    customerPhoneNumber = models.CharField(max_length=10, null=True, blank=False)
    customerEmail = models.CharField(max_length=100, null=True, blank=True)
    # computerChoice
    customerIdProof = models.CharField(max_length=50, null=True, blank=True)

    # ~~~~~~On checkout ~~~~~~~
    # price
    # Remarks


    def __str__(self):
        return self.customerName