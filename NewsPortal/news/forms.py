from django import forms
from django.apps import apps

class NewsForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('news', 'News')
        fields = ['title', 'content', 'author']
