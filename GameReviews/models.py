from django.db import models


# Create your models here.
# models.py

class Reviews(models.Model):
    website = models.CharField(max_length=64, default="")
    link = models.CharField(max_length=256, default="")
    title = models.CharField(max_length=64, default = "")
    developer = models.CharField(max_length=256, default = "")
    releaseDate = models.DateField(max_length=256, default = "")
    score = models.FloatField(max_length=64, default = 0)
    steamReview = models.CharField(max_length=256, default = "")
    consoles = models.CharField(max_length=256, default = "")