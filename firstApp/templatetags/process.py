from django import template

register = template.Library()


@register.filter
def str(value):
    """Removes all values of arg from the given string"""
    return str(value)



@register.simple_tag
def aggregate(p1,p2,p3):

    return (p1+p2+p3).upper()



