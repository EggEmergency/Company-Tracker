from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    website = models.CharField(max_length=100, null=True)
    careersPage = models.CharField(max_length=100, null=True)
    reviewCount = models.IntegerField(null=True)
    interviewCount = models.IntegerField(null=True)
    salaryCount = models.IntegerField(null=True)
    recommendedPercent = models.FloatField(null=True)
    rating = models.FloatField(null=True)
    location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name
