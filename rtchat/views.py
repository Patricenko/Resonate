from django.test import TestCase
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import ChatmessageCreateForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
# Create your tests here.

app_name = 'rtchat'

def chat_view(request, group_name='public2'):
    chat_group = get_object_or_404(ChatGroup, group_name = group_name)
    chat_messages = chat_group.chat_messages.all()[:]
    form = ChatmessageCreateForm()
    print("Form is valid1")
    print(request.method)
    
    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break
    if request.htmx:
        print("Form is valid2")
        form = ChatmessageCreateForm(request.POST)
        if True:#form.is_valid:
            print("Form is valid3")
            message = form.save(commit=False)
            message.author = request.user
            message.chat_group = chat_group
            message.group_id = chat_group.id
            message.save()
            context = {
                'message': message,
                'user': request.user,
            }
            return render(request, 'chat_message.html', context)
    context = {"chat_messages": chat_messages, 'form': form,
               "other_user": other_user,
               'group_name': group_name,}
    return render(request, 'chat.html', context)

@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')
    
    other_user = get_object_or_404(User, username=username)
    
    # Generate a consistent room name for the two users
    users = sorted([request.user.username, username])
    room_name = f"private_{users[0]}_{users[1]}"
    
    # Try to find existing chatroom
    try:
        chatroom = ChatGroup.objects.get(
            group_name=room_name,
            is_private=True
        )
    except ChatGroup.DoesNotExist:
        # Create new chatroom
        chatroom = ChatGroup.objects.create(
            group_name=room_name,
            is_private=True
        )
        chatroom.members.add(request.user, other_user)
        
    return redirect('rtchat:chat', group_name=chatroom.group_name)