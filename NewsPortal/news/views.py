from django.contrib.auth.models import User, Group, Permission
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment, News
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import NewsForm
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import update_session_auth_hash
from allauth.account.views import SignupView



class CustomSignupView(SignupView):
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.user


        common_group, created = Group.objects.get_or_create(name='common')
        user.groups.add(common_group)
        user.save()

        return response



def all_posts(request):
    posts = Post.objects.filter(post_type='AR').order_by('-rating')
    categories = Category.objects.all().distinct()
    return render(request, 'news/all_posts.html', {'posts': posts, 'categories': categories})



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

    paginator = Paginator(news, 10)
    page = request.GET.get('page')

    try:
        news_paginated = paginator.page(page)
    except PageNotAnInteger:
        news_paginated = paginator.page(1)
    except EmptyPage:
        news_paginated = paginator.page(paginator.num_pages)

    return render(request, 'news/news_list.html', {'news_paginated': news_paginated})



def news_search(request):
    query_title = request.GET.get('title', '').strip()
    query_author = request.GET.get('author', '').strip()
    query_date = request.GET.get('date', '').strip()

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

    return render(request, 'news/news_search.html', {'news': news})



def news_detail(request, pk):
    article = get_object_or_404(News, id=pk)
    return render(request, 'news/news_detail.html', {'article': article})



def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(categories=category).order_by('-rating')
    categories = Category.objects.all()
    return render(request, 'news/posts_by_category.html', {'posts': posts, 'category': category, 'categories': categories})



def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'news/post_detail.html', {'post': post, 'comments': comments})



class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_moderation')
    permission_required = 'news.add_news'



class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_moderation')
    permission_required = 'news.add_post'



@login_required
def news_moderation(request):
    news = News.objects.all().order_by('-published_date')
    posts = Post.objects.filter(post_type=Post.ARTICLE).order_by('-created_at')
    return render(request, 'news/news_moderation.html', {'news': news, 'posts': posts})



@login_required
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



@login_required
def profile_view(request):
    user = request.user
    is_author = user.groups.filter(name='authors').exists()
    return render(request, 'users/profile.html', {'user': user, 'is_author': is_author})



class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user



@login_required
def become_author(request):
    authors_group, created = Group.objects.get_or_create(name='authors')


    content_type_news = ContentType.objects.get_for_model(News)
    permissions_news = Permission.objects.filter(content_type=content_type_news)


    content_type_post = ContentType.objects.get_for_model(Post)
    permissions_post = Permission.objects.filter(content_type=content_type_post)


    request.user.groups.add(authors_group)


    for perm in permissions_news | permissions_post:
        request.user.user_permissions.add(perm)

    request.user.save()
    update_session_auth_hash(request, request.user)

    return redirect('profile')
