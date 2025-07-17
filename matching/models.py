from django.db import models
from django.contrib.auth.models import User
from profiles.models import Profile


class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_likes')
    liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('liker', 'liked')

    def __str__(self):
        return f"{self.liker.username} likes {self.liked.username}"


class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)
    user1_seen = models.BooleanField(default=False)
    user2_seen = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Match between {self.user1.username} and {self.user2.username}"
    
    def is_new_for_user(self, user):
        if user == self.user1:
            return not self.user1_seen
        elif user == self.user2:
            return not self.user2_seen
        return False
    
    def mark_seen_by_user(self, user):
        if user == self.user1:
            self.user1_seen = True
        elif user == self.user2:
            self.user2_seen = True
        self.save()


class Pass(models.Model):
    passer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_passes')
    passed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_passes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('passer', 'passed')

    def __str__(self):
        return f"{self.passer.username} passed on {self.passed.username}"
