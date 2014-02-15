from django import template

register = template.Library()

@register.filter(name='joinby')
def joinby(value, arg):
    return arg.join(value)