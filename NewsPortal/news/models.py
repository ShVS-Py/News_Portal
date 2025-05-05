from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

# Категория с подписчиками
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name="subscribed_categories", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")


# Посты и статьи
class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'

    POST_TYPE_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    post_type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES, default=ARTICLE, verbose_name="Тип поста")
    categories = models.ManyToManyField(Category, related_name="posts", verbose_name="Категории")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")


# Комментарии
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name=_("Пост"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Автор"))
    text = models.TextField(verbose_name=_("Комментарий"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата добавления"))

    def __str__(self):
        return f'Комментарий от {self.author.username}'

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")


# Новости (отдельно от Post)
class News(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Заголовок"))
    text = models.TextField(verbose_name=_("Текст"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="news", verbose_name=_("Категория"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Автор"))
    published_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата публикации"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")


# Асинхронная отправка email через Celery
@receiver(post_save, sender=News)
def notify_subscribers_on_create(sender, instance, created, **kwargs):
    if created:
        from .tasks import send_new_post_email
        send_new_post_email.delay(instance.id)


# Синхронная отправка email подписчикам
@receiver(post_save, sender=News)
def send_email_to_subscribers(sender, instance, created, **kwargs):
    if created:
        category = instance.category
        subscribers = category.subscribers.all()

        subject = f"Новая новость: {instance.title}"
        message = (
            f"Здравствуйте! В категории «{category.name}» опубликована новая новость:\n\n"
            f"{instance.text[:150]}...\n\n"
            f"Читать полностью: http://127.0.0.1:8000/news/{instance.id}/"
        )

        for user in subscribers:
            if user.email:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True,
                )
