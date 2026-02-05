from django import template

register = template.Library()


@register.filter
def youtube_nocookie(url):
    """Converte URL de embed do YouTube para o domínio youtube-nocookie.com (reduz Erro 153)."""
    if not url or not isinstance(url, str):
        return url
    return url.replace("youtube.com/embed", "youtube-nocookie.com/embed")

@register.filter(name='split')
def split(value):
    """
    Returns the value turned into a list.
    """
    
    return value.split(',')