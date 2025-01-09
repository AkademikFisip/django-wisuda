from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Menambahkan class CSS ke elemen field form"""
    return field.as_widget(attrs={"class": css_class})
