# Открыть Django Shell
python manage.py shell

# Импорт моделей
from news.models import Author, Category, Post, Comment
from django.contrib.auth.models import User

# Создать пользователей
user1 = User.objects.create_user(username='user1', password='password1')
user2 = User.objects.create_user(username='user2', password='password2')

# Создать авторов
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Создать категории
cat1 = Category.objects.create(name='Спорт')
cat2 = Category.objects.create(name='Политика')
cat3 = Category.objects.create(name='Наука')
cat4 = Category.objects.create(name='Финансы')

# Создать посты
post1 = Post.objects.create(
    author=author1,
    post_type=Post.ARTICLE,
    title='Наука в 2025 году',
    text='Все про науку в 2025 году....',
    rating=0,
)
post2 = Post.objects.create(
    author=author2,
    post_type=Post.ARTICLE,
    title='Политика и финансы',
    text='Всё о влиянии политических решений на мировой финансовый рынок....',
    rating=0,
)
post3 = Post.objects.create(
    author=author1,
    post_type=Post.NEWS,
    title='СРОЧНЫЕ НОВОСТИ',
    text='Очень срочные новости!....',
    rating=0,
)

# Присвоить постам категории
post1.categories.add(cat3)
post2.categories.add(cat2, cat4)
post3.categories.add(cat1)

# Создать комментарии
comment1 = Comment.objects.create(post=post1, user=user1, text='Great article!', rating=0)
comment2 = Comment.objects.create(post=post1, user=user2, text='Informative content.', rating=0)
comment3 = Comment.objects.create(post=post2, user=user1, text='Interesting perspective.', rating=0)
comment4 = Comment.objects.create(post=post3, user=user2, text='Very exciting news!', rating=0)

# Применить функции like() и dislike()
post1.like()
post1.like()
post2.dislike()
post3.like()
comment1.like()
comment2.dislike()
comment3.like()
comment4.like()
comment4.like()

# Обновить рейтинг авторов
author1.update_rating()
author2.update_rating()

# Вывести лучшего автора
best_author = Author.objects.order_by('-rating').first()
print(f"Лучший автор: {best_author.user.username}, Рейтинг: {best_author.rating}")

# Вывести лучшую статью
best_post = Post.objects.order_by('-rating').first()
print(f"Лучшая статья:")
print(f"  Дата: {best_post.created_at}")
print(f"  Автор: {best_post.author.user.username}")
print(f"  Рейтинг: {best_post.rating}")
print(f"  Заголовок: {best_post.title}")
print(f"  Превью: {best_post.preview()}")

# Вывести комментарии к лучшей статье
comments = Comment.objects.filter(post=best_post)
print(f"Комментарии к '{best_post.title}':")
for comment in comments:
    print(f"  Дата: {comment.created_at}, Пользователь: {comment.user.username}, Рейтинг: {comment.rating}, Текст: {comment.text}")
