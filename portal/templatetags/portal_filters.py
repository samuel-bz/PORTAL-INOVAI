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
@register.filter
def split_tags(tags_string):
    """Separa as tags, separadas por vírgula, em uma lista."""
    if not tags_string or not isinstance(tags_string, str):
        return []
    return [tag.strip() for tag in tags_string.split(',') if tag.strip()]

@register.filter
def split_lines(text):
    """Separa o texto em linhas."""
    if not text or not isinstance(text, str):
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]
