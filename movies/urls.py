from django.urls import path
from . import views
urlpatterns = [
    path('', views.movie_list, name='movies'),
    path('watch/<int:movie_id>/', views.watch_movie, name="watch"),
    path('load_more/', views.load_more_movies, name='load_more_movies'),
    path('toggle_star/<int:movie_id>/', views.toggle_star, name='toggle_star'),
    path('create_watch_room/', views.create_watch_room, name='create_watch_room'),
    path('watch_rooms/', views.watch_rooms, name='watch_rooms'),
    path('watch_rooms/remove/<int:room_id>/', views.remove_watch_room, name='remove_watch_room'),
    path('watch_rooms/leave/<int:room_id>/', views.leave_watch_room, name='leave_watch_room'),
    path('watch_room/<int:watch_room_id>/', views.watch_room, name='watch_room'),
    path('send_watch_room_message/<int:watch_room_id>/', views.send_group_message, name='send_watch_room_message'),
    path('fetch_watch_room_messages/<int:watch_room_id>/', views.fetch_group_messages, name='fetch_watch_room_messages'),
]