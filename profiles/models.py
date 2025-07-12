from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    PREFERED_GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('B', 'Both'),
        ('O', 'Other'),
    ]

    def contact_default():
        return {"email": "to1@example.com"}
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    height = models.PositiveIntegerField(help_text="Height in cm")
    interests = models.CharField(max_length=255, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    audio_bio = models.FileField(upload_to='media/audio_player/', default='media/IMG_2466.JPG')
    profile_photo = models.ImageField(upload_to='profile_photos/', default='media/IMG_2466.JPG')
    social_links = models.JSONField(default=contact_default, blank=True)  # Store social links as a JSON object
    is_public = models.BooleanField(default=True)  # Profile visibility
    preferred_gender = models.CharField(max_length=1, choices=PREFERED_GENDER_CHOICES, default='O')
    preferred_age_min = models.PositiveIntegerField(default=18)
    preferred_age_max = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"