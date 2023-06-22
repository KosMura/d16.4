from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Author(models.Model):
    rating = models.IntegerField(default=0)
    author = models.OneToOneField(User, on_delete=models.CASCADE)  # из фала users берем абстракт юзера

    def __str__(self):
        return f'{self.author}'






class Category(models.Model):
    name = models.CharField(unique=True, max_length=255, default='other')
    subscribers = models.ManyToManyField(User, through='SubscribeCategory')

    def __str__(self):
        return f'{self.name}'


class SubscribeCategory(models.Model):
    subscribers = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


POSITIONS = [
    ('article', 'Статья'),
    ('news', 'Новости'),
]


class Post(models.Model):
    field = models.CharField(max_length=7, choices=POSITIONS,
                             default='news')  # статья или новость, берем данные из файла data
    time_in = models.DateTimeField(auto_now_add=True)  # дата и время создания
    header_post = models.CharField(max_length=255, null=True)  # заголовок статьи новости
    text = models.TextField(unique=True)  # так как тексты могут быть большие берем TextField
    rating = models.IntegerField(default=0)  # рейтинг новости или статьи, флоат
    category = models.ManyToManyField(Category,
                                      through='PostCategory')  # тут остается сделать свзяь многие ко многим с моделью категории
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь один ко многим с автором

    def __str__(self):
        return f'{self.time_in}, {self.field}, {self.header_post}, {self.text}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def previev(self):  # метод для получения текста поста в зависимости от количества текста
        if len(self.text) < 128:
            return self.text
        else:
            text_post_short = self.text[0:129]
            return f'{text_post_short}...'

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.header_post} | {self.category.name}'


class Comment(models.Model):
    text_comment = models.TextField(max_length=255)  # текст комментария
    time_in = models.DateTimeField(auto_now_add=True)  # время когда создали комментарий
    rating_comment = models.FloatField(default=0.0)  # рейтинг комментария
    comments = models.ForeignKey(Post, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comments

    def like(self):
        self.rating_comment = self.rating_comment + 1
        self.save()

    def dislike(self):
        self.rating_comment = self.rating_comment - 1
        self.save()
