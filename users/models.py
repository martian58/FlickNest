from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends_of', blank=True)
    starred_movies = models.ManyToManyField(Movie, related_name='starred_by', blank=True)
    watched_movies = models.ManyToManyField(Movie, related_name='watched_by', blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True,default='default/female-default-profile.webp')

    def __str__(self):
        return self.user.username

    def get_friend_count(self):
        return self.friends.count()
    
    def add_starred_movie(self, movie):
        """Add a movie to starred movies if not already starred."""
        if not self.starred_movies.filter(id=movie.id).exists():
            self.starred_movies.add(movie)

    def remove_starred_movie(self, movie):
        """Remove a movie from starred movies if it exists."""
        if self.starred_movies.filter(id=movie.id).exists():
            self.starred_movies.remove(movie)

    def add_watched_movie(self, movie):
        """Add a movie to watched movies if not already watched."""
        if not self.watched_movies.filter(id=movie.id).exists():
            self.watched_movies.add(movie)

    def remove_watched_movie(self, movie):
        """Remove a movie from watched movies if it exists."""
        if self.watched_movies.filter(id=movie.id).exists():
            self.watched_movies.remove(movie)

    def get_starred_movie_count(self):
        return self.starred_movies.count()

    def get_watched_movie_count(self):
        return self.watched_movies.count()

# FriendRequest model
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"

# Signal receiver to create a Profile instance when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Optionally, save the Profile whenever the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}: {self.content[:20]}"

    class Meta:
        ordering = ['timestamp']

    # Method to mark a message as read
    def mark_as_read(self):
        self.is_read = True
        self.save()

    # Method to get all messages between two users
    @staticmethod
    def get_conversation(user1, user2):
        return Message.objects.filter(
            (models.Q(sender=user1) & models.Q(recipient=user2)) |
            (models.Q(sender=user2) & models.Q(recipient=user1))
        ).order_by('timestamp')

    # Method to get unread message count for a user
    @staticmethod
    def get_unread_count(user):
        return Message.objects.filter(recipient=user, is_read=False).count()



