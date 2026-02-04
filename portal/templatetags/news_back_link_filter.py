from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def news_back_link_filter(portal):
    match portal:
        case 'portal_inovai':
            return reverse('portal:index')
        case 'portal_mulheres_ciencia':
            return reverse('portal:mulheres')
        case _:
            return reverse('portal:index')
