from django import forms
from .models import *

INPUT_CLASS = (
    "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 "
    "text-gray-900 dark:text-gray-100 px-4 py-2.5 focus:ring-2 focus:ring-blue-500 focus:border-transparent "
    "dark:focus:ring-blue-400 transition placeholder-gray-400 dark:placeholder-gray-500"
)
SELECT_CLASS = (
    "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 "
    "text-gray-900 dark:text-gray-100 px-4 py-2.5 focus:ring-2 focus:ring-blue-500 focus:border-transparent "
    "dark:focus:ring-blue-400 transition"
)
FILE_CLASS = (
    "w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2.5 file:px-4 file:rounded-lg "
    "file:border-0 file:bg-blue-600 file:text-white file:font-medium hover:file:bg-blue-700 file:transition"
)
CHECKBOX_CLASS = (
    "rounded border-gray-300 dark:border-gray-600 text-blue-600 focus:ring-blue-500 focus:ring-2 "
    "dark:bg-gray-700 dark:checked:bg-blue-500 w-5 h-5"
)
TEXTAREA_CLASS = (
    "w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 "
    "text-gray-900 dark:text-gray-100 px-4 py-2.5 focus:ring-2 focus:ring-blue-500 focus:border-transparent "
    "dark:focus:ring-blue-400 transition placeholder-gray-400 dark:placeholder-gray-500 min-h-[100px] resize-y"
)


class DestaqueForm(forms.ModelForm):
    class Meta:
        model = Destaque
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_post'].required = False
        self.fields['link_url'].required = False
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': INPUT_CLASS})
            elif isinstance(field.widget, forms.URLInput):
                field.widget.attrs.update({'class': INPUT_CLASS})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': TEXTAREA_CLASS})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': SELECT_CLASS})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': FILE_CLASS})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': CHECKBOX_CLASS})

    def clean(self):
        data = super().clean()
        points_to_noticia = data.get('points_to_noticia')
        related_post = data.get('related_post')
        link_url = data.get('link_url')

        if points_to_noticia:
            data['link_url'] = ''
            if not related_post:
                self.add_error('related_post', 'Selecione a notícia quando o destaque aponta para notícia.')
        else:
            data['related_post'] = None
            # link_url can be blank (button will use # or default)
        return data


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