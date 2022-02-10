from django.template import Library

register = Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)
def add_paranthesis(context, context2):
    if context2:
        return f'({context2})'
    else:
        return ''