from django.urls import path
from . import views

urlpatterns = [

    path('', views.all_posts, name='all_posts'),
    path('news_list/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('news/search/', views.news_search, name='news_search'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<int:category_id>/', views.posts_by_category, name='posts_by_category'),


    path('news/<str:model_type>/<int:pk>/edit/', views.content_edit_delete, name='content_edit_delete'),
    path('moderation/', views.news_moderation, name='news_moderation'),
    path('news/create/', views.NewsCreateView.as_view(), name='news_create'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),

]
