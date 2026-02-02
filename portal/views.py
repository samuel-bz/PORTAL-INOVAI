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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def news_editor(request, news_id=None):
    if request.method == 'POST':
        try:
            data = request.POST
            
            # 1. Create/Update NewsPost
            # Note: For now assuming create only or simple update if I added that logic. 
            # Plan only specified saving. Ideally if news_id exists we update.
            
            title = data.get('title')
            description = data.get('description')
            tags = data.get('tags')
            
            if news_id:
                news_item = get_object_or_404(NewsPost, pk=news_id)
            else:
                news_item = NewsPost()
            
            news_item.title = title
            news_item.description = description
            news_item.tags = tags
            news_item.author = request.user
            
            if 'thumbnail' in request.FILES:
                news_item.thumbnail = request.FILES['thumbnail']
            
            news_item.save()
            
            # 2. Handle Blocks
            # Delete existing blocks if updating (simplest strategy)
            if news_id:
                 news_item.blocks.all().delete()
            
            blocks_json = data.get('blocks', '[]')
            blocks = json.loads(blocks_json)
            
            for index, block_data in enumerate(blocks):
                block = NewsBlock(
                    related_post=news_item,
                    block_type=block_data.get('type', 'paragraph'),
                    content=block_data.get('content', ''),
                    order=index
                )
                block.save()
                
                # 3. Handle Block Images
                # We expect files named 'block_{index}_image'
                image_key = f'block_{index}_image'
                if image_key in request.FILES:
                    img_file = request.FILES[image_key]
                    BlockImage.objects.create(
                        block=block,
                        image=img_file
                    )
            
            return JsonResponse({'success': True, 'redirect_url': '/news/'}) # or news detail
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)})

    # GET Request
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