from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_posts, name='all_posts'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('', views.news_list, name='news_list'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
    path('news/', views.news_list, name='news_list'),
]
