from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    website = models.CharField(max_length=100, null=True)
    careersPage = models.CharField(max_length=100, null=True)
    reviewCount = models.IntegerField(null=True)
    interviewCount = models.IntegerField(null=True)
    salaryCount = models.IntegerField(null=True)
    recommendedPercent = models.FloatField(null=True)
    rating = models.FloatField(null=True)
    locations = models.ManyToManyField(Location, related_name='companies')

    def __str__(self):
        return self.name
