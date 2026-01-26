from django.db import models

# Create your models here.

# Modelo de noticias
class Noticias(models.Model):
    image_Banner = models.ImageField(("Imagem de apresentação"), upload_to=None, blank=False, null=False)
    image_content = models.ImageField(("Imagem de conteudo"), upload_to=None, blank=True, null=True)
    title = models.CharField(("Titulo"), max_length=100, blank=False, null=False)
    subtitle = models.CharField(("Subtitulo"), max_length=100, blank=False, null=False)
    content = models.TextField(("Conteudo"), blank=False, null=False)
    date_publish = models.DateField(("Data de publicação"), blank=False, null=False)
    author = models.CharField(("Autor"), max_length=100, blank=False, null=False)

    def __str__(self):
        return self.title