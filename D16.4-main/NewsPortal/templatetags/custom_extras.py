from datetime import datetime

from django import template

from NewsPortal.templatetags.custom_filters import stop_words

register = template.Library()


@register.filter
def hide_forbidden(value):
    words = value.split()
    result = []
    for word in words:
        if word in stop_words:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)