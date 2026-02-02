from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from .models import NewsPost

def index(request):
    return render(request, 'index.html')

def mulheres(request):
    return render(request, 'mulheres.html')

class PortalLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


def logout_view(request):
    """Log out and redirect; no template."""
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

from django.shortcuts import render, redirect, get_object_or_404
import json 

# ... imports ...

def news_editor(request, news_id=None):
    context = {}
    if news_id:
        news_item = get_object_or_404(NewsPost, pk=news_id)
        context['news_item'] = news_item
        
        # Serialize Blocks
        blocks_data = []
        for block in news_item.blocks.all().order_by('order'):
            block_data = {
                'type': block.block_type,
                'content': block.content,
                'images': []
            }
            
            # Fetch images if applicable
            if block.block_type in ['image', 'carousel', 'image_with_text', 'paragraph_with_image']: # Check exact choices from model
                 # Model choices: paragraph, paragraph_with_image, subtitle, hr, image
                 # Wait, choices in models.py were:
                 # ('paragraph', 'Parágrafo'), ('paragraph_with_image', 'Parágrafo com imagem'), ('subtitle', 'Subtítulo'), ('hr', 'Separador horizontal'), ('image', 'Imagem')
                 # But template uses: title, subtitle, paragraph, image, carousel, image-text
                 # This indicates a mismatch or the template has types not yet in backend choices, or mapped differently.
                 # Let's map template types to backend types if possible, or just serialize what we have.
                 # Assuming backend has 'image' type which uses BlockImage.
                 pass

            # Getting Related Images
            # Using 'image' related_name from BlockImage model: block = ForeignKey(..., related_name="image")
            # So block.image.all()
            for img in block.image.all():
                 blocks_data[-1]['images'].append({
                     'url': img.image.url if img.image else '',
                     'caption': img.captions,
                     'alt': img.alt_text
                 })

            blocks_data.append(block_data)

        context['existing_blocks_json'] = json.dumps(blocks_data)

    return render(request, 'news_editor.html', context)

def news_list(request):
    """
    View to list, filter and sort news posts.
    """
    news_query = NewsPost.objects.all()

    # Filters
    title_query = request.GET.get('title')
    if title_query:
        news_query = news_query.filter(title__icontains=title_query)

    author_query = request.GET.get('author')
    if author_query:
        news_query = news_query.filter(author__username__icontains=author_query)
    
    tag_query = request.GET.get('tag')
    if tag_query:
        news_query = news_query.filter(tags__icontains=tag_query)

    date_query = request.GET.get('date')
    if date_query:
        news_query = news_query.filter(publish_date=date_query)

    # Sorting
    sort_order = request.GET.get('sort', 'desc')
    if sort_order == 'asc':
        news_query = news_query.order_by('publish_date')
    else:
        news_query = news_query.order_by('-publish_date')

    context = {
        'news_list': news_query,
    }
    return render(request, 'news_list.html', context)