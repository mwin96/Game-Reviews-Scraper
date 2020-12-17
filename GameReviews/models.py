from django.db import models

# Create your models here.
# models.py

class Reviews(models.Model):
    website = models.CharField(max_length=200, default="")

    link = models.CharField(max_length=2083, default="")

    title = models.CharField(max_length=200, default = "")

    developer = models.CharField(max_length=200, default = "")

    releaseDate = models.DateField(max_length=200)

    score = models.FloatField(max_length=200)
    
    steamReview = models.CharField(max_length=200, default = "")

    consoles = models.CharField(max_length=200)