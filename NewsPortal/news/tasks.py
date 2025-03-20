from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from django.conf import settings
from .models import News, Category

def send_weekly_newsletter():
    """ Отправляет пользователям подборку статей за неделю по их подпискам. """
    week_ago = now() - timedelta(days=7)

    for category in Category.objects.all():
        subscribers = category.subscribers.all()
        news_list = News.objects.filter(category=category, published_date__gte=week_ago)

        if news_list.exists() and subscribers:
            subject = f"Новые статьи в категории {category.name} за неделю!"
            message = "Вот список новых статей:\n\n"

            for news in news_list:
                message += f"- {news.title}: http://127.0.0.1:8000/news/{news.id}/\n"

            recipient_list = [user.email for user in subscribers if user.email]

            if recipient_list:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
