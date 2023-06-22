from celery import shared_task
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from Portals import settings
from .models import PostCategory, SubscribeCategory, Post, Category
from NewsPortal.signals import mail_notify_new_post
import datetime
import time


@shared_task
def send_post_for_subscribers_celery(post_pk):
    post = Post.objects.get(id=post_pk) #получаем пост
    categories = post.categories.all() #получаем все категории поста
    subscribers_all = []
    for category in categories:
        subscribers_all += category.subscribers.all() #для каждой категории находим подписчиков и добавляем в список
    subscribers_list = {} #создаем словарь
    for person in subscribers_all:
        subscribers_list[person.username] = person.email
    for n in subscribers_list.items():
        mail_notify_new_post(n[0], post.header_post, post.text[:50], n[1], post.pk)


@shared_task
def week_post():
    today = datetime.datetime.now()
    day_week_ago = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_post__gte=day_week_ago)
    categories = set(posts.values_list('cathegories__cathegory_name', flat=True)) #берем только имя
    subscribers = set(Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'week_posts.html',
        {
            'link': f'http://127.0.0.1:8000',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject="Новости за неделю",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
