from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'  # alebo vymenuj konkrétne polia, ak chceš
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Vlastné úpravy vzhľadu a atribútov polí
        self.fields['location'].widget.attrs.update({
            'id': 'id_location',  # Dôležité pre Google Autocomplete
            'class': 'form-control',
            'placeholder': 'Zadaj adresu',
            'autocomplete': 'off'
        })

        # Globálne nastavenie CSS pre všetky textové polia (okrem boolean a file fields)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ not in ['CheckboxInput', 'ClearableFileInput']:
                existing_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_class} form-control".strip()
