from django.db import models
from django.contrib.auth.models import User


class account(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_id = models.CharField(max_length=40)
    username = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class phone_number(models.Model):

    number = models.CharField(max_length=40)
    account = models.ForeignKey(account, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.username

