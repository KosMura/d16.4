from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Author
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
import datetime

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'header_post',
            'text',
            'category',
        ]

        def clean(self):
            cleaned_data = super().clean()
            header_post = cleaned_data.get("header_post")
            text = cleaned_data.get("text")
            if text is not None and len(text) < 20:
                raise ValidationError({
                    "text": "Текст не может быть менее 20 символов."
                })
            if not header_post:
                cleaned_data['header_post'] = datetime.datetime.now()

            return cleaned_data


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
