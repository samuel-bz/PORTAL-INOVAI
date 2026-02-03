from django.contrib import admin
from .models import *

# Register your models here.
class NewsPostAdmin(admin.ModelAdmin):
    class Meta:
        model = NewsPost

class NewsBlockAdmin(admin.ModelAdmin):
    class Meta:
        model = NewsBlock

class BlockImageAdmin(admin.ModelAdmin):
    class Meta:
        model = BlockImage

admin.site.register(NewsPost, NewsPostAdmin)
admin.site.register(NewsBlock, NewsBlockAdmin)
admin.site.register(BlockImage, BlockImageAdmin)