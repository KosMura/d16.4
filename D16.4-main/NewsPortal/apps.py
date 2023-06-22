from django.apps import AppConfig
import redis


class NewsPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NewsPortal'

    def ready(self):
        import NewsPortal.signals


red = redis.Redis(
    host='redis-16827.c90.us-east-1-3.ec2.cloud.redislabs.com',
    port=16827,
    password='85aKjSWjgMcx3QeSFX3PHgITnuzLy1qK',
)
