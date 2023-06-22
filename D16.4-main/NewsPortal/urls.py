from django.urls import path, include
# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, subscribe, unsubscribe, upgrade_me, ProfilAuthor

from django.views.decorators.cache import cache_page

urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('article/create/', PostCreate.as_view(), name='article_create'),
   path('article/<int:pk>/edit/', PostUpdate.as_view(), name='article_update'),
   path('article/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
   path('subscribe/<int:pk>/', subscribe, name='subscribe'),
   path('unsubscribe/<int:pk>/', unsubscribe, name='unsubscribe'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('profil/<int:pk>/', ProfilAuthor.as_view(), name='profil_user'),
]