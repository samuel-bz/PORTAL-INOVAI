import re
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

# Padrão [texto](url) — aceita http/https ou âncora #
LINK_PATTERN = re.compile(
    r'\[([^\]]*)\]\((https?://[^\)]+|#[^\)]*)\)',
    re.IGNORECASE
)
# URL solta (http/https) para linkificar quando o autor não usa [texto](url)
RAW_URL_PATTERN = re.compile(r'https?://[^\s\)\]<>]+')


def _link_class():
    return 'text-brand-blue dark:text-blue-400 hover:underline'


@register.filter
def linkify_markdown(text):
    """
    Converte [texto](url) e URLs soltas (http/https) em hyperlinks <a href="...">.
    Escapa o resto do texto para evitar XSS.
    """
    if not text or not isinstance(text, str):
        return text
    # Coletar spans: (start, end, label ou None, url)
    spans = []
    for m in LINK_PATTERN.finditer(text):
        spans.append((m.start(), m.end(), m.group(1), m.group(2)))
    for m in RAW_URL_PATTERN.finditer(text):
        # Ignorar se estiver dentro de um [text](url) já capturado
        if any(s[0] <= m.start() < s[1] for s in spans):
            continue
        url = m.group(0)
        spans.append((m.start(), m.end(), None, url))
    spans.sort(key=lambda s: s[0])
    parts = []
    last_end = 0
    for start, end, label, url in spans:
        parts.append(escape(text[last_end:start]))
        display = escape(label) if label is not None else escape(url)
        parts.append(
            '<a href="%s" class="%s" rel="noopener noreferrer">%s</a>'
            % (escape(url), _link_class(), display)
        )
        last_end = end
    parts.append(escape(text[last_end:]))
    return mark_safe(''.join(parts))


@register.filter
def youtube_nocookie(url):
    """Converte URL de embed do YouTube para o domínio youtube-nocookie.com (reduz Erro 153)."""
    if not url or not isinstance(url, str):
        return url
    return url.replace("youtube.com/embed", "youtube-nocookie.com/embed")

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
