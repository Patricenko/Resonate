from django.contrib import admin
from .models import Like, Match, Pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('liker', 'liked', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('liker__username', 'liked__username')
    ordering = ('-created_at',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user1__username', 'user2__username')
    ordering = ('-created_at',)


@admin.register(Pass)
class PassAdmin(admin.ModelAdmin):
    list_display = ('passer', 'passed', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('passer__username', 'passed__username')
    ordering = ('-created_at',)
