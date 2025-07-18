from django.test import TestCase
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from .models import *
from .forms import ChatmessageCreateForm

app_name = 'rtchat'

@login_required
def chat_view(request, group_name='public2'):
    chat_group = get_object_or_404(ChatGroup, group_name=group_name)
    chat_messages = chat_group.chat_messages.all()
    form = ChatmessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            return HttpResponseForbidden("You are not allowed to access this chat.")
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if True:
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

    context = {
        "chat_messages": chat_messages,
        'form': form,
        "other_user": other_user,
        'group_name': group_name,
    }
    return render(request, 'chat.html', context)

@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')

    other_user = get_object_or_404(User, username=username)

    users = sorted([request.user.username, username])
    room_name = f"private_{users[0]}_{users[1]}"

    try:
        chatroom = ChatGroup.objects.get(
            group_name=room_name,
            is_private=True
        )
    except ChatGroup.DoesNotExist:
        chatroom = ChatGroup.objects.create(
            group_name=room_name,
            is_private=True
        )
        chatroom.members.add(request.user, other_user)

    return redirect('rtchat:chat', group_name=chatroom.group_name)
