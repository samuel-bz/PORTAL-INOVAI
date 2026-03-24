import json

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import DestaqueForm
from .models import Attachment, NewsPost, NewsBlock, BlockImage, Destaque


def index(request):
    noticias = NewsPost.objects.filter(portal='portal_inovai').exclude(draft=True)
    if not request.user.is_authenticated:
        noticias = noticias.filter(active=True)
    noticias = noticias.order_by('-publish_date')[:3]
    destaques = Destaque.objects.filter(portal="portal_inovai")

    context = {
        'news_posts': noticias,
        'destaques': destaques
    }
    return render(request, 'index.html', context)

def mulheres(request):
    noticias = NewsPost.objects.filter(portal='portal_mulheres_ciencia').exclude(draft=True)
    if not request.user.is_authenticated:
        noticias = noticias.filter(active=True)
    noticias = noticias.order_by('-publish_date')[:3]
    destaques = Destaque.objects.filter(portal="portal_mulheres_ciencia")
    
    context = {
        'news_posts': noticias,
        'destaques': destaques,
    }
    return render(request, 'mulheres.html', context=context)

def sobre(request):
    return render(request, 'sobre.html')

class PortalLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


def logout_view(request):
    """Log out and redirect; no template."""
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


# --- Destaque CRUD (login required) ---

class DestaqueListView(LoginRequiredMixin, ListView):
    model = Destaque
    context_object_name = 'destaques'
    template_name = 'portal/destaque/list.html'
    login_url = reverse_lazy('portal:login')

    def get_queryset(self):
        return Destaque.objects.order_by('portal', '-created_at')


class DestaqueDetailView(LoginRequiredMixin, DetailView):
    model = Destaque
    context_object_name = 'destaque'
    template_name = 'portal/destaque/detail.html'
    login_url = reverse_lazy('portal:login')


class DestaqueCreateView(LoginRequiredMixin, CreateView):
    model = Destaque
    form_class = DestaqueForm
    template_name = 'portal/destaque/form.html'
    success_url = reverse_lazy('portal:destaque_list')
    login_url = reverse_lazy('portal:login')


class DestaqueUpdateView(LoginRequiredMixin, UpdateView):
    model = Destaque
    form_class = DestaqueForm
    context_object_name = 'destaque'
    template_name = 'portal/destaque/form.html'
    success_url = reverse_lazy('portal:destaque_list')
    login_url = reverse_lazy('portal:login')


class DestaqueDeleteView(LoginRequiredMixin, DeleteView):
    model = Destaque
    success_url = reverse_lazy('portal:destaque_list')
    login_url = reverse_lazy('portal:login')

    def get(self, request, *args, **kwargs):
        return redirect('portal:destaque_detail', pk=kwargs['pk'])
@login_required
def news_editor(request, news_id=None):
    if request.method == 'POST':
        try:
            data = request.POST
            
            # 1. Criar/Atualizar Notícia
            # Nota: Por enquanto assumindo apenas criação ou atualização simples se adicionada essa lógica. 
            # Plano especificou apenas salvar. Idealmente, se news_id existir, atualizamos.
            
            title = data.get('title')
            description = data.get('description')
            tags = data.get('tags')
            portal = data.get('portal')
            active = data.get('active') == 'on'
            
            if news_id:
                news_item = get_object_or_404(NewsPost, pk=news_id)
            else:
                news_item = NewsPost()
            
            news_item.title = title
            news_item.description = description
            news_item.tags = tags
            news_item.author = request.user
            news_item.portal = portal
            news_item.active = active
            
            if 'thumbnail' in request.FILES:
                news_item.thumbnail = request.FILES['thumbnail']
            
            news_item.save()

            # 2. Manipular Blocos (em edição: atualizar no lugar para preservar imagens existentes)
            # 2. Manipular Blocos (em edição: atualizar no lugar para preservar imagens existentes)
            blocks_json = data.get('blocks', '[]')
            blocks_data_list = json.loads(blocks_json)
            
            # Recuperar blocos existentes e mapear por ID para atualização
            existing_blocks_map = {b.id: b for b in news_item.blocks.all()} if news_id else {}
            processed_block_ids = []

            for index, block_data in enumerate(blocks_data_list):
                block_id = block_data.get('id')
                if block_id:
                    try:
                        block_id = int(block_id)
                    except (ValueError, TypeError):
                        block_id = None
                
                if block_id and block_id in existing_blocks_map:
                    # Atualizar bloco existente
                    block = existing_blocks_map[block_id]
                    block.block_type = block_data.get('type', 'paragraph')
                    block.content = block_data.get('content', '')
                    block.order = index
                    block.save()
                    processed_block_ids.append(block_id)
                else:
                    # Criar novo bloco
                    block = NewsBlock.objects.create(
                        related_post=news_item,
                        block_type=block_data.get('type', 'paragraph'),
                        content=block_data.get('content', ''),
                        order=index
                    )

                # 3. Imagens
                # Verificar carrossel primeiro
                carousel_prefix = f'block_{index}_carousel_file_'
                carousel_files = []
                f_idx = 0
                while f'{carousel_prefix}{f_idx}' in request.FILES:
                    carousel_files.append(request.FILES[f'{carousel_prefix}{f_idx}'])
                    f_idx += 1
                
                if block.block_type == 'carousel':
                    # Em carrossel, o content do bloco possui JSON com 'keep_urls'
                    # Mantemos apenas as imagens que estiverem na lista de keep_urls
                    try:
                        content_data = json.loads(block.content)
                        keep_urls = content_data.get('keep_urls', [])
                        # Excluir imagens antigas que não estão em keep_urls
                        for img in block.image.all():
                            if img.image.url not in keep_urls:
                                img.delete()
                    except:
                        block.image.all().delete()
                    
                    # Adicionar novas imagens
                    for img_file in carousel_files:
                        BlockImage.objects.create(
                            block=block,
                            image=img_file
                        )
                else:
                    image_key = f'block_{index}_image'
                    if image_key in request.FILES:
                        block.image.all().delete()
                        BlockImage.objects.create(
                            block=block,
                            image=request.FILES[image_key]
                        )
                
                # 4. Anexos: substituir quando houver novo upload
                attachment_key = f'block_{index}_attachment'
                file_obj = request.FILES.get(attachment_key) or request.FILES.get(f'block_{index}_attachments')
                if file_obj:
                    block.attachments.all().delete()
                    Attachment.objects.create(
                        block=block,
                        attachments=file_obj,
                        captions=block_data.get('content', '')
                    )

            # Remover blocos que não estão mais na lista (foram excluídos)
            for b_id, b_obj in existing_blocks_map.items():
                if b_id not in processed_block_ids:
                    b_obj.delete()

            return JsonResponse({'success': True, 'redirect_url': '/news/'})  # ou detalhe da notícia
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)})

    # Requisição GET
    context = {}
    if news_id:
        news_item = get_object_or_404(NewsPost, pk=news_id)
        context['news_item'] = news_item
        
        # Serializar Blocos
        blocks_data = []
        for block in news_item.blocks.all().order_by('order'):
            block_data = {
                'id': block.id,
                'type': block.block_type,
                'content': block.content,
                'images': []
            }
            for img in block.image.all():
                block_data['images'].append({
                    'url': img.image.url if img.image else '',
                    'caption': img.captions,
                    'alt': img.alt_text
                })
            
            for att in block.attachments.all():
                block_data['images'].append({
                    'url': att.attachments.url if att.attachments else '',
                    'name': att.attachments.name.split('/')[-1] if att.attachments else 'Arquivo',
                    'type': 'Anexo'
                })
            blocks_data.append(block_data)

        context['existing_blocks_json'] = json.dumps(blocks_data)

    return render(request, 'news_editor.html', context)

def news_list(request):
    """
    View to list, filter and sort news posts.
    """
    news_query = NewsPost.objects.all()
    if not request.user.is_authenticated:
        news_query = news_query.filter(active=True)

    # Filtros
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

    # Ordenação
    sort_order = request.GET.get('sort', 'desc')
    if sort_order == 'asc':
        news_query = news_query.order_by('publish_date')
    else:
        news_query = news_query.order_by('-publish_date')

    context = {
        'news_list': news_query,
    }
    return render(request, 'news_list.html', context)

def news_detail(request, pk):
    post = get_object_or_404(NewsPost, pk=pk)
    if not post.active and not request.user.is_authenticated:
        from django.http import Http404
        raise Http404("Notícia inativa")
    blocks = post.blocks.all().order_by('order')
    return render(request, 'news_detail.html', {'post': post, 'blocks': blocks})
