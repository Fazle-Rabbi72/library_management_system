
from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE

# Create your models here.

class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='account',on_delete=models.CASCADE)
    account_no= models.IntegerField(unique=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=10,choices=GENDER_TYPE)
    initial_deposit_date = models.DateTimeField(auto_now_add=True, blank=True)
    balance = models.DecimalField(default=0, max_digits=12,decimal_places=2)
    def __str__(self):
        return str(self.account_no)
class Transaction(models.Model):
    account = models.ForeignKey(UserAccount, related_name = 'transactions', on_delete = models.CASCADE) # ekjon user er multiple transactions hote pare
    amount = models.DecimalField(decimal_places=2, max_digits = 12)        