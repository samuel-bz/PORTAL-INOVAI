from django.db import models

# Modelo de noticias
class Noticia(models.Model):
    image_banner = models.ImageField("Imagem de apresentação", upload_to=None)
    image_content = models.ImageField("Imagem de conteudo", upload_to=None, blank=True, null=True)
    title = models.CharField("Titulo", max_length=100)
    subtitle = models.CharField("Subtítulo", max_length=100)
    content = models.TextField("Conteudo")
    publish_date = models.DateField("Data de publicação")
    author = models.CharField("Autor", max_length=100)

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ('-publish_date')
        
    def __str__(self):
        return self.title
