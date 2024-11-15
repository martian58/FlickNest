from django.contrib import admin
from .models import Movie, WatchRoom, GroupMessage

# Register your models here.
# movies/admin.py

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date', 'rating')

@admin.register(WatchRoom)
class WatchRoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'movie_in_room')

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('watch_room', 'sender', 'content', 'timestamp')