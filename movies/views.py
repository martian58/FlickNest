from django.shortcuts import render
from .models import Movie, WatchRoom, GroupMessage
from users.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def watch_movie(request, movie_id):
    # Retrieve the movie by ID or return a 404 if not found
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Render the watch.html template with the movie context
    return render(request, 'watch.html', {'movie': movie})



def movie_list(request):
    movies = Movie.objects.all()[:20]  # Initial load of 20 movies
    return render(request, 'movie_list.html', {'movies': movies})

def load_more_movies(request):
    page = request.GET.get('page', 1)
    paginator = Paginator(Movie.objects.all(), 20)
    movies = paginator.get_page(page)

    movie_data = [
        {
            'id': movie.id,
            'title': movie.title,
            'genre': movie.genre,
            'release_date': movie.release_date,
            'rating': movie.rating,
            'description': movie.description[:100],
            'poster_image': movie.poster_image.url if movie.poster_image else None,
            'is_starred': movie in request.user.profile.starred_movies.all(),
        }
        for movie in movies
    ]
    return JsonResponse({'movies': movie_data})



@login_required
def toggle_star(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    profile: Profile = request.user.profile

    if movie in profile.starred_movies.all():
        profile.starred_movies.remove(movie)
        is_starred = False
    else:
        profile.starred_movies.add(movie)
        is_starred = True

    return JsonResponse({'is_starred': is_starred})



@login_required
@csrf_exempt
def create_watch_room(request):
    if request.method == "GET":
        friends = request.user.profile.friends.all()
        movies = Movie.objects.all()
        return render(request, 'create_watch_room.html', {'movies': movies, 'friends': friends})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            room_name = data.get("room_name")
            users_in_room_ids = data.get("users_in_room_ids", [])
            movie_in_room_id = data.get("movie_in_room_id")

            if not room_name or not movie_in_room_id:
                return JsonResponse({"success": False, "error": "Room name and movie are required."})

            # Get the movie
            movie = Movie.objects.filter(id=movie_in_room_id).first()
            if not movie:
                return JsonResponse({"success": False, "error": "Selected movie does not exist."})

            # Create the watch room
            watch_room = WatchRoom.objects.create(room_name=room_name, movie_in_room=movie, creator=request.user)
            watch_room.add_user_to_room(request.user)

            # Add selected users to the room
            for user_id in users_in_room_ids:
                user = User.objects.filter(id=user_id).first()
                if user:
                    watch_room.add_user_to_room(user)

            return JsonResponse({"success": True})
        
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
@login_required
@csrf_exempt
def remove_watch_room(request, room_id):
    if request.method == "POST":
        try:
            # Retrieve the watch room or return a 404 if it doesn't exist
            watch_room = get_object_or_404(WatchRoom, id=room_id)

            # Check if the user is authorized to remove the room
            if request.user != watch_room.creator: 
                return JsonResponse({"success": False, "error": "You are not authorized to remove this room."}, status=403)

            # Delete the watch room
            watch_room.delete()

            # Respond with success
            return JsonResponse({"success": True, "message": "Watch room successfully removed."})
        
        except Exception as e:
            # Handle unexpected errors
            return JsonResponse({"success": False, "error": f"An error occurred: {str(e)}"}, status=500)
    else:
        # Handle non-POST requests
        return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)
    
@login_required
@csrf_exempt
def leave_watch_room(request, room_id):
    if request.method == "POST":
        try:
            watch_room = get_object_or_404(WatchRoom, id=room_id)

            if request.user not in watch_room.users_in_room.all():
                return JsonResponse({"success": False, "error": "You are not in this room."}, status=403)

            watch_room.users_in_room.remove(request.user)

            return JsonResponse({"success": True, "message": "You left the room successfully."})
        
        except Exception as e:
            return JsonResponse({"success": False, "error": f"An error occurred: {str(e)}"}, status=500)
    else:
        return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)
    
@login_required
def watch_rooms(request):
    user = request.user
    watch_rooms = WatchRoom.objects.filter(users_in_room=user)
    return render(request, 'watch_rooms.html', {'watch_rooms': watch_rooms})


@login_required
def watch_room(request, watch_room_id):
    watch_room = get_object_or_404(WatchRoom, id=watch_room_id)
    movie = watch_room.movie_in_room
    messages = GroupMessage.objects.filter(watch_room=watch_room)

    if request.method == 'POST':
        # Handling the new message post
        content = request.POST.get('content')
        if content:
            message = GroupMessage.objects.create(
                watch_room=watch_room,
                user=request.user,
                content=content
            )
            return JsonResponse({
                'username': request.user.username,
                'content': message.content
            })

    return render(request, 'watch_room.html', {
        'watch_room': watch_room,
        'movie': movie,
        'messages': messages
    })


# View to send a message in the group chat
@login_required
def send_group_message(request, watch_room_id):
    if request.method == "POST":
        data = json.loads(request.body)
        message_content = data.get('content')

        if message_content:
            watch_room = get_object_or_404(WatchRoom, id=watch_room_id)
            message = GroupMessage.objects.create(
                sender=request.user,
                watch_room=watch_room,
                content=message_content,
            )
            return JsonResponse({'success': True, 'message': message.content, 'timestamp': message.timestamp.strftime('%H:%M')})
        return JsonResponse({'success': False})

    return JsonResponse({'success': False})


# View to fetch messages from the group chat
@login_required
def fetch_group_messages(request, watch_room_id):
    watch_room = get_object_or_404(WatchRoom, id=watch_room_id)
    messages = GroupMessage.objects.filter(watch_room=watch_room).order_by('timestamp')
    
    # Prepare the data to return
    messages_data = [
        {
            "sender": message.sender.username,
            "sender_profile_pic": message.sender.profile.profile_pic.url,
            "content": message.content,
            "timestamp": message.timestamp.strftime("%H:%M")
        }
        for message in messages
    ]
    
    return JsonResponse({'success': True, 'messages': messages_data})