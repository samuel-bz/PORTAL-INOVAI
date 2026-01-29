from django.forms import forms
from .models import *

class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        exclude = ['author', 'publish_date']

class NewsBlockForm(forms.ModelForm):
    class Meta:
        model = NewsBlock
        exclude = ['related_post', 'order']

class BlockImageForm(forms.ModelForm):
    class Meta:
        model = BlockImage
        exclude = ['block']