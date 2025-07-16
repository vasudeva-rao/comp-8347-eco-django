from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tip(models.Model):
    CATEGORY_CHOICES = [
        ('energy', 'Energy'),
        ('waste', 'Waste'),
        ('water', 'Water'),
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='tip_files/', blank=True, null=True)

    def __str__(self):
        return self.title

class UserUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
