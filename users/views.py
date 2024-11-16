from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Profile, Message
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.serializers import serialize
from django.db.models import Q



# Create your views here


# signup page
@csrf_protect
def user_register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})

# login page
@csrf_protect
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('index')
            else:
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):

    user = request.user

    return render(request, 'profile.html', {"user": user})

@login_required
def profile_view_by_id(request, user_id):

    user = User.objects.get(id=user_id)

    return render(request, 'profile.html', {"user" : user})



@login_required
def add_friend(request, user_id):
    # Get the user to be added
    user_to_add = get_object_or_404(User, id=user_id)
    
    # Get the current user's profile
    profile = request.user.profile

    if user_to_add in profile.friends.all():
        return JsonResponse({'success': False, 'message': f"You are already friends with {user_to_add.username}."})
    else:
        profile.friends.add(user_to_add)
        user_to_add.profile.friends.add(request.user)
        return JsonResponse({'success': True, 'message': f"You are now friends with {user_to_add.username}."})
    
@login_required
def remove_friend(request, user_id):
    # Get the user to be added
    user_to_remove = get_object_or_404(User, id=user_id)
    
    # Get the current user's profile
    profile = request.user.profile

    if user_to_remove in profile.friends.all():
        profile.friends.remove(user_to_remove)
        user_to_remove.profile.friends.remove(request.user)
        return JsonResponse({'success': True, 'message': f"You removed {user_to_remove.username} from your friends."})
    else:
        return JsonResponse({'success': False, 'message': f"You are not friends with {user_to_remove.username}."})



@login_required
def find_users(request):
    return render(request, 'find-users.html', {})


@login_required
def search_users(request):
    if request.method == 'POST':
        search_term = request.POST.get('search-term', '').strip()
        users = (User.objects.filter(username__icontains=search_term) | User.objects.filter(email__icontains=search_term) |
                  User.objects.filter(first_name__icontains=search_term) | User.objects.filter(last_name__icontains=search_term))

        # Assuming User model has first_name, last_name, and id attributes
        user_list = [{"id": user.id, "first_name": user.first_name, "last_name": user.last_name} for user in users]

        if user_list:
            return JsonResponse({'users': user_list}, status=200)
        else:
            return JsonResponse({'error': 'No users found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def friend_list(request, user_id):
    if request.user == User.objects.get(id=user_id):
        profile = request.user.profile
        friends = profile.friends.all()
    else:
        profile = User.objects.get(id=user_id).profile
        friends = profile.friends.all()

    return render(request, 'friend_list.html', {'friends': friends})


@login_required
@require_POST
def send_message(request, recipient_id):
    data = json.loads(request.body)
    content = data.get("content", "").strip()
    
    if content:
        recipient = User.objects.get(id=recipient_id)
        Message.objects.create(sender=request.user, recipient=recipient, content=content)
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False})


@login_required
def chat_view(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    messages = Message.get_conversation(request.user, recipient)

    # Mark all unread messages from recipient as read
    for message in messages.filter(sender=recipient, is_read=False):
        message.mark_as_read()

    return render(request, 'chat.html', {
        'messages': messages,
        'recipient': recipient,
    })



@login_required
def fetch_messages(request, recipient_id):
    try:
        recipient = User.objects.get(id=recipient_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": "Recipient does not exist."})

    # Fetch the latest messages between the request.user and the recipient
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=request.user))
    ).order_by('timestamp')

    # Serialize messages
    messages_data = [
        {
            "sender": message.sender.username,
            "sender_profile_pic": message.sender.profile.profile_pic.url,
            "content": message.content,
            "timestamp": message.timestamp.strftime("%H:%M")
        }
        for message in messages
    ]

    return JsonResponse({"success": True, "messages": messages_data})
