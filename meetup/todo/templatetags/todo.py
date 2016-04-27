from django import template

register = template.Library()


@register.filter
def possessive(val):
    if not val:
        return val
    end = "'" if val.endswith('s') else "'s"
    return '{}{}'.format(val, end)
