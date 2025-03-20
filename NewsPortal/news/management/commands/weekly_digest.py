from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now, timedelta
from django.core.management.base import BaseCommand
from news.models import News, Category

class Command(BaseCommand):
    help = "Отправляет подписчикам подборку новостей раз в неделю"

    def handle(self, *args, **kwargs):
        week_ago = now() - timedelta(days=7)
        categories = Category.objects.all()

        for category in categories:
            news_list = News.objects.filter(category=category, published_date__gte=week_ago)
            if news_list.exists():
                subject = f"Новости за неделю в категории {category.name}"
                message = "\n".join([
                    f"{news.title}: http://127.0.0.1:8000/news/{news.id}/"
                    for news in news_list
                ])

                subscribers = category.subscribers.all()
                for user in subscribers:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )

        self.stdout.write(self.style.SUCCESS("Еженедельная рассылка успешно отправлена!"))
