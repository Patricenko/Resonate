from django.forms import ModelForm
from django import forms
from .models import *

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'message': forms.TextInput(attrs={
                'placeholder': 'Type your message here...', 
                'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'maxlength': 150,
                'autofocus': True
            })
        }
