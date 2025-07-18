from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class EcoCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class EcoAction(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(EcoCategory, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    points = models.IntegerField(default=10)
    last_approved_points = models.IntegerField(null=True, blank=True)
    date_logged = models.DateTimeField(auto_now_add=True)
    rejection_comment = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class Upload(models.Model):
    action = models.ForeignKey(EcoAction, on_delete=models.CASCADE)
    file = models.FileField(upload_to='proofs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload for {self.action.title} at {self.uploaded_at}"

class Reward(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    cost_in_points = models.IntegerField()
    image = models.ImageField(upload_to='rewards/', null=True, blank=True)

    def __str__(self):
        return self.name

class Redemption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
    redeemed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} redeemed {self.reward.name} on {self.redeemed_on}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Ensure user.profile always exists
def get_or_create_profile(self):
    profile, created = Profile.objects.get_or_create(user=self)
    return profile

User.add_to_class('profile', property(get_or_create_profile))

@receiver(pre_save, sender=EcoAction)
def update_points_on_status_change(sender, instance, **kwargs):
    if not instance._state.adding:
        previous = EcoAction.objects.get(pk=instance.pk)
        profile = instance.user.profile
        # If status is changing to Approved
        if previous.status != 'Approved' and instance.status == 'Approved':
            profile.points += instance.points
            profile.save()
        # If status is changing from Approved to something else
        elif previous.status == 'Approved' and instance.status != 'Approved':
            profile.points -= previous.points
            profile.save()
        # If status is staying Approved but points changed
        elif previous.status == 'Approved' and instance.status == 'Approved' and previous.points != instance.points:
            diff = instance.points - previous.points
            profile.points += diff
            profile.save()
