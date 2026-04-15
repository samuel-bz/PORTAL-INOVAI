from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .utils import upload_image_path

BLOCK_TYPES = (
    ('paragraph', 'Parágrafo'),
    ('paragraph_with_image', 'Parágrafo com imagem'),
    ('subtitle', 'Subtítulo'),
    ('hr', 'Separador horizontal'),
    ('image', 'Imagem'),
    ('title', 'Título'),
    ('carousel', 'Carrossel'),
    ('youtube', 'Vídeo YouTube'),
)

PORTAIS = (
    ('portal_inovai', 'Portal Inovaí'),
    ('portal_mulheres_ciencia', 'Portal Meninas e Mulheres na Ciência'),
)

# Modelo de noticias
class NewsPost(models.Model):
    title = models.CharField("Titulo", max_length=127, blank=False, null=False)
    description = models.CharField("Descrição", max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='news_post', null=True, blank=True)
    thumbnail = models.ImageField("Thumbnail", upload_to='news/', null=True, blank=True)
    publish_date = models.DateTimeField("Data de publicação", auto_now_add=True)
    tags = models.CharField("Tags", max_length=255, null=True, blank=True)
    active = models.BooleanField("Ativa", default=True)
    draft = models.BooleanField("Rascunho", default=False)
    portal = models.CharField("Portal", max_length=31, choices=PORTAIS, blank=False, null=False)

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ('-publish_date',)
    
    def formatted_publish_date(self) -> str:
        '''
        Returns the saved publish_date as a string in the format 'dd/mm/yy' where yy is the last two digits of the year.
        '''
        last_digits_of_year : str = str(self.publish_date.year)[-2:]
        return f"{self.publish_date.day:02}/{self.publish_date.month:02}/{last_digits_of_year}"

    def __str__(self) -> str:
        return f"{self.formatted_publish_date()} - {self.title}"

class NewsBlock(models.Model):
    block_type = models.CharField("Tipo", max_length=31, choices=BLOCK_TYPES)
    content = models.TextField("Conteúdo", blank=True)
    order = models.PositiveIntegerField("Ordem", default=0)
    related_post = models.ForeignKey("NewsPost", on_delete=models.CASCADE, related_name='blocks')

    class Meta:
        verbose_name = "Bloco de conteúdo"
        verbose_name_plural = "Blocos de conteúdo"
        ordering = ('related_post', 'order')

    def __str__(self):
        titulo_noticia = str(self.related_post)[:20].strip()
        return f"Notícia {titulo_noticia} | ({self.order:02d}).{self.get_block_type_display()}"
        # Exemplo:  Notícia 31/12/26 - Abertura | (01).Parágrafo
        #           Notícia 31/12/26 - Abertura | (02).Imagem

    def youtube_embed_src(self):
        """Para blocos YouTube, retorna a URL de embed no domínio youtube-nocookie.com (evita Erro 153)."""
        if self.block_type != 'youtube' or not self.content:
            return ''
        return self.content.replace('youtube.com/embed', 'youtube-nocookie.com/embed').replace('www.youtube.com/embed', 'www.youtube-nocookie.com/embed')

class BlockImage(models.Model):
    image = models.ImageField("Imagem", upload_to='news/blocks/')
    block = models.ForeignKey("NewsBlock", on_delete=models.CASCADE, related_name="image")
    captions = models.CharField("Legenda", max_length=127, null=True, blank=True, default="")
    alt_text = models.CharField("Texto acessibilidade", max_length=255, null=True, blank=True, default="")
    credits = models.CharField("Fotógrafo/Créditos", max_length=63, null=True, blank=True, default="")

    def __str__(self):
        return f"(Imagem) - {self.captions}"

class Destaque(models.Model):
    title = models.CharField("Título", max_length=127)
    image = models.ImageField("Imagem", upload_to="destaques")
    description = models.CharField("Descrição", max_length=255, null=True, blank=True)
    portal = models.CharField("Portal", max_length=31, choices=PORTAIS, default="portal_inovai")
    points_to_noticia = models.BooleanField("Aponta para notícia", default=False)
    related_post = models.ForeignKey("NewsPost", on_delete=models.CASCADE, related_name='destaques', null=True, blank=True)
    link_url = models.URLField("URL de destino", max_length=255, null=True, blank=True)
    button_color = models.CharField("Cor do botão", max_length=15, validators=[RegexValidator(regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', message="Cor inválida. Use formato hexadecimal (ex: #FFFFFF ou #FFF).")], default="#0d6efd")
    button_text = models.CharField("Texto do botão", max_length=127, default="Saiba mais")
    created_at = models.DateTimeField("Criado em:", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em:", auto_now=True)

    class Meta:
        verbose_name = "Destaque"
        verbose_name_plural = "Destaques"
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.get_portal_display()} --- {self.title} - {self.created_at.strftime('%d/%m/%Y %H:%M:%S')}"
    
    
class Attachment(models.Model):
    attachments = models.FileField("Arquivo", upload_to= 'attachments/')
    block = models.ForeignKey("NewsBlock", on_delete=models.CASCADE, related_name="attachments")
    captions = models.CharField("Legenda", max_length=127, null=True, blank=True, default="")
    alt_text = models.CharField("Texto acessibilidade", max_length=255, null=True, blank=True, default="")
    created_at = models.DateTimeField("Criado em:", auto_now_add=True)

    def __str__(self):
        return f"(arquivo) - {self.attachments}- {self.captions}"


