from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile


class Like(models.Model):
    """Model to track when a user likes another profile"""
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_likes')
    liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('liker', 'liked')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.liker.username} likes {self.liked.username}"


class Match(models.Model):
    """Model to track mutual matches between users"""
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Match between {self.user1.username} and {self.user2.username}"


class Pass(models.Model):
    """Model to track when a user passes on another profile"""
    passer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_passes')
    passed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_passes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('passer', 'passed')  # Prevent duplicate passes

    def __str__(self):
        return f"{self.passer.username} passed on {self.passed.username}"
