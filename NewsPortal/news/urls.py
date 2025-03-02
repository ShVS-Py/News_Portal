from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.all_posts, name='all_posts'),  # Главная страница с постами и новостями
    path('news_list/', views.news_list, name='news_list'),  # Список новостей
    path('news/<int:pk>/', views.news_detail, name='news_detail'),  # Детали новости
    path('news/search/', views.news_search, name='news_search'),  # Поиск новостей
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # Детали поста
    path('category/<int:category_id>/', views.posts_by_category, name='posts_by_category'),  # Посты по категориям


    path('news/<str:model_type>/<int:pk>/edit/', views.content_edit_delete, name='content_edit_delete'),  # Редактирование/удаление
    path('moderation/', views.news_moderation, name='news_moderation'),  # Модерация новостей и постов
    path('news/create/', views.NewsCreateView.as_view(), name='news_create'),  # Создание новости
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),  # Создание поста


    path('accounts/', include('allauth.urls')),  # allauth для логина/регистрации
    path('become-author/', views.become_author, name='become_author'),  # Стать автором
    path('profile/', views.profile_view, name='profile'),  # Профиль пользователя
]
