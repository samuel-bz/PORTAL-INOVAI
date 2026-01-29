from django.db import models
from django.contrib.auth.models import User

BLOCK_TYPES = (
    ('paragraph', 'Parágrafo'),
    ('paragraph_with_image', 'Parágrafo com imagem'),
    ('subtitle', 'Subtítulo'),
    ('hr', 'Separador horizontal'),
    ('image', 'Imagem'),
)

# Modelo de noticias
class NewsPost(models.Model):
    title = models.CharField("Titulo", max_length=127)
    description = models.CharField("Descrição", max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='news_post', null=True, blank=True)
    thumbnail = models.ImageField("Thumbnail", upload_to=None, null=True, blank=True)
    publish_date = models.DateField("Data de publicação", auto_now_add=True)
    tags = models.CharField("Tags", max_length=255, null=True, blank=True)

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
    related_post = models.ForeignKey("NewsPost", on_delete=models.CASCADE, related_name='news_post')

    class Meta:
        verbose_name = "Bloco de conteúdo"
        verbose_name_plural = "Blocos de conteúdo"
        ordering = ('-related_post',)

    def __str__(self):
        titulo_noticia = self.related_post[:20].strip()
        return f"Notícia {titulo_noticia} | ({self.order:02d}).{self.get_block_type_display()}"
        # Exemplo:  Notícia 31/12/26 - Abertura | (01).Parágrafo
        #           Notícia 31/12/26 - Abertura | (02).Imagem

class BlockImage(models.Model):
    image = models.ImageField("Imagem", upload_to=None)
    block = models.ForeignKey("NewsBlock", on_delete=models.CASCADE, related_name="image")
    captions = models.CharField("Legenda", max_length=127, null=True, blank=True, default="")
    alt_text = models.CharField("Texto acessibilidade", max_length=255, null=True, blank=True, default="")
    credits = models.CharField("Fotógrafo/Créditos", max_length=63, null=True, blank=True, default="")

    def __str__(self):
        return f"(Imagem) - {self.captions}"