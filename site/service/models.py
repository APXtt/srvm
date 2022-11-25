from django.db import models


class product(models.Model):
    name = models.CharField(max_length=200)
    img_url = models.TextField()
    create_date = models.DateTimeField()
    return_date = models.DateTimeField()
    rental_cost = models.IntegerField()


class user(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.IntegerField()
    point = models.IntegerField()
