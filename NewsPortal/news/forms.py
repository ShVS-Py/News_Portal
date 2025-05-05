from django import forms
from news.models import News, Post

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'text', 'author', 'category']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'post_type', 'categories']
