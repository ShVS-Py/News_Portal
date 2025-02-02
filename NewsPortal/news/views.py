from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment, News
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import NewsForm
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy


def index(request):
    posts = Post.objects.all()
    return render(request, 'news/index.html', {'posts': posts})

def news(request):
    posts = Post.objects.all()
    return render(request, 'news/news.html', {'posts': posts})

def all_posts(request):
    posts = Post.objects.all().order_by('-rating')
    categories = Category.objects.filter(name__in=['Спорт', 'Политика', 'Наука', 'Финансы'])
    return render(request, 'news/all_posts.html', {'posts': posts, 'categories': categories})

def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(categories=category).order_by('-rating')
    categories = Category.objects.all()
    return render(request, 'news/posts_by_category.html', {'posts': posts, 'category': category, 'categories': categories})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'news/post_detail.html', {'post': post, 'comments': comments})

def news_list(request):
    query_title = request.GET.get('title', '').strip()
    query_author = request.GET.get('author', '').strip()
    query_date = request.GET.get('date', '').strip()

    news = News.objects.all().order_by('-published_date')

    if query_title:
        news = news.filter(title__icontains=query_title)
    if query_author:
        news = news.filter(author__icontains=query_author)
    if query_date:
        try:
            query_date = datetime.strptime(query_date, '%Y-%m-%d')
            news = news.filter(published_date__gte=query_date)
        except ValueError:
            pass

    paginator = Paginator(news, 10)  # 10 news per page
    page = request.GET.get('page')

    try:
        news_paginated = paginator.page(page)
    except PageNotAnInteger:
        news_paginated = paginator.page(1)
    except EmptyPage:
        news_paginated = paginator.page(paginator.num_pages)

    context = {
        'news_paginated': news_paginated,
    }
    return render(request, 'news/news_list.html', context)
def news_detail(request, pk):
    article = get_object_or_404(News, id=pk)
    return render(request, 'news/news_detail.html', {'article': article})

def news_search(request):
    query_title = request.GET.get('title', '')
    query_author = request.GET.get('author', '')
    query_date = request.GET.get('date', '')

    news = News.objects.all()

    if query_title:
        news = news.filter(title__icontains=query_title)
    if query_author:
        news = news.filter(author__icontains=query_author)
    if query_date:
        try:
            query_date = datetime.strptime(query_date, '%Y-%m-%d')
            news = news.filter(published_date__gte=query_date)
        except ValueError:
            pass

    context = {
        'news': news,
    }
    return render(request, 'news/news_search.html', context)


class NewsCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_moderation')

    def form_valid(self, form):
        news = form.save(commit=False)
        news.save()
        return super().form_valid(form)

class PostCreateView(CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_moderation')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Post.ARTICLE
        post.save()
        return super().form_valid(form)

def news_moderation(request):
    news = News.objects.all().order_by('-published_date')
    posts = Post.objects.filter(post_type=Post.ARTICLE).order_by('-created_at') 
    return render(request, 'news/news_moderation.html', {'news': news, 'posts': posts})

def content_edit_delete(request, model_type, pk):
    if model_type == 'news':
        content = get_object_or_404(News, pk=pk)
    elif model_type == 'post':
        content = get_object_or_404(Post, pk=pk)
    else:
        return redirect('news_moderation')

    if request.method == 'POST':
        if 'delete' in request.POST:
            content.delete()
            return redirect('news_moderation')
        else:
            form = NewsForm(request.POST, instance=content)
            if form.is_valid():
                form.save()
                return redirect('news_moderation')
    else:
        form = NewsForm(instance=content)

    return render(request, 'news/news_edit_delete.html', {'form': form, 'content': content, 'model_type': model_type})
