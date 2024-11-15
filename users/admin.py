from django.contrib import admin
from .models import Profile, FriendRequest, Message
# Register your models here.


admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Message)