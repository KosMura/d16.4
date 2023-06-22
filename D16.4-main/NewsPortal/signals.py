from django.contrib.auth.models import User
from django.dispatch import receiver
import datetime
from django.core.mail import EmailMultiAlternatives, send_mail, mail_managers
from django.db.models.signals import m2m_changed, post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from Portals.settings import DEFAULT_FROM_EMAIL
from .models import Post, PostCategory, SubscribeCategory, Author
from Portals import settings


def mail_notify_new_post(msg_data):
    html_content = render_to_string(
        'post_for_subscribers.html',
        {
            'msg_data': msg_data,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Уведомление о новой публикации',
        body=f'Новая публикация в вашем любимом разделе',
        from_email=DEFAULT_FROM_EMAIL,
        to=[msg_data['subscriber_email'], ],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(m2m_changed, sender=Post.category.through)
def notify_post_subscriber(sender, instance, **kwargs):
    # print('signal_job')
    if kwargs['action'] == 'post_add':
        new_post = Post.objects.get(pk=instance.pk)
        msg_data = {}
        msg_data['new_post_title'] = new_post.header_post
        msg_data['new_post_text'] = new_post.text[:63]
        msg_data['new_post_pk'] = new_post.id
        subscribers_name = new_post.category.values_list('subscribers__username', flat=True)
        for subscriber_name in subscribers_name:
            if subscriber_name:
                msg_data['subscriber_name'] = subscriber_name
                subscriber_email = User.objects.get(username=subscriber_name).email
                if subscriber_email:
                    msg_data['subscriber_email'] = subscriber_email
                    mail_notify_new_post(msg_data)

