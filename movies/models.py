from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Movie(models.Model):
    LANGUAGE_CHOICES = [
        ('EN', 'English'),
        ('TR', 'Turkish'),
        ('FR', 'French'),
        ('ES', 'Spanish'),
        ('DE', 'German'),
        ('RU', 'Russian'),
        ('JP', 'Japanese'),
        ('KR', 'Korean'),
        ('CN', 'Chinese'),
        ('IN', 'Hindi'),
    ]

    COUNTRY_CHOICES = [
        ('US', 'United States'),
        ('TR', 'Turkey'),
        ('FR', 'France'),
        ('ES', 'Spain'),
        ('DE', 'Germany'),
        ('RU', 'Russia'),
        ('JP', 'Japan'),
        ('KR', 'South Korea'),
        ('CN', 'China'),
        ('IN', 'India'),
    ]

    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    movie_link = models.URLField(blank=True, null=True, help_text="URL to load the movie from")
    movie_file = models.FileField(upload_to='movies/', blank=True, null=True, help_text="Upload the movie file here")
    description = models.TextField()
    release_date = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)  # e.g., 8.5
    poster_image = models.ImageField(upload_to='posters/', blank=True, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='EN')  # Language selection
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='US')  # Country selection
    duration = models.PositiveIntegerField(help_text="Duration in minutes", default=120)  # Duration of the movie
    director = models.CharField(max_length=100, blank=True, null=True)  # Director's name
    actors = models.TextField(blank=True, null=True, help_text="List of main actors")  # Main actors, stored as a comma-separated list
    trailer_url = models.URLField(blank=True, null=True)  # Link to trailer
    imdb_id = models.CharField(max_length=15, blank=True, null=True, help_text="IMDb ID if available")  # Optional IMDb ID
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class WatchRoom(models.Model):
    creator = models.ForeignKey(User, related_name='room_creator', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=200)
    users_in_room = models.ManyToManyField(User, related_name='users_in_room', blank=True)
    movie_in_room = models.ForeignKey(Movie, related_name='movie_in_room', on_delete=models.CASCADE)

    def __str__(self):
        return self.room_name
    
    def add_user_to_room(self, user):
        """Add a user to the room if not already in."""
        if not self.users_in_room.filter(id=user.id).exists():
            self.users_in_room.add(user)
    def get_creator(self):
        return self.creator

    def remove_user_from_room(self, user):
        """Remove a user from room if it is in."""
        if self.users_in_room.filter(id=user.id).exists():
            self.users_in_room.remove(user)

    def get_users_in_room_count(self):
        return self.users_in_room.count()
    
    def get_movie_name(self):
        return self.movie_in_room.title
    

class GroupMessage(models.Model):
    # Store each message in the group chat
    watch_room = models.ForeignKey(WatchRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.watch_room.room_name} at {self.timestamp}:  {self.content[:20]}"