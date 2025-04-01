from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import News, Category
from datetime import datetime, timedelta

@shared_task
def send_new_post_email(news_id):
    news = News.objects.get(id=news_id)
    category = news.category
    subscribers = category.subscribers.all()

    subject = f"Новая новость в категории: {category.name}"
    message = f"{news.title}\n\n{news.text[:100]}...\n\nСсылка: http://127.0.0.1:8000/news/{news.id}/"

    for user in subscribers:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )

@shared_task
def send_weekly_digest():
    last_week = datetime.now() - timedelta(days=7)
    categories = Category.objects.all()

    for category in categories:
        news_items = News.objects.filter(category=category, published_date__gte=last_week)
        if not news_items:
            continue

        subscribers = category.subscribers.all()
        news_list = "\n".join(
            [f"{news.title} — http://127.0.0.1:8000/news/{news.id}/" for news in news_items]
        )
        subject = f"Еженедельная подборка новостей в категории: {category.name}"
        message = f"Здравствуйте!\n\nВот свежие статьи за неделю:\n\n{news_list}"

        for user in subscribers:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
