from django.db import models
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Comment, News

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
    news = News.objects.all().order_by('-published_date')
    return render(request, 'news/news_list.html', {'news': news})

def news_detail(request, pk):
    article = get_object_or_404(News, id=pk)
    return render(request, 'news/news_detail.html', {'article': article})
