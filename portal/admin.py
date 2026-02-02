from django.contrib import admin
from .models import NewsPost, NewsBlock, BlockImage, Destaque

admin.site.register(NewsPost)
admin.site.register(NewsBlock)
admin.site.register(BlockImage)
admin.site.register(Destaque)

# Register your models here.
