from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('register/', views.user_register, name="register"),
    path('profile/', views.profile_view, name="profile"),
    path('profile/<int:user_id>/', views.profile_view_by_id, name="profile_by_id"),
    path('find/', views.find_users, name="find-users"),
    path('search-users/', views.search_users, name='search_users'),
    path('add_friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('remove_friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('friends/<int:user_id>/', views.friend_list, name='friend_list'),
    path('chat/<int:recipient_id>', views.chat_view, name='chat_view'),
    path('send_message/<int:recipient_id>/', views.send_message, name='send_message'),
    path('fetch_messages/<int:recipient_id>/', views.fetch_messages, name='fetch_messages'),
]
