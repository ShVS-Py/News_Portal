from django import forms
from django.apps import apps  # ✅ Это устранит ошибку

class NewsForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('news', 'News')  # ✅ Безопасный импорт модели
        fields = ['title', 'content', 'author']
