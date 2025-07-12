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
    user1_seen = models.BooleanField(default=False)  # Has user1 seen this match?
    user2_seen = models.BooleanField(default=False)  # Has user2 seen this match?

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Match between {self.user1.username} and {self.user2.username}"
    
    def is_new_for_user(self, user):
        """Check if this match is new for the given user"""
        if user == self.user1:
            return not self.user1_seen
        elif user == self.user2:
            return not self.user2_seen
        return False
    
    def mark_seen_by_user(self, user):
        """Mark this match as seen by the given user"""
        if user == self.user1:
            self.user1_seen = True
        elif user == self.user2:
            self.user2_seen = True
        self.save()


class Pass(models.Model):
    """Model to track when a user passes on another profile"""
    passer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_passes')
    passed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_passes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('passer', 'passed')  # Prevent duplicate passes

    def __str__(self):
        return f"{self.passer.username} passed on {self.passed.username}"
