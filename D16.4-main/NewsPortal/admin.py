from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, SubscribeCategory


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ['field', 'author', 'time_in']  # генерируем
    # список имён всех полей для более красивого отображения
    list_filter = ('field', 'author', 'time_in')


class AuthorAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ['author', 'rating']  # генерируем
    # список имён всех полей для более красивого отображения
    list_filter = ('author', 'rating')


class CommentAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ['rating_comment', 'users']  # генерируем
    # список имён всех полей для более красивого отображения
    list_filter = ('rating_comment', 'users')



admin.site.register(Category)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
admin.site.register(SubscribeCategory)
