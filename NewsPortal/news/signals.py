from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now, timedelta
from .models import News, Category
from django.contrib.auth.models import User


@receiver(post_save, sender=News)
def send_email_to_subscribers(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        subscribers = category.subscribers.all()

        subject = f"Новая статья в категории {category.name}: {instance.title}"
        message = (
            f"Привет! В категории {category.name} появилась новая статья:\n\n"
            f"{instance.text[:200]}...\n\n"
            f"Читать дальше: http://127.0.0.1:8000/news/{instance.id}/"
        )

        recipient_list = [user.email for user in subscribers if user.email]

        if recipient_list:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
