from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile
import mimetypes

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Profile
        fields = '__all__'  # alebo vymenuj konkrétne polia, ak chceš
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        # Extract user instance if provided
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # If we have a user instance, set the email field's initial value
        if self.user:
            self.fields['email'].initial = self.user.email

        # Vlastné úpravy vzhľadu a atribútov polí
        self.fields['location'].widget.attrs.update({
            'id': 'id_location',  # Dôležité pre Google Autocomplete
            'class': 'form-control',
            'placeholder': 'Zadaj adresu',
            'autocomplete': 'off'
        })

        # Add accept attributes for file fields
        self.fields['audio_bio'].widget.attrs.update({
            'accept': 'audio/*'
        })
        
        self.fields['profile_photo'].widget.attrs.update({
            'accept': 'image/*'
        })

        # Globálne nastavenie CSS pre všetky textové polia (okrem boolean a file fields)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ not in ['CheckboxInput', 'ClearableFileInput']:
                existing_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_class} form-control".strip()

    def clean_audio_bio(self):
        audio_file = self.cleaned_data.get('audio_bio')
        
        if audio_file:
            # Check file extension and MIME type
            file_name = audio_file.name.lower()
            allowed_extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac']
            
            if not any(file_name.endswith(ext) for ext in allowed_extensions):
                raise ValidationError(
                    f'Please upload a valid audio file. Supported formats: {", ".join(allowed_extensions)}'
                )
            
            # Check MIME type
            mime_type, _ = mimetypes.guess_type(audio_file.name)
            if mime_type and not mime_type.startswith('audio/'):
                raise ValidationError('Please upload a valid audio file.')
            
            # Check file size (limit to 10MB)
            if audio_file.size > 10 * 1024 * 1024:  # 10MB
                raise ValidationError('Audio file size must be less than 10MB.')
        
        return audio_file

    def clean_profile_photo(self):
        image_file = self.cleaned_data.get('profile_photo')
        
        if image_file:
            # Check file extension
            file_name = image_file.name.lower()
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
            
            if not any(file_name.endswith(ext) for ext in allowed_extensions):
                raise ValidationError(
                    f'Please upload a valid image file. Supported formats: {", ".join(allowed_extensions)}'
                )
            
            # Check MIME type
            mime_type, _ = mimetypes.guess_type(image_file.name)
            if mime_type and not mime_type.startswith('image/'):
                raise ValidationError('Please upload a valid image file.')
            
            # Check file size (limit to 5MB)
            if image_file.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('Image file size must be less than 5MB.')
        
        return image_file

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Check if email is already taken by another user
            if self.user:
                # Editing existing profile - exclude current user from check
                if User.objects.filter(email=email).exclude(id=self.user.id).exists():
                    raise ValidationError('This email address is already in use.')
            else:
                # Creating new profile
                if User.objects.filter(email=email).exists():
                    raise ValidationError('This email address is already in use.')
        return email
