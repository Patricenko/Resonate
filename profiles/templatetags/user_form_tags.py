from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    if not isinstance(field, BoundField):
        # Už je to pravdepodobne SafeString alebo iný string, neaplikuj filter
        return field
    return field.as_widget(attrs={"class": css})
